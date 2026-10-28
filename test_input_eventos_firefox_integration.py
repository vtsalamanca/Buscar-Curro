"""Opt-in Firefox/X11 integration regression: local HTML and synthetic values only.

Usage: BC_FIREFOX_X11_SMOKE=1 python3 -m unittest test_input_eventos_firefox_integration -q
"""
from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import unittest

from input_eventos_firefox import X11Keyboard, focus_and_fill


@unittest.skipUnless(os.environ.get("BC_FIREFOX_X11_SMOKE") == "1",
                     "only run this graphical test explicitly in a local desktop")
class NativeFirefoxSyntheticSmokeTest(unittest.TestCase):
    def test_real_browser_dispatches_input_events_and_preserves_value(self):
        import gi
        gi.require_version("Atspi", "2.0")
        from gi.repository import Atspi

        title = "BC-SYNTHETIC-EVENT-REGRESSION"
        value = "SYNTHETIC-Abc123!"
        page = """<!DOCTYPE html><html lang="es"><head><title>BC-SYNTHETIC-EVENT-REGRESSION</title></head>
        <body><input type=text aria-label="Campo de prueba sintético"
        style="position:absolute;left:150px;top:240px;width:380px;height:42px;font-size:24px"/>
        <div role=status id=status aria-label="EVENT_COUNT_0">EVENT_COUNT_0</div>
        <script>let count=0;const input=document.querySelector('input'),status=document.querySelector('#status');
        input.addEventListener('input',()=>{count++;
        const state='EVENT_COUNT_'+count+';VALUE_MATCH_'+(input.value==='SYNTHETIC-Abc123!');
        status.setAttribute('aria-label',state);status.textContent=state;});</script></body></html>"""
        with tempfile.TemporaryDirectory(prefix="bc-firefox-native-regression-") as tmp:
            folder = Path(tmp)
            profile = folder / "profile"
            profile.mkdir(mode=0o700)
            html = folder / "fixture.html"
            html.write_text(page, encoding="utf8")
            env = os.environ | {
                "DISPLAY": ":0",
                "XAUTHORITY": str(Path.home() / ".Xauthority"),
                "DBUS_SESSION_BUS_ADDRESS": f"unix:path=/run/user/{os.getuid()}/bus",
                "MOZ_ACCESSIBILITY_ATK2": "1",
                "GNOME_ACCESSIBILITY": "1",
                "GTK_MODULES": "gail:atk-bridge",
            }
            browser = subprocess.Popen(
                ["firefox", "--no-remote", "--profile", str(profile), html.as_uri()],
                env=env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, start_new_session=True, close_fds=True,
            )
            try:
                window = None
                for _ in range(45):
                    desktop = Atspi.get_desktop(0)
                    for i in range(desktop.get_child_count()):
                        app = desktop.get_child_at_index(i)
                        if app.get_name() != "Firefox":
                            continue
                        for j in range(app.get_child_count()):
                            win = app.get_child_at_index(j)
                            if title in win.get_name():
                                window = win
                                break
                    if window:
                        break
                    if browser.poll() is not None:
                        break
                    time.sleep(.25)
                self.assertIsNotNone(window, "local synthetic Firefox window unavailable")
                def walk(root, limit=1000):
                    queue = [root]
                    for _ in range(limit):
                        if not queue:
                            break
                        e = queue.pop(0)
                        try:
                            yield e
                            n = e.get_child_count()
                            if n < 130:
                                queue.extend(e.get_child_at_index(i) for i in range(n))
                        except Exception:
                            pass
                inputs = [e for e in walk(window) if
                          e.get_role_name() == "entry"
                          and e.get_name() == "Campo de prueba sintético"]
                self.assertEqual(len(inputs), 1)
                tree = subprocess.check_output(["xwininfo", "-root", "-tree"],
                                               env=env, text=True)
                matches = [int(row.strip().split()[0], 16)
                           for row in tree.splitlines() if title in row and "Navigator" in row]
                self.assertEqual(len(matches), 1)
                info = subprocess.check_output(
                    ["xwininfo", "-id", hex(matches[0])], env=env, text=True)
                def origin(name):
                    m = re.search(r"^\s*" + re.escape(name) + r":\s*(-?\d+)", info, re.M)
                    self.assertIsNotNone(m)
                    return int(m.group(1))
                x = origin("Absolute upper-left X") + 170
                y = origin("Absolute upper-left Y") + 87 + 260
                driver = X11Keyboard()
                try:
                    focus_and_fill(inputs[0], value, driver, matches[0], x, y)
                finally:
                    driver.close()
                time.sleep(.6)
                self.assertEqual(inputs[0].get_text_iface().get_character_count(), len(value))
                indicators = [e.get_name() for e in walk(window)
                              if e.get_name().startswith("EVENT_COUNT_")]
                self.assertIn(f"EVENT_COUNT_{len(value)+2};VALUE_MATCH_true", indicators)
            finally:
                browser.terminate()
                try:
                    browser.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    browser.kill()
                    browser.wait(timeout=5)
