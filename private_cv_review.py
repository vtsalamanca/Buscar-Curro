"""Private Debian-only CV-based preliminary offer review (no paid services).

The PDF stays on Linux. Nothing from this module uploads the CV, contacts
third-party websites or claims a legally verified professional qualification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import tempfile
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

from employment_core import plain
from state_safety import atomic_write_bytes, parse_state

DEFAULT_HOME = Path.home() / ".local" / "share" / "buscar-curro"
MAX_CV_BYTES = 5 * 1024 * 1024
MAX_RESULTS_BYTES = 3 * 1024 * 1024


def _normalized(value: str) -> str:
    return " ".join("".join(
        c for c in unicodedata.normalize("NFKD", value.lower())
        if not unicodedata.combining(c)
    ).split())


def _private_regular_file(path: Path) -> bytes:
    if path.is_symlink():
        raise ValueError("cv_symlink_forbidden")
    info = path.stat()
    if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
            or info.st_mode & 0o077 or info.st_size < 1024
            or info.st_size > MAX_CV_BYTES):
        raise ValueError("cv_permissions_size_or_owner")
    data = path.read_bytes()
    if not data.startswith(b"%PDF-") or len(data) != info.st_size:
        raise ValueError("invalid_cv_pdf")
    return data


def extract_cv_profile(text: str) -> dict:
    """Return only non-identifying skill evidence, not any CV text or identity."""
    normalized = _normalized(text)
    if len(normalized) < 900:
        raise ValueError("cv_text_insufficient")
    anchors = {
        "psychology_degree": (
            "licenciado en psicologia" in normalized
            or "licenciatura en psicologia" in normalized
            or "grado en psicologia" in normalized
        ),
        "ate_experience": "auxiliar tecnico educativo" in normalized,
        "minors_family": "familia" in normalized and "menor" in normalized,
        "disability_support": "discapacidad" in normalized,
        "actia_experience": "actia" in normalized and "diam" in normalized,
        "accem_experience": "accem" in normalized,
        "driver_b": "permiso de conducir b" in normalized,
    }
    if not all((anchors["psychology_degree"], anchors["ate_experience"],
                anchors["minors_family"])):
        raise ValueError("cv_missing_core_anchors")
    return {
        "schema_version": 1,
        "evidence": anchors,
        "unverified_requirements": [
            "habilitacion psicologia general sanitaria",
            "colegiacion profesional",
            "titulacion de trabajo social",
            "fp superior en integracion social",
            "otros masteres exigidos",
        ],
        "note": "Ausencia de evidencia documental no equivale a ausencia de titulacion."
    }


def load_cv_profile(pdf: Path) -> dict:
    original = _private_regular_file(pdf)
    try:
        conversion = subprocess.run(
            ["pdftotext", "-layout", str(pdf), "-"],
            capture_output=True, text=True, timeout=20, check=True,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise ValueError("pdf_extraction_failed") from exc
    profile = extract_cv_profile(conversion.stdout)
    profile["cv_sha256"] = hashlib.sha256(original).hexdigest()
    return profile


def classify_offer(document: dict, profile: dict, today: str) -> dict:
    """Title-based relevance only; always require human/source verification."""
    title = document.get("title") or ""
    description = _normalized(title)
    issues: list[str] = []
    priority = 0
    decision = "datos_insuficientes"
    if not description:
        issues.append("sin titulo")
    elif re.search(r"\b(almacen|logistic|carretill|repartidor|camion|operario de produccion)\b", description):
        decision = "fuera_objetivo"
        issues.append("ambito de almacen o transporte excluido")
    elif any(word in description for word in ("psicologo general sanitario", "psicologia sanitaria", "psicologo sanitario")):
        decision = "requiere_habilitacion_no_acreditada"
        issues.append("la habilitacion sanitaria no consta acreditada en el CV")
    elif re.search(r"\b(trabajador(?:/a|a)? social|trabajadora social)\b", description) and "psicolog" not in description:
        decision = "revisar_titulacion_obligatoria"
        issues.append("titulo especifico de Trabajo Social no documentado en el CV")
    elif re.search(r"\b(enfermeria|enfermero|enfermera|medicina|fisioterapeuta)\b", description):
        decision = "requiere_titulacion_no_acreditada"
        issues.append("titulacion sanitaria especifica no documentada en el CV")
    elif "psicolog" in description and "forense" in description:
        priority = 1
        decision = "revisar_especializacion"
        issues.append("formacion y habilitacion forense especificas pendientes de verificar")
    elif "integrador social" in description and "psicolog" not in description and "educador" not in description:
        priority = 1
        decision = "revisar_titulacion_obligatoria"
        issues.append("comprobar si exige FP de Integracion Social")
    else:
        if ("auxiliar tecnico educativo" in description or
                re.search(r"\bate\b", description)):
            priority = 5 if profile["evidence"]["ate_experience"] else 1
            issues.append("experiencia ATE documentada")
        elif "psicolog" in description:
            priority = 4 if profile["evidence"]["psychology_degree"] else 1
            issues.append("licenciatura en Psicologia documentada; habilitacion del puesto por verificar")
        elif any(x in description for x in ("menor", "familia", "proteccion infantil", "acogimiento")):
            priority = 3 if profile["evidence"]["minors_family"] else 1
            issues.append("experiencia con menores y familias documentada")
        elif any(x in description for x in ("discapacidad", "educacion", "educador",
                                           "intervencion social", "orientador")):
            priority = 2
            issues.append("sector relacionado; requisitos concretos sin verificar")
        decision = "revisar_prioritariamente" if priority >= 3 else "revisar"
    eligibility = document.get("eligibility")
    if eligibility == "no_apta_por_requisito_explicito":
        decision = "requisito_explicito_excluyente"
        priority = 0
        issues.append("requisito obligatorio descartado por el extractor")
    if ((document.get("deadline") and document["deadline"] < today)
            or eligibility == "caducada"
            or document.get("status") == "cerrada_o_historica"):
        decision = "caducada_o_historica"
        priority = 0
        issues.append("plazo vencido o estado historico")
    if document.get("geographic_status") != "dentro_80km":
        priority = min(priority, 1)
        if decision == "revisar_prioritariamente":
            decision = "revisar_ubicacion_antes_de_priorizar"
        issues.append("municipio o distancia pendientes de comprobar; no afirmar radio de 80 km")
    if not document.get("deadline"):
        issues.append("vigencia y plazo no verificados")
    else:
        issues.append("confirmar vigencia en la ficha oficial")
    url = document.get("official_url")
    if not isinstance(url, str) or urlsplit(url).scheme != "https":
        raise ValueError("missing_valid_original_url")
    return {
        "title": title[:350],
        "source_url": url,
        "municipality": document.get("municipality"),
        "province": document.get("province"),
        "priority": priority, "decision": decision,
        "reasons": issues,
        "verified_offer": False,
    }


def review_states(state_dir: Path, profile: dict, today: str | None = None) -> dict:
    today = today or date.today().isoformat()
    if not state_dir.is_dir():
        raise ValueError("state_directory_missing")
    outcomes = []
    totals = {}
    for path in sorted(state_dir.glob("*.json")):
        if path.is_symlink():
            raise ValueError("state_symlink_forbidden")
        state = parse_state(path.read_bytes())
        count = 0
        for document in state["documents"].values():
            if document.get("act_type") != "oferta":
                continue
            count += 1
            outcomes.append(classify_offer(document, profile, today))
        totals[path.stem] = count
    outcomes.sort(key=lambda x: (-x["priority"], x["title"] or "", x["source_url"]))
    return {
        "schema_version": 1, "as_of": today,
        "cv_sha256": profile["cv_sha256"],
        "cv_evidence": profile["evidence"],
        "source_document_counts": totals,
        "offers": outcomes,
        "total_offers": len(outcomes),
        "warning": "Revisión preliminar por título y CV privado; comprobar anuncio, requisitos, plazo, ubicación y habilitación oficial. No se presenta ninguna candidatura."
    }


def review_public_git(repo: Path, profile: dict, *, refresh: bool = False) -> dict:
    """Read only public JSON from one pinned Git commit, without executing it."""
    if refresh:
        subprocess.run(
            ["git", "-C", str(repo), "fetch", "--no-tags", "origin",
             "buscar-curro-resultados"],
            check=True, capture_output=True, text=True, timeout=60,
        )
        ref = "FETCH_HEAD"
    else:
        ref = "origin/buscar-curro-resultados"
    commit = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", ref + "^{commit}"],
        check=True, capture_output=True, text=True, timeout=15,
    ).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("invalid_public_commit")
    with tempfile.TemporaryDirectory(prefix="bc-public-json-") as temp:
        folder = Path(temp)
        for source in ("ett", "publicas", "boe", "docm"):
            output = subprocess.run(
                ["git", "-C", str(repo), "show",
                 f"{commit}:notices/states/{source}.json"],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=15,
            ).stdout
            if len(output) > MAX_RESULTS_BYTES:
                raise ValueError("public_state_too_large")
            parse_state(output)
            (folder / (source + ".json")).write_bytes(output)
        result = review_states(folder, profile)
        result["public_results_commit"] = commit
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cv", type=Path, default=DEFAULT_HOME / "cv_actual.pdf")
    parser.add_argument("--states", type=Path,
                        help="Directorio de estados públicos ya descargados")
    parser.add_argument("--refresh-public", action="store_true",
                        help="Obtener última rama pública desde GitHub en Debian")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path, default=DEFAULT_HOME / "revision_privada.json")
    args = parser.parse_args()
    profile = load_cv_profile(args.cv)
    if args.states and args.refresh_public:
        parser.error("--states y --refresh-public son excluyentes")
    if args.states:
        result = review_states(args.states, profile)
    else:
        result = review_public_git(args.repo, profile, refresh=args.refresh_public)
    output = args.output
    if output.parent.resolve() != DEFAULT_HOME.resolve() or output.is_symlink():
        raise ValueError("output_must_stay_in_private_home")
    output.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if output.parent.stat().st_mode & 0o077:
        raise ValueError("output_directory_not_private")
    payload = (json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    if len(payload) > MAX_RESULTS_BYTES:
        raise ValueError("private_review_too_large")
    atomic_write_bytes(output, payload)
    os.chmod(output, 0o600)
    print(json.dumps({
        "status": "review_completed_privately",
        "cv_verified": True,
        "offers_reviewed": result["total_offers"],
        "high_priority": sum(row["priority"] >= 3 for row in result["offers"]),
        "needs_verification": True,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
