import unittest
from unittest.mock import Mock, patch
import sys
from infojobs_consulta_debian import review


class BrowserOrchestrationTests(unittest.TestCase):
    def test_authenticated_session_read_only(self):
        fake=Mock(return_value={"status":"private_read_verified","applications":1})
        result=review(fake)
        self.assertEqual(result["applications"],1)
        fake.assert_called_once_with("--revisar")

    def test_expired_session_defers_to_official_oauth(self):
        fake=Mock(return_value={"status":"authentication_required"})
        result=review(fake)
        self.assertEqual(result["status"],"official_oauth_authorization_required")
        fake.assert_called_once_with("--revisar")

    def test_unverified_page_stops(self):
        fake=Mock(return_value={"status":"private_read_unverified"})
        result=review(fake)
        self.assertEqual(result["status"],"private_read_unverified")
        fake.assert_called_once_with("--revisar")

    def test_cli_review_uses_accessibility_without_restarting_firefox(self):
        from infojobs_consulta_debian import main
        with patch.object(sys, "argv", ["infojobs_consulta_debian.py", "--revisar"]), \
             patch("infojobs_lector_accesible.main", return_value=0) as reader, \
             patch("infojobs_consulta_debian.run_managed", side_effect=AssertionError("must not restart browser")):
            self.assertEqual(main(), 0)
            reader.assert_called_once_with()

    def test_reader_does_not_call_raw_password_vault(self):
        from pathlib import Path
        source=Path(__file__).with_name("infojobs_consulta_debian.py").read_text()
        self.assertNotIn("load_credentials",source)
        self.assertNotIn("get_credentials",source)
        self.assertNotIn('lookup("clave")',source)
        self.assertIn('official_oauth_authorization_required',source)


if __name__=="__main__":
    unittest.main()
