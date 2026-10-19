import unittest
from pathlib import Path

from bc02_quality import MunicipalityIndex, requirement_evaluation


class BC02QualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = MunicipalityIndex.load(Path("data/municipios_nambroca_80km.csv"))

    def test_catalogue_has_259_unique_municipalities(self):
        self.assertEqual(len(self.index.rows), 259)
        self.assertEqual(self.index.classify("Nambroca", "Toledo")[0], "dentro_80km")

    def test_unknown_municipality_is_never_silently_rejected(self):
        self.assertEqual(self.index.classify("Barrio inventado", None), ("localidad_desconocida", None))

    def test_sanitary_habilitation_requires_review(self):
        result = requirement_evaluation(
            "Se exige Máster General Sanitario obligatorio", "abierta", "dentro_80km",
        )
        self.assertEqual(result["eligibility"], "no_apta_por_requisito_explicito")
        self.assertTrue(result["habilitation_requirements"])

    def test_expired_offer_is_caducada(self):
        self.assertEqual(requirement_evaluation("Grado en Psicología", "cerrada_o_historica", "dentro_80km")["eligibility"], "caducada")


if __name__ == "__main__":
    unittest.main()
