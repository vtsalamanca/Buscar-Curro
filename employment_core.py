"""Common records, relevance rules and persistent change tracking for BT-01B."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


ACTIVE_TERMS = {
    "ate": ("auxiliar tecnico educativo", "auxiliar tecnica educativa", "ate"),
    "psicologia": ("psicolog",),
    "intervencion_social": ("trabajador social", "trabajadora social", "trabajador/a social", "educador social", "educadora social", "educador/a social", "integracion social", "intervencion social"),
    "menores": ("menor", "infancia", "juvenil", "acogimiento", "barnahus"),
    "educacion": ("educador", "educadora", "educacion", "docente", "profesor", "monitora", "monitor "),
    "discapacidad": ("discapacidad", "diversidad funcional"),
}
SUSPENDED_TERMS = ("almacen", "carretill", "logistica", "repartidor", "transporte")
ACT_TYPES = (
    ("correccion", ("correccion", "rectificacion")),
    ("adjudicacion", ("adjudicacion", "destino definitivo", "nombramiento")),
    ("bolsa", ("bolsa", "ampliacion de bolsa")),
    ("convocatoria", ("convocatoria", "proceso selectivo", "oposicion", "concurso")),
    ("resolucion", ("resolucion", "decreto")),
)
MONTHS = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}


def plain(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", value).strip().lower()


def stable_hash(*parts: str) -> str:
    joined = "\x1f".join(plain(part) for part in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def date_from_text(text: str) -> str | None:
    normal = plain(text)
    match = re.search(r"\b(\d{1,2})\s+de\s+([a-z]+)\s+de\s+(20\d{2})\b", normal)
    if match and match.group(2) in MONTHS:
        try:
            return date(int(match.group(3)), MONTHS[match.group(2)], int(match.group(1))).isoformat()
        except ValueError:
            return None
    match = re.search(r"\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b", normal)
    if match:
        try:
            return date(int(match.group(3)), int(match.group(2)), int(match.group(1))).isoformat()
        except ValueError:
            return None
    return None


def categories_for(text: str) -> list[str]:
    normal = plain(text)
    if any(term in normal for term in SUSPENDED_TERMS):
        return []
    return sorted(category for category, terms in ACTIVE_TERMS.items() if any(term in normal for term in terms))


def act_type_for(text: str) -> str:
    normal = plain(text)
    for act_type, terms in ACT_TYPES:
        if any(term in normal for term in terms):
            return act_type
    return "oferta"


def public_id(source: str, url: str, text: str) -> str:
    query = parse_qs(urlsplit(url).query)
    for key in ("id", "nid"):
        if query.get(key):
            return f"{source}:{query[key][0]}"
    match = re.search(r"\b(?:BOE-A-)?20\d{2}[-_/]\d{3,6}\b", text, re.I)
    if match:
        return f"{source}:{match.group(0).upper().replace('_', '-').replace('/', '-')}"
    return f"{source}:{stable_hash(url)[:20]}"


def process_key(organisation: str, title: str) -> str:
    cleaned = plain(title)
    cleaned = re.sub(r"\b(correccion|resolucion|convocatoria|anuncio|decreto|boe|bop)\b", " ", cleaned)
    cleaned = re.sub(r"\b20\d{2}[-_/]\d+\b|\b\d{1,2}[/-]\d{1,2}[/-]20\d{2}\b", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return stable_hash(organisation, cleaned)[:24]


@dataclass
class SourceDocument:
    source: str
    document_id: str
    process_id: str
    title: str
    category: list[str]
    municipality: str | None
    province: str | None
    publication_date: str | None
    deadline: str | None
    official_url: str
    requirements: list[str]
    act_type: str
    status: str
    content_hash: str
    related_ids: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class SourceRun:
    source: str
    status: str
    checked_at: str
    documents: list[SourceDocument] = field(default_factory=list)
    error: str | None = None
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        result = asdict(self)
        result["documents"] = [document.as_dict() for document in self.documents]
        return result


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"schema_version": 1, "documents": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("documents"), dict):
        raise ValueError("invalid_state_schema")
    return data


def apply_runs(previous: dict, runs: list[SourceRun], checked_at: str) -> tuple[dict, dict]:
    relate_processes([document for run in runs for document in run.documents])
    documents = dict(previous.get("documents", {}))
    new_ids: list[str] = []
    changed_ids: list[str] = []
    seen_ids: list[str] = []
    failures: dict[str, str] = {}
    for run in runs:
        if run.status == "consulta_fallida":
            failures[run.source] = run.error or "unknown_error"
            continue
        for document in run.documents:
            seen_ids.append(document.document_id)
            old = documents.get(document.document_id)
            if old is None:
                new_ids.append(document.document_id)
            elif old.get("content_hash") != document.content_hash:
                changed_ids.append(document.document_id)
            documents[document.document_id] = document.as_dict()
    state = {"schema_version": 1, "updated_at": checked_at, "documents": documents}
    delta = {
        "checked_at": checked_at,
        "new_document_ids": sorted(new_ids),
        "changed_document_ids": sorted(changed_ids),
        "seen_document_ids": sorted(set(seen_ids)),
        "source_failures": failures,
        "no_changes": not new_ids and not changed_ids and not failures,
    }
    return state, delta


def _title_tokens(title: str) -> set[str]:
    ignored = {
        "convocatoria", "resolucion", "correccion", "anuncio", "decreto", "proceso", "selectivo",
        "para", "por", "del", "de", "la", "el", "los", "las", "una", "plaza", "plazas", "bolsa",
    }
    return {token for token in re.findall(r"[a-z0-9]+", plain(title)) if len(token) > 2 and token not in ignored}


def relate_processes(documents: list[SourceDocument]) -> None:
    """Relate similar acts without merging their distinct document identities."""
    for index, left in enumerate(documents):
        left_tokens = _title_tokens(left.title)
        if not left_tokens:
            continue
        for right in documents[index + 1:]:
            if not set(left.category).intersection(right.category):
                continue
            if left.municipality and right.municipality and left.municipality != right.municipality:
                continue
            right_tokens = _title_tokens(right.title)
            union = left_tokens | right_tokens
            similarity = len(left_tokens & right_tokens) / len(union) if union else 0
            if similarity < 0.55:
                continue
            common_process = min(left.process_id, right.process_id)
            left.process_id = right.process_id = common_process
            left.related_ids = sorted(set(left.related_ids + [right.document_id]))
            right.related_ids = sorted(set(right.related_ids + [left.document_id]))
