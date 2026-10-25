"""Offline regression tests: HTTP hard caps and honest partial-source status."""
import tempfile
import unittest
import zipfile
from email.message import Message
from pathlib import Path
from unittest.mock import patch

from employment_core import SourceRun, apply_runs
from ett_connectors import EttSpec, run_ett_connector
from public_connectors import configure_http_budget, fetch, http_metrics, reset_http_metrics
from state_safety import create_snapshot, restore_snapshot


class DummyResponse:
    def __init__(self, raw):
        self.raw = raw
        self.headers = Message()
        self.headers["Content-Type"] = "text/html; charset=utf-8"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, length):
        return self.raw[:length]

    def geturl(self):
        return "https://example.test/jobs"


class HTTPBudgetTests(unittest.TestCase):
    def tearDown(self):
        configure_http_budget()

    def test_request_limit_never_attempts_extra_fetch(self):
        reset_http_metrics()
        configure_http_budget(max_requests=1)
        with patch("public_connectors.build_opener") as patched:
            patched.return_value.open.return_value = DummyResponse(b"<p>Ok</p>")
            self.assertEqual(fetch("https://example.test/jobs", ("example.test",))[0], "<p>Ok</p>")
            with self.assertRaisesRegex(ValueError, "http_budget_exceeded_requests"):
                fetch("https://example.test/jobs", ("example.test",))
            self.assertEqual(patched.return_value.open.call_count, 1)
            self.assertEqual(http_metrics()["http_requests"], 1)

    def test_byte_limit_prevents_full_download(self):
        reset_http_metrics()
        configure_http_budget(max_bytes=4)
        with patch("public_connectors.build_opener") as patched:
            patched.return_value.open.return_value = DummyResponse(b"<html>large</html>")
            with self.assertRaisesRegex(ValueError, "http_budget_exceeded_bytes"):
                fetch("https://example.test/jobs", ("example.test",))
            self.assertLessEqual(http_metrics()["downloaded_bytes"], 5)

    def test_invalid_budget_rejected_before_any_fetch(self):
        with self.assertRaisesRegex(ValueError, "invalid_http_budget"):
            configure_http_budget(max_requests=-1)


class PartialAndSnapshotTests(unittest.TestCase):
    def test_partial_source_never_masquerades_as_no_changes(self):
        state, delta = apply_runs({"schema_version": 1, "documents": {}},
                                  [SourceRun("example", "consulta_parcial", "today", error="detail_errors")], "today")
        self.assertFalse(delta["no_changes"])
        self.assertEqual(delta["source_failures"], {"example": "detail_errors"})

    def test_connector_detail_error_becomes_partial(self):
        spec = EttSpec("demo", "Demo", "https://example.test/jobs",
                       ("example.test",), ("/job/",), detail_limit=1)
        page = '<a href="https://example.test/job/1">Educador social</a>'
        with patch("ett_connectors.fetch", side_effect=TimeoutError):
            run = run_ett_connector(spec, (page, spec.listing_url), {})
        self.assertEqual(run.status, "consulta_parcial")
        self.assertEqual(run.error, "detail_errors")

    def test_symlink_snapshot_cannot_be_restored(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            source = folder / "safe.zip"
            create_snapshot({"schema_version": 1, "documents": {}}, source)
            link = folder / "alias.zip"
            link.symlink_to(source)
            with self.assertRaisesRegex(ValueError, "invalid_snapshot_file"):
                restore_snapshot(link)

    def test_oversize_zip_member_rejected_before_decompression(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            archive = folder / "oversized.zip"
            with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
                z.writestr("state.json", b"x" * (5 * 1024 * 1024 + 1))
                z.writestr("manifest.json", "{}")
            with self.assertRaisesRegex(ValueError, "invalid_snapshot_member"):
                restore_snapshot(archive)


if __name__ == "__main__":
    unittest.main()
