"""Acceso público con Chrome estándar, sin credenciales ni técnicas de evasión."""
import json
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
URL = 'https://www.infojobs.net/candidate-login.xhtml'
result = {'service': 'infojobs', 'mode': 'standard_browser_public_only'}
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=True)
        try:
            context = browser.new_context(accept_downloads=False)
            try:
                page = context.new_page()
                response = page.goto(URL, wait_until='domcontentloaded', timeout=30000)
                result['initial_http_status'] = response.status if response else None
                try:
                    page.wait_for_function("""() => {
                      const visible = e => !!(e && e.getClientRects().length);
                      return [...document.querySelectorAll('input[type=password], iframe')].some(e =>
                        visible(e) && (e.matches('input[type=password]') || /captcha|challenge/i.test(e.src)))
                        || /verify you are human|comprueba que eres humano|captcha/i.test(document.body.innerText);
                    }""", timeout=15000)
                except PlaywrightTimeoutError:
                    pass
                result.update(page.evaluate("""() => {
                  const visible = e => !!(e && e.getClientRects().length);
                  const text = document.body.innerText.toLowerCase();
                  return {
                    login_password_visible: [...document.querySelectorAll('input[type=password]')].some(visible),
                    login_email_visible: [...document.querySelectorAll('input[type=email],input[name=email]')].some(visible),
                    challenge_frame_visible: [...document.querySelectorAll('iframe')].some(e => visible(e) && /captcha|challenge/i.test(e.src)),
                    challenge_text_visible: /captcha|verify you are human|comprueba que eres humano/.test(text),
                    browser_error_page: location.protocol === 'chrome-error:'
                  };
                }"""))
                result['status'] = ('interaction_required' if result['challenge_frame_visible'] or result['challenge_text_visible']
                                    else 'login_form_available' if result['login_password_visible'] or result['login_email_visible']
                                    else 'unverified')
            finally:
                context.close()
        finally:
            browser.close()
except Exception:
    result['status'] = 'browser_probe_error'
print(json.dumps(result))
