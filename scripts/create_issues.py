"""Legt Labels, Milestones und Issues für NoteNamer auf GitHub an.

Voraussetzungen:
    - GitHub CLI installiert und eingeloggt (`gh auth login`)
    - Aufruf im Repo-Ordner, nachdem das Repo auf GitHub existiert

Aufruf:
    uv run python scripts/create_issues.py

Das Skript ist idempotent: Bereits vorhandene Labels, Milestones und Issues
(gleicher Titel) werden übersprungen. Es kann also gefahrlos mehrfach laufen.
"""

import json
import shutil
import subprocess
import sys

LABELS = [
    ("logik", "1d76db", "Musiktheorie und Regel-Engine"),
    ("cv", "5319e7", "Klassische Bildverarbeitung"),
    ("ml", "d93f0b", "Modell und Training"),
    ("daten", "fbca04", "Datensätze, Testkorpus, Referenzdaten"),
    ("eval", "0e8a16", "Messung, Metriken, Fehleranalyse"),
    ("infra", "6a737d", "Setup, CI, Docker, Deployment"),
    ("doku", "c5def5", "README und Dokumentation"),
]

MILESTONES = [
    ("Phase 0 · Setup & Baseline", "Woche 1. Gate: Baseline-Zahl steht."),
    ("Phase 1 · Musiklogik", "Woche 2–3. Gate: alle Regel-Tests grün."),
    ("Phase 2 · Notenlinien", "Woche 4–5. Gate: Linien auf allen Testseiten korrekt."),
    ("Phase 3 · Daten + Modell", "Woche 6–9. Gate: Notenköpfe zuverlässig erkannt."),
    ("Phase 4 · End-to-End", "Woche 10–11. Gate: Genauigkeitsziel N1 erreicht."),
    ("Phase 5 · Release", "Woche 12–13. Gate: öffentlicher Demo-Link."),
]

FOOTER = "\n\n---\nKonzept: `docs/konzept.md` im Repo"

