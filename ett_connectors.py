"""Lightweight public ETT diagnostics and connectors for ETT-01."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

from bc02_quality import MunicipalityIndex, requirement_evaluation
from employment_core import SourceDocument, SourceRun, SUSPENDED_TERMS, categories_for, date_from_text, plain, process_key, stable_hash
from public_connectors import Blocks, error_code, fetch, requirements_from


@dataclass(frozen=True)
class EttSpec:
    key: str
    agency: str
    listing_url: str
    hosts: tuple[str, ...]
    path_markers: tuple[str, ...]
    seed_urls: tuple[str, ...] = ()
    detail_limit: int = 4


ETT_SPECS = (
    EttSpec(
        "tratem", "Tratem", "https://agenciaempleo.tratem.com/ofertas/", ("tratem.com",), ("/oferta/",),
        ("https://agenciaempleo.tratem.com/oferta/docente-certificado-habilitacion-docencia-ab-y-c",), 5,
    ),
    EttSpec(
        "adecco", "Adecco", "https://www.adecco.com/es-es/ofertas-trabajo/localizacion/trabajos-en-toledo",
        ("adecco.com",), ("/es-es/ofertas-trabajo/",),
        ("https://www.adecco.com/es-es/ofertas-trabajo/coordinador-a-de-transporte-escolar-y-acompanantes-20h-toledo-toledo/feff860faf43f8aa1b13e4812d309296",), 4,
    ),
    EttSpec("eurofirms", "Eurofirms", "https://jobs.eurofirms.com/es/es/trabajo/toledo", ("eurofirms.com",), ("/es/es/",), detail_limit=4),
    EttSpec("randstad", "Randstad", "https://www.randstad.es/candidatos/ofertas-empleo/p-toledo/", ("randstad.es",), ("/oferta/",), detail_limit=3),
    EttSpec("manpower", "Manpower", "https://www.manpower.es/es/buscar-trabajo/ciudad/toledo/", ("manpower.es",), ("/es/empleos/",), detail_limit=4),
    EttSpec(
        "gi_group", "Gi Group", "https://es.gigroup.com/ofertas-de-trabajo/castilla-la-mancha-re/toledo-pr/illescas-ci/",
        ("gigroup.com",),
        ("/ofertas-de-trabajo-detalle/",), detail_limit=4,
    ),
)


class StructuredDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._capture = False
        self._parts: list[str] = []
        self.blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        if tag == "script" and "ld+json" in (dict(attrs).get("type") or "").lower():
            self._capture = True
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._capture:
            self.blocks.append("".join(self._parts))
            self._capture = False


def _walk_json(value):  # noqa: ANN001
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_json(child)


def job_postings(html: str) -> list[dict]:
    parser = StructuredDataParser()
    parser.feed(html)
    found: list[dict] = []
    for block in parser.blocks:
        try:
            value = json.loads(block.strip())
        except (json.JSONDecodeError, TypeError):
            continue
        for item in _walk_json(value):
            kinds = item.get("@type", [])
            if isinstance(kinds, str):
                kinds = [kinds]
            if "JobPosting" in kinds:
                found.append(item)
    return found


def _text(value) -> str | None:  # noqa: ANN001
    if value is None:
        return None
    if isinstance(value, dict):
        value = value.get("name") or value.get("value")
    if isinstance(value, list):
        value = ", ".join(filter(None, (_text(item) for item in value)))
    result = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", str(value)))).strip()
    return result or None


def _location(item: dict) -> tuple[str | None, str | None]:
    locations = item.get("jobLocation") or []
    if isinstance(locations, dict):
        locations = [locations]
    for location in locations:
        address = location.get("address", {}) if isinstance(location, dict) else {}
        if isinstance(address, str):
            return address, None
        return _text(address.get("addressLocality")), _text(address.get("addressRegion"))
    return None, None


def _iso_date(value) -> str | None:  # noqa: ANN001
    if not value:
        return None
    match = re.match(r"(20\d{2}-\d{2}-\d{2})", str(value))
    if match:
        try:
            return date.fromisoformat(match.group(1)).isoformat()
        except ValueError:
            return None
    return date_from_text(str(value))


def _salary(value) -> str | None:  # noqa: ANN001
    if not isinstance(value, dict):
        return _text(value)
    currency = value.get("currency") or ""
    inner = value.get("value") or {}
    if isinstance(inner, dict):
        amount = inner.get("value") or inner.get("minValue")
        unit = inner.get("unitText") or ""
        return _text(f"{amount or ''} {currency} {unit}".strip())
    return _text(f"{inner} {currency}".strip())


def _html_text(html: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html))).strip()


def listing_links(spec: EttSpec, html: str, final_url: str) -> list[tuple[str, str]]:
    parser = Blocks(final_url)
    parser.feed(html)
    links: dict[str, str] = {}
    for block in parser.blocks:
        for url, label in block["links"]:
            parsed = urlsplit(url)
            if parsed.scheme != "https" or not parsed.hostname:
                continue
            if not any(parsed.hostname == host or parsed.hostname.endswith("." + host) for host in spec.hosts):
                continue
            if not any(marker in parsed.path.lower() for marker in spec.path_markers):
                continue
            haystack = plain(url + " " + label)
            if any(term in haystack for term in ("login", "registro", "alerta", "suscripcion", "apply")):
                continue
            if url.rstrip("/") == final_url.rstrip("/"):
                continue
            links[url] = block["text"] or label
    for url, label in parser.all_links:
        parsed = urlsplit(url)
        if parsed.scheme == "https" and parsed.hostname and any(
            parsed.hostname == host or parsed.hostname.endswith("." + host) for host in spec.hosts
        ) and any(marker in parsed.path.lower() for marker in spec.path_markers) and not any(
            term in plain(url + " " + label) for term in ("login", "registro", "alerta", "suscripcion", "apply")
        ):
            links.setdefault(url, label)
    return sorted(links.items())


def pagination_links(spec: EttSpec, html: str, final_url: str) -> list[str]:
    """Return only pagination URLs explicitly linked by the public listing."""
    parser = Blocks(final_url)
    parser.feed(html)
    found: set[str] = set()
    for url, label in parser.all_links:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname or not any(
            parsed.hostname == host or parsed.hostname.endswith("." + host) for host in spec.hosts
        ):
            continue
        marker = plain(f"{parsed.path} {parsed.query} {label}")
        if any(word in marker for word in ("siguiente", "next", "pagina siguiente", "ver mas resultados")) or re.search(
            r"(?:^|[/_?&=-])(?:pg|page|pagina)[-_/=]?\d+(?:$|[/&#])", marker,
        ):
            if url.rstrip("/") != final_url.rstrip("/"):
                found.add(url)
    return sorted(found)


def diagnose(spec: EttSpec, listing_snapshot: tuple[str, str] | list[tuple[str, str]] | None = None) -> dict:
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    result = {"source": spec.key, "checked_at": checked_at, "status": "bloqueado", "error": None}
    try:
        snapshots = listing_snapshot if isinstance(listing_snapshot, list) else [listing_snapshot or fetch(spec.listing_url, spec.hosts)]
        links = {url: label for html, final_url in snapshots for url, label in listing_links(spec, html, final_url)}
        result.update({
            "status": "HTTP_HTML_verificado" if links else "HTTP_parcial",
            "final_url": snapshots[0][1],
            "bytes": sum(len(html.encode("utf-8")) for html, _ in snapshots),
            "jobposting_count": sum(len(job_postings(html)) for html, _ in snapshots),
            "candidate_links": len(links),
            "listing_pages": len(snapshots),
            "sample_urls": list(links)[:3],
        })
    except Exception as exc:
        result["error"] = error_code(exc)
    return result


def _document_from_job(spec: EttSpec, url: str, item: dict, fallback: str, html_text: str) -> SourceDocument | None:
    title = _text(item.get("title")) or fallback or url
    description = _text(item.get("description")) or html_text
    combined = f"{title} {description}"
    categories = categories_for(title) if item.get("_html_fallback") else categories_for(combined)
    if not categories:
        return None
    municipality, province = _location(item)
    publication = _iso_date(item.get("datePosted"))
    deadline = _iso_date(item.get("validThrough"))
    quality: list[str] = []
    normal = plain(combined)
    if spec.key == "adecco" and "tiempo completo" in normal and "20h" in normal:
        quality.append("datos_contradictorios:jornada")
    if spec.key == "adecco" and "temporal" in normal and "fijo discontinuo" in normal:
        quality.append("datos_contradictorios:contrato")
    status = "plazo_desconocido"
    if deadline:
        status = "abierta" if deadline >= date.today().isoformat() else "cerrada_o_historica"
    elif publication and publication < (date.today() - timedelta(days=180)).isoformat():
        status = "cerrada_o_historica"
        quality.append("anuncio_antiguo_sin_cierre")
    raw_identifier = item.get("identifier")
    identifier = _text(raw_identifier.get("value") or raw_identifier.get("name")) if isinstance(raw_identifier, dict) else _text(raw_identifier)
    if not identifier:
        identifier = urlsplit(url).path.rstrip("/").split("/")[-1]
    hiring = _text(item.get("hiringOrganization"))
    requirements = requirements_from(description)
    qualifications = _text(item.get("qualifications"))
    if qualifications:
        requirements.append(qualifications[:800])
    stable_content = stable_hash(
        title, publication or "", deadline or "", municipality or "", province or "",
        hiring or "", _text(item.get("employmentType")) or "", _salary(item.get("baseSalary")) or "",
        " | ".join(sorted(set(requirements))), " | ".join(quality), url,
    )
    return SourceDocument(
        source=spec.key, document_id=f"{spec.key}:{identifier or stable_hash(url)[:20]}",
        process_id=process_key(hiring or spec.agency, title), title=title[:500], category=categories,
        municipality=municipality, province=province, publication_date=publication, deadline=deadline,
        official_url=url, requirements=sorted(set(requirements)), act_type="oferta", status=status,
        content_hash=stable_content,
        agency=spec.agency, hiring_organization=hiring,
        employment_type=_text(item.get("employmentType")), salary=_salary(item.get("baseSalary")),
        data_quality=quality,
    )


def _fallback_item(html: str) -> dict:
    text = _html_text(html)
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    title = _text(title_match.group(1)) if title_match else None
    return {"title": title, "description": text, "datePosted": date_from_text(text), "_html_fallback": True}


def unrelated_gi_redirect(spec: EttSpec, final_url: str) -> bool:
    """Reject Gi detail links that silently fall back to a generic catalogue."""
    return spec.key == "gi_group" and "/ofertas-de-trabajo-detalle/" not in urlsplit(final_url).path


def _clear_suspended_title(label: str) -> bool:
    normal = plain(label)
    return bool(normal and len(normal) <= 160 and any(term in normal for term in SUSPENDED_TERMS) and not categories_for(label))


def run_ett_connector(
    spec: EttSpec,
    listing_snapshot: tuple[str, str] | list[tuple[str, str]] | None = None,
    queue_state: dict | None = None,
    municipality_index: MunicipalityIndex | None = None,
) -> SourceRun:
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    try:
        snapshots = listing_snapshot if isinstance(listing_snapshot, list) else [listing_snapshot or fetch(spec.listing_url, spec.hosts)]
        candidates = dict(spec.seed_urls and ((url, url) for url in spec.seed_urls) or ())
        for listing, final_url in snapshots:
            candidates.update(dict(listing_links(spec, listing, final_url)))
        entries = queue_state if queue_state is not None else {}
        for url, label in candidates.items():
            entry = entries.setdefault(url, {"label": label, "status": "pending", "checks": 0})
            entry["label"] = label
            if url in spec.seed_urls and entry.get("status") == "prefiltered":
                entry["status"] = "pending"
            elif entry.get("status") == "prefiltered" and not _clear_suspended_title(label):
                entry["status"] = "pending"
            elif url not in spec.seed_urls and _clear_suspended_title(label):
                entry["status"] = "prefiltered"
        for url, entry in entries.items():
            if url not in candidates and entry.get("status") == "pending":
                entry["status"] = "not_listed"
                entry["last_checked"] = checked_at
        eligible = [(url, item["label"]) for url, item in entries.items() if url in candidates and item.get("status") != "prefiltered"]
        eligible.sort(key=lambda pair: (
            0 if entries[pair[0]].get("status") == "pending" else 1,
            0 if entries[pair[0]].get("status") == "pending" and pair[0] in spec.seed_urls else 1,
            0 if entries[pair[0]].get("status") == "pending" and categories_for(pair[1]) else 1,
            entries[pair[0]].get("last_checked", ""), pair[0],
        ))
        pending = [pair for pair in eligible if entries[pair[0]].get("status") == "pending"]
        refresh_before = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        due = [pair for pair in eligible if entries[pair[0]].get("status") in {"checked", "error"} and entries[pair[0]].get("last_checked", "") < refresh_before]
        ordered = (pending or due)[: spec.detail_limit]
        documents: list[SourceDocument] = []
        notes = [
            f"candidate_links:{len(candidates)}", f"listing_pages:{len(snapshots)}",
            f"listing_jobposting:{sum(len(job_postings(html)) for html, _ in snapshots)}",
            f"prefiltered:{sum(1 for item in entries.values() if item.get('status') == 'prefiltered')}",
            f"unvisited_candidates:{sum(1 for item in entries.values() if item.get('status') == 'pending')}",
            f"already_known_skipped:{sum(1 for url, _ in eligible if entries[url].get('status') == 'checked')}",
        ]
        for url, fallback in ordered:
            try:
                detail, detail_final = fetch(url, spec.hosts)
                entries[url].update(status="checked", last_checked=checked_at, checks=int(entries[url].get("checks", 0)) + 1)
                if unrelated_gi_redirect(spec, detail_final):
                    notes.append("redirected_to_unrelated_catalog")
                    continue
                items = job_postings(detail)
                notes.append(f"detail_jobposting:{len(items)}")
                if not items:
                    items = [_fallback_item(detail)]
                for item in items:
                    document = _document_from_job(spec, detail_final, item, fallback, _html_text(detail))
                    if document:
                        if municipality_index:
                            geo_status, place = municipality_index.classify(document.municipality, document.province)
                            document.geographic_status = geo_status
                            document.distance_km = place.distance_km if place else None
                            evaluation = requirement_evaluation(
                                " ".join([document.title] + document.requirements), document.status, geo_status,
                            )
                            document.eligibility = evaluation["eligibility"]
                            document.qualification_requirements = evaluation["qualification_requirements"]
                            document.habilitation_requirements = evaluation["habilitation_requirements"]
                            document.experience_requirements = evaluation["experience_requirements"]
                        documents.append(document)
            except Exception as exc:
                entries[url].update(status="error", last_checked=checked_at, checks=int(entries[url].get("checks", 0)) + 1)
                notes.append(f"detail_error:{error_code(exc)}")
        unique = {document.document_id: document for document in documents}
        had_detail_errors = any(note.startswith("detail_error:") for note in notes)
        status = "consulta_parcial" if had_detail_errors else ("ok" if unique else "sin_resultados_relevantes")
        return SourceRun(spec.key, status, checked_at, list(unique.values()),
                         error="detail_errors" if had_detail_errors else None, notes=notes[:20])
    except Exception as exc:
        return SourceRun(spec.key, "consulta_fallida", checked_at, error=error_code(exc))


def get_ett_spec(key: str) -> EttSpec:
    for spec in ETT_SPECS:
        if spec.key == key:
            return spec
    raise KeyError(key)
