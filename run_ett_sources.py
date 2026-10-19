"""Run ETT-01 diagnostics and viable lightweight connectors."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

from employment_core import apply_runs, categories_for, load_state
from bc02_quality import MunicipalityIndex
from ett_connectors import ETT_SPECS, diagnose, pagination_links, run_ett_connector
from public_connectors import error_code, fetch, http_metrics, reset_http_metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=Path("data/ett-state.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("ett01-output"))
    parser.add_argument("--municipalities", type=Path, default=Path("data/municipios_nambroca_80km.csv"))
    parser.add_argument("--page-budget", type=int, default=2)
    parser.add_argument("--detail-budget", type=int, default=12)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    previous = load_state(args.state)
    pruned_false_positives = []
    for document_id, document in list(previous.get("documents", {}).items()):
        invalid_gi_identifier = document.get("source") == "gi_group" and document_id == "gi_group:Gi Group SpA"
        if invalid_gi_identifier or (document.get("source") in {spec.key for spec in ETT_SPECS} and not categories_for(document.get("title", ""))):
            pruned_false_positives.append(document_id)
            del previous["documents"][document_id]
    municipality_index = MunicipalityIndex.load(args.municipalities)
    bc02 = previous.setdefault("bc02", {"queues": {}, "http_cache": {}})
    queues = bc02.setdefault("queues", {})
    reset_http_metrics()
    wall_started = time.monotonic()
    snapshots: dict[str, list[tuple[str, str]]] = {}
    listing_bytes = 0
    listing_seconds = 0.0
    diagnostics: list[dict] = []
    runs = []
    source_metrics: dict[str, dict] = {}
    for spec in ETT_SPECS:
        before = http_metrics()
        pages: list[tuple[str, str]] = []
        try:
            first = fetch(spec.listing_url, spec.hosts)
            pages.append(first)
            seen_pages = {first[1].rstrip("/")}
            frontier = pagination_links(spec, *first)
            while frontier and len(pages) < max(1, args.page_budget):
                page_url = frontier.pop(0)
                if page_url.rstrip("/") in seen_pages:
                    continue
                page = fetch(page_url, spec.hosts)
                seen_pages.add(page[1].rstrip("/"))
                pages.append(page)
                for discovered in pagination_links(spec, *page):
                    if discovered.rstrip("/") not in seen_pages and discovered not in frontier:
                        frontier.append(discovered)
            snapshots[spec.key] = pages
            diagnostic = diagnose(spec, pages)
            diagnostics.append(diagnostic)
            after_pages = http_metrics()
            listing_bytes += after_pages["downloaded_bytes"] - before["downloaded_bytes"]
            listing_seconds += after_pages["elapsed_seconds"] - before["elapsed_seconds"]
            effective_spec = replace(spec, detail_limit=max(1, args.detail_budget))
            run = run_ett_connector(
                effective_spec, pages, queues.setdefault(spec.key, {}), municipality_index,
            )
            runs.append(run)
        except Exception as exc:
            diagnostics.append({
                "source": spec.key, "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "status": "bloqueado", "error": error_code(exc),
            })
        after = http_metrics()
        queue = queues.get(spec.key, {})
        page_count = len(pages)
        source_metrics[spec.key] = {
            "listings_pages": page_count,
            "listing_links": diagnostics[-1].get("candidate_links", 0),
            "candidate_urls": len(queue),
            "detail_fetches": max(0, after["http_requests"] - before["http_requests"] - page_count),
            "unique_candidates_visited": sum(1 for item in queue.values() if item.get("status") == "checked"),
            "pending_candidates": sum(1 for item in queue.values() if item.get("status") == "pending"),
            "preliminarily_filtered": sum(1 for item in queue.values() if item.get("status") == "prefiltered"),
            "errors": sum(1 for item in queue.values() if item.get("status") == "error"),
            "requests": after["http_requests"] - before["http_requests"],
            "bytes": after["downloaded_bytes"] - before["downloaded_bytes"],
            "http_seconds": round(after["elapsed_seconds"] - before["elapsed_seconds"], 3),
            "pagination_discovered": bool(page_count > 1),
        }
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    state, delta = apply_runs(previous, runs, checked_at)
    state["bc02"] = bc02
    measured = http_metrics()
    metrics = {
        **measured,
        "wall_seconds": round(time.monotonic() - wall_started, 3),
        "listing_fetches": sum(len(items) for items in snapshots.values()),
        "detail_fetches": sum(item["detail_fetches"] for item in source_metrics.values()),
        "docs_examined": sum(item["detail_fetches"] for item in source_metrics.values()),
        "relevant_docs": sum(len(run.documents) for run in runs),
        "unvisited_candidates": sum(1 for queue in queues.values() for item in queue.values() if item.get("status") == "pending"),
        "errors": sum(1 for run in runs if run.status == "consulta_fallida") + sum(1 for run in runs for note in run.notes if note.startswith("detail_error:")),
        "municipalities_loaded": len(municipality_index.rows),
        "conditional_http": "not_enabled_without_verified_etag_or_last_modified_savings",
        "pruned_false_positive_ids": sorted(pruned_false_positives),
        "per_source": source_metrics,
    }
    metrics["elapsed_seconds"] = round(metrics["elapsed_seconds"], 3)
    metrics["legacy_equivalent"] = {
        "http_requests": metrics["http_requests"] + len(ETT_SPECS),
        "downloaded_bytes": metrics["downloaded_bytes"] + listing_bytes,
        "elapsed_seconds": round(metrics["elapsed_seconds"] + listing_seconds, 3),
        "listing_fetches": metrics["listing_fetches"] + len(ETT_SPECS),
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
