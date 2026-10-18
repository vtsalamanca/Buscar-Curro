"""Una petición pública de diagnóstico. Sin Secrets, login ni modificación de huella."""
import hashlib
import json
import re
import urllib.error
from html.parser import HTMLParser
from infojobs_auth import Session, LOGIN_PAGE

class PageShape(HTMLParser):
    def __init__(self):
        super().__init__()
        self.counts = {k: 0 for k in ('form', 'input', 'iframe', 'script')}
        self.external_script_hosts = set()
        self.skip_text = False
        self.texts = []
    def handle_starttag(self, tag, attrs):
        from urllib.parse import urlsplit
        if tag in ('script', 'style'):
            self.skip_text = True
        if tag in self.counts:
            self.counts[tag] += 1
        if tag == 'script':
            src = dict(attrs).get('src', '')
            host = urlsplit(src).hostname
            if host:
                self.external_script_hosts.add(host)

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip_text = False
    def handle_data(self, data):
        if not self.skip_text:
            self.texts.append(data)

def sanitize(text):
    text = re.sub(r'https?://\S+|[\w.+-]+@[\w.-]+', '[omitted]', text)
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b|\b[\da-fA-F]{16,}\b|\b\d{6,}\b', '[omitted]', text)
    return re.sub(r'\s+', ' ', text).strip()[:500]

result = {'phase': 'public_login_page', 'method': 'GET'}
session = Session()
try:
    import urllib.request
    req = urllib.request.Request(LOGIN_PAGE)
    try:
        response = session.opener.open(req, timeout=20)
    except urllib.error.HTTPError as exc:
        response = exc
    with response:
        raw = response.read(262144)
        headers = response.headers
        text = raw.decode('utf-8', errors='replace')
        parsed = PageShape()
        parsed.feed(text)
        lower = text.lower()
        allowed = [v.strip().upper() for v in headers.get('Allow', '').split(',')]
        result.update({
            'http_status': response.code,
            'allow_header_present': 'Allow' in headers,
            'allowed_methods': [v for v in allowed if v in {'GET','HEAD','POST','OPTIONS','PUT','DELETE','PATCH'}],
            'content_type': headers.get_content_type(),
            'response_bytes_up_to_limit': len(raw),
            'body_hash_prefix': hashlib.sha256(raw).hexdigest()[:16],
            'elements': parsed.counts,
            'public_text_sanitized': sanitize(' '.join(parsed.texts)),
            'public_script_hosts': sorted(parsed.external_script_hosts),
            'markers': {k: k in lower for k in ('captcha','akamai','imperva','datadome','kasada','cloudflare','perimeterx','access denied','method not allowed','enable javascript')},
            'known_security_script_host': any(any(v in host for v in ('captcha','datadome','kasada','perimeterx','hcaptcha','recaptcha','geetest')) for host in parsed.external_script_hosts),
            'external_script_count': len(parsed.external_script_hosts),
            'header_signals': {k: k in headers for k in ('Allow','Location','Set-Cookie','Retry-After','X-DataDome','CF-Mitigated')},
        })
except Exception:
    result['status'] = 'transport_error'
finally:
    session.cookies.clear()
print(json.dumps(result))
