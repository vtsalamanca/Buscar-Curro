import io
import json
import unittest
import urllib.error
from infojobs_auth import *


class Tests(unittest.TestCase):
    def test_allowed_destinations(self):
        for url in [ME, '/candidate/my-infojobs.xhtml']:
            self.assertTrue(safe_redirect(url))
        for url in ['https://evil.invalid', '//evil.invalid', 'http://www.infojobs.net',
                    'https://u:p@www.infojobs.net', 'https://www.infojobs.net:444/']:
            self.assertFalse(safe_redirect(url))

    def test_success(self):
        calls = []
        def fetch(url, data=None, headers=None):
            calls.append(url)
            if url == LOGIN_PAGE: return '<form></form>'
            if url == LOGIN_API:
                self.assertEqual(json.loads(data)['rememberMe'], False)
                return '{}'
            if url == ME: return '{"login":"SYNTHETIC@example.invalid"}'
            if url == APPLICATIONS: return '<h1 class="title">Mis ofertas</h1>'
            raise AssertionError('unexpected_destination')
        result = probe('synthetic@example.invalid', 'SYNTHETIC_PASSWORD', fetch)
        self.assertEqual(result['status'], 'authenticated_current_run')
        self.assertEqual(calls.count(LOGIN_API), 1)
        self.assertNotIn('synthetic', json.dumps(result).lower())
        self.assertFalse(result['future_access_verified'])

    def test_mfa_no_retry(self):
        calls = []
        def fetch(url, data=None, headers=None):
            calls.append(url)
            if url == LOGIN_PAGE: return ''
            error = io.BytesIO(b'{"code":"MfaRequiredByCode","private":"DO_NOT_LOG"}')
            raise urllib.error.HTTPError(url, 400, '', {}, error)
        result = probe('synthetic@example.invalid', 'SYNTHETIC', fetch)
        self.assertEqual(result['status'], 'interaction_required')
        self.assertEqual(calls.count(LOGIN_API), 1)
        self.assertNotIn('DO_NOT_LOG', json.dumps(result))

    def test_wrong_account_stops_private_read(self):
        calls = []
        def fetch(url, data=None, headers=None):
            calls.append(url)
            return '{"login":"other@example.invalid"}' if url == ME else '{}'
        self.assertEqual(probe('synthetic@example.invalid', 'SYNTHETIC', fetch)['status'], 'wrong_account')
        self.assertNotIn(APPLICATIONS, calls)

    def test_redirect_external_blocked(self):
        calls = []
        def fetch(url, data=None, headers=None):
            calls.append(url)
            return '{"redirectUrl":"https://evil.invalid"}' if url == LOGIN_API else ''
        self.assertEqual(probe('synthetic@example.invalid', 'SYNTHETIC', fetch)['status'], 'unexpected_destination')
        self.assertNotIn(ME, calls)

    def test_empty_credentials(self):
        def fetch(*args, **kwargs): raise AssertionError('unexpected_network')
        self.assertEqual(probe('', '', fetch)['status'], 'credentials_not_configured')


if __name__ == '__main__': unittest.main()
