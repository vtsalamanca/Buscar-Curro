import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from private_cv_review import classify_offer, extract_cv_profile, load_cv_profile, review_states


class PrivateProfileTests(unittest.TestCase):
    def setUp(self):
        self.text = (("Licenciatura en Psicología. Auxiliar técnico educativo. "
                      "ACTIA DIAM. ACCEM. Personas con discapacidad. "
                      "Trabajo con menores y familias. Permiso de conducir B. ") * 28)
        self.profile = extract_cv_profile(self.text)
        self.profile["cv_sha256"] = "a" * 64

    def test_profile_extracts_evidence_without_personal_content(self):
        self.assertTrue(self.profile["evidence"]["psychology_degree"])
        self.assertTrue(self.profile["evidence"]["ate_experience"])
        self.assertTrue(self.profile["evidence"]["minors_family"])
        self.assertNotIn("Carlos", json.dumps(self.profile))
        self.assertNotIn("608 ", json.dumps(self.profile))

    def test_profile_requires_essential_documented_anchors(self):
        with self.assertRaises(ValueError):
            extract_cv_profile("estudiante " * 400)

    def doc(self, title, geographic_status="dentro_80km", **extra):
        return {"title": title, "official_url": "https://example.org/oferta",
                "geographic_status": geographic_status, "act_type": "oferta",
                "eligibility": "apta_probable", **extra}

    def test_ate_is_high_priority_when_documented(self):
        r = classify_offer(self.doc("Auxiliar Técnico Educativo"), self.profile, "2026-10-26")
        self.assertEqual(r["priority"], 5)
        self.assertFalse(r["verified_offer"])

    def test_sanitary_habilitation_not_inferred(self):
        r = classify_offer(self.doc("Psicólogo General Sanitario"), self.profile, "2026-10-26")
        self.assertEqual(r["priority"], 0)

    def test_social_worker_slash_gender_not_wrongly_prioritized(self):
        r = classify_offer(self.doc("TRABAJADOR/A SOCIAL | Menores en Acogimiento"), self.profile, "2026-10-26")
        self.assertEqual(r["priority"], 0)
        self.assertEqual(r["decision"], "revisar_titulacion_obligatoria")

    def test_healthcare_and_forensic_specialization_not_inferred(self):
        self.assertEqual(classify_offer(self.doc("Auxiliar de Enfermería"), self.profile, "2026-10-26")["priority"], 0)
        self.assertEqual(classify_offer(self.doc("Psicólogo Forense"), self.profile, "2026-10-26")["priority"], 1)

    def test_ambiguous_geography_cannot_be_priority(self):
        r = classify_offer(self.doc("Psicólogo en Elche", "localidad_desconocida"), self.profile, "2026-10-26")
        self.assertLessEqual(r["priority"], 1)

    def test_expired_and_excluded_stay_excluded(self):
        a = self.doc("Psicólogo", deadline="2026-09-20")
        b = self.doc("Auxiliar Técnico Educativo", eligibility="no_apta_por_requisito_explicito")
        self.assertEqual(classify_offer(a, self.profile, "2026-10-26")["priority"], 0)
        self.assertEqual(classify_offer(b, self.profile, "2026-10-26")["priority"], 0)

    def test_symlink_cv_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src.pdf"
            src.write_bytes(b"%PDF-" + b"x" * 1100)
            src.chmod(0o600)
            link = Path(tmp) / "alias.pdf"
            link.symlink_to(src)
            with self.assertRaisesRegex(ValueError, "symlink"):
                load_cv_profile(link)

    def test_unprivate_pdf_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "cv.pdf"
            src.write_bytes(b"%PDF-" + b"x" * 1100)
            src.chmod(0o644)
            with self.assertRaisesRegex(ValueError, "permissions"):
                load_cv_profile(src)

    def test_valid_empty_state_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = {"schema_version": 1, "documents": {}}
            (Path(tmp) / "boe.json").write_text(json.dumps(state))
            report = review_states(Path(tmp), self.profile, "2026-10-26")
            self.assertEqual(report["total_offers"], 0)
            self.assertEqual(report["cv_sha256"], "a" * 64)


if __name__ == "__main__":
    unittest.main()
