import json
import urllib.error
import urllib.request
from infojobs_auth import Session, LOGIN_PAGE, ME

for label, url in [('login_page', LOGIN_PAGE), ('private_identity_without_session', ME)]:
    session = Session()
    try:
        response = session.fetch(url)
        print(json.dumps({'phase': label, 'http_status': 200, 'response_received': True}))
    except urllib.error.HTTPError as exc:
        body = exc.read(65536).decode('utf-8', errors='replace').lower()
        signals = {word: word in body for word in ['captcha', 'datadome', 'cloudflare', 'access denied']}
        print(json.dumps({'phase': label, 'http_status': exc.code, 'challenge_signals': signals}))
    except Exception:
        print(json.dumps({'phase': label, 'status': 'transport_error'}))
    finally:
        session.cookies.clear()
