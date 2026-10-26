from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

from infojobs_acceso_local import (
    INFOJOBS_URL, check_environment, launch, launcher_text, install_launcher
)


class InfoJobsLocalLoginTest(unittest.TestCase):
    def setUp(self):
        self.env = {"DISPLAY": ":0"}
        self.which = lambda name: "/usr/bin/firefox" if name == "firefox" else None

    def test_graphical_session_and_browser_required(self):
        self.assertEqual(check_environment(env={}, which=self.which, euid=1001),
                         "graphical_session_unavailable")
        self.assertEqual(check_environment(env=self.env, which=lambda _: None, euid=1001),
                         "firefox_not_installed")
        self.assertEqual(check_environment(env=self.env, which=self.which, euid=0),
                         "user_session_required")
        self.assertEqual(check_environment(env=self.env, which=self.which, euid=1001),
                         "ready")

    def test_fixed_official_url_without_credentials(self):
        mock = Mock()
        result = launch(env=self.env, which=self.which, popen=mock, euid=1001)
        self.assertEqual(result, "launched")
        self.assertEqual(mock.call_args.args[0],
                         ["/usr/bin/firefox", "--private-window", INFOJOBS_URL])
        self.assertEqual(mock.call_args.kwargs["close_fds"], True)
        self.assertNotIn("password", str(mock.call_args).lower())

    def test_failed_precheck_never_launches(self):
        mock = Mock()
        status = launch(env={}, which=self.which, popen=mock, euid=1001)
        self.assertEqual(status, "graphical_session_unavailable")
        mock.assert_not_called()

    def test_desktop_launcher_is_local_and_not_autostart(self):
        with tempfile.TemporaryDirectory() as td:
            dest = install_launcher(Path(td), Path("/opt/project/infojobs_acceso_local.py"),
                                    Path("/usr/bin/python3"))
            text = dest.read_text()
            self.assertEqual(INFOJOBS_URL, "https://www.infojobs.net/")
            self.assertIn("Exec=/usr/bin/python3 /opt/project/infojobs_acceso_local.py --abrir", text)
            self.assertIn("--abrir", text)
            self.assertNotIn("X-GNOME-Autostart-enabled", text)
            self.assertNotIn("contraseña", text.lower())
            self.assertEqual(dest.stat().st_mode & 0o777, 0o600)

    def test_symlink_launcher_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td) / ".local" / "share" / "applications"
            folder.mkdir(parents=True)
            target = folder / "buscar-curro-infojobs.desktop"
            target.symlink_to("/tmp/nonexistent-target")
            with self.assertRaises(ValueError):
                install_launcher(Path(td), Path("/opt/project/infojobs_acceso_local.py"),
                                 Path("/usr/bin/python3"))

    def test_paths_must_be_absolute(self):
        with self.assertRaises(ValueError):
            launcher_text(Path("relative.py"), Path("/usr/bin/python3"))


if __name__ == "__main__":
    unittest.main()
