"""Restore validated state from the latest earlier successful workflow artifact."""

from __future__ import annotations

import argparse
import io
import json
import os
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError
from urllib.parse import urlsplit


MAX_ARCHIVE = 5 * 1024 * 1024


def validate_state_bytes(raw: bytes) -> dict:
    if len(raw) > MAX_ARCHIVE:
        raise ValueError("state_too_large")
    data = json.loads(raw.decode("utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("documents"), dict):
        raise ValueError("invalid_state_schema")
    return data


def extract_state(archive: bytes) -> bytes:
    if len(archive) > MAX_ARCHIVE:
        raise ValueError("archive_too_large")
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        matches = [name for name in bundle.namelist() if PurePosixPath(name).name == "state.json"]
        if len(matches) != 1 or ".." in PurePosixPath(matches[0]).parts:
            raise ValueError("invalid_archive_layout")
        raw = bundle.read(matches[0])
    validate_state_bytes(raw)
    return raw


def api_json(url: str, token: str) -> dict:
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def allowed_artifact_redirect(location: str) -> bool:
    parsed = urlsplit(location)
    return bool(parsed.scheme == "https" and parsed.hostname and (
        parsed.hostname == "objects.githubusercontent.com"
        or parsed.hostname.endswith(".blob.core.windows.net")
    ))


def download(url: str, token: str) -> bytes:
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
            return None

    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    try:
        response = urllib.request.build_opener(NoRedirect()).open(request, timeout=20)
    except HTTPError as exc:
        if exc.code not in (301, 302, 303, 307, 308) or not exc.headers.get("Location"):
            raise
        location = exc.headers["Location"]
        if not allowed_artifact_redirect(location):
            raise ValueError("unexpected_artifact_redirect") from exc
        # The signed Azure/GitHub URL authenticates itself. Forwarding the
        # repository Bearer token to another host both leaks scope and fails.
        response = urllib.request.urlopen(urllib.request.Request(location), timeout=20)
    with response:
        body = response.read(MAX_ARCHIVE + 1)
    if len(body) > MAX_ARCHIVE:
        raise ValueError("archive_too_large")
    return body


def restore(repository: str, workflow: str, artifact_name: str, current_run: int, token: str, destination: Path) -> bool:
    base = f"https://api.github.com/repos/{repository}"
    runs = api_json(f"{base}/actions/workflows/{workflow}/runs?event=workflow_dispatch&status=success&per_page=20", token)
    prior_success_exists = False
    for run in runs.get("workflow_runs", []):
        if int(run.get("id", 0)) == current_run:
            continue
        prior_success_exists = True
        artifacts = api_json(f"{base}/actions/runs/{run['id']}/artifacts?name={artifact_name}", token)
        valid = [item for item in artifacts.get("artifacts", []) if not item.get("expired") and item.get("name") == artifact_name]
        if not valid:
            continue
        raw = extract_state(download(valid[0]["archive_download_url"], token))
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
        return True
    if prior_success_exists:
        raise ValueError("prior_state_unavailable")
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", type=Path, default=Path("data/ett-state.json"))
    parser.add_argument("--workflow", default="ett01.yml")
    parser.add_argument("--artifact-name", default="ett01-state")
    parser.add_argument("--fallback-workflow")
    parser.add_argument("--fallback-artifact-name")
    args = parser.parse_args()
    required = {name: os.environ.get(name, "") for name in ("GITHUB_REPOSITORY", "GITHUB_RUN_ID", "GITHUB_TOKEN")}
    if not all(required.values()):
        print("state_restore=skipped_missing_ci_context")
        return 0
    restored = restore(
        required["GITHUB_REPOSITORY"], args.workflow, args.artifact_name,
        int(required["GITHUB_RUN_ID"]), required["GITHUB_TOKEN"], args.destination,
    )
    if not restored and args.fallback_workflow and args.fallback_artifact_name:
        restored = restore(
            required["GITHUB_REPOSITORY"], args.fallback_workflow, args.fallback_artifact_name,
            0, required["GITHUB_TOKEN"], args.destination,
        )
    print("state_restore=restored" if restored else "state_restore=first_run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
