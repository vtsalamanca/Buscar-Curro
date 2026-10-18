import io
import json
import unittest
import zipfile

from restore_previous_state import extract_state, validate_state_bytes


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


if __name__ == "__main__":
    unittest.main()
