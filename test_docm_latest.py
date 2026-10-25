"""DOCM current sumario synthetic tests."""
import unittest
from datetime import date

from docm_latest import collect_latest, parse_latest

DAY = date(2026, 10, 23)


def sample(nid="2026/7591", role="Auxiliar Técnico Educativo", publication="2026/10/23"):
    code = nid.replace("/", "_")
    return ('<html><body>'
            '<div><p class="sumario"><a href="./descargarArchivo.do?ruta=' + publication +
            '/pdf/' + code + '.pdf&amp;tipo=rutaDocm">Oposiciones.</a> '
            'Resolución por la que se convoca proceso selectivo de ' + role + ' [NID ' + nid + ']</p>'
            '</div></body></html>')


class DOCMLatestTests(unittest.TestCase):
    def test_parses_valid_nid_official_url_and_date(self):
        docs, meta = parse_latest(sample(), date(2026, 10, 25))
        self.assertEqual(meta["documents_verified"], 1)
        self.assertEqual(meta["publication_date"], DAY.isoformat())
        self.assertEqual(docs[0].document_id, "docm:2026/7591")
        self.assertTrue(docs[0].official_url.startswith("https://docm.jccm.es/docm/"))
        self.assertIn("ate", docs[0].category)

    def test_irrelevant_notice_no_false_candidate(self):
        docs, meta = parse_latest(sample(role="sanciones tributarias"), date(2026, 10, 25))
        self.assertEqual(docs, [])
        self.assertEqual(meta["documents_verified"], 1)

    def test_bad_nid_route_mismatch_not_accepted(self):
        with self.assertRaisesRegex(ValueError, "docm_no_verified_publication_date"):
            parse_latest(sample(nid="2026/7591", publication="2026/10/20").replace("2026_7591.pdf","2026_7592.pdf"),
                         date(2026, 10, 25))

    def test_false_external_domain_blocked(self):
        with self.assertRaisesRegex(ValueError, "docm_no_verified_publication_date"):
            parse_latest(sample().replace("./descargarArchivo.do","https://malicious.test/descargarArchivo.do"),date(2026,10,25))

    def test_mixed_dates_fail_closed(self):
        payload=sample().replace("</body></html>","") + sample(nid="2026/7592",publication="2026/10/22").replace("<html><body>","")
        with self.assertRaisesRegex(ValueError, "docm_mixed_publication_dates"):
            parse_latest(payload, date(2026, 10, 25))

    def test_old_content_is_not_fresh(self):
        with self.assertRaisesRegex(ValueError, "docm_stale_or_future_page"):
            parse_latest(sample(), date(2026, 11, 12))

    def test_html_layout_change_explicit_failure(self):
        res, meta = collect_latest(today=date(2026,10,25),html="<html><body>Changed DOM</body></html>")
        self.assertEqual(res.status, "consulta_fallida")
        self.assertEqual(meta["error"], "docm_no_document_paragraphs")

    def test_no_silent_new_on_repeat(self):
        from employment_core import apply_runs
        first, _ = collect_latest(today=date(2026,10,25),html=sample())
        base, delta = apply_runs({"schema_version":1,"documents":{}}, [first], "now")
        self.assertEqual(len(delta["new_document_ids"]),1)
        _, delta2 = apply_runs(base,[first],"later")
        self.assertTrue(delta2["no_changes"])


if __name__ == "__main__":
    unittest.main()
