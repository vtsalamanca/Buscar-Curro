import unittest
from unittest.mock import Mock
from infojobs_consulta_debian import review,find_browser_processes


class BrowserOrchestrationTests(unittest.TestCase):
    def test_authenticated_skips_keyring(self):
        fake=Mock(return_value={"status":"private_read_verified","applications":1})
        key=Mock(side_effect=RuntimeError("vault_must_not_be_loaded"))
        result=review(fake,key)
        self.assertEqual(result["applications"],1)
        fake.assert_called_once_with("--revisar")
        key.assert_not_called()

    def test_auth_required_uses_credentials_one_time(self):
        fake=Mock(side_effect=[
            {"status":"authentication_required"},
            {"status":"login_submitted_check_session"},
            {"status":"private_read_verified","applications":1},
        ])
        key=Mock(return_value=("synthetic@example.invalid","SYNTHETIC"))
        result=review(fake,key)
        self.assertEqual(result["status"],"private_read_verified")
        self.assertEqual(fake.call_count,3)
        self.assertEqual(fake.call_args_list[1].args[0],"--iniciar-sesion")
        key.assert_called_once()

    def test_failed_mfa_does_not_retry(self):
        fake=Mock(side_effect=[
            {"status":"authentication_required"},
            {"status":"login_submitted_check_session"},
            {"status":"authentication_required"},
        ])
        result=review(fake,lambda:("synthetic@example.invalid","SYNTHETIC"))
        self.assertEqual(result["status"],"second_factor_or_login_required")
        self.assertEqual(fake.call_count,3)

    def test_missing_keyring_does_not_try_login(self):
        fake=Mock(return_value={"status":"authentication_required"})
        result=review(fake,lambda:None)
        self.assertEqual(result["status"],"vault_locked_or_missing")
        fake.assert_called_once()

    def test_unverified_page_stops(self):
        fake=Mock(return_value={"status":"private_read_unverified"})
        result=review(fake,Mock())
        self.assertEqual(result["status"],"private_read_unverified")
        fake.assert_called_once()


if __name__=="__main__":
    unittest.main()
