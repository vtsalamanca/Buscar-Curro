"""Abre InfoJobs en Firefox con un perfil local y persistente en Debian.

El script no recibe ni guarda credenciales o códigos: Firefox puede conservar
el inicio de sesión y, si el usuario lo elige, autocompletar contraseñas.
No se conecta a APIs privadas ni elude CAPTCHA/MFA.
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
PROFILE_PATH = Path.home() / ".local" / "share" / "buscar-curro" / "firefox-infojobs"


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


def ensure_profile(profile: Path) -> Path:
    """Limit private browser storage to the Debian user's home."""
    if not profile.is_absolute() or profile.is_symlink():
        raise ValueError("invalid_firefox_profile")
    parent = profile.parent
    if parent.is_symlink() or (parent.exists() and parent.stat().st_mode & 0o077):
        raise ValueError("unprotected_private_parent")
    parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if parent.stat().st_mode & 0o077:
        raise ValueError("unprotected_private_parent")
    profile.mkdir(mode=0o700, exist_ok=True)
    if profile.is_symlink() or profile.stat().st_mode & 0o077:
        raise ValueError("unprotected_firefox_profile")
    return profile


def launch(env=None, which=None, popen=None, euid=None, profile=None):
    env = os.environ if env is None else env
    which = shutil.which if which is None else which
    popen = subprocess.Popen if popen is None else popen
    status = check_environment(env=env, which=which, euid=euid)
    if status != "ready":
        return status
    browser = which("firefox")
    path = ensure_profile(PROFILE_PATH if profile is None else profile)
    # Cookies and logins are saved only in Firefox's dedicated private
    # filesystem profile, never in our code, Git, stdout or process arguments.
    # A 2FA challenge may still require the account owner's intervention.
    popen(
        [browser, "--no-remote", "--profile", str(path), INFOJOBS_URL],
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
        print("Si la sesión sigue abierta, Firefox la reutilizará. Si es la primera vez, "
              "Firefox podrá guardar y autocompletar los datos que introduzcas allí. "
              "Los códigos de seguridad de InfoJobs pueden seguir requiriendo aprobación.")
    return 0 if status == "launched" else 2


if __name__ == "__main__":
    sys.exit(main())
