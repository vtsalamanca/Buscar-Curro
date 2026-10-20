import unittest
from unittest.mock import patch

from ett_connectors import EttSpec, run_ett_connector
from public_connectors import ConnectorSpec, parse_listing


class PruebasConectoresSinRed(unittest.TestCase):
    def test_publico_rechaza_destino_externo(self):
        spec = ConnectorSpec("demo", "Demo", "https://example.test/jobs", "Demo",
                             ("example.test",), ("/job/",), "Toledo", detail_limit=0)
        html = '<a href="https://externo.test/job/1">Educador social</a>'
        self.assertEqual(parse_listing(spec, html, spec.url), [])

    def test_ett_usa_fixture_sin_descargar(self):
        spec = EttSpec("demo", "Demo", "https://example.test/jobs",
                       ("example.test",), ("/job/",), detail_limit=0)
        with patch("ett_connectors.fetch", side_effect=AssertionError("No descargar")) as fetch:
            run_ett_connector(spec, ('<html><body>Sin ofertas</body></html>', spec.listing_url), {})
            fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
