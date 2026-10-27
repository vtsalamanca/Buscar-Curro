import base64
import json
import os
import tempfile
import unittest
import urllib.parse
from pathlib import Path
from unittest.mock import patch

import infojobs_oauth_oficial as ij


class OAuthOfficialTests(unittest.TestCase):
    def test_authorisation_url_contains_only_public_client_id(self):
        url=ij.authorisation_url("demo-client-12","a"*32)
        parsed=urllib.parse.urlsplit(url)
        args=urllib.parse.parse_qs(parsed.query)
        self.assertEqual(parsed.scheme,"https")
        self.assertEqual(parsed.hostname,"www.infojobs.net")
        self.assertEqual(args["scope"],["MY_APPLICATIONS,APPLICATION_TIMELINE"])
        self.assertEqual(args["redirect_uri"],[ij.DESKTOP_REDIRECT])
        self.assertEqual(args["response_type"],["code"])
        self.assertEqual(args["state"],["a"*32])
        self.assertNotIn("password",url)

    def test_invalid_client_id_and_state_rejected(self):
        for cid in ("", "a", "bad&id=value", "bad@example.com"):
            with self.assertRaises(ValueError):
                ij.authorisation_url(cid,"a"*32)
        with self.assertRaises(ValueError):
            ij.authorisation_url("demo-client-12","short")

    def test_exact_endpoint_allowlist_no_arbitrary_urls(self):
        for target in ("http://www.infojobs.net/oauth/authorize",
                       "https://evil.invalid/oauth/authorize",
                       "https://www.infojobs.net.evil.invalid/oauth/authorize"):
            with self.assertRaisesRegex(ValueError,"destino"):
                ij.fetch_json(target)

    def test_token_body_is_urlencoded(self):
        body=ij._token_form("authorization_code","id","secret+/&",code="abc")
        args=urllib.parse.parse_qs(body.decode())
        self.assertEqual(args["client_secret"],["secret+/&"])
        self.assertEqual(args["grant_type"],["authorization_code"])
        self.assertEqual(args["redirect_uri"],[ij.DESKTOP_REDIRECT])

    def test_accept_only_authorized_grants(self):
        with self.assertRaises(ValueError):
            ij._token_form("password","id","secret")

    def test_credentials_not_in_authorisation_url(self):
        self.assertEqual("client_secret" in ij.authorisation_url("demo-client-12","a"*32),False)

    def test_redeem_only_credentials_of_developer_and_save_tokens(self):
        calls=[]
        def transport(url,**k):
            self.assertEqual(url,ij.TOKEN_ENDPOINT)
            form=urllib.parse.parse_qs(k["body"].decode())
            self.assertEqual(form["grant_type"],["authorization_code"])
            calls.append(url)
            return {"access_token":"A"*40,"refresh_token":"R"*40}
        store=[]
        with patch.object(ij,"lookup",side_effect=["app-demo-9","SYNTHETIC-APP-SECRET"]),patch.object(ij,"store",side_effect=lambda f,v:store.append(f)):
            self.assertTrue(ij.redeem_code("authorizationcode123",transport=transport))
        self.assertEqual(store,["access_token","refresh_token"])
        self.assertEqual(len(calls),1)

    def test_minimal_report_excludes_private_and_token_fields(self):
        data={"applications":[{"jobOffer":{"title":"Psicólogo","company":"Empresa","city":"Toledo"},
            "rejected":False,"name":"PRIVATE-NAME","access_token":"SECRET-NOT-LOGGED"}],
            "token":"SYNTHETIC"}
        result=ij._minimal_report(data)
        serialized=json.dumps(result)
        for text in ("PRIVATE-NAME","SECRET-NOT-LOGGED","SYNTHETIC","Toledo"):
            self.assertNotIn(text,serialized)
        self.assertEqual(result["count"],1)
        self.assertEqual(result["applications"][0]["title"],"Psicólogo")

    def test_save_report_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            p.chmod(0o700)
            with patch("os.getuid",return_value=p.stat().st_uid):
                ij.save_report({"count":0,"applications":[]},p)
            target=p/"infojobs_oauth_privado.json"
            self.assertEqual(target.stat().st_mode&0o777,0o600)
            target.unlink()
            outside=p/"external";outside.write_text("untouched")
            target.symlink_to(outside)
            with self.assertRaisesRegex(RuntimeError,"enlace"):
                ij.save_report({"count":0},p)

    def test_http_basic_bearer_combined_header(self):
        result=ij._header("id","devsecret","accesstoken")
        self.assertTrue(result.startswith("Basic "))
        self.assertIn(",Bearer accesstoken",result)
        raw=result.split(",",1)[0].split(" ",1)[1]
        self.assertEqual(base64.b64decode(raw).decode(),"id:devsecret")

    def test_no_login_password_grant_or_candidate_password(self):
        source=Path(ij.__file__).read_text()
        self.assertNotIn('grant_type="password"',source)
        self.assertNotIn('infojobs_keyring_client',source)
        self.assertNotIn('lookup("clave")',source)


if __name__=="__main__":
    unittest.main()
