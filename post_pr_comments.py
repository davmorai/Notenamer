"""Postet ein Self-Review mit Inline-Kommentaren auf den PR «UTF-8 und CRLF».

Aufruf im Repo-Ordner, während der Branch chore/utf8-crlf ausgecheckt ist:
    uv run python post_pr_comments.py

Voraussetzung: GitHub CLI eingeloggt, PR bereits mit `gh pr create --fill` eröffnet.
"""

import json
import subprocess
import sys

SUMMARY = """**Self-Review**

Der PR ändert nur Konfiguration, kein Produktivcode ist betroffen.

Lokal geprüft:
- Nach frischem Checkout sind alle Textdateien UTF-8 ohne BOM mit CRLF
- `ruff check`, `ruff format --check` und `pytest` grün
- Patch lässt sich auf einem frischen Klon sauber anwenden

Nach dem Merge einmal `git rm -rq --cached .` und `git reset --hard` ausführen \
(nur mit sauberem Arbeitsverzeichnis), damit bestehende Arbeitskopien CRLF bekommen."""

COMMENTS = [
    (
        ".gitattributes",
        2,
        "Kern des PRs: `text=auto` lässt Git Text- und Binärdateien selbst erkennen, "
        "`eol=crlf` erzwingt CRLF beim Auschecken – auf jedem Rechner, auch im CI-Runner. "
        "Im Repo selbst bleibt LF gespeichert. Dadurch entstehen keine Diffs, "
        "die nur aus Zeilenenden bestehen.",
    ),
    (
        ".gitattributes",
        5,
        "Bewusste Ausnahme: Shell-Skripte mit CRLF brechen unter Linux mit "
        "`bad interpreter`. Wird spätestens beim Docker-Image in Phase 5 relevant.",
    ),
    (
        ".gitattributes",
        8,
        "Explizit `binary`, obwohl `text=auto` die meisten Binärdateien erkennt. "
        "Git prüft dafür nur den Dateianfang, und manche PDFs sehen dort wie Text aus. "
        "Ein umgewandeltes PDF oder Modellgewicht wäre kaputt.",
    ),
    (
        ".editorconfig",
        4,
        "UTF-8 ohne BOM. Ein BOM würde z. B. den ersten Spaltennamen in `data/corpus.csv` "
        "verfälschen, wenn die Datei ohne `utf-8-sig` gelesen wird.",
    ),
    (
        ".editorconfig",
        5,
        "Damit auch neue Dateien direkt mit CRLF gespeichert werden. PyCharm liest "
        "`.editorconfig` automatisch, VS Code braucht dafür die EditorConfig-Erweiterung.",
    ),
    (
        "pyproject.toml",
        30,
        "Standard wäre `auto` (pro Datei erkannt). Fest auf `cr-lf` gesetzt, damit "
        "`ruff format` immer dasselbe Ergebnis liefert, egal auf welchem Rechner.",
    ),
    (
        "scripts/create_issues.py",
        435,
        "Wird die Ausgabe unter Windows umgeleitet (z. B. `> log.txt`), nutzt Python "
        "die Systemkodierung cp1252. Darin fehlt das Zeichen `→`, das das Skript ausgibt, "
        "und es käme zu einem `UnicodeEncodeError`.",
    ),
    (
        "README.md",
        48,
        "Konvention dokumentiert, damit niemand raten muss, warum Dateien CRLF haben.",
    ),
]


def gh(*args: str, input_text: str | None = None) -> str:
    result = subprocess.run(
        ["gh", *args], input=input_text, capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        sys.exit(f"Fehler bei `gh {' '.join(args)}`:\n{result.stderr.strip()}")
    return result.stdout


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    pr = json.loads(gh("pr", "view", "--json", "number,headRefOid"))
    review = {
        "commit_id": pr["headRefOid"],
        "event": "COMMENT",
        "body": SUMMARY,
        "comments": [
            {"path": path, "line": line, "side": "RIGHT", "body": body}
            for path, line, body in COMMENTS
        ],
    }
    gh(
        "api",
        f"repos/{{owner}}/{{repo}}/pulls/{pr['number']}/reviews",
        "--method",
        "POST",
        "--input",
        "-",
        input_text=json.dumps(review),
    )
    print(f"Review mit {len(COMMENTS)} Kommentaren auf PR #{pr['number']} gepostet.")


if __name__ == "__main__":
    main()
