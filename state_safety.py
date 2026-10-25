"""BC-04: validated atomic state and offline recoverable snapshots (stdlib only).

Snapshots are local files, not an indefinite GitHub Actions persistence service.
No secrets, network access or scheduled side effects are introduced.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import stat
import tempfile
import zipfile
from pathlib import Path


MAX_STATE_BYTES = 5 * 1024 * 1024
MAX_SNAPSHOT_BYTES = 10 * 1024 * 1024


def validate_state(state: dict) -> dict:
    if not isinstance(state, dict) or state.get("schema_version") != 1:
        raise ValueError("invalid_state_schema")
    docs = state.get("documents")
    if not isinstance(docs, dict):
        raise ValueError("invalid_state_documents")
    for key, document in docs.items():
        if not isinstance(key, str) or not key or len(key) > 512 or not isinstance(document, dict):
            raise ValueError("invalid_state_document")
        if document.get("document_id", key) != key:
            raise ValueError("state_document_id_mismatch")
        if "content_hash" in document and not isinstance(document["content_hash"], str):
            raise ValueError("invalid_content_hash")
    if "bc02" in state:
        bc02 = state["bc02"]
        if not isinstance(bc02, dict) or not isinstance(bc02.get("queues", {}), dict):
            raise ValueError("invalid_state_queue")
        for queue in bc02["queues"].values():
            if not isinstance(queue, dict):
                raise ValueError("invalid_state_queue")
            for link, item in queue.items():
                if not isinstance(link, str) or not isinstance(item, dict):
                    raise ValueError("invalid_queue_item")
    return state


def state_bytes(state: dict) -> bytes:
    validate_state(state)
    raw = (json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    if len(raw) > MAX_STATE_BYTES:
        raise ValueError("state_too_large")
    return raw


def parse_state(raw: bytes) -> dict:
    if len(raw) > MAX_STATE_BYTES:
        raise ValueError("state_too_large")
    try:
        return validate_state(json.loads(raw.decode("utf-8")))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid_state_json") from exc


def atomic_write_bytes(path: Path, raw: bytes) -> None:
    """Replace only after durable temporary write. Never follow a target symlink."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError("destination_symlink")
    fd, tmp = tempfile.mkstemp(prefix=".bc-state-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            os.fchmod(handle.fileno(), 0o600)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        if path.is_symlink():
            raise ValueError("destination_symlink")
        os.replace(tmp, path)
    finally:
        if os.path.lexists(tmp):
            os.unlink(tmp)


def check_output_budget(folder: Path, limit: int = 9 * 1024 * 1024) -> int:
    """Reject symlinks, nonregular files and oversized output before artifacts."""
    if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
        raise ValueError("invalid_output_budget")
    folder = Path(folder)
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("invalid_output_folder")
    total = 0
    for child in folder.rglob("*"):
        if child.is_symlink():
            raise ValueError("output_symlink")
        if child.is_file():
            total += child.stat().st_size
        elif not child.is_dir():
            raise ValueError("output_unexpected_file_type")
        if total > limit:
            raise ValueError("output_budget_exceeded")
    return total



def atomic_write_json(path: Path, state: dict) -> None:
    atomic_write_bytes(path, state_bytes(state))


def create_snapshot(state: dict, destination: Path) -> str:
    """Create a tamper-evident *local* ZIP. Never overwrite an existing backup."""
    raw = state_bytes(state)
    digest = hashlib.sha256(raw).hexdigest()
    manifest = {"snapshot_version": 1, "content_file": "state.json",
                "sha256": digest, "bytes": len(raw)}
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, mode="w", compression=zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr("state.json", raw)
        bundle.writestr("manifest.json", json.dumps(manifest, sort_keys=True))
    package = stream.getvalue()
    if len(package) > MAX_SNAPSHOT_BYTES:
        raise ValueError("snapshot_too_large")
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(destination)
    fd, tmp = tempfile.mkstemp(prefix=".bc-snapshot-", dir=destination.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            os.fchmod(handle.fileno(), 0o600)
            handle.write(package)
            handle.flush()
            os.fsync(handle.fileno())
        # A hard link supplies atomic creation without overwrite, even on races.
        os.link(tmp, destination, follow_symlinks=False)
    finally:
        if os.path.lexists(tmp):
            os.unlink(tmp)
    return digest


def restore_snapshot(archive: Path, destination: Path | None = None) -> dict:
    archive = Path(archive)
    if archive.is_symlink() or not archive.is_file() or archive.stat().st_size > MAX_SNAPSHOT_BYTES:
        raise ValueError("invalid_snapshot_file")
    try:
        with zipfile.ZipFile(archive) as bundle:
            infos = bundle.infolist()
            if len(infos) != 2 or {i.filename for i in infos} != {"state.json", "manifest.json"}:
                raise ValueError("invalid_snapshot_layout")
            for info in infos:
                if info.file_size > MAX_STATE_BYTES or stat.S_ISLNK(info.external_attr >> 16):
                    raise ValueError("invalid_snapshot_member")
            raw = bundle.read("state.json")
            manifest = json.loads(bundle.read("manifest.json").decode("utf-8"))
    except (zipfile.BadZipFile, KeyError, json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        raise ValueError("invalid_snapshot") from exc
    if (not isinstance(manifest, dict) or manifest.get("snapshot_version") != 1
            or manifest.get("content_file") != "state.json"
            or manifest.get("bytes") != len(raw)
            or manifest.get("sha256") != hashlib.sha256(raw).hexdigest()):
        raise ValueError("snapshot_integrity_mismatch")
    state = parse_state(raw)
    if destination is not None:
        atomic_write_bytes(Path(destination), raw)
    return state
