"""Cliente autorizado de una sola ejecución para InfoJobs y el llavero de Debian.

No acepta credenciales por CLI, ficheros ni entorno. No imprime secretos ni
detalles de cuenta. No copia cookies de Firefox ni publica datos en GitHub.
El inicio de sesión desde navegador se realiza en infojobs_consulta_debian.py:
este módulo NO realiza peticiones HTTP ni imprime secretos.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass


VAULT_TITLE = "Credenciales del laboratorio"
SCHEMA_NAME = "org.buscarcurro.laboratorio.credenciales.v1"
SERVICE = "infojobs"
ALLOWED_FIELDS = ("usuario", "clave")


def secret_module():
    import gi
    gi.require_version("Secret", "1")
    from gi.repository import Secret
    return Secret


@dataclass(frozen=True)
class KeyringState:
    available: bool
    locked: bool | None
    username_present: bool
    password_present: bool


def _collection(secret):
    service = secret.Service.get_sync(secret.ServiceFlags.LOAD_COLLECTIONS, None)
    collections = [c for c in service.get_collections()
                   if c.get_label() == VAULT_TITLE]
    if len(collections) != 1:
        return None
    return collections[0]


def _schema(secret):
    return secret.Schema.new(
        SCHEMA_NAME, secret.SchemaFlags.NONE,
        {"service": secret.SchemaAttributeType.STRING,
         "field": secret.SchemaAttributeType.STRING},
    )


def _entries(collection):
    collection.load_items_sync(None)
    items = collection.get_items()
    return {
        field: [item for item in items
                if item.get_attributes().get("service") == SERVICE
                and item.get_attributes().get("field") == field]
        for field in ALLOWED_FIELDS
    }


def check_keyring(secret=None) -> KeyringState:
    secret = secret_module() if secret is None else secret
    coll = _collection(secret)
    if coll is None:
        return KeyringState(False, None, False, False)
    items = _entries(coll)
    return KeyringState(
        True, bool(coll.get_locked()),
        len(items["usuario"]) == 1, len(items["clave"]) == 1,
    )


def load_credentials(secret=None) -> tuple[str, str] | None:
    """Plaintext remains only in this Linux process memory; never output it."""
    secret = secret_module() if secret is None else secret
    coll = _collection(secret)
    if coll is None or coll.get_locked():
        return None
    items = _entries(coll)
    if any(len(items[field]) != 1 for field in ALLOWED_FIELDS):
        return None
    values = []
    for field in ALLOWED_FIELDS:
        item = items[field][0]
        if not item.load_secret_sync(None):
            return None
        value = item.get_secret()
        text = value.get_text() if value is not None else None
        if not text or len(text) > 8192:
            return None
        values.append(text)
    return values[0], values[1]



def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--estado", action="store_true", required=True)
    args = parser.parse_args(argv)
    try:
        s = check_keyring()
        result = {
            "status": "ready" if (s.available and not s.locked and
                                  s.username_present and s.password_present)
                      else "not_ready",
            "vault_available": s.available,
            "vault_unlocked": s.locked is False,
            "username_saved": s.username_present,
            "password_saved": s.password_present,
        }
    except Exception:
        result = {"status": "keyring_unavailable"}
    print(json.dumps(result, sort_keys=True))
    return 0 if result.get("status") == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
