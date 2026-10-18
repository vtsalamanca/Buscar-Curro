import unittest
from urllib.error import HTTPError, URLError

from source_viability import Source, analyse_html, classify, sanitise_error


class SourceViabilityTests(unittest.TestCase):
    def setUp(self):
        self.source = Source("example", "T", "Example", "https://example.test/jobs", ("empleo",), ("oferta",))

    def test_verified_requires_relevant_page_and_link(self):
        data = analyse_html(self.source, b'<h1>Empleo</h1><a href="/oferta/42">Puesto</a>', self.source.url, "text/html; charset=utf-8")
        self.assertEqual(classify(200, data, None)[0], "verificada_desde_runner")
        self.assertEqual(data["relevant_link_examples"], ["https://example.test/oferta/42"])

    def test_http_200_is_not_enough(self):
        data = analyse_html(self.source, b"<html>Welcome</html>", self.source.url, "text/html")
        self.assertEqual(classify(200, data, None), ("parcial", "http_200_sin_estructura_relevante_confirmada"))

    def test_challenge_is_blocked(self):
        data = analyse_html(self.source, b"<html>CAPTCHA: eres humano o robot</html>", self.source.url, "text/html")
        self.assertEqual(classify(200, data, None), ("bloqueada", "verificacion_humana_detectada"))

    def test_login_is_partial(self):
        body = "<html>Empleo - Iniciar sesi\u00f3n</html>".encode("utf-8")
        data = analyse_html(self.source, body, self.source.url, "text/html")
        self.assertEqual(classify(200, data, None), ("parcial", "carga_publica_con_senal_login"))

    def test_errors_are_sanitised(self):
        error = HTTPError("https://example.test", 403, "forbidden", {}, None)
        try:
            self.assertEqual(sanitise_error(error), "HTTPError:403")
        finally:
            error.close()
        self.assertEqual(sanitise_error(URLError("private host detail")), "network_error")


if __name__ == "__main__":
    unittest.main()
