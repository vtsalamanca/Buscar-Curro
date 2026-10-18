"""Manual BT-01B runner: collect, filter, deduplicate and report public jobs."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from employment_core import apply_runs, load_state
from public_connectors import SPECS, get_spec, run_connector


def render_report(runs, delta) -> str:
    lines = [
        "# BT-01B — Fuentes públicas",
        "",
        f"Ejecución UTC: `{delta['checked_at']}`.",
        "",
        "| Fuente | Consulta | Documentos relevantes | Error / notas |",
        "|---|---|---:|---|",
    ]
    for run in runs:
        detail = run.error or "; ".join(run.notes)
        lines.append(f"| {run.source} | **{run.status}** | {len(run.documents)} | {detail} |")
    lines.extend((
        "",
        f"Nuevos: **{len(delta['new_document_ids'])}**. Cambiados: **{len(delta['changed_document_ids'])}**. "
        f"Fallos de fuente: **{len(delta['source_failures'])}**.",
        "",
        "Una consulta fallida nunca se presenta como «sin novedades». La vigencia solo se afirma cuando existe una fecha de cierre explícita.",
        "",
        "## Documentos detectados",
        "",
        "| Fuente | Tipo | Estado | Publicación | Cierre | Título | URL oficial |",
        "|---|---|---|---|---|---|---|",
    ))
    for run in runs:
        for document in run.documents:
            safe_title = document.title.replace("|", "\\|")
            lines.append(
                f"| {document.source} | {document.act_type} | {document.status} | "
                f"{document.publication_date or '—'} | {document.deadline or '—'} | "
                f"{safe_title} | {document.official_url} |"
            )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", default=",".join(spec.key for spec in SPECS))
    parser.add_argument("--state", type=Path, default=Path("data/public-source-state.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("bt01b-output"))
    args = parser.parse_args()
    keys = [key.strip() for key in args.sources.split(",") if key.strip()]
    specs = [get_spec(key) for key in keys]
    previous = load_state(args.state)
    runs = [run_connector(spec) for spec in specs]
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    state, delta = apply_runs(previous, runs, checked_at)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "source-runs.json").write_text(json.dumps([run.as_dict() for run in runs], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "delta.json").write_text(json.dumps(delta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render_report(runs, delta)
    (args.output_dir / "report.md").write_text(report, encoding="utf-8")
    print(report)
    # Individual source failures are data. The program fails only if every
    # requested source failed, which would make the collection unusable.
    return 1 if runs and all(run.status == "consulta_fallida" for run in runs) else 0


if __name__ == "__main__":
    raise SystemExit(main())
