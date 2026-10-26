"""Abrir el acceso oficial a InfoJobs en Firefox, exclusivamente en Debian.

No recibe ni guarda credenciales, MFA, cookies ni contenido de candidaturas.
No accede a interfaces privadas mediante HTTP y no elude CAPTCHA/2FA.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

INFOJOBS_URL = "https://www.infojobs.net/"
APP_NAME = "Buscar Curro - acceso InfoJobs"
DESKTOP_FILENAME = "buscar-curro-infojobs.desktop"


def check_environment(env=None, which=None, euid=None):
    env = os.environ if env is None else env
    which = shutil.which if which is None else which
    euid = os.geteuid() if euid is None else euid
    if euid == 0:
        return "user_session_required"
    if not (env.get("DISPLAY") or env.get("WAYLAND_DISPLAY")):
        return "graphical_session_unavailable"
    if which("firefox") is None:
        return "firefox_not_installed"
    return "ready"


def launch(env=None, which=None, popen=None, euid=None):
    env = os.environ if env is None else env
    which = shutil.which if which is None else which
    popen = subprocess.Popen if popen is None else popen
    status = check_environment(env=env, which=which, euid=euid)
    if status != "ready":
        return status
    browser = which("firefox")
    # Private browsing keeps authentication within Firefox, not our program.
    # Closing the private windows discards their session cookies.
    popen(
        [browser, "--private-window", INFOJOBS_URL],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, close_fds=True, start_new_session=True,
    )
    return "launched"


def launcher_text(script: Path, interpreter: Path):
    if not script.is_absolute() or not interpreter.is_absolute():
        raise ValueError("absolute_executable_paths_required")
    if any(c in str(script) + str(interpreter) for c in "\n\r%"):
        raise ValueError("invalid_launcher_path")
    return (
        "[Desktop Entry]\n"
        "Type=Application\n"
        f"Name={APP_NAME}\n"
        "Comment=Abre la web oficial en Firefox sin recoger credenciales\n"
        f"Exec={interpreter} {script} --abrir\n"
        "Icon=firefox\n"
        "Terminal=false\n"
        "Categories=Network;WebBrowser;\n"
        "StartupNotify=true\n"
    )


def install_launcher(home: Path, script: Path, interpreter: Path):
    if not home.is_absolute() or home.is_symlink():
        raise ValueError("invalid_home")
    folder = home / ".local" / "share" / "applications"
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    target = folder / DESKTOP_FILENAME
    if target.is_symlink():
        raise ValueError("launcher_symlink_not_allowed")
    text = launcher_text(script, interpreter)
    target.write_text(text, encoding="utf-8")
    target.chmod(0o600)
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--comprobar", action="store_true")
    group.add_argument("--abrir", action="store_true")
    group.add_argument("--instalar-lanzador", action="store_true")
    args = parser.parse_args(argv)
    if args.instalar_lanzador:
        result = install_launcher(Path.home(), Path(__file__).resolve(),
                                  Path(sys.executable).resolve())
        print("Lanzador creado en:", result)
        return 0
    if args.comprobar:
        status = check_environment()
        print("InfoJobs Debian: " + status)
        return 0 if status == "ready" else 2
    status = launch()
    print("InfoJobs Debian: " + status)
    if status == "launched":
        print("En Firefox, selecciona Acceso candidatos e identifícate tú mismo; "
              "completa el código 2FA allí, nunca en este programa.")
    return 0 if status == "launched" else 2


if __name__ == "__main__":
    sys.exit(main())
