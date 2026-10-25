"""Full collector entrypoint smoke tests without network or personal data."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_ett_sources
import run_public_sources
from employment_core import SourceDocument, SourceRun
from ett_connectors import EttSpec
from public_connectors import ConnectorSpec


def sample_doc():
    return SourceDocument(
        source="demo", document_id="demo:1", process_id="process-1",
        title="Educador social", category=["educacion", "intervencion_social"],
        municipality="Toledo", province="Toledo", publication_date="2026-10-25",
        deadline="2026-11-10", official_url="https://example.test/job/1",
        requirements=["Grado en Educación Social"], act_type="oferta",
        status="abierta", content_hash="digest", hiring_organization="Entidad Demo",
    )


class OfflinePipelines(unittest.TestCase):
    def test_ett_emits_state_and_explainable_review(self):
        spec = EttSpec("demo", "Agencia", "https://example.test/jobs", ("example.test",), ("/job/",))
        doc = sample_doc()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            args = ["run_ett_sources.py", "--state", str(root / "missing-state.json"),
                    "--output-dir", str(root / "output"), "--page-budget", "1", "--detail-budget", "1"]
            with patch.object(sys, "argv", args), patch.object(run_ett_sources, "ETT_SPECS", (spec,)),                  patch.object(run_ett_sources, "fetch", return_value=("<html></html>", spec.listing_url)),                  patch.object(run_ett_sources, "run_ett_connector",
                              return_value=SourceRun("demo", "ok", "now", [doc])),                  contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(run_ett_sources.main(), 0)
            state = json.loads((root / "output/state.json").read_text())
            review = json.loads((root / "output/review-provisional.json").read_text())
            self.assertIn("demo:1", state["documents"])
            self.assertEqual(review["total_groups"], 1)

    def test_public_emits_enriched_offer_without_external_network(self):
        spec = ConnectorSpec("demo", "Demo", "https://example.test/jobs", "Demo",
                             ("example.test",), ("/job/",))
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            args = ["run_public_sources.py", "--sources", "demo", "--state",
                    str(root / "missing-state.json"), "--output-dir", str(root / "output")]
            with patch.object(sys, "argv", args), patch.object(run_public_sources, "get_spec", return_value=spec),                  patch.object(run_public_sources, "run_connector",
                              return_value=SourceRun("demo", "ok", "now", [sample_doc()])),                  contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(run_public_sources.main(), 0)
            state = json.loads((root / "output/state.json").read_text())
            self.assertEqual(state["documents"]["demo:1"]["geographic_status"], "dentro_80km")
            self.assertTrue((root / "output/review-provisional.json").is_file())


if __name__ == "__main__":
    unittest.main()
