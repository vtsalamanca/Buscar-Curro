"""Manual BC-06 runner for BOE open-data summaries by date (stdlib only)."""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from boe_discovery import MAX_DAYS, collect_window
from employment_core import apply_runs, load_state
from offer_review import build_review
from state_safety import atomic_write_json, check_output_budget


def main() -> int:
    today = datetime.now(ZoneInfo("Europe/Madrid")).date()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", type=date.fromisoformat, default=today)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--state", type=Path, default=Path("data/boe-discovery-state.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("boe-output"))
    args = parser.parse_args()
    if args.as_of > today or not 1 <= args.days <= MAX_DAYS:
        parser.error("date must not be future and days must be 1..7")
    previous = load_state(args.state)
    result, metrics = collect_window(args.as_of, days=args.days)
    state, delta = apply_runs(previous, [result], result.checked_at)
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    atomic_write_json(output / "state.json", state)
    (output / "source-run.json").write_text(
        json.dumps(result.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (output / "delta.json").write_text(
        json.dumps(delta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (output / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (output / "review-provisional.json").write_text(
        json.dumps(build_review(state, delta, today=today.isoformat()), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# BOE — comprobación documental por fecha (BC-06)",
        "", f"Intervalo: {args.days} días hasta {args.as_of.isoformat()}.",
        f"Estado: **{result.status}**. Títulos examinados: "
        f"**{sum(x.get('items_scanned', 0) for x in metrics['daily'])}**.",
        f"Candidatos seleccionados: **{len(result.documents)}**. Nuevos: **{len(delta['new_document_ids'])}**.",
        f"Modificados: **{len(delta['changed_document_ids'])}**. "
        f"Fechas con fallos: **{len(metrics['failures'])}**.",
        "", "Solo se seleccionan títulos con coincidencia profesional Y señales de empleo público.",
        "No se han comprobado requisitos, vigencia de plazos ni distancias por carretera.",
        "Un 404 se conserva como edición no disponible; no demuestra ausencia de convocatorias.",
        "Fuente: Agencia Estatal BOE, sumarios de datos abiertos; consultar condiciones de reutilización.",
        "", "| Día | Resultado | Entradas | Seleccionadas |",
        "|---|---|---:|---:|",
    ]
    for day in metrics["daily"]:
        lines.append(
            f"| {day['date']} | {day['status']} | "
            f"{day.get('items_scanned', '—')} | {day.get('selected', '—')} |"
        )
    lines.extend(["", "## Documentos candidatos detectados", "",
                  "Son títulos preliminares: comprobar la resolución, requisitos, plazos y ámbito geográfico.",
                  "", "| BOE | Título | Enlace oficial |", "|---|---|---|"])
    for doc in result.documents[:50]:
        safe_title = doc.title.replace("|", "\\|").replace("\n", " ")[:350]
        lines.append(f"| {doc.document_id} | {safe_title} | {doc.official_url} |")
    if len(result.documents) > 50:
        lines.append(f"Más títulos ({len(result.documents)-50}) en source-run.json.")
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        check_output_budget(output)
    except ValueError as exc:
        print(f"output_guard={exc}")
        return 2
    print("\n".join(lines))
    return 2 if result.status == "consulta_parcial" else 0


if __name__ == "__main__":
    raise SystemExit(main())
