"""BC-06 pipeline smoke test, repeated run with only synthetic BOE XML."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import run_boe_discovery
from boe_discovery import collect_window
from test_boe_discovery import DAY, xml


class BOEPipelineTests(unittest.TestCase):
    def test_twice_same_data_not_two_new_publications(self):
        def fake(end, *, days):
            return collect_window(end, days=days, request=lambda day: xml(day=day))
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            previous = root / "before.json"
            for iteration in (1, 2):
                out = root / f"run{iteration}"
                args = ["run_boe_discovery.py", "--as-of", "2026-10-24",
                        "--days", "1", "--state", str(previous), "--output-dir", str(out)]
                with patch.object(sys, "argv", args),                      patch.object(run_boe_discovery, "collect_window", side_effect=fake),                      contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(run_boe_discovery.main(), 0)
                delta = json.loads((out / "delta.json").read_text())
                self.assertEqual(len(delta["new_document_ids"]), 1 if iteration == 1 else 0)
                if iteration == 2:
                    self.assertTrue(delta["no_changes"])
                previous = out / "state.json"


if __name__ == "__main__":
    unittest.main()
