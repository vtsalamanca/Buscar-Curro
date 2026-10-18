"""BT-01A: bounded public-source diagnostics for a GitHub Actions runner.

This module is intentionally not an extractor.  It records only public,
sanitised metadata needed to decide whether a later connector is viable.
"""

from __future__ import annotations

import argparse
import json
import re
import socket
import ssl
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


MAX_BYTES = 1024 * 1024
TIMEOUT_SECONDS = 15
USER_AGENT = "Buscar-Curro-BT-01A/1.0 (+public-source-viability)"


@dataclass(frozen=True)
class Source:
    key: str
    family: str
    name: str
    url: str | None
    expected_terms: tuple[str, ...] = ()
    link_terms: tuple[str, ...] = ()
    note: str = ""


SOURCES = (
    Source("docm", "A", "DOCM", "https://docm.jccm.es/docm/busquedaAvanzada.do", ("búsqueda", "docm"), ("verarchivo", "nid", "sumario")),
    Source("boe", "A", "BOE", "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7237", ("boe", "trabajador"), ("diario_boe", "pdf", "toledo")),
    Source("bop_toledo", "A", "BOP Toledo", "https://bop.diputoledo.es/webEbop/ebop.jsp", ("boletín", "toledo"), ("anuncio", "ebop", "pdf")),
    Source("jccm_modificaciones", "A", "JCCM últimas modificaciones", "https://empleopublico.castillalamancha.es/ultimas-modificaciones", ("últimas", "modificaciones"), ("bolsas", "procesos-selectivos", "document")),
    Source("empleo_clm", "B", "Empleo CLM", "https://empleo.castillalamancha.es/", ("empleo",), ("oferta", "municipio", "provincia")),
    Source("empleate", "B", "Empléate", "https://empleate.gob.es/empleo/index_nojs.html?JAVASCRIPTSTATUS=NONE", ("empleo",), ("oferta", "buscar")),
    Source("toledo", "B", "Ayuntamiento de Toledo", "https://www.toledo.es/el-ayuntamiento/empleo-publico/", ("empleo", "toledo"), ("bolsa", "convocatoria", "oferta")),
    Source("nambroca", "B", "Sede de Nambroca", "https://nambroca.sedelectronica.es/info.0", ("nambroca",), ("empleo", "proceso", "convocatoria", "anuncio")),
    Source("aranjuez", "B", "Ayuntamiento de Aranjuez", "https://www.aranjuez.es/transparencia/empleo-publico/documentacion-importante/", ("empleo", "aranjuez"), ("convocatoria", "proceso", "trabajador-social", "pdf")),
    Source("trama", "C", "Centro Trama", "https://www.trama.org/empleo/", ("empleo", "trama"), ("oferta.php", "oferta")),
    Source("ilunion", "C", "ILUNION VidaSénior", "https://empleo.ilunion.com/go/ILUNION-VIDASENIOR/8683602/", ("ilunion",), ("job", "vacante", "puesto")),
    Source("cruz_roja", "C", "Cruz Roja", "https://cruzroja.epreselec.com/Ofertas/Ofertas.aspx", ("ofertas",), ("oferta", "detalle")),
    Source("accem", "C", "ACCEM", None, note="No se ha validado una URL oficial directa de vacantes; la página de programas no es un catálogo de empleo."),
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.forms = 0
        self.scripts = 0
        self._href: str | None = None
        self._label: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a":
            self._href = values.get("href") or ""
            self._label = []
        elif tag == "form":
            self.forms += 1
        elif tag == "script":
            self.scripts += 1

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._label.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._label)))
            self._href = None
            self._label = []


