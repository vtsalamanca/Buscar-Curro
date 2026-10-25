"""BC-06: public DOCM latest-edition monitor, using official HTML only."""
from __future__ import annotations

import re
import urllib.request
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from urllib.parse import parse_qs, urljoin, urlsplit

from employment_core import SourceDocument, SourceRun, act_type_for, categories_for, plain, process_key, stable_hash
from public_connectors import Redirects, error_code

DOCM_URL = "https://docm.jccm.es/docm/"
MAX_HTML_BYTES = 1024 * 1024
TIMEOUT_SECONDS = 15
MAX_STALE_DAYS = 10
DOCUMENT_ROUTE = re.compile(r"^(20\d{2})/(\d{2})/(\d{2})/pdf/(20\d{2})_(\d+)\.pdf$")
NID_RE = re.compile(r"\bNID\s*(20\d{2})\s*/\s*(\d+)\b", re.I)
JOB_EVENTS = ("oposiciones", "bolsa", "plaza", "puesto de trabajo", "personal laboral",
              "proceso selectivo", "convocatoria", "concurso", "adjudicacion", "nombramiento")
UNRELATED_EVENTS = ("premios", "subvenciones", "ayudas", "becas", "oposiciones de precio")


def fetch_latest() -> str:
    req = urllib.request.Request(DOCM_URL, headers={"User-Agent": "Buscar-Curro-DOCM/1.0",
                                                      "Accept": "text/html"})
    opener = urllib.request.build_opener(Redirects(("docm.jccm.es",)))
    with opener.open(req, timeout=TIMEOUT_SECONDS) as response:
        end = urlsplit(response.geturl())
        if end.scheme != "https" or end.hostname != "docm.jccm.es":
            raise ValueError("docm_unexpected_destination")
        if "html" not in response.headers.get("Content-Type", "").lower():
            raise ValueError("docm_unexpected_type")
        body = response.read(MAX_HTML_BYTES + 1)
        if len(body) > MAX_HTML_BYTES:
            raise ValueError("docm_oversize_page")
        return body.decode(response.headers.get_content_charset() or "utf-8", errors="replace")


class LatestDocumentParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.inside = False
        self.depth = 0
        self.tokens: list[str] = []
        self.links: list[str] = []
        self.items: list[tuple[str, list[str]]] = []

    def handle_starttag(self, tag, attrs):
        if tag == "p" and "sumario" in (dict(attrs).get("class", "").split()):
            self.inside = True
            self.depth = 1
            self.tokens = []
            self.links = []
        elif self.inside:
            if tag == "p":
                self.depth += 1
            if tag == "a":
                href = dict(attrs).get("href")
                if href:
                    self.links.append(href)

    def handle_data(self, data):
        if self.inside:
            self.tokens.append(data)

    def handle_endtag(self, tag):
        if self.inside and tag == "p":
            self.depth -= 1
            if self.depth == 0:
                text = " ".join(" ".join(self.tokens).split())
                self.items.append((text, list(self.links)))
                self.inside = False


def parse_latest(html: str, today: date) -> tuple[list[SourceDocument], dict]:
    if len(html.encode("utf-8")) > MAX_HTML_BYTES:
        raise ValueError("docm_oversize_page")
    parser = LatestDocumentParser()
    parser.feed(html)
    if not parser.items:
        raise ValueError("docm_no_document_paragraphs")
    found: dict[str, SourceDocument] = {}
    seen_dates: set[date] = set()
    rejected = 0
    parsed = 0
    for text, links in parser.items:
        match = NID_RE.search(text)
        evidence = None
        if match:
            for candidate in links:
                uri = urljoin(DOCM_URL, candidate)
                parsed_url = urlsplit(uri)
                if parsed_url.scheme != "https" or parsed_url.hostname != "docm.jccm.es" or parsed_url.path != "/docm/descargarArchivo.do":
                    continue
                route = parse_qs(parsed_url.query).get("ruta", [])
                if len(route) != 1:
                    continue
                route_match = DOCUMENT_ROUTE.fullmatch(route[0])
                if not route_match or (route_match.group(4), route_match.group(5)) != match.groups():
                    continue
                try:
                    when = date(*(int(route_match.group(i)) for i in (1, 2, 3)))
                except ValueError:
                    continue
                evidence = (uri, when)
                break
        if not evidence:
            rejected += 1
            continue
        link, when = evidence
        seen_dates.add(when)
        parsed += 1
        normalized = plain(text)
        if any(excluded in normalized for excluded in UNRELATED_EVENTS):
            continue
        categories = categories_for(text)
        if not categories or not any(event in normalized for event in JOB_EVENTS):
            continue
        nid = f"{match.group(1)}/{match.group(2)}"
        doc_id = f"docm:{nid}"
        found[doc_id] = SourceDocument(
            source="docm", document_id=doc_id, process_id=process_key("DOCM", text),
            title=text[:500], category=categories, municipality=None, province="Castilla-La Mancha",
            publication_date=when.isoformat(), deadline=None, official_url=link,
            requirements=[], act_type=act_type_for(text), status="plazo_desconocido",
            content_hash=stable_hash(nid, text, link),
            data_quality=["solo_sumario_sin_requisitos_o_plazo"],
        )
    if not seen_dates:
        raise ValueError("docm_no_verified_publication_date")
    if len(seen_dates) != 1:
        raise ValueError("docm_mixed_publication_dates")
    pub_date = next(iter(seen_dates))
    if pub_date > today or (today - pub_date).days > MAX_STALE_DAYS:
        raise ValueError("docm_stale_or_future_page")
    return list(found.values()), {"publication_date": pub_date.isoformat(),
             "document_paragraphs": len(parser.items), "documents_verified": parsed,
             "entries_rejected": rejected, "candidate_titles": len(found)}


def collect_latest(*, today: date | None = None, html: str | None = None) -> tuple[SourceRun, dict]:
    today = today or date.today()
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    try:
        docs, metrics = parse_latest(fetch_latest() if html is None else html, today)
        run = SourceRun("docm", "ok", checked_at, docs,
                        notes=[f"latest_edition:{metrics['publication_date']}",
                               f"scanned:{metrics['documents_verified']}",
                               f"candidates:{metrics['candidate_titles']}"])
        return run, metrics
    except Exception as exc:
        code = str(exc) if isinstance(exc, ValueError) and str(exc).startswith("docm_") else error_code(exc)
        run = SourceRun("docm", "consulta_fallida", checked_at, error=code)
        return run, {"status": "consulta_fallida", "error": code}
