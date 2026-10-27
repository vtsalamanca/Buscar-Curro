import os
from pathlib import Path
import tempfile
import unittest
from infojobs_lector_accesible import Tree, clean, candidate_card, candidates_from_tree, save_private


def fixture_card(position="Psicólogo", company="ILUNION", status="Inscrito"):
    return Tree("list item", "summary of vacancy", (
        Tree("heading", position),
        Tree("heading", company),
        Tree("list", "", (
            Tree("list item", "\ue609Hace 16h"),
            Tree("list item", "\ue608" + status),
        )),
        Tree("list", "", (
            Tree("list item", "Recommended position", (Tree("heading", "Something else"),)),
        )),
    ))


class AtspiReaderTest(unittest.TestCase):
    def test_real_card_excludes_nested_recommended_jobs(self):
        result = candidates_from_tree(Tree("document web", "Mis candidaturas", (
            Tree("list", "", (fixture_card(),)),
        )))
        self.assertEqual(result, [{"title": "Psicólogo", "company": "ILUNION",
                                   "status": "Inscrito",
                                   "last_company_activity_label": "Hace 16h"}])

    def test_two_candidates(self):
        root = Tree("document web", "Mis candidaturas", (
            fixture_card(), fixture_card("Auxiliar", "Intress", "Preseleccionado")
        ))
        self.assertEqual(len(candidates_from_tree(root)), 2)

    def test_no_bad_status_is_not_interpreted_as_candidate(self):
        self.assertIsNone(candidate_card(fixture_card(status="apuntarme")))
        self.assertEqual(candidates_from_tree(Tree("document web", "not logged in")), [])

    def test_clean_private_use_unicode(self):
        self.assertEqual(clean(" \ue608Inscrito\n  "), "Inscrito")

    def test_persist_has_protected_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/"private"
            folder.mkdir(mode=0o700)
            path=folder/"infojobs_privado.json"
            save_private({"status": "private_read_verified", "applications_count": 1}, path)
            self.assertEqual(path.stat().st_mode&0o777, 0o600)

    def test_reject_unsafe_output_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/"target"
            target.mkdir(mode=0o700)
            alias=Path(tmp)/"alias"
            alias.symlink_to(target, target_is_directory=True)
            with self.assertRaises(ValueError):
                save_private({"status":"private_read_verified"},alias/"report.json")


if __name__ == "__main__":
    unittest.main()
