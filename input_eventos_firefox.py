"""X11 Firefox field-event repair for locally authorized form interactions.

No credentials are sourced here. A caller supplies its already-authorized
accessible field and value. Only an explicit focused field may receive data.
No HTTP, WebDriver, Clipboard, cookies, hidden browser or credential logging.
"""
from __future__ import annotations

import ctypes
import ctypes.util
import os
import re
import subprocess
import time

class UnsafeTarget(RuntimeError):
    """The expected, visible control is not demonstrably focused."""


class X11Keyboard:
    def __init__(self, display: bytes = b":0"):
        xlib_path = ctypes.util.find_library("X11")
        xtest_path = ctypes.util.find_library("Xtst")
        if not xlib_path or not xtest_path:
            raise UnsafeTarget("x11_input_unavailable")
        self.x = ctypes.CDLL(xlib_path)
        self.t = ctypes.CDLL(xtest_path)
        P = ctypes.c_void_p
        U = ctypes.c_ulong
        I = ctypes.c_int
        self.x.XOpenDisplay.argtypes = [ctypes.c_char_p]
        self.x.XOpenDisplay.restype = P
        self.x.XCloseDisplay.argtypes = [P]
        self.x.XCloseDisplay.restype = I
        self.x.XDefaultRootWindow.argtypes = [P]
        self.x.XDefaultRootWindow.restype = U
        self.x.XRaiseWindow.argtypes = [P, U]
        self.x.XSetInputFocus.argtypes = [P, U, I, U]
        self.x.XWarpPointer.argtypes = [P, U, U, I, I, ctypes.c_uint, ctypes.c_uint, I, I]
        self.x.XFlush.argtypes = [P]
        self.x.XStringToKeysym.argtypes = [ctypes.c_char_p]
        self.x.XStringToKeysym.restype = U
        self.x.XKeysymToKeycode.argtypes = [P, U]
        self.x.XKeysymToKeycode.restype = ctypes.c_uint
        self.t.XTestFakeButtonEvent.argtypes = [P, ctypes.c_uint, I, U]
        self.t.XTestFakeButtonEvent.restype = I
        self.t.XTestFakeKeyEvent.argtypes = [P, ctypes.c_uint, I, U]
        self.t.XTestFakeKeyEvent.restype = I
        self.d = self.x.XOpenDisplay(display)
        if not self.d:
            raise UnsafeTarget("x11_display_unavailable")

    def close(self):
        if self.d:
            self.x.XCloseDisplay(self.d)
            self.d = None

    def click(self, window_id: int, x: int, y: int) -> None:
        if not all((isinstance(window_id, int), window_id > 0,
                    isinstance(x, int), isinstance(y, int),
                    0 <= x < 6000, 0 <= y < 4000)):
            raise UnsafeTarget("coordinates_invalid")
        root = self.x.XDefaultRootWindow(self.d)
        self.x.XRaiseWindow(self.d, window_id)
        self.x.XSetInputFocus(self.d, window_id, 1, 0)
        self.x.XFlush(self.d)
        time.sleep(.35)
        self.x.XWarpPointer(self.d, 0, root, 0, 0, 0, 0, x, y)
        self.x.XFlush(self.d)
        time.sleep(.15)
        if not self.t.XTestFakeButtonEvent(self.d, 1, 1, 0):
            raise UnsafeTarget("mouse_down_failed")
        if not self.t.XTestFakeButtonEvent(self.d, 1, 0, 0):
            raise UnsafeTarget("mouse_up_failed")
        self.x.XFlush(self.d)
        time.sleep(.3)

    def _keycode_map(self):
        env = dict(os.environ, DISPLAY=":0")
        mapping = {}
        raw = subprocess.check_output(
            ["xmodmap", "-pke"], env=env, text=True, timeout=4)
        for line in raw.splitlines():
            match = re.match(r"keycode\s+(\d+)\s+=\s+(.+)", line)
            if not match:
                continue
            code = int(match.group(1))
            levels = match.group(2).split()[:2]
            for shift, keysym_name in enumerate(levels):
                if keysym_name == "NoSymbol":
                    continue
                keysym = self.x.XStringToKeysym(keysym_name.encode("ascii"))
                if keysym and keysym not in mapping:
                    mapping[keysym] = (code, bool(shift))
        return mapping

    def prepare(self, value: str) -> None:
        if not isinstance(value, str) or not value:
            raise UnsafeTarget("empty_keyboard_input")
        mapping = self._keycode_map()
        strokes = []
        for char in value:
            if not (32 <= ord(char) <= 126):
                raise UnsafeTarget("unsupported_character")
            # ASCII Latin-1 keysyms are Unicode codepoints. XStringToKeysym
            # expects symbolic names (minus/exclam), not punctuation.
            sym = ord(char)
            if sym not in mapping:
                raise UnsafeTarget("unsupported_keymap_character")
            strokes.append(mapping[sym])
        shift_code = self.x.XKeysymToKeycode(self.d,
                        self.x.XStringToKeysym(b"Shift_L"))
        if not shift_code:
            raise UnsafeTarget("shift_unavailable")
        self._prepared = (value, strokes, shift_code)

    def type_ascii(self, value: str) -> None:
        if not hasattr(self,"_prepared") or self._prepared[0] != value:
            self.prepare(value)
        _, strokes, shift_code = self._prepared
        for code, shifted in strokes:
            if shifted:
                self.t.XTestFakeKeyEvent(self.d, shift_code, 1, 0)
            self.t.XTestFakeKeyEvent(self.d, code, 1, 0)
            self.t.XTestFakeKeyEvent(self.d, code, 0, 0)
            if shifted:
                self.t.XTestFakeKeyEvent(self.d, shift_code, 0, 0)
            self.x.XFlush(self.d)
            time.sleep(.025)

    def clear_with_control_a(self) -> None:
        control = self.x.XKeysymToKeycode(self.d,
                     self.x.XStringToKeysym(b"Control_L"))
        letter = self.x.XKeysymToKeycode(self.d,
                    self.x.XStringToKeysym(b"a"))
        if not control or not letter:
            raise UnsafeTarget("ctrl_a_unavailable")
        self.t.XTestFakeKeyEvent(self.d, control, 1, 0)
        self.t.XTestFakeKeyEvent(self.d, letter, 1, 0)
        self.t.XTestFakeKeyEvent(self.d, letter, 0, 0)
        self.t.XTestFakeKeyEvent(self.d, control, 0, 0)
        self.x.XFlush(self.d)
        time.sleep(.1)
        self.key(b"BackSpace")

    def key(self, name: bytes) -> None:
        sym = self.x.XStringToKeysym(name)
        if not sym:
            raise UnsafeTarget("unsupported_key")
        code = self.x.XKeysymToKeycode(self.d, sym)
        if not code:
            raise UnsafeTarget("unsupported_key")
        if not self.t.XTestFakeKeyEvent(self.d, code, 1, 0):
            raise UnsafeTarget("key_down_failed")
        if not self.t.XTestFakeKeyEvent(self.d, code, 0, 0):
            raise UnsafeTarget("key_up_failed")
        self.x.XFlush(self.d)
        time.sleep(.05)


