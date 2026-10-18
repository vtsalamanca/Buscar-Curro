"""Prueba InfoJobs de solo lectura. Cookies en memoria, salida sin datos privados."""
import http.cookiejar
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from ate_auth import StopRedirect

ORIGIN = 'https://www.infojobs.net'
LOGIN_PAGE = ORIGIN + '/candidate-login.xhtml'
LOGIN_API = ORIGIN + '/webapp/1/iam-candidate/login'
ME = ORIGIN + '/webapp/2/candidate/me'
APPLICATIONS = ORIGIN + '/candidate/applications/list.xhtml'
ERRORS = {
    'MfaRequiredByLink': 'interaction_required',
    'MfaRequiredByCode': 'interaction_required',
    'MfaFailed': 'interaction_required',
    'MfaBlocked': 'account_blocked',
    'AccountBlocked': 'account_blocked',
    'BadCredentials': 'credentials_rejected',
    'ExpiredPassword': 'password_expired',
    'InvalidParam': 'form_changed',
}


def safe_redirect(url):
    try:
        parsed = urllib.parse.urlsplit(urllib.parse.urljoin(ORIGIN, url))
        return (parsed.scheme == 'https' and parsed.hostname == 'www.infojobs.net'
                and not parsed.username and not parsed.password and parsed.port in (None, 443))
    except (ValueError, TypeError):
        return False


class Session:
    def __init__(self):
        self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            StopRedirect(), urllib.request.HTTPCookieProcessor(self.cookies))

    def fetch(self, url, data=None, headers=None):
        if not safe_redirect(url):
            raise ValueError('unexpected_destination')
        req = urllib.request.Request(url, data=data, headers=headers or {})
        with self.opener.open(req, timeout=20) as response:
            body = response.read(5000001)
            if len(body) > 5000000:
                raise ValueError('response_too_large')
            return body.decode('utf-8')


def probe(username, password, fetch):
    if not username or not password:
        return {'status': 'credentials_not_configured'}
    # Obtener cookies ordinarias desde página oficial; no importar sesión de Edge.
    fetch(LOGIN_PAGE)
    body = json.dumps({'username': username, 'password': password,
                       'rememberMe': False, 'mfa': None}).encode('utf-8')
    try:
        result = json.loads(fetch(LOGIN_API, data=body, headers={
            'Content-Type': 'application/json', 'Accept': 'application/json',
            'Origin': ORIGIN, 'Referer': LOGIN_PAGE}))
    except urllib.error.HTTPError as exc:
        # Examinar únicamente el código de error cerrado, nunca imprimir cuerpo remoto.
        if exc.code == 400:
            try:
                error = json.loads(exc.read(65536))
                return {'status': ERRORS.get(error.get('code'), 'authentication_unverified')}
            except (ValueError, AttributeError):
                return {'status': 'authentication_unverified'}
        raise
    if not isinstance(result, dict):
        return {'status': 'authentication_unverified'}
    if result.get('code') in ERRORS:
        return {'status': ERRORS[result['code']]}
    redirect = result.get('redirectUrl')
    if redirect:
        if not isinstance(redirect, str) or not safe_redirect(redirect):
            return {'status': 'unexpected_destination'}
        fetch(urllib.parse.urljoin(ORIGIN, redirect))
    profile = json.loads(fetch(ME, headers={'Accept': 'application/json'}))
    if not isinstance(profile, dict) or not isinstance(profile.get('login'), str):
        return {'status': 'identity_unverified'}
    if profile['login'].strip().casefold() != username.strip().casefold():
        return {'status': 'wrong_account'}
    page = fetch(APPLICATIONS)
    # Identidad única de /me más señal privada de la página observada.
    if not re.search(r'<h[1-6]\b[^>]*>\s*Mis ofertas\s*</h[1-6]>', page, re.I):
        return {'status': 'private_read_unverified', 'identity_verified': True}
    return {'status': 'authenticated_current_run', 'identity_verified': True,
            'private_read_verified': True, 'future_access_verified': False}


def main():
    result = {'status': 'execution_error'}
    try:
        if os.environ.get('AUTH_RUNTIME_APPROVED') != '1':
            result = {'status': 'runtime_not_approved'}
        else:
            session = Session()
            try:
                result = probe(os.environ.get('INFOJOBS_USERNAME', ''),
                               os.environ.get('INFOJOBS_PASSWORD', ''), session.fetch)
            finally:
                session.cookies.clear()
    except urllib.error.HTTPError as exc:
        result = {'status': 'http_error', 'http_status': exc.code}
    except (urllib.error.URLError, TimeoutError):
        result = {'status': 'network_error'}
    except Exception:
        result = {'status': 'execution_error'}
    result['service'] = 'infojobs'
    print(json.dumps(result))
    return 0 if result['status'] == 'authenticated_current_run' else 1


if __name__ == '__main__':
    sys.exit(main())
