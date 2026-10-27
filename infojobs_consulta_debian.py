"""Revisión autorizada de InfoJobs desde Debian con Firefox y GNOME Keyring.

Usa WebDriver BiDi ligado a localhost y un perfil Firefox autorizado.
Sólo lee candidaturas. Si caduca la sesión, indica que debe utilizarse
el flujo OAuth oficial; no accede a contraseñas de candidato.
Cierra el agente de depuración y recupera el Firefox ordinario al terminar.
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import socket
import stat
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROFILE = Path.home() / ".local/share/buscar-curro/firefox-infojobs"
BIDI_SCRIPT = ROOT / "infojobs_browser_bidi.mjs"
BROWSER_URL = "https://www.infojobs.net/candidate/applications/list.xhtml"
AGENT_PORT = 9222


def find_browser_processes():
    """Only the main Firefox process with this exact dedicated profile."""
    matches=[]
    proc=Path("/proc")
    if not proc.is_dir():
        return matches
    for p in proc.iterdir():
        if not p.name.isdigit():
            continue
        try:
            argv=(p/"cmdline").read_bytes().decode("utf-8","replace").split("\x00")
        except (OSError,PermissionError):
            continue
        if not argv or Path(argv[0]).name not in {"firefox-esr","firefox"}:
            continue
        if "--profile" not in argv:
            continue
        i=argv.index("--profile")
        if i+1>=len(argv) or argv[i+1]!=str(PROFILE):
            continue
        matches.append((int(p.name), "--remote-debugging-port" in argv))
    return matches


def agent_reachable():
    try:
        with socket.create_connection(("127.0.0.1",AGENT_PORT),timeout=.5):
            return True
    except OSError:
        return False


def check_environment():
    if os.geteuid()==0 or not PROFILE.is_dir() or PROFILE.is_symlink():
        return "profile_not_ready"
    info=PROFILE.stat()
    if info.st_uid!=os.getuid() or info.st_mode & 0o077:
        return "profile_not_private"
    if not (Path("/tmp/.X11-unix/X0").exists()
            and (Path.home()/".Xauthority").is_file()):
        return "desktop_not_ready"
    if not (ROOT / "infojobs_browser_bidi.mjs").is_file():
        return "reviewer_missing"
    return "ready"


def desktop_env():
    env=dict(os.environ)
    env["DISPLAY"]=":0"
    env["XAUTHORITY"]=str(Path.home()/".Xauthority")
    env["DBUS_SESSION_BUS_ADDRESS"]=f"unix:path=/run/user/{os.getuid()}/bus"
    return env


def terminate_browser(pid:int,seconds:float=11):
    if pid==os.getpid():
        raise RuntimeError("unsafe_process")
    os.kill(pid,signal.SIGTERM)
    deadline=time.monotonic()+seconds
    while time.monotonic()<deadline:
        try: os.kill(pid,0)
        except ProcessLookupError:return
        time.sleep(.25)
    raise RuntimeError("browser_did_not_exit")


def start_browser(debugging:bool):
    args=["firefox","--no-remote"]
    if debugging: args.extend(["--remote-debugging-port",str(AGENT_PORT)])
    args.extend(["--profile",str(PROFILE),BROWSER_URL])
    return subprocess.Popen(args,env=desktop_env(),stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                            close_fds=True,start_new_session=True)


def run_node(mode:str, credentials:tuple[str,str]|None=None)->dict:
    if mode != "--revisar" or credentials is not None:
        raise ValueError("unsupported_command")
    args=["node",str(BIDI_SCRIPT),mode]
    payload=None
    try:
        p=subprocess.run(args,input=payload,capture_output=True,text=True,
                         timeout=40,env=desktop_env(),check=False)
        if len(p.stdout)>4000:return {"status":"unexpected_output"}
        result=json.loads(p.stdout)
        if not isinstance(result,dict):return {"status":"unexpected_output"}
        safe_status=result.get("status")
        if safe_status not in (
            "private_read_verified","authentication_required",
            "private_read_unverified","login_submitted_check_session",
            "interaction_or_login_required",
            "login_form_unrecognized","browser_unavailable_or_unverified",
        ):return {"status":"unexpected_output"}
        response={"status":safe_status}
        if isinstance(result.get("applications"),int) and 0<=result["applications"]<=100:
            response["applications"]=result["applications"]
        if result.get("reason") in ("bidi_session_not_created","script_evaluation_failed",
                                    "bidi_timeout","no_infojobs_browser_tab"):
            response["reason"]=result["reason"]
        return response
    except (OSError,subprocess.TimeoutExpired,ValueError,TypeError):
        return {"status":"local_browser_error"}


def review(run=run_node)->dict:
    """Read existing authorized Firefox session; do not request account password.

    For new authentication, register the application and grant OAuth consent
    using infojobs_oauth_oficial.py, as required by the provider's developer terms.
    """
    first=run("--revisar")
    if first["status"]=="authentication_required":
        return {"status":"official_oauth_authorization_required"}
    return first


def run_managed()->dict:
    problem=check_environment()
    if problem!="ready":return {"status":problem}
    old=find_browser_processes()
    if len(old)>1:return {"status":"multiple_browser_processes"}
    was_open=bool(old)
    debug_started=False
    try:
        if old:
            terminate_browser(old[0][0])
        for _ in range(40):
            if not agent_reachable():break
            time.sleep(.25)
        if agent_reachable():return {"status":"port_unavailable"}
        proc=start_browser(True)
        debug_started=True
        for _ in range(60):
            if agent_reachable():break
            if proc.poll() is not None:return {"status":"browser_start_failed"}
            time.sleep(.25)
        else:return {"status":"browser_start_timeout"}
        time.sleep(1.5)
        return review()
    finally:
        if debug_started:
            current=find_browser_processes()
            for pid,_ in current:
                try:terminate_browser(pid)
                except (ProcessLookupError,RuntimeError):pass
            if was_open and not find_browser_processes():
                start_browser(False)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--revisar",action="store_true")
    group.add_argument("--comprobar",action="store_true")
    args=p.parse_args()
    if args.comprobar:
        response={"status":check_environment(),"browser_open":bool(find_browser_processes())}
    else:
        try:response=run_managed()
        except Exception:response={"status":"execution_error"}
    print(json.dumps(response,sort_keys=True))
    return 0 if response["status"] in ("ready","private_read_verified") else 2


if __name__=="__main__":
    raise SystemExit(main())
