"""Offline checks for public-source review and artifact boundaries."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from bc02_quality import MunicipalityIndex
from employment_core import SourceDocument, SourceRun, apply_runs
from public_connectors import ConnectorSpec, run_connector
from run_public_sources import enrich_public_runs
from state_safety import check_output_budget


class BC04PublicTests(unittest.TestCase):
    def test_public_detail_error_is_partial_not_empty(self):
        spec = ConnectorSpec("demo", "Demo", "https://example.test/jobs", "Demo",
                             ("example.test",), ("/job/",), detail_limit=1)
        listing = '<article><a href="https://example.test/job/1">Educador social</a></article>'
        with patch("public_connectors.fetch", side_effect=[(listing, spec.url), TimeoutError()]):
            run = run_connector(spec)
        self.assertEqual(run.status, "consulta_parcial")
        self.assertEqual(run.error, "detail_errors")
        _, delta = apply_runs({"schema_version": 1, "documents": {}}, [run], "now")
        self.assertFalse(delta["no_changes"])

    def test_public_documents_get_geographic_and_professional_metadata(self):
        doc = SourceDocument(
            "demo", "demo:1", "p", "Educador social", ["educacion"],
            "Toledo", "Toledo", "2026-10-25", "2026-11-01",
            "https://example.test/job", ["Grado en Educación Social"],
            "oferta", "abierta", "hash"
        )
        run = SourceRun("demo", "ok", "now", [doc])
        enrich_public_runs([run], MunicipalityIndex.load(Path("data/municipios_nambroca_80km.csv")))
        self.assertEqual(doc.geographic_status, "dentro_80km")
        self.assertIsNotNone(doc.distance_km)
        self.assertEqual(doc.eligibility, "apta_probable")

    def test_output_budget_detects_oversize_without_deleting(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "output.bin"
            p.write_bytes(b"x" * 21)
            with self.assertRaisesRegex(ValueError, "output_budget_exceeded"):
                check_output_budget(Path(temp), limit=20)
            self.assertEqual(p.stat().st_size, 21)

    def test_output_budget_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            (base / "real").write_text("ok")
            (base / "link").symlink_to(base / "real")
            with self.assertRaisesRegex(ValueError, "output_symlink"):
                check_output_budget(base)


if __name__ == "__main__":
    unittest.main()
