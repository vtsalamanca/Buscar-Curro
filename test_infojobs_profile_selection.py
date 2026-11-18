"""Selección del Firefox privado sin tocar cuentas ni perfiles reales."""
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import infojobs_lector_accesible as reader


class Node:
    def __init__(self, role, name="", pid=0, url="", children=()):
        self.role, self.name, self.pid, self.url = role, name, pid, url
        self.children = list(children)
    def get_role_name(self): return self.role
    def get_name(self): return self.name
    def get_process_id(self): return self.pid
    def get_child_count(self): return len(self.children)
    def get_child_at_index(self, i): return self.children[i]
    def get_document_iface(self): return self
    def get_document_attribute_value(self, name): return self.url


class FakeProcess:
    name = "4321"
    def __init__(self, profile): self.profile = profile
    def stat(self): return SimpleNamespace(st_uid=os.getuid())
    def __truediv__(self, name):
        self_cmd = b"/usr/bin/firefox-esr\0--no-remote\0--profile\0"
        return SimpleNamespace(read_bytes=lambda: self_cmd + str(self.profile).encode() + b"\0")


class BrowserSelectionTests(unittest.TestCase):
    def test_dedicated_profile_is_used_without_legacy_browser(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            profile = home / ".local/share/lab-auth-infojobs/profile"
            profile.mkdir(parents=True)
            doc = Node("document web", url="https://www.infojobs.net/candidate/applications/list.xhtml")
            window = Node("frame", children=[doc])
            app = Node("application", name="Firefox", pid=4321, children=[window])
            desktop = Node("desktop", children=[app])
            atspi = SimpleNamespace(get_desktop=lambda _: desktop, Document=SimpleNamespace(get_document_attribute_value=lambda d, n: d.get_document_attribute_value(n)))
            with patch.object(Path, "home", return_value=home), patch.object(Path, "iterdir", return_value=[FakeProcess(profile)]), patch.object(reader, "get_legacy_accessible_browser", side_effect=AssertionError("legacy")):
                self.assertIs(reader.get_accessible_browser(atspi), window)
                app.children.append(Node("frame", children=[doc]))
                with self.assertRaisesRegex(ValueError, "ambiguous"):
                    reader.get_accessible_browser(atspi)


if __name__ == "__main__":
    unittest.main()
