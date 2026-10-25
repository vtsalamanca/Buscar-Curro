"""BC-06: bounded, official BOE daily XML discovery (no login, no LLM)."""
from __future__ import annotations

import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit

from employment_core import SourceDocument, SourceRun, act_type_for, categories_for, plain, process_key, stable_hash
from public_connectors import Redirects, error_code

BOE_API = "https://www.boe.es/datosabiertos/api/boe/sumario/"
BOE_HOSTS = ("boe.es",)
MAX_DAILY_BYTES = 1024 * 1024
MAX_DAYS = 7
TIMEOUT_SECONDS = 15
ID_PATTERN = re.compile(r"^BOE-[AB]-20\d{2}-\d{1,8}$")
RECRUITMENT_TERMS = (
    "convoca", "plazas", "puestos de trabajo", "personal laboral", "empleo publico",
    "oposicion", "concurso", "proceso selectivo", "bolsa de empleo", "bolsa de trabajo",
    "nombramiento", "adjudicacion", "seleccion de personal", "funcionarios",
)


def request_day(day: date) -> bytes | None:
    """Return None ONLY for an official 404; all other failures propagate."""
    url = BOE_API + day.strftime("%Y%m%d")
    opener = urllib.request.build_opener(Redirects(BOE_HOSTS))
    req = urllib.request.Request(
        url, headers={"Accept": "application/xml", "User-Agent": "Buscar-Curro-BOE/1.0"},
    )
    try:
        response = opener.open(req, timeout=TIMEOUT_SECONDS)
    except HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    with response:
        url_parts = urlsplit(response.geturl())
        if url_parts.scheme != "https" or url_parts.hostname not in ("www.boe.es", "boe.es"):
            raise ValueError("boe_unexpected_final_host")
        if "xml" not in response.headers.get("Content-Type", "").lower():
            raise ValueError("boe_unexpected_content_type")
        raw = response.read(MAX_DAILY_BYTES + 1)
        if len(raw) > MAX_DAILY_BYTES:
            raise ValueError("boe_daily_too_large")
        return raw


def _official_html_url(identifier: str, raw: str) -> str | None:
    if not raw:
        return None
    parsed = urlsplit(raw.strip())
    if parsed.scheme != "https" or parsed.hostname not in ("boe.es", "www.boe.es"):
        return None
    if parsed.path != "/diario_boe/txt.php":
        return None
    if parse_qs(parsed.query).get("id") != [identifier]:
        return None
    return raw.strip()


def parse_daily(raw: bytes, day: date) -> tuple[list[SourceDocument], dict]:
    if not raw or len(raw) > MAX_DAILY_BYTES or b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise ValueError("boe_invalid_xml_bounds")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise ValueError("boe_invalid_xml") from exc
    if root.tag != "response" or root.findtext("./status/code") != "200":
        raise ValueError("boe_unexpected_status")
    publication = root.findtext("./data/sumario/metadatos/fecha_publicacion")
    if publication != day.strftime("%Y%m%d"):
        raise ValueError("boe_wrong_publication_date")
    if root.find("./data/sumario/diario") is None:
        raise ValueError("boe_missing_diary")
    found: dict[str, SourceDocument] = {}
    total = 0
    excluded_invalid = 0
    for item in root.findall(".//sumario/diario//item"):
        total += 1
        identifier = (item.findtext("identificador") or "").strip()
        title = " ".join((item.findtext("titulo") or "").split())[:1000]
        link = _official_html_url(identifier, item.findtext("url_html") or "")
        if not ID_PATTERN.fullmatch(identifier) or not title or link is None:
            excluded_invalid += 1
            continue
        category = categories_for(title)
        normalized_title = plain(title)
        # Generic university teaching civil-service competitions are not
        # school/ATE/social-care jobs. This avoids the measured Jaén false hit.
        irrelevant_university_teaching = any(phrase in normalized_title for phrase in (
            "cuerpos docentes universitarios", "catedraticos de universidad",
            "profesores titulares de universidad",
        ))
        unrelated_administrative = any(phrase in normalized_title for phrase in (
            "premios extraordinarios de formacion profesional",
            "se nombra personal funcionario de carrera",
            "se nombran funcionarios de carrera",
            "nombramiento de funcionarios de carrera",
        )) and "se convoca" not in normalized_title and "convocatoria de" not in normalized_title
        unrelated_physical_education = (
            "educacion fisica" in normalized_title and
            not any(term in normalized_title for term in ("educador social", "auxiliar tecnico educativo"))
        )
        remote_region = any(phrase in normalized_title for phrase in (
            "universidad de valladolid", "universidad de jaen",
            "comunidad autonoma de cataluna", "comunidad de castilla y leon",
            "comunidad autonoma de andalucia", "ceuta y melilla",
        )) and not any(phrase in normalized_title for phrase in (
            "castilla-la mancha", "castilla la mancha", "toledo", "nambroca",
        ))
        if (not category or irrelevant_university_teaching or unrelated_administrative or
                unrelated_physical_education or remote_region or
                not any(term in normalized_title for term in RECRUITMENT_TERMS)):
            continue
        doc_id = "boe:" + identifier
        found[doc_id] = SourceDocument(
            source="boe", document_id=doc_id,
            process_id=process_key("Boletín Oficial del Estado", title),
            title=title[:500], category=category, municipality=None, province=None,
            publication_date=day.isoformat(), deadline=None, official_url=link,
            requirements=[], act_type=act_type_for(title), status="plazo_desconocido",
            content_hash=stable_hash(identifier, title, link),
            data_quality=["sumario_sin_requisitos_ni_plazo"],
        )
    return list(found.values()), {
        "items_scanned": total, "selected": len(found), "invalid_entries": excluded_invalid,
        "publication_date": day.isoformat(),
    }


def collect_window(end: date, *, days: int = 7, request=request_day) -> tuple[SourceRun, dict]:
    if not 1 <= days <= MAX_DAYS:
        raise ValueError("boe_days_limit")
    all_docs: dict[str, SourceDocument] = {}
    daily: list[dict] = []
    failed: list[str] = []
    for index in reversed(range(days)):
        day = end - timedelta(days=index)
        try:
            raw = request(day)
            if raw is None:
                daily.append({"date": day.isoformat(), "status": "no_publicado_o_404"})
                continue
            documents, meta = parse_daily(raw, day)
            daily.append({"date": day.isoformat(), "status": "consultado", **meta})
            for doc in documents:
                all_docs[doc.document_id] = doc
        except Exception as exc:
            code = str(exc) if isinstance(exc, ValueError) and str(exc).startswith("boe_") else error_code(exc)
            failed.append(f"{day.isoformat()}:{code}")
            daily.append({"date": day.isoformat(), "status": "consulta_fallida", "error": code})
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    status = "consulta_parcial" if failed else "ok"
    if all(x["status"] == "no_publicado_o_404" for x in daily):
        status = "consulta_parcial"
        failed.append("no_official_editions_verified_in_window")
    run = SourceRun("boe", status, checked_at, list(all_docs.values()),
                    error="; ".join(failed) if failed else None,
                    notes=[f"days_requested:{days}", f"days_ok:{sum(x['status']=='consultado' for x in daily)}",
                           f"days_404:{sum(x['status']=='no_publicado_o_404' for x in daily)}",
                           f"items_scanned:{sum(x.get('items_scanned',0) for x in daily)}",
                           f"documents_selected:{len(all_docs)}"])
    return run, {"daily": daily, "failures": failed, "documents": len(all_docs)}
