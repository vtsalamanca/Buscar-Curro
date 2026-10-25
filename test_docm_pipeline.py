"""Offline DOCM runner smoke and safe-failure tests."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import run_docm_latest
from docm_latest import collect_latest
from test_docm_latest import sample


class DOCMRunnerTests(unittest.TestCase):
    def test_repeat_does_not_generate_false_new_documents(self):
        def fake(*, today):
            return collect_latest(today=date(2026, 10, 25), html=sample())
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            previous = root / "missing.json"
            for number in (1, 2):
                output = root / f"pass{number}"
                args = ["run_docm_latest.py", "--state", str(previous), "--output-dir", str(output)]
                with patch.object(sys, "argv", args),                      patch.object(run_docm_latest, "collect_latest", side_effect=fake),                      contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(run_docm_latest.main(), 0)
                delta = json.loads((output / "delta.json").read_text())
                self.assertEqual(len(delta["new_document_ids"]), 1 if number == 1 else 0)
                if number == 2:
                    self.assertTrue(delta["no_changes"])
                previous = output / "state.json"

    def test_broken_site_exits_nonzero_without_claiming_success(self):
        def fake(*, today):
            return collect_latest(today=date(2026, 10, 25), html="<div>No sumario</div>")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            args = ["run_docm_latest.py", "--state", str(root / "missing.json"),
                    "--output-dir", str(root / "output")]
            with patch.object(sys, "argv", args),                  patch.object(run_docm_latest, "collect_latest", side_effect=fake),                  contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(run_docm_latest.main(), 2)
            d = json.loads((root / "output/delta.json").read_text())
            self.assertFalse(d["no_changes"])
            self.assertTrue(d["source_failures"])


if __name__ == "__main__":
    unittest.main()
