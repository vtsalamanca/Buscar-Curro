"""Buscar Curro: integración OFICIAL de InfoJobs mediante OAuth2.

Nunca solicita la contraseña personal de InfoJobs. El candidato entra en la
web oficial; la aplicación utiliza exclusivamente credenciales de desarrollador
y tokens OAuth concedidos mediante consentimiento. Nada va a GitHub.

Esta integración sólo puede entrar en servicio después de registrar la app
en InfoJobs y obtener las credenciales del desarrollador.
"""
from __future__ import annotations

import base64
import json
import os
import re
import secrets
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ORIGIN = "https://www.infojobs.net"
AUTHORIZE = ORIGIN + "/api/oauth/user-authorize/index.xhtml"
TOKEN_ENDPOINT = ORIGIN + "/oauth/authorize"
API_ENDPOINT = "https://api.infojobs.net/api/1/application"
DEVELOPER_PORTAL = "https://developer.infojobs.net/"
# URI for desktop applications as documented by InfoJobs.
DESKTOP_REDIRECT = "http://www.infojobs.net/core/oauth2vc/index.xhtml"
SCOPES = ("MY_APPLICATIONS", "APPLICATION_TIMELINE")
COLLECTION = "Credenciales del laboratorio"
SCHEMA_NAME = "org.buscarcurro.infojobs.oauth.v1"
SERVICE_ID = "buscar-curro-oauth"
PRIVATE_HOME = Path.home() / ".local" / "share" / "buscar-curro"
MAX_API_RESPONSE = 1024 * 1024


def authorisation_url(client_id: str, state: str) -> str:
    """Only public app ID and random local state appear in browser URL."""
    if not re.fullmatch(r"[a-zA-Z0-9_.:-]{4,220}", client_id):
        raise ValueError("identificador_aplicacion_invalido")
    if not re.fullmatch(r"[a-zA-Z0-9_-]{20,180}", state):
        raise ValueError("state_invalido")
    args = urllib.parse.urlencode({
        "scope": ",".join(SCOPES),
        "client_id": client_id,
        "redirect_uri": DESKTOP_REDIRECT,
        "response_type": "code",
        "state": state,
    })
    return AUTHORIZE + "?" + args


def _libsecret():
    import gi
    gi.require_version("Secret", "1")
    from gi.repository import Secret
    return Secret


def _collection(secret):
    service = secret.Service.get_sync(secret.ServiceFlags.LOAD_COLLECTIONS, None)
    matches = [c for c in service.get_collections() if c.get_label() == COLLECTION]
    if len(matches) != 1:
        raise RuntimeError("almacen_no_disponible")
    collection = matches[0]
    if collection.get_locked():
        raise RuntimeError("almacen_bloqueado")
    return collection


def _schema(secret):
    return secret.Schema.new(
        SCHEMA_NAME, secret.SchemaFlags.NONE,
        {"service": secret.SchemaAttributeType.STRING,
         "field": secret.SchemaAttributeType.STRING},
    )


FIELDS = frozenset(("client_id", "client_secret", "access_token", "refresh_token"))


def _attributes(field):
    if field not in FIELDS:
        raise ValueError("campo_no_autorizado")
    return {"service": SERVICE_ID, "field": field}


def store(field, value, *, secret=None):
    """Store in a dedicated GNOME Keyring collection, no files/logging."""
    _attributes(field)
    if not isinstance(value, str) or not value or len(value) > 8192:
        raise ValueError("valor_invalido")
    secret = secret or _libsecret()
    coll = _collection(secret)
    result = secret.password_store_sync(
        _schema(secret), _attributes(field), coll.get_object_path(),
        "Buscar Curro: OAuth " + field, value, None)
    if not result:
        raise RuntimeError("no_se_pudo_guardar")


def lookup(field, *, secret=None):
    """Return sensitive values only inside this local process."""
    _attributes(field)
    secret = secret or _libsecret()
    coll = _collection(secret)
    coll.load_items_sync(None)
    matches = [
        item for item in coll.get_items()
        if item.get_attributes().get("service") == SERVICE_ID
        and item.get_attributes().get("field") == field
    ]
    if len(matches) != 1:
        return None
    item = matches[0]
    if not item.load_secret_sync(None):
        return None
    payload = item.get_secret()
    result = payload.get_text() if payload else None
    return result if isinstance(result, str) and 0 < len(result) <= 8192 else None


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("redireccion_no_permitida")


def fetch_json(url, *, body=None, headers=None, opener=None):
    if url not in (TOKEN_ENDPOINT, API_ENDPOINT):
        raise ValueError("destino_no_autorizado")
    req = urllib.request.Request(
        url, data=body, headers=headers or {},
        method="POST" if body is not None else "GET")
    opener = opener or urllib.request.build_opener(NoRedirect())
    with opener.open(req, timeout=12) as response:
        content = response.read(MAX_API_RESPONSE + 1)
        if len(content) > MAX_API_RESPONSE:
            raise ValueError("respuesta_excesiva")
        return json.loads(content)


