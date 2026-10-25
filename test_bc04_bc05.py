"""Pruebas adversariales para persistencia, consumo y selección BC-04/BC-05."""
import json
import tempfile
import unittest
from pathlib import Path

from bc02_quality import requirement_evaluation
from employment_core import SourceDocument
from state_safety import atomic_write_json, create_snapshot, restore_snapshot, validate_state
from offer_review import build_review


class BC04StateTests(unittest.TestCase):
    def test_snapshot_roundtrip_keeps_queue_and_hash(self):
        state = {"schema_version": 1, "documents": {"ett:x": {"document_id": "ett:x", "content_hash": "abc"}},
                 "bc02": {"queues": {"ett": {"https://example.test/o": {"status": "error", "checks": 2}}}}}
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            archive = root / "backup.snapshot.zip"
            create_snapshot(state, archive)
            restored = restore_snapshot(archive)
            self.assertEqual(state, restored)
            with self.assertRaises(FileExistsError):
                create_snapshot(state, archive)

    def test_snapshot_corruption_fails_without_overwriting_target(self):
        state = {"schema_version": 1, "documents": {}}
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            archive = root / "snapshot.zip"
            target = root / "current.json"
            atomic_write_json(target, state)
            before = target.read_bytes()
            create_snapshot(state, archive)
            broken = bytearray(archive.read_bytes())
            broken[len(broken)//2] ^= 5
            archive.write_bytes(broken)
            with self.assertRaises((ValueError, OSError, RuntimeError, EOFError, Exception)):
                restore_snapshot(archive, target)
            self.assertEqual(before, target.read_bytes())

    def test_invalid_state_and_identifier_mismatch_fail_closed(self):
        with self.assertRaises(ValueError):
            validate_state({"schema_version": 1, "documents": []})
        with self.assertRaises(ValueError):
            validate_state({"schema_version": 1, "documents": {"x": {"document_id": "y"}}})

    def test_atomic_write_keeps_existing_file_if_payload_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "state.json"
            p.write_text("ORIGINAL", encoding="utf-8")
            with self.assertRaises((TypeError, ValueError)):
                atomic_write_json(p, {"unserializable": object()})
            self.assertEqual(p.read_text(encoding="utf-8"), "ORIGINAL")


def doc(ident, title="Psicólogo de menores", employer="Entidad A", municipality="Toledo",
        category=("psicologia",), eligibility="apta_probable", deadline=None):
    return SourceDocument(
        source=ident.split(":")[0], document_id=ident, process_id=ident,
        title=title, category=list(category), municipality=municipality, province="Toledo",
        publication_date="2026-10-20", deadline=deadline, official_url="https://example.test/"+ident,
        requirements=[], act_type="oferta", status="plazo_desconocido", content_hash="abc",
        hiring_organization=employer, eligibility=eligibility, geographic_status="dentro_80km",
        distance_km=15.5)


class BC05EvaluationTests(unittest.TestCase):
    def test_not_required_sanitary_master_does_not_exclude(self):
        result = requirement_evaluation("No se requiere Máster en Psicología General Sanitaria.",
                                        "abierta", "dentro_80km")
        self.assertNotEqual(result["eligibility"], "no_apta_por_requisito_explicito")

    def test_optional_social_work_degree_does_not_exclude(self):
        result = requirement_evaluation("Se valorará grado en Trabajo Social.",
                                        "abierta", "dentro_80km")
        self.assertNotEqual(result["eligibility"], "no_apta_por_requisito_explicito")

    def test_mandatory_social_work_degree_does_exclude(self):
        result = requirement_evaluation("Imprescindible grado en Trabajo Social.",
                                        "abierta", "dentro_80km")
        self.assertEqual(result["eligibility"], "no_apta_por_requisito_explicito")

    def test_review_does_not_merge_distinct_employers_or_unknown_employer(self):
        docs = [doc("a:1"), doc("b:2"), doc("c:3", employer="Entidad B"), doc("d:4", employer=None)]
        state = {"schema_version": 1, "documents": {d.document_id: d.as_dict() for d in docs}}
        review = build_review(state, {"new_document_ids": ["a:1", "b:2", "c:3", "d:4"], "changed_document_ids": []})
        self.assertEqual(len(review["offers"]), 3)
        merged = next(x for x in review["offers"] if len(x["source_document_ids"]) == 2)
        self.assertEqual(sorted(merged["source_document_ids"]), ["a:1", "b:2"])

    def test_expired_or_ineligible_not_top_priority(self):
        good = doc("a:1")
        wrong = doc("b:2", eligibility="no_apta_por_requisito_explicito", employer="B")
        old = doc("c:3", employer="C", deadline="2025-01-01")
        state = {"schema_version": 1, "documents": {d.document_id: d.as_dict() for d in (good, wrong, old)}}
        review = build_review(state, {"new_document_ids": [], "changed_document_ids": []}, today="2026-10-25")
        self.assertEqual(review["offers"][0]["source_document_ids"], ["a:1"])
        self.assertTrue(all(item["decision"] != "oportunidad_probable" for item in review["offers"][1:]))


if __name__ == "__main__":
    unittest.main()