ISSUES = [
    # ---------------- Phase 0 ----------------
    (
        "Entwicklungsumgebung einrichten und CI grün",
        ["infra"],
        0,
        """## Ziel
Das Repo läuft lokal, und GitHub Actions prüft jeden Push.

## Aufgaben
- [ ] uv installieren
- [ ] `uv sync` ausführen
- [ ] `uv run pytest` und `uv run ruff check .` lokal grün
- [ ] Ersten Push machen und prüfen, dass der CI-Lauf grün ist
- [ ] CI-Badge ins README einfügen

## Fertig, wenn
- Der CI-Lauf auf `main` ist grün.""",
    ),
    (
        "GPU-Setup prüfen (PyTorch mit CUDA)",
        ["infra", "ml"],
        0,
        """## Ziel
Sicherstellen, dass das Training später auf der RTX 4070 Ti Super läuft.

## Aufgaben
- [ ] NVIDIA-Treiber aktualisieren
- [ ] PyTorch mit CUDA in einer eigenen Dependency-Gruppe `ml` installieren
      (Befehl von pytorch.org; für uv den Abschnitt zu PyTorch in der uv-Doku beachten,
      dort steht, wie der CUDA-Index eingebunden wird)
- [ ] Kurzes Skript: `torch.cuda.is_available()` und Name der GPU ausgeben
- [ ] Setup-Schritte in `docs/setup.md` festhalten

## Fertig, wenn
- Das Skript gibt `True` und die RTX 4070 Ti Super aus.""",
    ),
    (
        "Testkorpus zusammenstellen (10 gemeinfreie Klavierstücke)",
        ["daten"],
        0,
        """## Ziel
Ein fester Satz Stücke, an dem alles gemessen wird.

## Aufgaben
- [ ] 10 Stücke finden, für die es PDF **und** MusicXML gibt (z. B. OpenScore, MuseScore, IMSLP)
- [ ] Mischung: einfach (z. B. Menuett) bis dicht (Chopin Op. 28 Nr. 4)
- [ ] Mindestens ein Stück mit vielen Vorzeichen und eines im Bassschlüssel mit Hilfslinien
- [ ] Lizenz pro Stück prüfen
- [ ] Alles in `data/corpus.csv` eintragen, Dateien lokal unter `data/raw/` ablegen

## Fertig, wenn
- `corpus.csv` hat 10 Zeilen, alle Lizenzen sind geprüft.
- Diese Stücke werden **nie** fürs Training verwendet.""",
    ),
    (
        "Referenz-Notennamen aus MusicXML extrahieren (Ground Truth)",
        ["daten", "eval"],
        0,
        """## Ziel
Für jedes Korpus-Stück die korrekten Notennamen als Referenz haben.

## Aufgaben
- [ ] MusicXML mit music21 laden
- [ ] Pro Note ausgeben: Takt, System (rechte/linke Hand), Tonhöhe (Name, Oktave)
- [ ] Akkordtöne einzeln auflisten
- [ ] Als CSV pro Stück unter `data/reference/` speichern
- [ ] Unit-Test mit einem kleinen, selbst geschriebenen MusicXML-Beispiel
- [ ] Chopin-Prelude stichprobenartig mit dem Notenblatt vergleichen

## Fertig, wenn
- Für alle 10 Stücke gibt es eine Referenz-CSV.""",
    ),
    (
        "Audiveris-Baseline messen",
        ["eval"],
        0,
        """## Ziel
Wissen, wie gut ein bestehendes Tool ist, bevor eigener Code entsteht.

## Aufgaben
- [ ] Audiveris installieren
- [ ] Alle Korpus-PDFs in MusicXML umwandeln
- [ ] Vergleich mit der Referenz: pro Takt die Tonhöhen als Multimenge vergleichen
      (robust gegen Unterschiede in Stimmen und Reihenfolge)
- [ ] Ergebnis in `docs/baseline.md`: Genauigkeit pro Stück und gesamt, 3–5 typische Fehlerarten

## Fertig, wenn
- Eine Baseline-Zahl steht (Gate Phase 0).
- Die Zielwerte im Konzept sind bei Bedarf angepasst.""",
    ),
    # ---------------- Phase 1 ----------------
    (
        "note_name(): Tonhöhe aus Schlüssel und Linienposition",
        ["logik"],
        1,
        """## Ziel
Die Kernfunktion in `src/notenamer/pitch.py` implementieren (Signatur steht bereits).

## Aufgaben
- [ ] Violin- und Bassschlüssel
- [ ] Hilfslinien: negative Positionen und Positionen über 8
- [ ] Skip in `tests/test_pitch.py` entfernen
- [ ] Mindestens 10 Tests, inklusive Grenzfälle

## Fertig, wenn
- Alle Tests in `test_pitch.py` laufen grün.""",
    ),
    (
        "Generalvorzeichen und Versetzungszeichen",
        ["logik"],
        1,
        """## Ziel
Vorzeichen korrekt anwenden – die häufigste Fehlerquelle beim Notenlesen.

## Aufgaben
- [ ] Generalvorzeichen −7 bis +7 (Reihenfolge Kreuze: F C G D A E H; b: H E A D G C F)
- [ ] Versetzungszeichen gilt bis zum Taktstrich, nur für dieselbe Position
- [ ] Auflösungszeichen hebt Generalvorzeichen im Takt auf
- [ ] Optional: Doppelkreuz und Doppel-b
- [ ] Ein Test pro Regel

## Fertig, wenn
- Jede Regel ist durch mindestens einen Test abgedeckt.""",
    ),
    (
        "Benennung Deutsch/Englisch konfigurierbar",
        ["logik"],
        1,
        """## Ziel
Die Benennung umschaltbar machen (Anforderung F5).

## Aufgaben
- [ ] Deutsch: C D E F G A H; Fis, Cis …; B (= englisch Bb), Es, As, Des
- [ ] Deutsche Sonderfälle: Eis, His, Ces, Fes
- [ ] Englisch: C D E F G A B; F#, Bb …
- [ ] Oktavangabe als Option vorbereiten (F11, Could)
- [ ] Tests für die Fallen H/B, Es, As

## Fertig, wenn
- Gate Phase 1: alle Regel-Tests grün.""",
    ),
    # ---------------- Phase 2 ----------------
    (
        "PDF-Seiten rendern und begradigen",
        ["cv"],
        2,
        """## Ziel
Aus jeder PDF-Seite ein sauberes, gerades Bild machen.

## Aufgaben
- [ ] `uv add pymupdf opencv-python-headless`
- [ ] Seiten mit 300 dpi als NumPy-Array rendern
- [ ] Graustufen und Binarisierung (Otsu oder adaptiv, beides vergleichen)
- [ ] Schräglage schätzen (Projektionsprofil oder Hough) und korrigieren
- [ ] Debug-Bilder unter `runs/` speichern

## Fertig, wenn
- Alle Korpus-Seiten sind gerade (Sichtprüfung der Debug-Bilder).""",
    ),
    (
        "Notenlinien und Linienabstand erkennen",
        ["cv"],
        2,
        """## Ziel
Jedes Fünfliniensystem mit Position und Linienabstand finden – die Grundlage für die Tonhöhe.

## Aufgaben
- [ ] Horizontales Projektionsprofil berechnen
- [ ] Linien zu Fünfergruppen zusammenfassen
- [ ] Linienabstand und Liniendicke schätzen
- [ ] Optional: Linien entfernen, um Symbole freizustellen
- [ ] Tests mit synthetisch erzeugten Bildern

## Fertig, wenn
- Auf allen Korpus-Seiten werden alle Systeme korrekt gefunden.""",
    ),
    (
        "Systeme zu Akkoladen gruppieren",
        ["cv"],
        2,
        """## Ziel
Rechte und linke Hand einander zuordnen.

## Aufgaben
- [ ] Je zwei Systeme (oben/unten) zu einer Akkolade gruppieren
- [ ] Datenstruktur: Seite → Akkolade → System, mit Koordinaten und Linienabstand
- [ ] Optional: Taktstriche erkennen (brauchen wir für Versetzungszeichen)

## Fertig, wenn
- Gate Phase 2: Struktur für alle Korpus-Seiten korrekt.""",
    ),
    # ---------------- Phase 3 ----------------
    (
        "Synthetische Trainingsdaten mit Verovio erzeugen",
        ["ml", "daten"],
        3,
        """## Ziel
Trainingsbilder mit exakten Labels, ohne von Hand zu annotieren.

## Aufgaben
- [ ] `uv add verovio`
- [ ] MusicXML → SVG (Verovio) → PNG
- [ ] Bounding Boxes für Notenköpfe, Schlüssel und Vorzeichen aus den SVG-Elementen lesen
- [ ] Im YOLO-Format speichern
- [ ] Variation: verschiedene Seitenbreiten, Skalierungen, Schriften
- [ ] Stichprobe visuell prüfen (Boxen einzeichnen)
- [ ] **Keine Stücke aus dem Testkorpus verwenden**

## Fertig, wenn
- Mehrere Tausend gelabelte Ausschnitte, Stichprobe fehlerfrei.""",
    ),
    (
        "DeepScores V2 ins YOLO-Format konvertieren",
        ["ml", "daten"],
        3,
        """## Ziel
Echte Notenseiten als zweite Trainingsquelle.

## Aufgaben
- [ ] Datensatz herunterladen
- [ ] Klassen auf das Nötige reduzieren: Notenkopf (gefüllt, hohl, ganz),
      Violin- und Bassschlüssel, Kreuz, b, Auflösungszeichen
- [ ] Ins YOLO-Format konvertieren
- [ ] Klassenverteilung dokumentieren

## Fertig, wenn
- Datensatz lädt in Ultralytics ohne Fehler.""",
    ),
    (
        "YOLO fine-tunen und Läufe in MLflow tracken",
        ["ml"],
        3,
        """## Ziel
Ein erstes Modell, das Notensymbole erkennt.

## Aufgaben
- [ ] `uv add --group ml ultralytics mlflow`
- [ ] Erster Lauf mit Standardparametern als Referenz
- [ ] Kleine Notenköpfe beachten: Seiten in Kacheln schneiden oder Bildgrösse erhöhen
- [ ] Jeden Lauf mit Parametern und Metriken in MLflow tracken
- [ ] Beste Gewichte ausserhalb des Repos ablegen (z. B. Hugging Face Hub oder GitHub Release)

## Fertig, wenn
- Ein Modell ist trainiert, der Lauf ist reproduzierbar dokumentiert.""",
    ),
    (
        "Symbolerkennung evaluieren und Fehleranalyse",
        ["ml", "eval"],
        3,
        """## Ziel
Ehrlich messen, wo das Modell versagt.

## Aufgaben
- [ ] mAP@0.5 pro Klasse auf einem getrennten Testsplit
- [ ] Beispielbilder der häufigsten Fehler sammeln
- [ ] Fehler gruppieren (z. B. dichte Akkorde, kleine Vorzeichen, Hilfslinien)
- [ ] Ergebnisse in `docs/results.md`

## Fertig, wenn
- Gate Phase 3: Notenköpfe werden zuverlässig erkannt (Zielwert nach dem ersten Lauf festlegen).""",
    ),
    # ---------------- Phase 4 ----------------
    (
        "End-to-End-Pipeline: Erkennung → Tonhöhe → PDF",
        ["ml", "logik"],
        4,
        """## Ziel
Alle Teile verbinden.

## Aufgaben
- [ ] Zentrum jedes Notenkopfs → Linienposition (aus Phase 2)
- [ ] Schlüssel und Vorzeichen aus der Erkennung den Noten zuordnen
- [ ] `note_name()` aufrufen
- [ ] CLI: `uv run notenamer input.pdf -o output.pdf` (Einstiegspunkt in `pyproject.toml`)

## Fertig, wenn
- Das Chopin-Prelude läuft komplett durch und liefert ein PDF.""",
    ),
    (
        "Notennamen im PDF ohne Überlappung platzieren",
        ["logik"],
        4,
        """## Ziel
Lesbare Annotation – das, was man am Ende sieht.

## Aufgaben
- [ ] Text mit PyMuPDF ins Original-PDF schreiben
- [ ] Schriftgrösse relativ zum Linienabstand
- [ ] Akkordtöne gestapelt (F6)
- [ ] Kollisionen mit Noten und Linien vermeiden
- [ ] Unsichere Erkennungen farbig markieren (F7)
- [ ] Offene Frage aus dem Konzept klären: über oder unter dem System?

## Fertig, wenn
- Ausgabe des Chopin-Preludes ist ohne Überlappungen lesbar.""",
    ),
    (
        "End-to-End-Evaluation gegen Referenz und Audiveris",
        ["eval"],
        4,
        """## Ziel
Die zentrale Zahl fürs README.

## Aufgaben
- [ ] Dieselbe Metrik wie bei der Baseline verwenden (Tonhöhen pro Takt)
- [ ] Vergleichstabelle NoteNamer vs. Audiveris pro Stück
- [ ] Fehleranalyse: woher kommen die Fehler (Modell oder Logik)?
- [ ] Laufzeit pro Seite auf CPU messen (N2)

## Fertig, wenn
- Gate Phase 4: Genauigkeitsziel N1 erreicht oder begründet angepasst.""",
    ),
    # ---------------- Phase 5 ----------------
    (
        "Gradio-App mit FastAPI-Backend",
        ["infra"],
        5,
        """## Ziel
Das Tool im Browser nutzbar machen.

## Aufgaben
- [ ] FastAPI-Endpoint: PDF rein, annotiertes PDF raus
- [ ] Gradio-Oberfläche: Upload, Auswahl DE/EN, Download
- [ ] Uploads nach der Verarbeitung löschen (N4)
- [ ] Fehlermeldungen für ungültige Dateien

## Fertig, wenn
- Lokal läuft der komplette Ablauf im Browser.""",
    ),
    (
        "Docker-Image",
        ["infra"],
        5,
        """## Ziel
Reproduzierbar starten mit einem Befehl (N3).

## Aufgaben
- [ ] `Dockerfile` (CPU-Variante für die Demo)
- [ ] Modellgewichte beim Build oder Start laden
- [ ] Startbefehl im README dokumentieren

## Fertig, wenn
- `docker run …` startet die App lokal.""",
    ),
    (
        "Deployment auf Hugging Face Spaces",
        ["infra"],
        5,
        """## Ziel
Öffentliche Demo per Link.

## Aufgaben
- [ ] Space anlegen (Docker oder Gradio SDK)
- [ ] Nur gemeinfreie Beispielstücke einbinden
- [ ] Laufzeit auf der Gratis-CPU prüfen (N2)
- [ ] Link ins README

## Fertig, wenn
- Gate Phase 5: Demo-Link funktioniert.""",
    ),
    (
        "README finalisieren: Metriken, Fehleranalyse, Demo",
        ["doku"],
        5,
        """## Ziel
Das README so, dass ein Recruiter in einer Minute versteht, was das Projekt kann.

## Aufgaben
- [ ] Vorher/Nachher-Bild (Notenblatt ohne und mit Notennamen)
- [ ] Ergebnistabelle: Genauigkeit, Vergleich Audiveris, Laufzeit
- [ ] Wichtigste Erkenntnisse aus der Fehleranalyse
- [ ] Demo-Link und Quickstart
- [ ] Status-Hinweis oben entfernen

## Fertig, wenn
- Das README zeigt Problem, Lösung, Messwerte und Demo.""",
    ),
]


