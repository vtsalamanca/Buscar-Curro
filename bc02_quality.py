"""BC-02 locality and professional-requirement evaluation (standard library only)."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

from employment_core import plain


@dataclass(frozen=True)
class Municipality:
    name: str
    code: str
    province: str
    distance_km: float


class MunicipalityIndex:
    def __init__(self, rows: list[Municipality]) -> None:
        self.rows = rows
        self.by_name_province = {(plain(row.name), plain(row.province)): row for row in rows}
        self.by_name: dict[str, list[Municipality]] = {}
        for row in rows:
            self.by_name.setdefault(plain(row.name), []).append(row)

    @classmethod
    def load(cls, path: Path) -> "MunicipalityIndex":
        with path.open(encoding="utf-8", newline="") as handle:
            raw = list(csv.DictReader(handle))
        rows = [Municipality(
            item["municipio"], item["codigo_ine"], item["provincia"],
            float(item["distancia_linea_recta_km"]),
        ) for item in raw]
        if len(rows) != 259 or len({row.code for row in rows}) != 259:
            raise ValueError("invalid_municipality_catalogue")
        return cls(rows)

    def classify(self, municipality: str | None, province: str | None) -> tuple[str, Municipality | None]:
        if not municipality:
            return "distancia_pendiente", None
        name = plain(municipality)
        if province:
            match = self.by_name_province.get((name, plain(province)))
            return ("dentro_80km", match) if match else ("localidad_desconocida", None)
        matches = self.by_name.get(name, [])
        if len(matches) == 1:
            return "dentro_80km", matches[0]
        return "localidad_ambigua" if matches else "localidad_desconocida", None


def requirement_evaluation(text: str, deadline_status: str, geographic_status: str) -> dict:
    normal = plain(text)
    qualifications: list[str] = []
    habilitations: list[str] = []
    experience: list[str] = []
    patterns = (
        (qualifications, r"(?:grado|licenciatura|diplomatura|fp|tecnico superior)[^.\n;]{0,100}"),
        (habilitations, r"(?:psicolog[oa] general sanitario|master general sanitario|colegiacion|certificado negativo de delitos sexuales|habilitacion)[^.\n;]{0,120}"),
        (experience, r"(?:experiencia (?:minima|de al menos)|\d+ anos? de experiencia)[^.\n;]{0,100}"),
    )
    for target, pattern in patterns:
        target.extend(match.group(0).strip() for match in re.finditer(pattern, normal))
    explicit_mismatch = any(term in normal for term in (
        "grado en trabajo social obligatorio", "fp integracion social obligatorio",
        "psicologo general sanitario obligatorio", "master general sanitario obligatorio",
    ))
    if deadline_status == "cerrada_o_historica":
        eligibility = "caducada"
    elif explicit_mismatch:
        eligibility = "no_apta_por_requisito_explicito"
    elif geographic_status != "dentro_80km" or habilitations:
        eligibility = "revisar"
    elif qualifications:
        eligibility = "apta_probable"
    else:
        eligibility = "datos_insuficientes"
    return {
        "eligibility": eligibility,
        "qualification_requirements": sorted(set(qualifications)),
        "habilitation_requirements": sorted(set(habilitations)),
        "experience_requirements": sorted(set(experience)),
    }
