import unittest
from pathlib import Path

from employment_core import (
    SourceDocument,
    SourceRun,
    apply_runs,
    categories_for,
    date_from_text,
    load_state,
)


def document(document_id="doc:1", title="Convocatoria Educador Social Toledo", content_hash="a", act_type="convocatoria"):
    return SourceDocument(
        source="test", document_id=document_id, process_id=document_id, title=title,
        category=["intervencion_social"], municipality="Toledo", province="Toledo",
        publication_date="2026-10-01", deadline="2026-10-31", official_url="https://example.test/1",
        requirements=["Grado en Educación Social"], act_type=act_type, status="abierta", content_hash=content_hash,
    )


class EmploymentCoreTests(unittest.TestCase):
    def test_active_filter_and_suspended_logistics(self):
        self.assertIn("psicologia", categories_for("Psicólogo para intervención con menores"))
        self.assertIn("intervencion_social", categories_for("Trabajador/a Social"))
        self.assertIn("educacion", categories_for("Coordinador de transporte escolar y educación"))
        self.assertNotIn("ate", categories_for("Cobertura por maternidad"))
        self.assertEqual(categories_for("Mozo de almacén y logística"), [])

    def test_spanish_dates(self):
        self.assertEqual(date_from_text("hasta el 31 de octubre de 2026"), "2026-10-31")
        self.assertEqual(date_from_text("publicado 7/7/2026"), "2026-07-07")

    def test_state_detects_new_changed_and_failure(self):
        first = SourceRun("one", "ok", "now", [document()])
        state, delta = apply_runs({"schema_version": 1, "documents": {}}, [first], "now")
        self.assertEqual(delta["new_document_ids"], ["doc:1"])
        changed = SourceRun("one", "ok", "later", [document(content_hash="b")])
        failed = SourceRun("two", "consulta_fallida", "later", error="timeout")
        _, delta = apply_runs(state, [changed, failed], "later")
        self.assertEqual(delta["changed_document_ids"], ["doc:1"])
        self.assertEqual(delta["source_failures"], {"two": "timeout"})
        self.assertFalse(delta["no_changes"])

    def test_related_acts_keep_distinct_ids(self):
        first = document("doc:1", "Convocatoria Educador Social Toledo", act_type="convocatoria")
        second = document("doc:2", "Corrección Educador Social Toledo", act_type="correccion")
        state, _ = apply_runs({"schema_version": 1, "documents": {}}, [SourceRun("x", "ok", "now", [first, second])], "now")
        self.assertEqual(state["documents"]["doc:1"]["process_id"], state["documents"]["doc:2"]["process_id"])
        self.assertEqual(first.related_ids, ["doc:2"])

    def test_invalid_state_is_rejected(self):
        path = Path("test-invalid-state.json")
        try:
            path.write_text('{"schema_version": 2, "documents": {}}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_state(path)
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