def _token_form(grant_type, client_id, client_secret, **params):
    if grant_type not in ("authorization_code", "refresh_token"):
        raise ValueError("grant_no_admitido")
    values = {"grant_type":grant_type, "client_id":client_id,
              "client_secret":client_secret, "redirect_uri":DESKTOP_REDIRECT}
    values.update(params)
    return urllib.parse.urlencode(values).encode("utf-8")


def redeem_code(code, *, transport=fetch_json):
    """Exchange a one-use code. No candidate account password involved."""
    if not re.fullmatch(r"[a-zA-Z0-9_.:-]{10,500}", code.strip()):
        raise ValueError("codigo_invalido")
    client_id, client_secret = lookup("client_id"), lookup("client_secret")
    if not client_id or not client_secret:
        raise RuntimeError("aplicacion_no_registrada")
    result = transport(
        TOKEN_ENDPOINT, body=_token_form(
            "authorization_code",client_id,client_secret,code=code.strip()),
        headers={"Content-Type":"application/x-www-form-urlencoded",
                 "Accept":"application/json"})
    persist_tokens(result)
    return True


def persist_tokens(result):
    if not isinstance(result, dict):
        raise RuntimeError("tokens_no_verificados")
    token = result.get("access_token")
    refresh = result.get("refresh_token")
    if not all(isinstance(t, str) and 12 <= len(t) <= 8192
               for t in (token, refresh)):
        raise RuntimeError("tokens_no_verificados")
    store("access_token", token)
    store("refresh_token", refresh)


def refresh_access_token(*, transport=fetch_json):
    credentials = [lookup(k) for k in ("client_id","client_secret","refresh_token")]
    if any(not x for x in credentials):
        raise RuntimeError("autorizacion_pendiente")
    client_id,client_secret,refresh=credentials
    response=transport(TOKEN_ENDPOINT,
        body=_token_form("refresh_token",client_id,client_secret,
                         refresh_token=refresh),
        headers={"Content-Type":"application/x-www-form-urlencoded",
                 "Accept":"application/json"})
    persist_tokens(response)


def _header(client_id, client_secret, access):
    if not all(isinstance(x,str) and x for x in (client_id,client_secret,access)):
        raise RuntimeError("token_no_disponible")
    basic=base64.b64encode((client_id+":"+client_secret).encode()).decode()
    return "Basic "+basic+",Bearer "+access


def get_applications(*, transport=fetch_json):
    """Read-only, one page, never call POST applications endpoints."""
    keys=[lookup(k) for k in ("client_id","client_secret","access_token")]
    if any(not x for x in keys):
        raise RuntimeError("autorizacion_pendiente")
    response=transport(API_ENDPOINT,headers={
        "Authorization":_header(*keys), "Accept":"application/json"})
    if not isinstance(response,dict):
        raise RuntimeError("resultado_invalido")
    return _minimal_report(response)


def _minimal_report(payload):
    """Never persist raw API responses, names, tokens or IDs."""
    if not isinstance(payload,dict):
        raise ValueError("respuesta_invalida")
    rows=payload.get("applications")
    if not isinstance(rows,list) or len(rows)>30:
        raise ValueError("listado_no_confirmado")
    safe=[]
    for item in rows:
        if not isinstance(item,dict): continue
        offer=item.get("jobOffer") or {}
        if not isinstance(offer,dict): continue
        title=str(offer.get("title") or "")[:180].strip()
        company=str(offer.get("company") or "")[:180].strip()
        if not title: continue
        safe.append({"title":title,"company":company,
                     "rejected":item.get("rejected") is True})
    return {"schema_version":1,"service":"InfoJobs API OAuth",
            "count":len(safe),"applications":safe}


def save_report(report, target=PRIVATE_HOME):
    import tempfile
    if target.is_symlink() or not target.is_dir():
        raise RuntimeError("destino_invalido")
    info=target.stat()
    if info.st_uid!=os.getuid() or info.st_mode & 0o077:
        raise RuntimeError("permisos_no_privados")
    final=target/"infojobs_oauth_privado.json"
    if final.is_symlink():
        raise RuntimeError("archivo_enlace_no_permitido")
    fd,temp=tempfile.mkstemp(prefix=".oauth-report-",dir=target)
    try:
        os.fchmod(fd,0o600)
        with os.fdopen(fd,"w",encoding="utf-8") as out:
            json.dump(report,out,ensure_ascii=False)
        os.replace(temp,final)
    finally:
        if os.path.exists(temp):os.unlink(temp)


def launch_official_page(url):
    allowed= (url==DEVELOPER_PORTAL or
              (url.startswith(AUTHORIZE+"?") and
               urllib.parse.urlsplit(url).hostname=="www.infojobs.net"))
    if not allowed:raise ValueError("destino_no_oficial")
    subprocess.Popen(["firefox",url],stdin=subprocess.DEVNULL,
                     stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                     close_fds=True,start_new_session=True)