class TrackingRedirect(HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        target = urljoin(req.full_url, newurl)
        if urlsplit(target).scheme not in {"http", "https"}:
            raise ValueError("unexpected_redirect_scheme")
        self.targets.append(target)
        return super().redirect_request(req, fp, code, msg, headers, target)


def sanitise_error(exc: BaseException) -> str:
    """Return a stable error category without response bodies or local details."""
    if isinstance(exc, HTTPError):
        return f"HTTPError:{exc.code}"
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return "timeout"
    if isinstance(exc, ssl.SSLError):
        return "tls_error"
    if isinstance(exc, URLError):
        reason = exc.reason
        if isinstance(reason, (TimeoutError, socket.timeout)):
            return "timeout"
        return "network_error"
    return type(exc).__name__


def analyse_html(source: Source, body: bytes, final_url: str, content_type: str) -> dict:
    text = body.decode("utf-8", errors="replace")
    lowered = text.lower()
    parser = PageParser()
    parser.feed(text)
    expected_hits = [term for term in source.expected_terms if term.lower() in lowered]
    relevant_links = []
    for href, label in parser.links:
        absolute = urljoin(final_url, href)
        haystack = f"{absolute} {label}".lower()
        if urlsplit(absolute).scheme in {"http", "https"} and any(term in haystack for term in source.link_terms):
            relevant_links.append(absolute)
    relevant_links = sorted(set(relevant_links))
    login_signal = bool(re.search(r"\b(iniciar sesi[oó]n|identif[ií]cate|login|contrase[nñ]a)\b", lowered))
    # Avoid generic words such as ``robots`` (the normal indexing meta tag)
    # and passive CAPTCHA libraries.  These phrases indicate an actual access
    # challenge rather than merely code that could display one on a form.
    challenge_signal = any(
        term in lowered
        for term in (
            "eres humano o un robot",
            "are you a human or a robot",
            "actividad poco habitual",
            "unusual traffic",
            "cf-chl-",
            "challenge-platform",
            "geetest_challenge",
        )
    )
    js_signal = any(term in lowered for term in ("javascriptstatus", "enable javascript", "habilite javascript"))
    return {
        "content_type": content_type.split(";", 1)[0].lower(),
        "bytes_read": len(body),
        "truncated": len(body) == MAX_BYTES,
        "expected_terms_found": expected_hits,
        "link_count": len(parser.links),
        "relevant_link_count": len(relevant_links),
        "relevant_link_examples": relevant_links[:3],
        "form_count": parser.forms,
        "script_count": parser.scripts,
        "login_signal": login_signal,
        "challenge_signal": challenge_signal,
        "javascript_signal": js_signal,
    }


def classify(http_status: int | None, analysis: dict | None, error: str | None) -> tuple[str, str]:
    if error or http_status is None:
        return "bloqueada", error or "unknown_error"
    if http_status != 200:
        return "bloqueada", f"http_{http_status}"
    if analysis is None:
        return "parcial", "respuesta_sin_html_analizable"
    if analysis["challenge_signal"]:
        return "bloqueada", "verificacion_humana_detectada"
    if analysis["login_signal"]:
        return "parcial", "carga_publica_con_senal_login"
    if analysis["expected_terms_found"] and analysis["relevant_link_count"]:
        return "verificada_desde_runner", "pagina_y_enlaces_relevantes_detectados"
    if analysis["expected_terms_found"]:
        return "parcial", "pagina_relevante_sin_enlaces_de_resultado_confirmados"
    return "parcial", "http_200_sin_estructura_relevante_confirmada"


def probe(source: Source) -> dict:
    base = {"source": source.key, "family": source.family, "name": source.name, "url": source.url}
    if source.url is None:
        return {**base, "classification": "no_probada", "reason": "sin_url_oficial_directa_validada", "note": source.note}
    redirect = TrackingRedirect()
    opener = build_opener(redirect)
    started = time.monotonic()
    try:
        request = Request(source.url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            status = response.status
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type", "")
            body = response.read(MAX_BYTES)
        analysis = analyse_html(source, body, final_url, content_type) if "html" in content_type.lower() else None
        classification, reason = classify(status, analysis, None)
        return {
            **base,
            "classification": classification,
            "reason": reason,
            "http_status": status,
            "final_url": final_url,
            "redirects": redirect.targets,
            "elapsed_ms": round((time.monotonic() - started) * 1000),
            "analysis": analysis,
        }
    except Exception as exc:  # diagnostics must continue with independent sources
        error = sanitise_error(exc)
        classification, reason = classify(None, None, error)
        return {
            **base,
            "classification": classification,
            "reason": reason,
            "redirects": redirect.targets,
            "elapsed_ms": round((time.monotonic() - started) * 1000),
            "error": error,
        }


def render_markdown(report: dict) -> str:
    lines = [
        "# BT-01A — Viabilidad de fuentes públicas",
        "",
        f"Ejecución UTC: `{report['run_utc']}`. Entorno: `{report['environment']}`.",
        "",
        "Diagnóstico acotado: una petición por fuente, sin login, cookies, JavaScript ni reintentos. "
        "`verificada_desde_runner` confirma acceso y enlaces relevantes, no un extractor completo ni vigencia de ofertas.",
        "",
        "| Familia | Fuente | Estado | HTTP | Motivo | URL final |",
        "|---|---|---|---:|---|---|",
    ]
    for item in report["results"]:
        final_url = item.get("final_url") or item.get("url") or "—"
        lines.append(
            f"| {item['family']} | {item['name']} | **{item['classification']}** | "
            f"{item.get('http_status', '—')} | {item['reason']} | {final_url} |"
        )
    lines.extend(("", "Los detalles estructurales y errores sanitizados están en `bt01a-results.json`."))
    return "\n".join(lines) + "\n"


def build_report(sources: Iterable[Source], environment: str) -> dict:
    return {
        "schema_version": 1,
        "run_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "environment": environment,
        "limits": {"timeout_seconds": TIMEOUT_SECONDS, "max_bytes": MAX_BYTES, "attempts_per_source": 1},
        "results": [probe(source) for source in sources],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("bt01a-output"))
    parser.add_argument("--environment", default="local")
    args = parser.parse_args()
    report = build_report(SOURCES, args.environment)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "bt01a-results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown = render_markdown(report)
    (args.output_dir / "bt01a-report.md").write_text(markdown, encoding="utf-8")
    print(markdown)
    # A blocked source is a valid diagnostic result. Fail only if the tool itself
    # did not produce one result per configured source.
    return 0 if len(report["results"]) == len(SOURCES) else 1


if __name__ == "__main__":
    sys.exit(main())
