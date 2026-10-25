"""Manual, bounded DOCM current-edition runner."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from docm_latest import collect_latest
from employment_core import apply_runs, load_state
from state_safety import atomic_write_json, check_output_budget


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path("data/docm-latest-state.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("docm-output"))
    args = parser.parse_args()
    previous = load_state(args.state)
    result, metadata = collect_latest(today=datetime.now(ZoneInfo("Europe/Madrid")).date())
    state, delta = apply_runs(previous, [result], result.checked_at)
    folder = args.output_dir
    folder.mkdir(parents=True, exist_ok=True)
    atomic_write_json(folder / "state.json", state)
    for name, content in (("delta", delta), ("metrics", metadata), ("source-run", result.as_dict())):
        (folder / (name + ".json")).write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n",
                                              encoding="utf-8")
    lines = ["# DOCM — último diario disponible (BC-06)", "",
             f"Consulta UTC: {result.checked_at}. Estado: **{result.status}**.",
             f"Fecha sumario: {metadata.get('publication_date') or 'no comprobada'}.",
             f"Disposiciones verificadas: {metadata.get('documents_verified', '—')}.",
             f"Títulos candidatos: {len(result.documents)}. "
             f"Nuevos: {len(delta['new_document_ids'])}. Cambiados: {len(delta['changed_document_ids'])}.",
             "", "Solo cubre el último diario expuesto. No se han descargado ni verificado plazos de las disposiciones.",
             "Si el origen falla, no declarar ausencia de novedades.", "",
             "| NID | Título candidato | Enlace oficial |", "|---|---|---|"]
    for doc in result.documents[:60]:
        title = doc.title.replace("|", "&#124;").replace("\n", " ")[:350]
        lines.append(f"| {doc.document_id} | {title} | {doc.official_url} |")
    if len(result.documents) > 60:
        lines.append(f"Otros {len(result.documents)-60} candidatos en source-run.json.")
    (folder / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        check_output_budget(folder)
    except ValueError as exc:
        print(f"output_guard={exc}")
        return 2
    print("\n".join(lines))
    return 2 if result.status != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
