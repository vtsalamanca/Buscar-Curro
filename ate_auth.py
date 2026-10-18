"""Prueba de acceso ATE. Solo metadatos a stdout; secretos y tokens en memoria."""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

PORTAL = 'https://bolsasempleopublico.castillalamancha.es/'
ROOT = 'https://bolsasportalfuncionpublica.jccm.es/ServicioPortalBolsasTrabajoFuncionPublica'
TOKEN_URL = ROOT + '/oauth/token'
API_URL = ROOT + '/api/v1/aspirante'


class StopRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class AuthFailure(Exception):
    pass


def request(url, data=None, headers=None, opener=None):
    # Evitar que credenciales/Bearer se reenvíen por redirecciones.
    opener = opener or urllib.request.build_opener(StopRedirect())
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with opener.open(req, timeout=20) as response:
        raw = response.read(15000001)
        if len(raw) > 15000000:
            raise AuthFailure('response_too_large')
        return raw.decode('utf-8')


def parse_config(config, bundle):
    env = re.search(r'^entorno:\s*(\w+)\s*$', config, re.M)
    if not env or env.group(1) != 'pro':
        raise AuthFailure('unexpected_environment')
    block = re.search(r'\bpro:\{([^{}]+)\}', bundle)
    if not block:
        raise AuthFailure('public_config_changed')
    values = dict(re.findall(r'(\w+):"([^"\n]*)"', block.group(1)))
    if values.get('loginUrl') != TOKEN_URL or values.get('apiUrl') != API_URL:
        raise AuthFailure('unexpected_destination')
    # Identificador de aplicación publicado por el propio frontend, no secreto del usuario.
    basic = values.get('accessToken', '')
    if not re.fullmatch(r'[A-Za-z0-9+/=]{8,1024}', basic):
        raise AuthFailure('public_config_changed')
    return basic


def app_config(fetch=request):
    config = fetch(PORTAL + 'assets/config/config.yml')
    html = fetch(PORTAL)
    script = re.search(r'<script[^>]+src="(main\.[a-zA-Z0-9]+\.js)"', html)
    if not script:
        raise AuthFailure('public_config_changed')
    bundle = fetch(PORTAL + script.group(1))
    return parse_config(config, bundle)


def identity_matches(profile, expected):
    # Comparación exacta normalizada, sin inferir identidad de nombres o JWT sin verificar.
    expected = re.sub(r'[\s-]', '', expected).upper()
    if not re.fullmatch(r'(?:[0-9]{8}[A-Z]|[XYZ][0-9]{7}[A-Z])', expected):
        return False
    pending = [profile]
    while pending:
        value = pending.pop()
        if isinstance(value, dict):
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value)
        elif isinstance(value, str) and re.sub(r'[\s-]', '', value).upper() == expected:
            return True
    return False


def probe(username, password, fetch=request):
    if not username or not password:
        return {'status': 'credentials_not_configured'}
    basic = app_config(fetch)
    body = urllib.parse.urlencode({'grant_type': 'password', 'username': username,
                                  'password': password}).encode('utf-8')
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': 'Basic ' + basic}
    token = json.loads(fetch(TOKEN_URL, data=body, headers=headers))
    access = token.get('access_token')
    if not isinstance(access, str) or not access or '\r' in access or '\n' in access:
        return {'status': 'token_unverified'}
    auth = {'Authorization': 'Bearer ' + access, 'Accept': 'application/json'}
    profile = json.loads(fetch(API_URL + '/datos_personales/', headers=auth))
    if not identity_matches(profile, username):
        return {'status': 'identity_unverified'}
    # Solo lectura; no aceptación, modificación de datos ni marcado de notificaciones.
    offers = json.loads(fetch(API_URL + '/llamamientosvolunarios/all', headers=auth))
    if not isinstance(offers, (dict, list)):
        return {'status': 'private_read_unverified'}
    return {'status': 'authenticated_current_run', 'identity_verified': True,
            'private_read_verified': True, 'future_access_verified': False}


def main():
    result = {'status': 'execution_error'}
    try:
        if os.environ.get('AUTH_RUNTIME_APPROVED') != '1':
            result = {'status': 'runtime_not_approved'}
        else:
            result = probe(os.environ.get('ATE_USERNAME', ''), os.environ.get('ATE_PASSWORD', ''))
    except AuthFailure as exc:
        result = {'status': str(exc)}  # Solo códigos internos cerrados, nunca error remoto.
    except urllib.error.HTTPError as exc:
        result = {'status': 'http_error', 'http_status': exc.code}
    except (urllib.error.URLError, TimeoutError):
        result = {'status': 'network_error'}
    except Exception:
        result = {'status': 'execution_error'}
    result['service'] = 'ate'
    print(json.dumps(result))
    return 0 if result['status'] == 'authenticated_current_run' else 1


if __name__ == '__main__':
    sys.exit(main())
