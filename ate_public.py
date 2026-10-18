"""Public ATE source probe: metadata only, no applicant data retained."""
import hashlib
import json
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
from urllib.request import Request, urlopen

SOURCE = 'https://empleopublico.castillalamancha.es/bolsas/personal-laboral/grupo-iii-auxiliar-tecnico-educativo'
HOST = urlsplit(SOURCE).hostname
LIMIT = 12 * 1024 * 1024

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.current = None
    def handle_starttag(self, tag, attrs):
        if tag == 'a': self.current = [dict(attrs).get('href', ''), '']
    def handle_data(self, data):
        if self.current is not None: self.current[1] += data
    def handle_endtag(self, tag):
        if tag == 'a' and self.current is not None:
            self.links.append(self.current); self.current = None

def toledo_links(html):
    p = Links(); p.feed(html)
    result = set()
    for href, label in p.links:
        url = urljoin(SOURCE, href)
        parsed = urlsplit(url)
        if (parsed.scheme == 'https' and parsed.hostname == HOST
                and parsed.path.lower().endswith('.pdf')
                and 'toledo' in (unquote(parsed.path) + ' ' + label).lower()):
            result.add(url)
    if not result: raise ValueError('toledo_document_missing')
    return sorted(result)

def read(url):
    # Redirect targets must remain within the official source host.
    from urllib.request import build_opener, HTTPRedirectHandler
    class OfficialRedirect(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            target = urljoin(req.full_url, newurl)
            if urlsplit(target).scheme != 'https' or urlsplit(target).hostname != HOST:
                raise ValueError('unexpected_redirect')
            return super().redirect_request(req, fp, code, msg, headers, target)
    with build_opener(OfficialRedirect()).open(Request(url, headers={'User-Agent':'Buscar-Curro-public-source-check/1.0'}), timeout=30) as r:
        body = r.read(LIMIT + 1)
        if len(body) > LIMIT: raise ValueError('response_too_large')
        return body

def main():
    try:
        html = read(SOURCE).decode('utf-8')
        if 'Auxiliar Técnico Educativo' not in html: raise ValueError('unexpected_page')
        documents = []
        for url in toledo_links(html):
            body = read(url)
            if not body.startswith(b'%PDF-'): raise ValueError('invalid_pdf')
            documents.append({'url':url, 'sha256':hashlib.sha256(body).hexdigest(), 'bytes':len(body)})
        print(json.dumps({'source':'ate_public_toledo','status':'public_documents_verified','documents':documents,'content_extracted':False}, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(json.dumps({'source':'ate_public_toledo','status':'access_failed','error_type':type(exc).__name__}))
        return 1

if __name__ == '__main__': sys.exit(main())
