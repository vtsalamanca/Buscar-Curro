import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock,patch
from infojobs_keyring_client import (
    KeyringState, check_keyring, load_credentials, main
)


class FakeItem:
    def __init__(self, field, value, service="infojobs"):
        self.field,self.value,self.service=field,value,service
    def get_attributes(self):
        return {"service":self.service,"field":self.field}
    def load_secret_sync(self,_):
        return True
    def get_secret(self):
        return Mock(get_text=Mock(return_value=self.value))


class FakeCollection:
    def __init__(self,items,locked=False):
        self.items,self.locked=items,locked
    def get_label(self): return "Credenciales del laboratorio"
    def get_locked(self): return self.locked
    def load_items_sync(self,_): return True
    def get_items(self): return self.items


class FakeSecret:
    class ServiceFlags: LOAD_COLLECTIONS=1
    def __init__(self,collections):
        self.Service=Mock(get_sync=Mock(return_value=Mock(get_collections=Mock(return_value=collections))))


class Tests(unittest.TestCase):
    def setUp(self):
        self.coll=FakeCollection([FakeItem("usuario","SYNTHETIC@example.invalid"),
                                  FakeItem("clave","SYNTHETIC_PRIVATE")])
        self.secret=FakeSecret([self.coll])

    def test_metadata_only_presence(self):
        self.assertEqual(check_keyring(self.secret),KeyringState(True,False,True,True))

    def test_only_exact_dedicated_collection(self):
        self.assertIsNone(load_credentials(FakeSecret([])))
        duplicate=FakeCollection([])
        self.assertIsNone(load_credentials(FakeSecret([self.coll,duplicate])))

    def test_locked_never_reads(self):
        self.coll.locked=True
        self.assertIsNone(load_credentials(self.secret))

    def test_missing_field_or_duplicate_fail_closed(self):
        self.coll.items=self.coll.items[:1]
        self.assertIsNone(load_credentials(self.secret))
        self.coll.items=[FakeItem("usuario","a"),FakeItem("clave","a"),FakeItem("clave","b")]
        self.assertIsNone(load_credentials(self.secret))

    def test_ignores_other_service(self):
        self.coll.items.append(FakeItem("clave","ignored","service_not_allowed"))
        self.assertEqual(load_credentials(self.secret),("SYNTHETIC@example.invalid","SYNTHETIC_PRIVATE"))

    def test_probe_does_not_pass_secrets_to_output(self):
        out=io.StringIO()
        with patch("infojobs_keyring_client.check_keyring",return_value=
                   KeyringState(True,False,True,True)),redirect_stdout(out):
            self.assertEqual(main(["--estado"]),0)
        s=out.getvalue()
        self.assertNotIn("PRIVATE",s)
        self.assertNotIn("example.invalid",s)
        self.assertTrue(json.loads(s)["password_saved"])

    def test_client_does_not_post_or_login_by_http(self):
        from pathlib import Path
        source=Path(__file__).with_name('infojobs_keyring_client.py').read_text()
        self.assertNotIn('infojobs_auth',source)
        self.assertNotIn('urllib.request',source)
        self.assertNotIn('--autenticar-una-vez',source)


if __name__=="__main__":
    unittest.main()
