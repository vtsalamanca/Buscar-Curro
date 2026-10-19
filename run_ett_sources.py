"""Run ETT-01 diagnostics and viable lightweight connectors."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from employment_core import apply_runs, load_state
from bc02_quality import MunicipalityIndex
from ett_connectors import ETT_SPECS, diagnose, run_ett_connector
from public_connectors import error_code, fetch, http_metrics, reset_http_metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=Path("data/ett-state.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("ett01-output"))
    parser.add_argument("--municipalities", type=Path, default=Path("data/municipios_nambroca_80km.csv"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    previous = load_state(args.state)
    municipality_index = MunicipalityIndex.load(args.municipalities)
    bc02 = previous.setdefault("bc02", {"queues": {}, "http_cache": {}})
    queues = bc02.setdefault("queues", {})
    reset_http_metrics()
    wall_started = time.monotonic()
    snapshots: dict[str, tuple[str, str]] = {}
    listing_bytes = 0
    listing_seconds = 0.0
    diagnostics: list[dict] = []
    for spec in ETT_SPECS:
        before = http_metrics()
        try:
            snapshot = fetch(spec.listing_url, spec.hosts)
            snapshots[spec.key] = snapshot
            diagnostics.append(diagnose(spec, snapshot))
        except Exception as exc:
            diagnostics.append({
                "source": spec.key, "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "status": "bloqueado", "error": error_code(exc),
            })
            continue
        after = http_metrics()
        listing_bytes += after["downloaded_bytes"] - before["downloaded_bytes"]
        listing_seconds += after["elapsed_seconds"] - before["elapsed_seconds"]
    viable = {item["source"] for item in diagnostics if item["status"] == "HTTP_HTML_verificado"}
    runs = [run_ett_connector(
        spec, snapshots[spec.key], queues.setdefault(spec.key, {}), municipality_index,
    ) for spec in ETT_SPECS if spec.key in viable]
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    state, delta = apply_runs(previous, runs, checked_at)
    state["bc02"] = bc02
    measured = http_metrics()
    metrics = {
        **measured,
        "wall_seconds": round(time.monotonic() - wall_started, 3),
        "listing_fetches": len(snapshots),
        "detail_fetches": measured["http_requests"] - len(snapshots),
        "docs_examined": measured["http_requests"] - len(snapshots),
        "relevant_docs": sum(len(run.documents) for run in runs),
        "unvisited_candidates": sum(1 for queue in queues.values() for item in queue.values() if item.get("status") == "pending"),
        "errors": sum(1 for run in runs if run.status == "consulta_fallida") + sum(1 for run in runs for note in run.notes if note.startswith("detail_error:")),
        "municipalities_loaded": len(municipality_index.rows),
        "conditional_http": "not_enabled_without_verified_etag_or_last_modified_savings",
    }
    metrics["elapsed_seconds"] = round(metrics["elapsed_seconds"], 3)
    metrics["legacy_equivalent"] = {
        "http_requests": metrics["http_requests"] + len(snapshots),
        "downloaded_bytes": metrics["downloaded_bytes"] + listing_bytes,
        "elapsed_seconds": round(metrics["elapsed_seconds"] + listing_seconds, 3),
        "listing_fetches": len(snapshots) * 2,
        "detail_fetches": metrics["detail_fetches"],
    }
    (args.output_dir / "viability.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "source-runs.json").write_text(json.dumps([run.as_dict() for run in runs], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "delta.json").write_text(json.dumps(delta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# ETT-01 — viabilidad y conectores", "", "| Fuente | Viabilidad | Enlaces | JobPosting | Error |", "|---|---|---:|---:|---|"]
    for item in diagnostics:
        lines.append(f"| {item['source']} | **{item['status']}** | {item.get('candidate_links', 0)} | {item.get('jobposting_count', 0)} | {item.get('error') or '—'} |")
    lines += [
        "", f"Nuevos: **{len(delta['new_document_ids'])}**. Cambiados: **{len(delta['changed_document_ids'])}**. Fallos: **{len(delta['source_failures'])}**.",
        f"IDs nuevos: `{', '.join(delta['new_document_ids']) or 'ninguno'}`.",
        f"IDs cambiados: `{', '.join(delta['changed_document_ids']) or 'ninguno'}`.",
        "", "| Fuente | Estado | Documentos | Notas |", "|---|---|---:|---|",
    ]
    for run in runs:
        lines.append(f"| {run.source} | **{run.status}** | {len(run.documents)} | {'; '.join(run.notes) if run.notes else '—'} |")
    report = "\n".join(lines) + "\n"
    (args.output_dir / "report.md").write_text(report, encoding="utf-8")
    print(report)
    return 1 if diagnostics and all(item["status"] == "bloqueado" for item in diagnostics) else 0


if __name__ == "__main__":
    raise SystemExit(main())
