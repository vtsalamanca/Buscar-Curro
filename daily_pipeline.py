"""Daily public-only, zero paid dependencies search and GitHub-readable results.

A separate *public* results branch is the durable store. Only a strict field
allowlist is published; never raw harvested HTML, arbitrary text or private
application records. The four existing bounded source programs do the fetching.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

from state_safety import atomic_write_bytes, parse_state, state_bytes

SOURCES = {
    "ett": ("run_ett_sources.py", "ett01-output"),
    "publicas": ("run_public_sources.py", "bt01b-output"),
    "boe": ("run_boe_discovery.py", "boe-output"),
    "docm": ("run_docm_latest.py", "docm-output"),
}
PUBLIC_DOCUMENT_FIELDS = (
    "document_id", "source", "content_hash", "act_type", "title", "official_url",
    "municipality", "province", "publication_date", "deadline", "status",
    "geographic_status", "eligibility", "hiring_organization", "salary",
)
SECRET_QUERY_KEYS = {"token", "key", "auth", "password", "secret", "session", "code", "signature", "access_token"}
MAX_JSON = 3 * 1024 * 1024
MAX_EVENTS = 120


def safe_public_url(url: object) -> str | None:
    if not isinstance(url, str) or len(url) > 1400 or any(ord(c) < 32 for c in url):
        return None
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
        return None
    if any(key.lower() in SECRET_QUERY_KEYS for key, _ in parse_qsl(parsed.query, keep_blank_values=True)):
        return None
    return url


def clean(value: object, limit: int = 200) -> str | None:
    if not isinstance(value, str):
        return None
    return re.sub(r"[\r\n\t\x00-\x1f]", " ", value).strip()[:limit]


def minimal_state(state: dict) -> dict:
    """Never write a full collector state to the PUBLIC results branch."""
    docs = {}
    for key, doc in state.get("documents", {}).items():
        if not isinstance(doc, dict) or not isinstance(key, str) or len(key) > 512:
            continue
        if not re.fullmatch(r"[0-9a-f]{64}", doc.get("content_hash", "")):
            continue
        url = safe_public_url(doc.get("official_url"))
        if not url:
            continue
        record = {k: clean(doc.get(k), 500 if k == "title" else 250)
                  for k in PUBLIC_DOCUMENT_FIELDS if k in doc and isinstance(doc.get(k), str)}
        record.update(document_id=key, content_hash=doc["content_hash"], official_url=url)
        docs[key] = record
    output: dict = {"schema_version": 1, "documents": docs}
    if "bc02" in state:
        queues = {}
        for source, queue in state["bc02"].get("queues", {}).items():
            if source not in {"tratem", "adecco", "eurofirms", "randstad", "manpower", "gi_group"}:
                continue
            clean_queue = {}
            for url, item in queue.items():
                if not safe_public_url(url) or not isinstance(item, dict):
                    continue
                status = item.get("status")
                if status not in {"pending", "checked", "error", "prefiltered", "not_listed"}:
                    continue
                clean_queue[url] = {
                    "label": clean(item.get("label"), 160) or "",
                    "status": status,
                    "checks": min(max(int(item.get("checks", 0)), 0), 10000),
                    "last_checked": clean(item.get("last_checked"), 40) or "",
                }
            queues[source] = clean_queue
        output["bc02"] = {"queues": queues, "http_cache": {}}
    if len(state_bytes(output)) > MAX_JSON:
        raise ValueError("public_state_size_limit")
    return output


def document_event(doc: dict, kind: str) -> dict | None:
    url = safe_public_url(doc.get("official_url"))
    if not url:
        return None
    return {
        "type": kind, "document_hash": hashlib.sha256(doc["document_id"].encode()).hexdigest(),
        "source": clean(doc.get("source"), 60),
        "title": clean(doc.get("title"), 350),
        "municipality": clean(doc.get("municipality"), 120),
        "province": clean(doc.get("province"), 100),
        "url": url,
        "publication_date": clean(doc.get("publication_date"), 16),
        "deadline": clean(doc.get("deadline"), 16),
        "geographic_status": clean(doc.get("geographic_status"), 45),
        "eligibility": clean(doc.get("eligibility"), 60),
        "act_type": clean(doc.get("act_type"), 40),
        "verified_offer": False,
    }


def monitor_ate(code_dir: Path, state_root: Path) -> tuple[dict, list[dict]]:
    """Track only public Toledo ATE PDF digests; never publish applicant data."""
    target = state_root / "ate.json"
    try:
        result = subprocess.run(
            [sys.executable, str(code_dir / "ate_public.py")],
            cwd=code_dir, capture_output=True, text=True, timeout=120, check=False,
        )
        if result.returncode or len(result.stdout) > 40000:
            return {"source": "ate", "status": "failed", "state_preserved": target.exists()}, []
        payload = json.loads(result.stdout)
        if payload.get("status") != "public_documents_verified":
            return {"source": "ate", "status": "failed", "state_preserved": target.exists()}, []
        old = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {"documents": {}}
        existing = old.get("documents")
        if not isinstance(existing, dict):
            raise ValueError("invalid_ate_state")
        current = {}
        events = []
        for doc in payload.get("documents", []):
            url = safe_public_url(doc.get("url"))
            digest = doc.get("sha256")
            if (url is None or urlsplit(url).hostname != "empleopublico.castillalamancha.es"
                    or not urlsplit(url).path.lower().endswith(".pdf")
                    or not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest)):
                raise ValueError("invalid_ate_document")
            current[url] = digest
            if target.exists() and existing.get(url) != digest:
                events.append({
                    "type": "ate_pdf_changed" if url in existing else "ate_pdf_new",
                    "source": "ate_public_toledo", "title": "Bolsas ATE Toledo: PDF público",
                    "url": url, "verified_offer": False,
                    "notice": "Cambió la huella del PDF; no se extraen datos personales ni se infieren llamamientos.",
                })
        if not current:
            raise ValueError("no_ate_documents")
        clean_state = {"schema_version": 1, "documents": current}
        atomic_write_bytes(target, (json.dumps(clean_state, indent=2, sort_keys=True) + "\n").encode())
        return {"source": "ate", "status": "ok", "new_or_changed": len(events),
                "first_baseline": not bool(existing)}, events
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired):
        return {"source": "ate", "status": "failed", "state_preserved": target.exists()}, []


def generate_summary(now: str, reports: list[dict], events: list[dict]) -> dict:
    failure_count = sum(1 for r in reports if r["status"] != "ok")
    return {
        "schema_version": 1, "project": "Buscar-Curro", "generated_at": now,
        "overall_status": "partial" if failure_count else "ok",
        "sources": reports, "events": events[:MAX_EVENTS],
        "event_count": len(events), "events_truncated": len(events) > MAX_EVENTS,
        "notice": "Candidatos preliminares, no plazas o vigencias confirmadas. Validar requisitos, fechas y ubicación en origen. No se presentan kilómetros por carretera.",
    }


def run_all(*, results_dir: Path, code_dir: Path, execute: bool = True, bootstrap_ett: Path | None = None) -> dict:
    """Fail closed: leave previous state if a source fails or state is corrupt."""
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    reports: list[dict] = []
    events: list[dict] = []
    state_root = results_dir / "notices" / "states"
    state_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="bc-daily-") as temp:
        temp_root = Path(temp)
        for name, (script, _legacy_output) in SOURCES.items():
            state_path = state_root / f"{name}.json"
            previous_path = temp_root / f"{name}-previous.json"
            output = temp_root / f"{name}-out"
            if state_path.is_symlink():
                raise ValueError("public_state_symlink")
            if not state_path.exists() and name == "ett" and bootstrap_ett is not None and bootstrap_ett.is_file():
                raw_seed = parse_state(bootstrap_ett.read_bytes())
                projected_seed = minimal_state(raw_seed)
                atomic_write_bytes(state_path, state_bytes(projected_seed))
            if state_path.exists():
                # Reading this strict schema is essential; never reset silently.
                prior = parse_state(state_path.read_bytes())
                atomic_write_bytes(previous_path, state_bytes(prior))
            args = [sys.executable, str(code_dir / script), "--state", str(previous_path),
                    "--output-dir", str(output)]
            if name == "boe":
                args += ["--days", "7"]
            if execute:
                try:
                    completed = subprocess.run(args, cwd=code_dir, capture_output=True, text=True,
                                               timeout=600, check=False)
                    exit_code = completed.returncode
                except subprocess.TimeoutExpired:
                    exit_code = 124
            else:
                exit_code = 1
            if exit_code or not (output / "delta.json").exists() or not (output / "state.json").exists():
                reports.append({"source": name, "status": "failed", "exit_code": exit_code,
                                "state_preserved": state_path.exists()})
                continue
            try:
                state = parse_state((output / "state.json").read_bytes())
                delta = json.loads((output / "delta.json").read_text(encoding="utf-8"))
                projection = minimal_state(state)
                source_events = []
                for kind, ids in (("new", delta["new_document_ids"]), ("changed", delta["changed_document_ids"])):
                    for doc_id in ids:
                        doc = projection["documents"].get(doc_id)
                        if doc:
                            candidate = document_event(doc, kind)
                            if candidate:
                                source_events.append(candidate)
                atomic_write_bytes(state_path, state_bytes(projection))
                failures = delta.get("source_failures", {})
                reports.append({"source": name, "status": "partial" if failures else "ok",
                                "new": len(delta["new_document_ids"]),
                                "changed": len(delta["changed_document_ids"]),
                                "source_failures": sorted(failures),
                                "state_preserved": True})
                events.extend(source_events)
            except (OSError, KeyError, ValueError, TypeError, json.JSONDecodeError):
                reports.append({"source": name, "status": "invalid_result", "state_preserved": state_path.exists()})
    ate_status, ate_events = monitor_ate(code_dir, state_root) if execute else ({"source": "ate", "status": "failed"}, [])
    reports.append(ate_status)
    events.extend(ate_events)
    summary = generate_summary(now, reports, events)
    output = results_dir / "notices" / "latest.json"
    atomic_write_bytes(output, (json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--code-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--bootstrap-ett", type=Path)
    args = parser.parse_args()
    summary = run_all(results_dir=args.results_dir.resolve(), code_dir=args.code_dir.resolve(), bootstrap_ett=args.bootstrap_ett)
    print(json.dumps({"status": summary["overall_status"], "sources": summary["sources"],
                      "event_count": summary["event_count"]}, ensure_ascii=False))
    return 0 if summary["overall_status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
