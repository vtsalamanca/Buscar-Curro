"""Bounded public HTML connectors selected by BT-01A evidence."""

from __future__ import annotations

import re
import socket
import ssl
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from employment_core import (
    SourceDocument,
    SourceRun,
    act_type_for,
    categories_for,
    date_from_text,
    plain,
    process_key,
    public_id,
    stable_hash,
)


MAX_BYTES = 2 * 1024 * 1024
TIMEOUT_SECONDS = 20
USER_AGENT = "Buscar-Curro-BT-01B/1.0 (+public-employment-monitor)"


@dataclass(frozen=True)
class ConnectorSpec:
    key: str
    name: str
    url: str
    organisation: str
    host_suffixes: tuple[str, ...]
    link_patterns: tuple[str, ...]
    province: str | None = None
    municipality: str | None = None
    seed_urls: tuple[str, ...] = ()
    detail_limit: int = 1
    partial: bool = False


SPECS = (
    ConnectorSpec(
        "docm", "DOCM", "https://docm.jccm.es/docm/busquedaAvanzada.do", "Junta de Comunidades de Castilla-La Mancha",
        ("docm.jccm.es",), ("verarchivohtml.do",), "Castilla-La Mancha", seed_urls=(
            "https://docm.jccm.es/docm/verArchivoHtml.do?ruta=2026%2F07%2F07%2Fhtml%2F2026_5156.html&tipo=rutaDocm",
            "https://docm.jccm.es/docm/verArchivoHtml.do?ruta=2026%2F07%2F10%2Fhtml%2F2026_5293.html&tipo=rutaDocm",
            "https://docm.jccm.es/docm/verArchivoHtml.do?ruta=2026%2F08%2F03%2Fhtml%2F2026_5762.html&tipo=rutaDocm",
        ), detail_limit=3,
    ),
    ConnectorSpec(
        "boe", "BOE", "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7237", "Boletín Oficial del Estado",
        ("boe.es",), ("diario_boe", "pdf"), "Toledo",
        seed_urls=("https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7237",), detail_limit=1,
    ),
    ConnectorSpec(
        "bop_toledo", "BOP Toledo", "https://bop.diputoledo.es/webEbop/ebop.jsp", "Diputación de Toledo",
        ("diputoledo.es",), ("anuncio", "pdf", "ebop"), "Toledo", detail_limit=1,
    ),
    ConnectorSpec(
        "jccm", "JCCM últimas modificaciones", "https://empleopublico.castillalamancha.es/ultimas-modificaciones", "JCCM Empleo Público",
        ("castillalamancha.es",), ("/bolsas/", "/procesos-selectivos/"), "Castilla-La Mancha", detail_limit=2,
    ),
    ConnectorSpec(
        "empleo_clm", "Empleo CLM", "https://empleo.castillalamancha.es/", "Empleo Castilla-La Mancha",
        ("castillalamancha.es",), ("oferta",), "Castilla-La Mancha", detail_limit=1, partial=True,
    ),
    ConnectorSpec(
        "toledo", "Ayuntamiento de Toledo", "https://www.toledo.es/el-ayuntamiento/empleo-publico/", "Ayuntamiento de Toledo",
        ("toledo.es",), ("/empleo_publico/",), "Toledo", "Toledo", detail_limit=2,
    ),
    ConnectorSpec(
        "aranjuez", "Ayuntamiento de Aranjuez", "https://www.aranjuez.es/transparencia/empleo-publico/documentacion-importante/", "Ayuntamiento de Aranjuez",
        ("aranjuez.es",), ("/empleo-publico/", "pdf"), "Madrid", "Aranjuez",
        seed_urls=("https://www.aranjuez.es/transparencia/empleo-publico/trabajador-social/",), detail_limit=2,
    ),
    ConnectorSpec(
        "trama", "Centro Trama", "https://www.trama.org/empleo/", "Asociación Centro Trama",
        ("trama.org",), ("oferta.php?id=",), detail_limit=4,
    ),
    ConnectorSpec(
        "ilunion", "ILUNION VidaSénior", "https://empleo.ilunion.com/go/ILUNION-VIDASENIOR/8683602/", "ILUNION VidaSénior",
        ("ilunion.com",), ("/job/", "vacante"), detail_limit=2,
    ),
    ConnectorSpec(
        "cruz_roja", "Cruz Roja", "https://cruzroja.epreselec.com/Ofertas/Ofertas.aspx", "Cruz Roja",
        ("epreselec.com",), ("oferta", "detalle"), detail_limit=1, partial=True,
    ),
)


