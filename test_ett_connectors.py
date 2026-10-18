import unittest

from ett_connectors import ETT_SPECS, job_postings, listing_links, _document_from_job


class EttConnectorTests(unittest.TestCase):
    def test_jobposting_in_graph_ignores_other_schema(self):
        html = '''<script type="application/ld+json">{"@graph":[{"@type":"BreadcrumbList"},{"@type":"JobPosting","title":"Educador social","datePosted":"2026-10-18","validThrough":"2026-10-30","jobLocation":{"address":{"addressLocality":"Toledo","addressRegion":"Toledo"}}}]}</script>'''
        posts = job_postings(html)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["title"], "Educador social")

    def test_listing_excludes_login_and_alert_links(self):
        spec = ETT_SPECS[0]
        html = '<article>Docente <a href="/oferta/docente">Ver oferta</a><a href="/oferta/login">Login</a></article>'
        self.assertEqual(listing_links(spec, html, spec.listing_url), [("https://agenciaempleo.tratem.com/oferta/docente", "Docente Ver oferta Login")])

    def test_expired_jobposting_is_historical(self):
        spec = ETT_SPECS[0]
        item = {"@type": "JobPosting", "title": "Docente", "datePosted": "2025-01-01", "validThrough": "2025-02-01"}
        doc = _document_from_job(spec, "https://agenciaempleo.tratem.com/oferta/docente", item, "", "")
        self.assertEqual(doc.status, "cerrada_o_historica")

    def test_adecco_contradiction_is_not_silently_resolved(self):
        spec = ETT_SPECS[1]
        item = {"title": "Coordinador educación", "description": "Tiempo completo temporal. 20h fijo discontinuo"}
        doc = _document_from_job(spec, "https://www.adecco.com/es-es/ofertas-trabajo/x/id", item, "", "")
        self.assertIn("datos_contradictorios:jornada", doc.data_quality)
        self.assertIn("datos_contradictorios:contrato", doc.data_quality)

    def test_suspended_logistics_is_filtered(self):
        spec = ETT_SPECS[2]
        item = {"title": "Mozo de almacén con discapacidad", "description": "Logística"}
        self.assertIsNone(_document_from_job(spec, "https://jobs.eurofirms.com/es/es/x", item, "", ""))


if __name__ == "__main__":
    unittest.main()
