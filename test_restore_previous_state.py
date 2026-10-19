import io
import json
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from restore_previous_state import allowed_artifact_redirect, extract_state, restore, validate_state_bytes


class RestoreStateTests(unittest.TestCase):
    def archive(self, name="state.json", value=None):
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as bundle:
            bundle.writestr(name, json.dumps(value or {"schema_version": 1, "documents": {}}))
        return output.getvalue()

    def test_extracts_valid_state(self):
        self.assertEqual(validate_state_bytes(extract_state(self.archive()))["documents"], {})

    def test_rejects_invalid_schema(self):
        with self.assertRaises(ValueError):
            extract_state(self.archive(value={"schema_version": 2, "documents": {}}))

    def test_rejects_ambiguous_archive(self):
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as bundle:
            bundle.writestr("one/state.json", '{}')
            bundle.writestr("two/state.json", '{}')
        with self.assertRaises(ValueError):
            extract_state(output.getvalue())

    def test_artifact_redirect_allowlist(self):
        self.assertTrue(allowed_artifact_redirect("https://abc.blob.core.windows.net/results/state.zip?sig=x"))
        self.assertTrue(allowed_artifact_redirect("https://objects.githubusercontent.com/a.zip"))
        self.assertFalse(allowed_artifact_redirect("https://evil.example/state.zip"))
        self.assertFalse(allowed_artifact_redirect("http://abc.blob.core.windows.net/state.zip"))

    def test_prior_success_without_valid_artifact_fails_closed(self):
        responses = [
            {"workflow_runs": [{"id": 10}]},
            {"artifacts": [{"name": "ett01-state", "expired": True}]},
        ]
        with patch("restore_previous_state.api_json", side_effect=responses):
            with self.assertRaisesRegex(ValueError, "prior_state_unavailable"):
                restore("owner/repo", "ett01.yml", "ett01-state", 11, "token", Path("test-state-unused.json"))


if __name__ == "__main__":
    unittest.main()
