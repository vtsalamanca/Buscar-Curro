"""BC-06 BOE discovery fixture tests: no external network or billing."""
import unittest
from datetime import date
from urllib.error import HTTPError
from unittest.mock import patch

from boe_discovery import collect_window, parse_daily, request_day

DAY = date(2026, 10, 24)


def xml(day=DAY, *, include_bad=False, malicious=False):
    ident = "BOE-A-2026-22230"
    link = ("https://evil.example/job?id=" + ident) if malicious else (
        "https://www.boe.es/diario_boe/txt.php?id=" + ident
    )
    bad = ("<item><identificador>BOE-A-2026-22231</identificador>"
           "<titulo>Resolución sobre precios del tabaco</titulo>"
           "<url_html>https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-22231</url_html>"
           "</item>") if include_bad else ""
    return (f'<response><status><code>200</code><text>ok</text></status><data>'
            f'<sumario><metadatos><fecha_publicacion>{day:%Y%m%d}</fecha_publicacion></metadatos>'
            f'<diario numero="264"><seccion num="II"><departamento>'
            f'<item><identificador>{ident}</identificador>'
            f'<titulo>Resolución por la que se convocan plazas de Auxiliar Técnico Educativo en Toledo</titulo>'
            f'<url_html>{link}</url_html></item>{bad}'
            f'</departamento></seccion></diario></sumario></data></response>').encode()


class BOEDiscoveryTests(unittest.TestCase):
    def test_daily_selects_professional_call_and_ignores_unrelated(self):
        docs, meta = parse_daily(xml(include_bad=True), DAY)
        self.assertEqual(meta["items_scanned"], 2)
        self.assertEqual(meta["selected"], 1)
        self.assertEqual(docs[0].document_id, "boe:BOE-A-2026-22230")
        self.assertIn("ate", docs[0].category)
        self.assertEqual(docs[0].status, "plazo_desconocido")
        self.assertEqual(docs[0].publication_date, "2026-10-24")

    def test_actual_boelist_university_professors_not_candidate(self):
        sample = xml().decode("utf-8").replace(
            "Resolución por la que se convocan plazas de Auxiliar Técnico Educativo en Toledo",
            "Resolución de 19 de octubre de 2026 de la Universidad de Jaén por la que se convoca concurso de acceso a plazas de cuerpos docentes universitarios.",
        )
        documents, metadata = parse_daily(sample.encode("utf-8"), DAY)
        self.assertEqual(documents, [])
        self.assertEqual(metadata["selected"], 0)

    def test_appointments_awards_and_distant_areas_not_offered_as_jobs(self):
        original = "Resolución por la que se convocan plazas de Auxiliar Técnico Educativo en Toledo"
        misleading_titles = [
            "Orden por la que se nombra personal funcionario de carrera del Cuerpo de Profesores de Enseñanza Secundaria en Cataluña.",
            "Extracto de la convocatoria de los Premios Extraordinarios de Formación Profesional de Ceuta y Melilla.",
            "Resolución de la Universidad de Valladolid por la que se convoca proceso selectivo de Técnico Superior de Educación Física.",
        ]
        for title in misleading_titles:
            with self.subTest(title=title):
                body = xml().decode("utf-8").replace(original, title).encode("utf-8")
                docs, _ = parse_daily(body, DAY)
                self.assertEqual(docs, [])

    def test_actual_local_ate_call_is_preserved(self):
        docs, _ = parse_daily(xml(), DAY)
        self.assertEqual(len(docs), 1)
        self.assertIn("ate", docs[0].category)

    def test_invalid_source_link_never_inserts_record(self):
        docs, meta = parse_daily(xml(malicious=True), DAY)
        self.assertEqual(docs, [])
        self.assertEqual(meta["invalid_entries"], 1)

    def test_wrong_publication_date_is_not_silent(self):
        with self.assertRaisesRegex(ValueError, "boe_wrong_publication_date"):
            parse_daily(xml(day=date(2026, 10, 23)), DAY)

    def test_bad_xml_and_doctype_rejected(self):
        with self.assertRaisesRegex(ValueError, "boe_invalid_xml_bounds"):
            parse_daily(b'<!DOCTYPE foo><response/>', DAY)
        with self.assertRaisesRegex(ValueError, "boe_invalid_xml"):
            parse_daily(b'<broken', DAY)

    def test_absent_day_is_not_same_as_failed_query(self):
        def fake(day):
            return xml(day=day) if day == DAY else None
        result, metrics = collect_window(DAY, days=2, request=fake)
        self.assertEqual(result.status, "ok")
        self.assertEqual(len(result.documents), 1)
        self.assertEqual(metrics["daily"][0]["status"], "no_publicado_o_404")
        self.assertEqual(metrics["daily"][1]["status"], "consultado")

    def test_api_error_yields_explicit_partial_status(self):
        def fake(day):
            if day == date(2026, 10, 23):
                raise TimeoutError("offline synthetic timeout")
            return xml(day=day)
        result, metrics = collect_window(DAY, days=2, request=fake)
        self.assertEqual(result.status, "consulta_parcial")
        self.assertTrue(result.error)
        self.assertEqual(len(metrics["failures"]), 1)
        self.assertEqual(len(result.documents), 1)

    def test_all_404_cannot_be_interpreted_as_no_job_changes(self):
        result, metrics = collect_window(DAY, days=2, request=lambda _: None)
        self.assertEqual(result.status, "consulta_parcial")
        self.assertIn("no_official_editions_verified_in_window", result.error)
        self.assertEqual(result.documents, [])

    def test_seven_day_hard_cap(self):
        with self.assertRaisesRegex(ValueError, "boe_days_limit"):
            collect_window(DAY, days=8, request=lambda day: None)

    def test_official_404_is_distinct_from_network_failure(self):
        error = HTTPError("https://www.boe.es/api", 404, "Not Found", {}, None)
        with patch("urllib.request.build_opener") as opener:
            opener.return_value.open.side_effect = error
            self.assertIsNone(request_day(DAY))
            opener.return_value.open.assert_called_once()


if __name__ == "__main__":
    unittest.main()
