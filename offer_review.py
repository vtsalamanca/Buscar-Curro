"""BC-05: conservative, explainable review; no automatic applications or LLM calls."""
from __future__ import annotations

from datetime import date
from employment_core import plain
from state_safety import validate_state


def _match_key(document: dict) -> tuple:
    """Only group across providers when employer, title, place AND date agree."""
    employer = plain(document.get("hiring_organization") or "")
    title = plain(document.get("title") or "")
    town = plain(document.get("municipality") or "")
    province = plain(document.get("province") or "")
    published = document.get("publication_date")
    if not all((employer, title, town, province, published)):
        return ("unique", document["document_id"])
    return ("matched", employer, title, town, province, published)


def _decision(document: dict, today: str) -> tuple[str, list[str], int]:
    reason: list[str] = []
    deadline = document.get("deadline")
    expiry = bool(deadline and deadline < today)
    if expiry or document.get("status") == "cerrada_o_historica" or document.get("eligibility") == "caducada":
        return "historica_o_caducada", ["plazo vencido o anuncio clasificado como histórico"], 5
    if document.get("eligibility") == "no_apta_por_requisito_explicito":
        return "requisito_excluyente", ["requisito obligatorio no acreditado en el perfil"], 4
    if document.get("geographic_status") != "dentro_80km":
        reason.append("ubicación o distancia por comprobar; los kilómetros disponibles son en línea recta")
    else:
        reason.append("municipio incluido en el catálogo de 80 km en línea recta, no por carretera")
    if not deadline:
        reason.append("plazo o vigencia no confirmado")
    else:
        reason.append("fecha de cierre publicada; comprobar vigencia en la fuente")
    if document.get("data_quality"):
        reason.append("información contradictoria o incompleta en origen")
    if document.get("habilitation_requirements"):
        reason.append("habilitación profesional por verificar")
    if document.get("eligibility") == "apta_probable" and deadline and document.get("geographic_status") == "dentro_80km" and not document.get("data_quality"):
        return "oportunidad_probable", reason + ["compatibilidad preliminar; comprobar requisitos oficiales"], 0
    if document.get("eligibility") in ("revisar", "apta_probable"):
        return "revisar_requisitos_o_vigencia", reason, 1
    return "datos_insuficientes", reason + ["no hay datos suficientes para afirmar compatibilidad"], 2


def build_review(state: dict, delta: dict, *, today: str | None = None) -> dict:
    validate_state(state)
    today = today or date.today().isoformat()
    newest = set(delta.get("new_document_ids", []))
    changed = set(delta.get("changed_document_ids", []))
    groups: dict[tuple, list[dict]] = {}
    for key, value in state["documents"].items():
        if value.get("act_type") != "oferta":
            continue
        doc = {"document_id": key, **value}
        groups.setdefault(_match_key(doc), []).append(doc)
    offers = []
    for group in groups.values():
        # Choose the most conservative status. An outdated sibling does not
        # silently turn a live candidate into an automatic recommendation.
        evaluated = [(_decision(doc, today), doc) for doc in group]
        decision, reasons, priority = max((item[0] for item in evaluated), key=lambda i: i[2])
        newest_docs = sorted(doc["document_id"] for doc in group)
        links = sorted({doc["official_url"] for doc in group if isinstance(doc.get("official_url"), str) and doc["official_url"].startswith("https://")})
        first = group[0]
        offers.append({
            "title": first.get("title"),
            "municipality": first.get("municipality"),
            "province": first.get("province"),
            "hiring_organization": first.get("hiring_organization"),
            "publication_date": first.get("publication_date"),
            "deadline": first.get("deadline"),
            "decision": decision,
            "reasons": reasons,
            "source_document_ids": newest_docs,
            "source_urls": links,
            "new": any(key in newest for key in newest_docs),
            "changed": any(key in changed for key in newest_docs),
            "priority": priority,
        })
    offers.sort(key=lambda offer: (offer["priority"], not offer["new"], plain(offer["title"] or ""), offer["source_document_ids"]))
    return {"review_version": 1, "as_of": today,
            "policy": "provisional_read_only; no automatic applications; no confirmed road distances",
            "offers": offers, "total_groups": len(offers)}