def gh(*args: str, input_text: str | None = None) -> str:
    result = subprocess.run(
        ["gh", *args],
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        sys.exit(f"Fehler bei `gh {' '.join(args)}`:\n{result.stderr.strip()}")
    return result.stdout


def main() -> None:
    if shutil.which("gh") is None:
        sys.exit("GitHub CLI nicht gefunden. Installation: https://cli.github.com")

    print("Labels …")
    for name, color, description in LABELS:
        gh("label", "create", name, "--color", color, "--description", description, "--force")

    print("Milestones …")
    existing = json.loads(gh("api", "repos/{owner}/{repo}/milestones?state=all&per_page=100"))
    existing_titles = {m["title"] for m in existing}
    for title, description in MILESTONES:
        if title in existing_titles:
            print(f"  übersprungen: {title}")
            continue
        gh(
            "api",
            "repos/{owner}/{repo}/milestones",
            "-f",
            f"title={title}",
            "-f",
            f"description={description}",
        )
        print(f"  angelegt: {title}")

    print("Issues …")
    existing_issues = json.loads(
        gh("issue", "list", "--state", "all", "--limit", "500", "--json", "title")
    )
    existing_issue_titles = {i["title"] for i in existing_issues}
    for title, labels, phase, body in ISSUES:
        if title in existing_issue_titles:
            print(f"  übersprungen: {title}")
            continue
        url = gh(
            "issue",
            "create",
            "--title",
            title,
            "--label",
            ",".join(labels),
            "--milestone",
            MILESTONES[phase][0],
            "--body-file",
            "-",
            input_text=body + FOOTER,
        ).strip()
        print(f"  angelegt: {title} → {url}")

    print(f"Fertig: {len(LABELS)} Labels, {len(MILESTONES)} Milestones, {len(ISSUES)} Issues.")


if __name__ == "__main__":
    main()
