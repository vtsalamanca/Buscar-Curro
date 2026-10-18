import unittest

from public_connectors import ConnectorSpec, make_document, parse_listing, requirements_from, title_from_html


SPEC = ConnectorSpec(
    "test", "Test", "https://jobs.example.test/list", "Example",
    ("example.test",), ("/job/",), "Toledo", detail_limit=0,
)


class PublicConnectorTests(unittest.TestCase):
    def test_listing_keeps_only_allowed_relevant_links(self):
        html = '''
        <ul><li>Psicólogo/a en Toledo <a href="/job/42">Ver oferta</a></li>
        <li>Educador <a href="https://evil.test/job/9">Externa</a></li>
        <li>Contacto <a href="/contact">Ir</a></li></ul>'''
        self.assertEqual(parse_listing(SPEC, html, SPEC.url), [("https://jobs.example.test/job/42", "Psicólogo/a en Toledo Ver oferta")])

    def test_document_extracts_fields_and_requirements(self):
        detail = "Requisitos: Grado en Psicología y experiencia con menores. Fecha de cierre: 31 de octubre de 2026"
        item = make_document(SPEC, "https://jobs.example.test/job/42", "Psicólogo/a en Toledo", detail)
        self.assertIsNotNone(item)
        self.assertEqual(item.deadline, "2026-10-31")
        self.assertEqual(item.status, "abierta")
        self.assertIn("psicologia", item.category)
        self.assertTrue(item.requirements)

    def test_irrelevant_or_suspended_item_is_filtered(self):
        self.assertIsNone(make_document(SPEC, "https://jobs.example.test/job/1", "Ingeniero industrial"))
        self.assertIsNone(make_document(SPEC, "https://jobs.example.test/job/2", "Mozo de almacén logística"))

    def test_title_and_requirements_helpers(self):
        self.assertEqual(title_from_html("<html><h1> Oferta <b>ATE</b> </h1></html>"), "Oferta ATE")
        self.assertEqual(requirements_from("REQUISITOS: Grado en Psicología. COMPETENCIAS: Empatía"), ["Grado en Psicología."])


if __name__ == "__main__":
    unittest.main()
