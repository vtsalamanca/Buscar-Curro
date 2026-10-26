from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

from infojobs_acceso_local import (
    INFOJOBS_URL, check_environment, launch, launcher_text, install_launcher, ensure_profile
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
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "firefox-infojobs"
            result = launch(env=self.env, which=self.which, popen=mock,
                            euid=1001, profile=path)
            self.assertEqual(result, "launched")
            self.assertEqual(mock.call_args.args[0],
                             ["/usr/bin/firefox", "--no-remote", "--profile",
                              str(path), INFOJOBS_URL])
            self.assertTrue(path.is_dir())
            self.assertEqual(path.stat().st_mode & 0o777, 0o700)
        self.assertEqual(mock.call_args.kwargs["close_fds"], True)
        self.assertNotIn("password", str(mock.call_args).lower())

    def test_private_profile_reused_without_erasing_session(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "firefox-infojobs"
            ensure_profile(path)
            marker = path / "firefox-session-sentinel"
            marker.write_text("retained")
            ensure_profile(path)
            self.assertEqual(marker.read_text(), "retained")

    def test_profile_symlink_and_permissions_are_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            private = root / "profile"
            private.mkdir()
            alias = root / "alias"
            alias.symlink_to(private, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "invalid_firefox_profile"):
                ensure_profile(alias)
            private.chmod(0o755)
            with self.assertRaisesRegex(ValueError, "unprotected_firefox_profile"):
                ensure_profile(private)

    def test_profile_parent_with_loose_permissions_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "parent"
            p.mkdir(mode=0o755)
            p.chmod(0o755)
            with self.assertRaisesRegex(ValueError, "unprotected_private_parent"):
                ensure_profile(p / "firefox-infojobs")

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
