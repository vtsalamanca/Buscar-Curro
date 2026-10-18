import json
import unittest
import urllib.request
from ate_auth import *


class Tests(unittest.TestCase):
    def config(self):
        return 'pro:{apiUrl:"' + API_URL + '",loginUrl:"' + TOKEN_URL + '",accessToken:"U1lOVEhFVElD"}'

    def test_destinations(self):
        self.assertEqual(parse_config('entorno: pro\r\n', self.config()), 'U1lOVEhFVElD')
        for config, bundle in [('entorno: pre', self.config()), ('entorno: pro', self.config().replace(ROOT, 'https://evil.invalid'))]:
            with self.assertRaises(AuthFailure):
                parse_config(config, bundle)

    def test_identity(self):
        self.assertTrue(identity_matches({'data': {'nif': '12345678-Z'}}, '12345678Z'))
        self.assertFalse(identity_matches({'name': 'Some Name'}, '12345678Z'))
        self.assertFalse(identity_matches({'name': 'Some Name'}, 'Some Name'))

    def test_full_flow_and_no_token_output(self):
        calls = []
        def fetch(url, data=None, headers=None):
            calls.append(url)
            if url.endswith('config.yml'): return 'entorno: pro'
            if url == PORTAL: return '<script src="main.abc123.js"></script>'
            if url.endswith('.js'): return self.config()
            if url == TOKEN_URL: return json.dumps({'access_token': 'SYNTHETIC_TOKEN'})
            if url.endswith('/datos_personales/'): return json.dumps({'nif': '12345678Z'})
            if url.endswith('/llamamientosvolunarios/all'): return '[]'
            raise AssertionError('unexpected_destination')
        result = probe('12345678Z', 'SYNTHETIC_PASSWORD', fetch)
        self.assertEqual(result['status'], 'authenticated_current_run')
        self.assertEqual(calls.count(TOKEN_URL), 1)
        self.assertNotIn('SYNTHETIC', json.dumps(result))
        self.assertFalse(result['future_access_verified'])

    def test_redirects_disabled(self):
        self.assertIsNone(StopRedirect().redirect_request(None, None, 307, '', {}, 'https://evil.invalid'))

    def test_missing_secrets_no_network(self):
        def fail(*args, **kwargs): raise AssertionError('network_used')
        self.assertEqual(probe('', '', fail)['status'], 'credentials_not_configured')


if __name__ == '__main__': unittest.main()
