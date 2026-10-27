"""Lector local de candidaturas de InfoJobs con Firefox y AT-SPI (sin WebDriver).

No usa contraseñas, cookies, solicitudes HTTP ni interfaces privadas del portal.
Interpreta exclusivamente el árbol de accesibilidad de la sesión que el usuario
ya ha abierto en Firefox, sin cerrar ni reiniciar el navegador.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile
import time

HOME_REPORT = Path.home() / ".local/share/buscar-curro/infojobs_privado.json"
STATES = ("Inscrito", "CV leído", "Preseleccionado", "Descartado", "En proceso", "Finalista", "Seleccionado")


def clean(value: str) -> str:
    value = re.sub(r"[\ue000-\uf8ff]", "", value or "")
    return " ".join(value.split()).strip()


@dataclass(frozen=True)
class Tree:
    role: str
    name: str
    children: tuple["Tree", ...] = ()


def candidate_card(node: Tree) -> dict | None:
    if node.role != "list item":
        return None
    direct = [x.name for x in node.children if x.role == "heading" and clean(x.name)]
    if len(direct) < 2:
        return None
    statuses = [
        clean(y.name)
        for x in node.children if x.role == "list"
        for y in x.children if y.role == "list item"
    ]
    status = next((s for s in statuses if s in STATES), None)
    if status is None:
        return None
    activity = next((s for s in statuses if re.fullmatch(r"Hace \d+\s*[mhd]", s, re.I)), None)
    title, company = [clean(x)[:200] for x in direct[:2]]
    return {"title": title, "company": company, "status": status,
            "last_company_activity_label": activity}


def candidates_from_tree(root: Tree) -> list[dict]:
    found = []
    def visit(node: Tree):
        item = candidate_card(node)
        if item is not None:
            found.append(item)
            return  # Do not interpret suggested jobs nested inside the card.
        for child in node.children:
            visit(child)
    visit(root)
    return found


def atspi():
    import gi
    gi.require_version("Atspi", "2.0")
    from gi.repository import Atspi
    return Atspi


def get_accessible_browser(Atspi):
    # Only the locally-authorized dedicated instance, not arbitrary windows.
    from infojobs_consulta_debian import find_browser_processes, agent_reachable
    browser = find_browser_processes()
    if len(browser) != 1 or browser[0][1] or agent_reachable():
        raise ValueError("dedicated_browser_not_ready")
    desktop = Atspi.get_desktop(0)
    matches = []
    for i in range(desktop.get_child_count()):
        app = desktop.get_child_at_index(i)
        if app.get_name() != "Firefox":
            continue
        for j in range(app.get_child_count()):
            window = app.get_child_at_index(j)
            if "InfoJobs" in window.get_name() and "Mozilla Firefox" in window.get_name():
                matches.append(window)
    if len(matches) != 1:
        raise ValueError("accessible_infojobs_window_missing_or_ambiguous")
    return matches[0]


def walk_live(root, maximum=1300):
    queue = [root]
    count = 0
    while queue and count < maximum:
        item = queue.pop(0)
        count += 1
        try:
            yield item
            n = item.get_child_count()
            if n < 180:
                queue.extend(item.get_child_at_index(i) for i in range(n))
        except (RuntimeError, TypeError):
            pass


def click_one(root, name: str) -> bool:
    links = [
        e for e in walk_live(root)
        if e.get_role_name() == "link" and clean(e.get_name()) == name
    ]
    if len(links) != 1:
        return False
    actions = links[0].get_action_iface()
    return bool(actions and actions.get_n_actions() == 1 and actions.do_action(0))


def accessible_tree(node, budget: list[int]) -> Tree:
    if budget[0] <= 0:
        raise ValueError("accessibility_tree_too_large")
    budget[0] -= 1
    role = node.get_role_name()
    name = clean(node.get_name())[:260]
    count = node.get_child_count()
    if count >= 180:
        raise ValueError("unexpected_accessibility_branch")
    children = tuple(accessible_tree(node.get_child_at_index(i), budget) for i in range(count))
    return Tree(role, name, children)


def read_current_application_list() -> dict:
    Atspi = atspi()
    window = get_accessible_browser(Atspi)
    for _ in range(3):
        title = window.get_name()
        if title.startswith("Mis candidaturas"):
            # Hidden section has a different link to return to visible applications.
            if any(clean(e.get_name()) == "Volver a Mis candidaturas" for e in walk_live(window)):
                if not click_one(window, "Volver a Mis candidaturas"):
                    raise ValueError("cannot_return_from_hidden_list")
                time.sleep(2.5)
                continue
            break
        action = ("Mis ofertas" if click_one(window, "Mis ofertas")
                  else "Ir a Candidaturas" if click_one(window, "Ir a Candidaturas")
                  else None)
        if action is None:
            raise ValueError("candidatures_navigation_unavailable")
        time.sleep(3)
    docs = [
        e for e in walk_live(window)
        if e.get_role_name() == "document web"
        and e.get_name().startswith("Mis candidaturas")
    ]
    if len(docs) != 1:
        raise ValueError("authenticated_applications_document_not_found")
    tree = accessible_tree(docs[0], [2200])
    jobs = candidates_from_tree(tree)
    if not jobs:
        raise ValueError("no_candidates_extraction_unverified")
    unique = {(j["title"], j["company"]) for j in jobs}
    if len(unique) != len(jobs):
        raise ValueError("duplicate_candidates")
    return {"status": "private_read_verified", "source": "infojobs_accessibility",
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "applications_count": len(jobs), "applications": jobs}


def save_private(report: dict, path=HOME_REPORT) -> None:
    path = Path(path)
    root = path.parent
    if root.is_symlink() or not root.is_dir():
        raise ValueError("private_directory_unavailable")
    if root.stat().st_mode & 0o077:
        raise ValueError("private_directory_permissions")
    if path.is_symlink():
        raise ValueError("symlink_report_rejected")
    data = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(dir=root, prefix=".infojobs-")
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            file.write(data)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revisar", action="store_true", required=True)
    args = parser.parse_args()
    try:
        report = read_current_application_list()
        save_private(report)
        print(json.dumps({
            "status": report["status"],
            "applications_count": report["applications_count"],
            "applications": report["applications"],
        }, ensure_ascii=False))
        return 0
    except Exception as ex:
        err = str(ex)
        allowed = {
            "dedicated_browser_not_ready",
            "accessible_infojobs_window_missing_or_ambiguous",
            "cannot_return_from_hidden_list",
            "candidatures_navigation_unavailable",
            "authenticated_applications_document_not_found",
            "accessibility_tree_too_large",
            "unexpected_accessibility_branch",
            "no_candidates_extraction_unverified",
            "duplicate_candidates",
            "private_directory_unavailable",
            "private_directory_permissions",
            "symlink_report_rejected",
        }
        print(json.dumps({"status": "private_read_unverified",
                          "reason": err if err in allowed else "unexpected_local_error"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
