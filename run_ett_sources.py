"""Run ETT-01 diagnostics and viable lightweight connectors."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from employment_core import apply_runs, load_state
from ett_connectors import ETT_SPECS, diagnose, run_ett_connector


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=Path("data/ett-state.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("ett01-output"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    diagnostics = [diagnose(spec) for spec in ETT_SPECS]
    viable = {item["source"] for item in diagnostics if item["status"] == "HTTP_HTML_verificado"}
    runs = [run_ett_connector(spec) for spec in ETT_SPECS if spec.key in viable]
    previous = load_state(args.state)
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    state, delta = apply_runs(previous, runs, checked_at)
    (args.output_dir / "viability.json").write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "source-runs.json").write_text(json.dumps([run.as_dict() for run in runs], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "delta.json").write_text(json.dumps(delta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# ETT-01 — viabilidad y conectores", "", "| Fuente | Viabilidad | Enlaces | JobPosting | Error |", "|---|---|---:|---:|---|"]
    for item in diagnostics:
        lines.append(f"| {item['source']} | **{item['status']}** | {item.get('candidate_links', 0)} | {item.get('jobposting_count', 0)} | {item.get('error') or '—'} |")
    lines += ["", f"Nuevos: **{len(delta['new_document_ids'])}**. Cambiados: **{len(delta['changed_document_ids'])}**. Fallos: **{len(delta['source_failures'])}**.", "", "| Fuente | Estado | Documentos | Notas |", "|---|---|---:|---|"]
    for run in runs:
        lines.append(f"| {run.source} | **{run.status}** | {len(run.documents)} | {'; '.join(run.notes) if run.notes else '—'} |")
    report = "\n".join(lines) + "\n"
    (args.output_dir / "report.md").write_text(report, encoding="utf-8")
    print(report)
    return 1 if diagnostics and all(item["status"] == "bloqueado" for item in diagnostics) else 0


if __name__ == "__main__":
    raise SystemExit(main())
