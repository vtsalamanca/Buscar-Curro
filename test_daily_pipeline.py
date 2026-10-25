"""Offline, non-network BC-08 continuity and notification tests."""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from daily_pipeline import document_event, generate_summary, minimal_state, run_all, safe_public_url
from state_safety import state_bytes


class DailyPipelineTests(unittest.TestCase):
    def test_safe_url_rejects_credentials_tokens_non_https(self):
        for url in ("http://example.org", "https://me:pass@example.org/a", "https://e.org/?token=abc", "https://e.org/#frag", "https://e.org/\nheader"):
            self.assertIsNone(safe_public_url(url))
        self.assertEqual(safe_public_url("https://example.org/oferta?id=42"), "https://example.org/oferta?id=42")

    def test_state_redaction_drops_private_and_retains_queues(self):
        hash_value = hashlib.sha256(b"public-job").hexdigest()
        state = {
            "schema_version": 1,
            "documents": {
                "id": {"document_id": "id", "source": "tratem", "content_hash": hash_value,
                       "act_type": "oferta", "title": "ATE", "official_url": "https://example.org/oferta",
                       "requirements": ["private applicant email"], "private_notes": "token SECRET", "eligibility": "revisar"},
                "invalid": {"document_id": "invalid", "content_hash": hash_value,
                            "official_url": "https://example.org/?secret=ABC"},
            },
            "personal_email": "do-not-leak@example.com",
            "bc02": {"queues": {"tratem": {"https://example.org/oferta": {"status": "checked", "checks": 2, "label": "ATE", "last_checked": "2026-10-25"}}}},
        }
        clean = minimal_state(state)
        data = state_bytes(clean)
        self.assertNotIn(b"private", data)
        self.assertNotIn(b"SECRET", data)
        self.assertNotIn(b"personal_email", data)
        self.assertEqual(list(clean["documents"]), ["id"])
        self.assertEqual(clean["bc02"]["queues"]["tratem"]["https://example.org/oferta"]["status"], "checked")

    def test_event_is_explicitly_provisional(self):
        e = document_event({"document_id": "doc", "official_url": "https://boe.es/x", "title": "ATE"}, "new")
        self.assertFalse(e["verified_offer"])
        self.assertEqual(len(e["document_hash"]), 64)

    def test_summary_handles_partial_and_truncation(self):
        s = generate_summary("2026-10-25T09:00:00+00:00", [{"source": "boe", "status": "ok"},
                                                         {"source": "ate", "status": "failed"}], list(range(121)))
        self.assertEqual(s["overall_status"], "partial")
        self.assertEqual(s["event_count"], 121)
        self.assertEqual(len(s["events"]), 120)
        self.assertTrue(s["events_truncated"])

    def test_failures_preserve_previous_and_never_claim_no_novelties(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state_file = root / "notices" / "states" / "ett.json"
            state_file.parent.mkdir(parents=True)
            state_file.write_bytes(state_bytes({"schema_version": 1, "documents": {}}))
            before = state_file.read_bytes()
            with patch("daily_pipeline.subprocess.run") as run:
                run.return_value.returncode = 1
                result = run_all(results_dir=root, code_dir=root)
            self.assertEqual(result["overall_status"], "failed")
            self.assertEqual(state_file.read_bytes(), before)
            self.assertTrue(all(item["status"] == "failed" for item in result["sources"]))
            self.assertEqual(json.loads((root / "notices" / "latest.json").read_text())["overall_status"], "failed")
            self.assertEqual(run.call_count, 5)

    def test_corrupt_persistent_state_does_not_reset(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            dest = root / "notices" / "states" / "ett.json"
            dest.parent.mkdir(parents=True)
            dest.write_text("bad JSON")
            with self.assertRaises(ValueError):
                run_all(results_dir=root, code_dir=root, execute=False)
            self.assertEqual(dest.read_text(), "bad JSON")

    def test_ate_baseline_and_change_without_private_data(self):
        from daily_pipeline import monitor_ate
        from unittest.mock import Mock
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            url = "https://empleopublico.castillalamancha.es/docs/toledo.pdf"
            output = {"source": "ate_public_toledo", "status": "public_documents_verified",
                      "documents": [{"url": url, "sha256": "a" * 64}]}
            with patch("daily_pipeline.subprocess.run", return_value=Mock(returncode=0, stdout=json.dumps(output))):
                first, events = monitor_ate(root, root)
                self.assertEqual(first["status"], "ok")
                self.assertEqual(events, [])
                output["documents"][0]["sha256"] = "b" * 64
                with patch("daily_pipeline.subprocess.run", return_value=Mock(returncode=0, stdout=json.dumps(output))):
                    second, events = monitor_ate(root, root)
            self.assertEqual(second["new_or_changed"], 1)
            self.assertEqual(events[0]["type"], "ate_pdf_changed")
            self.assertNotIn("applicant", (root / "ate.json").read_text())

    def test_first_scan_creates_baseline_not_new_offer_alerts(self):
        from unittest.mock import Mock
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ident = "boe:BOE-A-2026-123456"
            doc = {"document_id": ident, "source": "boe", "content_hash": "c" * 64,
                   "title": "Auxiliar técnico educativo", "official_url": "https://www.boe.es/x",
                   "act_type": "convocatoria", "status": "por_verificar"}
            def fake_run(args, **kwargs):
                if args[1].endswith("ate_public.py"):
                    return Mock(returncode=1, stdout="")
                out = Path(args[args.index("--output-dir") + 1])
                out.mkdir(parents=True, exist_ok=True)
                (out / "state.json").write_bytes(state_bytes({
                    "schema_version": 1, "documents": {ident: doc},
                }))
                (out / "delta.json").write_text(json.dumps({
                    "new_document_ids": [ident], "changed_document_ids": [],
                    "source_failures": {},
                }))
                return Mock(returncode=0)
            with patch("daily_pipeline.subprocess.run", side_effect=fake_run):
                first = run_all(results_dir=root, code_dir=root)
                second = run_all(results_dir=root, code_dir=root)
            self.assertEqual(first["events"], [])
            self.assertTrue(all(s.get("initial_baseline") for s in first["sources"][:-1]))
            self.assertEqual(second["event_count"], 4)
            self.assertTrue(all(not s.get("initial_baseline") for s in second["sources"][:-1]))

    def test_ate_http_503_is_explicit_and_history_is_preserved(self):
        from unittest.mock import Mock
        from daily_pipeline import monitor_ate
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state = root / "ate.json"
            state.write_text('{"schema_version":1,"documents":{"https://empleopublico.castillalamancha.es/toledo.pdf":"'
                             + "a" * 64 + '"}}')
            before = state.read_bytes()
            error = {"source": "ate_public_toledo", "status": "access_failed",
                     "error_type": "HTTPError", "http_status": 503}
            with patch("daily_pipeline.subprocess.run",
                       return_value=Mock(returncode=1, stdout=json.dumps(error))):
                status, events = monitor_ate(root, root)
            self.assertEqual(status["reason"], "http_503")
            self.assertTrue(status["state_preserved"])
            self.assertEqual(state.read_bytes(), before)
            self.assertEqual(events, [])

    def test_status_is_red_only_when_all_source_families_fail(self):
        failed = [{"source": "ate", "status": "failed"}]
        self.assertEqual(generate_summary("2026-10-25T00:00:00Z", failed, [])["overall_status"], "failed")
        self.assertEqual(generate_summary("2026-10-25T00:00:00Z", failed +
                         [{"source": "boe", "status": "ok"}], [])["overall_status"], "partial")
        self.assertEqual(generate_summary("2026-10-25T00:00:00Z",
                         [{"source": "boe", "status": "ok"}], [])["overall_status"], "ok")

    def test_seed_is_redacted_before_persisted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed = root / "raw.json"
            raw = {"schema_version": 1, "documents": {}, "my_private_key": "must-never-publish"}
            seed.write_bytes(state_bytes(raw))
            result = run_all(results_dir=root, code_dir=root, execute=False, bootstrap_ett=seed)
            self.assertEqual(result["overall_status"], "failed")
            self.assertNotIn("must-never-publish", (root / "notices" / "states" / "ett.json").read_text())


if __name__ == "__main__":
    unittest.main()