class Redirects(HTTPRedirectHandler):
    def __init__(self, allowed_suffixes: tuple[str, ...]) -> None:
        super().__init__()
        self.allowed_suffixes = allowed_suffixes

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        target = urljoin(req.full_url, newurl)
        parsed = urlsplit(target)
        if parsed.scheme != "https" or not any(parsed.hostname == suffix or parsed.hostname.endswith("." + suffix) for suffix in self.allowed_suffixes):
            raise ValueError("unexpected_redirect")
        return super().redirect_request(req, fp, code, msg, headers, target)


def error_code(exc: BaseException) -> str:
    if isinstance(exc, HTTPError):
        return f"HTTPError:{exc.code}"
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return "timeout"
    if isinstance(exc, ssl.SSLError):
        return "tls_error"
    if isinstance(exc, URLError):
        return "timeout" if isinstance(exc.reason, (TimeoutError, socket.timeout)) else "network_error"
    if isinstance(exc, ValueError) and str(exc) in {
        "url_not_allowed", "unexpected_redirect", "response_too_large", "unexpected_content_type",
    }:
        return f"ValueError:{exc}"
    return type(exc).__name__


def fetch(url: str, host_suffixes: tuple[str, ...]) -> tuple[str, str]:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not any(parsed.hostname == suffix or parsed.hostname.endswith("." + suffix) for suffix in host_suffixes):
        raise ValueError("url_not_allowed")
    opener = build_opener(Redirects(host_suffixes))
    with opener.open(Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"}), timeout=TIMEOUT_SECONDS) as response:
        content_type = response.headers.get("Content-Type", "")
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError("response_too_large")
        if "html" not in content_type.lower():
            raise ValueError("unexpected_content_type")
        charset = response.headers.get_content_charset() or "utf-8"
        return body.decode(charset, errors="replace"), response.geturl()


class Blocks(HTMLParser):
    BLOCK_TAGS = {"article", "li", "tr", "section", "h2", "h3", "h4", "p"}

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.blocks: list[dict] = []
        self.all_links: list[tuple[str, str]] = []
        self._depth = 0
        self._texts: list[str] = []
        self._links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._link_text: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        if tag in self.BLOCK_TAGS:
            if self._depth == 0:
                self._texts, self._links = [], []
            self._depth += 1
        if tag == "a":
            self._href = dict(attrs).get("href") or ""
            self._link_text = []

    def handle_data(self, data: str) -> None:
        if self._depth:
            self._texts.append(data)
        if self._href is not None:
            self._link_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href is not None:
            url = urljoin(self.base_url, self._href)
            label = " ".join(self._link_text).strip()
            self.all_links.append((url, label))
            self._links.append((url, label))
            self._href = None
        if tag in self.BLOCK_TAGS and self._depth:
            self._depth -= 1
            if self._depth == 0:
                text = re.sub(r"\s+", " ", unescape(" ".join(self._texts))).strip()
                if text or self._links:
                    self.blocks.append({"text": text, "links": list(self._links)})


def relevant_url(spec: ConnectorSpec, url: str, label: str) -> bool:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname:
        return False
    if not any(parsed.hostname == suffix or parsed.hostname.endswith("." + suffix) for suffix in spec.host_suffixes):
        return False
    haystack = plain(url + " " + label)
    return any(plain(pattern) in haystack for pattern in spec.link_patterns)


def requirements_from(text: str) -> list[str]:
    normal = re.sub(r"\s+", " ", text).strip()
    match = re.search(r"requisitos?\s*[:|-]\s*(.{1,800}?)(?:competencias|se ofrece|fecha de cierre|$)", normal, re.I)
    if not match:
        return []
    return [match.group(1).strip()[:800]]


def title_from_html(html: str) -> str | None:
    for tag in ("h1", "title"):
        match = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", html, re.I | re.S)
        if match:
            value = unescape(re.sub(r"<[^>]+>", " ", match.group(1)))
            value = re.sub(r"\s+", " ", value).strip()
            if value:
                return value
    return None


def deadline_from(text: str) -> str | None:
    match = re.search(r"(?:fecha de cierre|hasta el|fin(?:al)? del plazo)\s*[:|-]?\s*(.{0,80})", text, re.I)
    return date_from_text(match.group(1)) if match else None


def place_from(text: str, spec: ConnectorSpec) -> tuple[str | None, str | None]:
    normal = plain(text)
    municipality = spec.municipality
    province = spec.province
    for place, detected_province in (("Toledo", "Toledo"), ("Aranjuez", "Madrid"), ("Nambroca", "Toledo"), ("Madrid", "Madrid"), ("Sonseca", "Toledo")):
        if plain(place) in normal:
            municipality, province = place, detected_province
            break
    return municipality, province


def make_document(spec: ConnectorSpec, url: str, text: str, detail_text: str = "") -> SourceDocument | None:
    combined = re.sub(r"\s+", " ", f"{text} {detail_text}").strip()
    categories = categories_for(combined)
    if not categories:
        return None
    title = re.sub(r"\s+", " ", text).strip()[:500] or url
    document_id = public_id(spec.key, url, combined)
    municipality, province = place_from(combined, spec)
    publication_date = date_from_text(combined)
    deadline = deadline_from(combined)
    requirements = requirements_from(detail_text or combined)
    act_type = act_type_for(combined)
    today = datetime.now(timezone.utc).date().isoformat()
    status = "plazo_desconocido"
    if deadline:
        status = "abierta" if deadline >= today else "cerrada_o_historica"
    return SourceDocument(
        source=spec.key,
        document_id=document_id,
        process_id=process_key(spec.organisation, title),
        title=title,
        category=categories,
        municipality=municipality,
        province=province,
        publication_date=publication_date,
        deadline=deadline,
        official_url=url,
        requirements=requirements,
        act_type=act_type,
        status=status,
        content_hash=stable_hash(title, combined, url),
    )


def parse_listing(spec: ConnectorSpec, html: str, final_url: str) -> list[tuple[str, str]]:
    parser = Blocks(final_url)
    parser.feed(html)
    candidates: dict[str, str] = {}
    for block in parser.blocks:
        for url, label in block["links"]:
            if relevant_url(spec, url, label) and url.rstrip("/") != final_url.rstrip("/"):
                # JCCM has large navigation blocks whose surrounding text can
                # contaminate every link. Other catalogues may keep the role
                # beside a generic "Ver oferta" anchor, so retain their block.
                candidate_text = label if spec.key in {"jccm", "toledo"} else (block["text"] or label)
                path = urlsplit(url).path.rstrip("/")
                if spec.key == "jccm" and path.endswith((
                    "/turno-discapacidad", "/turno-discapacidad-intelectual",
                )):
                    continue
                if spec.key != "jccm" or categories_for(url + " " + candidate_text):
                    candidates[url] = candidate_text
    for url, label in parser.all_links:
        if relevant_url(spec, url, label) and url.rstrip("/") != final_url.rstrip("/"):
            path = urlsplit(url).path.rstrip("/")
            if spec.key == "jccm" and path.endswith((
                "/turno-discapacidad", "/turno-discapacidad-intelectual",
            )):
                continue
            if spec.key != "jccm" or categories_for(url + " " + label):
                candidates.setdefault(url, label)
    return sorted(candidates.items())


def run_connector(spec: ConnectorSpec) -> SourceRun:
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    try:
        listing, final_url = fetch(spec.url, spec.host_suffixes)
        candidates = parse_listing(spec, listing, final_url)
        deduped: dict[str, str] = {seed: seed for seed in spec.seed_urls}
        deduped.update(candidates)
        documents: list[SourceDocument] = []
        detail_errors: list[str] = []
        for index, (url, text) in enumerate(deduped.items()):
            detail_text = ""
            if index < spec.detail_limit:
                try:
                    detail_html, _ = fetch(url, spec.host_suffixes)
                    text = title_from_html(detail_html) or text
                    detail_text = re.sub(r"<[^>]+>", " ", detail_html)
                    detail_text = unescape(re.sub(r"\s+", " ", detail_text))[:12000]
                except Exception as exc:
                    detail_errors.append(f"detail:{public_id(spec.key, url, text)}:{error_code(exc)}")
            document = make_document(spec, url, text, detail_text)
            if document:
                documents.append(document)
        unique = {document.document_id: document for document in documents}
        status = "ok" if unique else "sin_resultados_relevantes"
        notes = [f"candidate_links:{len(deduped)}", f"relevant_documents:{len(unique)}"] + detail_errors[:10]
        if spec.partial:
            notes.append("source_was_partial_in_bt01a")
        return SourceRun(spec.key, status, checked_at, list(unique.values()), notes=notes)
    except Exception as exc:
        return SourceRun(spec.key, "consulta_fallida", checked_at, error=error_code(exc))


def get_spec(key: str) -> ConnectorSpec:
    for spec in SPECS:
        if spec.key == key:
            return spec
    raise KeyError(key)