def open_gui():
    import gi
    gi.require_version("Gtk","3.0")
    from gi.repository import Gtk,GLib
    from threading import Thread

    win=Gtk.Window(title="Buscar Curro · Conexión oficial InfoJobs")
    win.set_default_size(480,450);win.set_border_width(18)
    win.connect("destroy",Gtk.main_quit)
    layout=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=9)
    win.add(layout)
    def label(s):
        w=Gtk.Label(label=s);w.set_xalign(0);w.set_line_wrap(True)
        layout.pack_start(w,False,False,0)
        return w
    label("OAuth oficial: la aplicación nunca solicita tu contraseña de InfoJobs.")
    label("Primero registra Buscar Curro en InfoJobs Developers para obtener "
          "las claves de aplicación (Client ID y Client Secret).")
    def entry(placeholder,masked=False):
        w=Gtk.Entry();w.set_placeholder_text(placeholder)
        if masked:
            w.set_visibility(False)
            w.set_input_purpose(Gtk.InputPurpose.PASSWORD)
        layout.pack_start(w,False,False,0)
        return w
    developer=Gtk.Button(label="1. Abrir registro oficial de desarrolladores")
    layout.pack_start(developer,False,False,0)
    cid=entry("Client ID de TU aplicación (no tu email)")
    csec=entry("Client Secret de la aplicación",masked=True)
    save=Gtk.Button(label="2. Guardar credenciales de aplicación en el llavero")
    layout.pack_start(save,False,False,0)
    auth=Gtk.Button(label="3. Autorizar en InfoJobs (página oficial)")
    layout.pack_start(auth,False,False,0)
    code=entry("Código OAuth que muestra InfoJobs (no la contraseña)")
    exchange=Gtk.Button(label="4. Canjear autorización y guardar tokens")
    layout.pack_start(exchange,False,False,0)
    read=Gtk.Button(label="5. Consultar candidaturas (solo lectura)")
    layout.pack_start(read,False,False,0)
    status=label("Estado: configuración pendiente; no se ha solicitado ningún permiso.")
    buttons=(developer,save,auth,exchange,read)
    def notify(msg):
        status.set_text("Estado: "+msg)
        for b in buttons:b.set_sensitive(True)
        return False
    def run(action,success):
        for b in buttons:b.set_sensitive(False)
        status.set_text("Estado: comprobando con InfoJobs…")
        def target():
            try: action()
            except urllib.error.HTTPError as ex:
                msg="respuesta HTTP "+str(ex.code)+"; verificar registro/API"
            except Exception as ex:
                msg="no completado ("+type(ex).__name__+")"
            else:msg=success
            GLib.idle_add(notify,msg)
        Thread(target=target,daemon=True).start()
    developer.connect("clicked",lambda _:run(
        lambda:launch_official_page(DEVELOPER_PORTAL),"abre la web oficial y registra la aplicación"))
    def save_clicked(_button):
        identifier=cid.get_text().strip()
        devsecret=csec.get_text()
        csec.set_text("")
        def save_action():
            if not re.fullmatch(r"[a-zA-Z0-9_.:-]{4,220}",identifier):
                raise ValueError("id_invalido")
            if not devsecret:
                raise ValueError("secret_vacio")
            store("client_id",identifier)
            store("client_secret",devsecret)
        run(save_action,"claves de APLICACIÓN guardadas")
    save.connect("clicked",save_clicked)
    def authorize_action():
        identifier=lookup("client_id")
        if not identifier:raise ValueError("faltan_credenciales_desarrollador")
        launch_official_page(authorisation_url(identifier,secrets.token_urlsafe(24)))
    auth.connect("clicked",lambda _:run(authorize_action,
        "aprueba el consentimiento en InfoJobs y copia el código en el paso 4"))
    def exchange_clicked(_button):
        once=code.get_text().strip()
        code.set_text("")
        run(lambda:redeem_code(once),
            "autorización OAuth guardada en el llavero")
    exchange.connect("clicked",exchange_clicked)
    def read_action():
        try:report=get_applications()
        except urllib.error.HTTPError as ex:
            if ex.code!=401:raise
            refresh_access_token()
            report=get_applications()
        save_report(report)
    read.connect("clicked",lambda _:run(read_action,
        "candidaturas consultadas; informe privado actualizado"))
    win.show_all();Gtk.main()


def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ("--abrir","--comprobar"):
        print("Uso: infojobs_oauth_oficial.py --abrir|--comprobar")
        return 2
    if sys.argv[1]=="--comprobar":
        print(json.dumps({"official_oauth_client":"available",
          "provider_app_registration":"required",
          "personal_password_requested":False}))
        return 0
    open_gui();return 0


if __name__=="__main__":
    raise SystemExit(main())
