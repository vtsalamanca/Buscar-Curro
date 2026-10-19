import unittest
from unittest.mock import patch

from ett_connectors import EttSpec, ETT_SPECS, job_postings, listing_links, pagination_links, run_ett_connector, unrelated_gi_redirect, _document_from_job


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

    def test_pagination_uses_only_explicit_same_host_links(self):
        spec = ETT_SPECS[3]
        html = '<a href="/candidatos/ofertas-empleo/p-toledo/pg-2/">Siguiente</a><a href="https://evil.test/page-2">Next</a>'
        self.assertEqual(
            pagination_links(spec, html, spec.listing_url),
            ["https://www.randstad.es/candidatos/ofertas-empleo/p-toledo/pg-2/"],
        )

    def test_expired_jobposting_is_historical(self):
        spec = ETT_SPECS[0]
        item = {"@type": "JobPosting", "title": "Docente", "datePosted": "2025-01-01", "validThrough": "2025-02-01"}
        doc = _document_from_job(spec, "https://agenciaempleo.tratem.com/oferta/docente", item, "", "")
        self.assertEqual(doc.status, "cerrada_o_historica")

    def test_old_tratem_ad_without_deadline_is_historical(self):
        spec = ETT_SPECS[0]
        item = {"@type": "JobPosting", "title": "Docente", "datePosted": "2025-10-29"}
        doc = _document_from_job(spec, "https://agenciaempleo.tratem.com/oferta/docente", item, "", "")
        self.assertEqual(doc.status, "cerrada_o_historica")
        self.assertIn("anuncio_antiguo_sin_cierre", doc.data_quality)

    def test_adecco_contradiction_is_not_silently_resolved(self):
        spec = ETT_SPECS[1]
        item = {"title": "Coordinador educación", "description": "Tiempo completo temporal. 20h fijo discontinuo"}
        doc = _document_from_job(spec, "https://www.adecco.com/es-es/ofertas-trabajo/x/id", item, "", "")
        self.assertIn("datos_contradictorios:jornada", doc.data_quality)
        self.assertIn("datos_contradictorios:contrato", doc.data_quality)

    def test_property_value_identifier_uses_unique_value(self):
        spec = ETT_SPECS[5]
        item = {
            "title": "Educador social", "description": "Intervención social",
            "identifier": {"@type": "PropertyValue", "name": "Gi Group SpA", "value": "103825"},
        }
        doc = _document_from_job(spec, "https://es.gigroup.com/ofertas-de-trabajo-detalle/x/103825/", item, "", "")
        self.assertEqual(doc.document_id, "gi_group:103825")

    def test_dynamic_page_chrome_does_not_change_hash(self):
        spec = ETT_SPECS[0]
        item = {"title": "Docente", "description": "Requisitos: Grado en Educación."}
        first = _document_from_job(spec, "https://agenciaempleo.tratem.com/oferta/docente", item, "", "sesión 1")
        second = _document_from_job(spec, "https://agenciaempleo.tratem.com/oferta/docente", item, "", "sesión 2")
        self.assertEqual(first.content_hash, second.content_hash)

    def test_suspended_logistics_is_filtered(self):
        spec = ETT_SPECS[2]
        item = {"title": "Mozo de almacén con discapacidad", "description": "Logística"}
        self.assertIsNone(_document_from_job(spec, "https://jobs.eurofirms.com/es/es/x", item, "", ""))

    def test_html_navigation_does_not_make_unrelated_title_relevant(self):
        spec = ETT_SPECS[0]
        item = {"title": "Camarero de pisos", "description": "Menú: formación, educación y empleo", "_html_fallback": True}
        self.assertIsNone(_document_from_job(spec, "https://agenciaempleo.tratem.com/oferta/camarero", item, "", item["description"]))

    def test_gi_detail_redirect_to_catalogue_is_rejected(self):
        spec = ETT_SPECS[5]
        self.assertTrue(unrelated_gi_redirect(spec, "https://es.gigroup.com/ofertas-de-trabajo/"))
        self.assertFalse(unrelated_gi_redirect(spec, "https://es.gigroup.com/ofertas-de-trabajo-detalle/trabajo-x/"))

    def test_snapshot_is_reused_and_queue_rotates_pending_details(self):
        spec = EttSpec(
            "demo", "Demo", "https://example.test/jobs", ("example.test",), ("/job/",),
            seed_urls=("https://example.test/job/a",), detail_limit=1,
        )
        listing = '<article><a href="/job/a">Docente A</a></article><article><a href="/job/b">Educador social B</a></article>'
        queue = {}

        def detail(url, hosts):
            return f"<h1>{'Docente A' if url.endswith('/a') else 'Educador social B'}</h1>", url

        with patch("ett_connectors.fetch", side_effect=detail) as mocked:
            run_ett_connector(spec, (listing, spec.listing_url), queue)
            first_checked = {url for url, item in queue.items() if item["status"] == "checked"}
            run_ett_connector(spec, (listing, spec.listing_url), queue)
        self.assertEqual(mocked.call_count, 2)  # one detail per run; listing is never downloaded twice
        self.assertEqual(len(first_checked), 1)
        self.assertEqual({url for url, item in queue.items() if item["status"] == "checked"}, set(queue))

    def test_disappeared_pending_candidate_is_not_left_pending(self):
        spec = EttSpec("demo", "Demo", "https://example.test/jobs", ("example.test",), ("/job/",), detail_limit=1)
        queue = {"https://example.test/job/old": {"label": "Docente", "status": "pending", "checks": 0}}
        with patch("ett_connectors.fetch") as mocked:
            run_ett_connector(spec, ("<html></html>", spec.listing_url), queue)
        self.assertEqual(queue["https://example.test/job/old"]["status"], "not_listed")
        mocked.assert_not_called()


if __name__ == "__main__":
    unittest.main()
