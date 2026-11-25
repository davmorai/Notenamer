"""Build data/raw/<id>/ (score.musicxml and, if available, score.pdf) from data/corpus.csv."""

import csv
import pathlib
import shutil

from music21 import corpus

with open("data/corpus.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        source = row["source_musicxml"]
        out = pathlib.Path("data/raw") / row["id"]
        out.mkdir(parents=True, exist_ok=True)
        target = out / "score.musicxml"
        if source.startswith("music21:"):
            corpus.parse(source.removeprefix("music21:")).write("musicxml", fp=target)
        elif source.startswith("file:"):
            shutil.copyfile(source.removeprefix("file:"), target)
        else:
            print("skipped, unknown source:", row["id"])
            continue
        pdf_source = row["source_pdf"]
        if pdf_source.startswith("file:"):
            shutil.copyfile(pdf_source.removeprefix("file:"), out / "score.pdf")
        print("ok", row["id"])