def focus_and_fill(field, value: str, keyboard: X11Keyboard,
                   window_id: int, x: int, y: int) -> None:
    """Type real X11 key events, which generate browser input/change events.

    Reject secrets with unsupported keyboard characters BEFORE typing; the
    first key is a harmless sentinel, whose appearance in this precise
    accessible field proves the target before the real value is entered.
    """
    if type(value) is not str or not value or len(value) > 8192:
        raise UnsafeTarget("value_invalid")
    if field.get_role_name() not in ("entry", "password text"):
        raise UnsafeTarget("field_role_invalid")
    reader = field.get_text_iface()
    if not reader:
        raise UnsafeTarget("field_not_readable")
    # Validate the entire keyboard mapping before any secret is entered.
    keyboard.prepare(value)
    keyboard.click(window_id, x, y)

    def count_is(expected: int) -> bool:
        # Firefox accessibility notifications arrive after the XTest event.
        for _ in range(20):
            if reader.get_character_count() == expected:
                return True
            time.sleep(.08)
        return False

    initial = reader.get_character_count()
    keyboard.type_ascii("z")
    if not count_is(initial + 1):
        raise UnsafeTarget("native_focus_not_proven")
    keyboard.clear_with_control_a()
    if not count_is(0):
        raise UnsafeTarget("field_not_cleared")
    keyboard.type_ascii(value)
    if not count_is(len(value)):
        raise UnsafeTarget("native_entry_not_verified")


def valid_screen_point(x: int, y: int, width: int, height: int) -> bool:
    return (all(type(v) is int for v in (x, y, width, height))
            and x >= 0 and y >= 0 and 1 <= width <= 3000 and 1 <= height <= 1500
            and x + width <= 6000 and y + height <= 4000)
