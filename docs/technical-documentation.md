# Technical documentation

How NoteNamer is built. The why and the what are in [concept.md](concept.md);
the workflow is in [CONTRIBUTING.md](../CONTRIBUTING.md).

## Project structure

```
Notenamer/
  src/notenamer/      # all logic, importable and tested
  scripts/            # thin entry points that call src/notenamer
  tests/              # pytest, one test file per module
  data/
    corpus.csv        # test corpus: sources and licenses
    external/         # openly licensed scores (committed)
    raw/              # built locally, never committed
  docs/               # concept, technical documentation, test concept
```

## Conventions

- **Pitch** is always `(step, alter, octave)` with English letters C–B, in the reference CSV, the pipeline and the evaluation. German names (H, Fis) are created only when formatting the output.
- **Spelling** follows the printed score: a flat before an E is E-flat ("Es"), never D-sharp ("Dis").
- **Staff position:** 0 = bottom line, odd numbers are spaces, negative values and values above 8 are on ledger lines.
- **Coordinates** are pixels at 300 dpi internally; conversion to PDF points happens only when drawing.
- **Piece IDs** are kebab-case, e.g. `chopin-prelude-op28-4`.

## Decisions

| Date | Decision | Reason |
| --- | --- | --- |
| 24.11.2026 | Version 1 detects pitch only, no rhythm | Note names need no rhythm; keeps the problem small without losing the ML core. |
| 24.11.2026 | Rule engine separated from the model | Every error can be attributed to either the model or the logic; the logic is fully unit-testable. |
| 24.11.2026 | UTF-8 and CRLF as standard | Consistent files on Windows, no diffs that only change line endings. |
| 25.11.2026 | Repository in English | Reach beyond German-speaking readers. |
| 25.11.2026 | Printed spelling defines the note name | The tool names what is on the page (Es, not Dis); the reference stores step and alter for this reason. |
| 25.11.2026 | Test corpus from the music21 corpus | Free and reproducible on every PC without downloads; musescore.com requires a paid plan. |
| 25.11.2026 | Chopin Op. 28 No. 4 converted from LilyPond | Openly licensed source (CC BY-SA 4.0); its own PDF has a different engraving than the MusicXML, a realistic test. |
| 25.11.2026 | Test corpus never used for training | Otherwise the measurements are worthless. |
| 25.11.2026 | Changelog per version instead of a session log | Git history, pull requests and issues already record what happened; the changelog records what changed for users. |
| 25.11.2026 | Openly licensed sources of the test corpus are committed in `data/external/`, only the pages needed | Small (one page: 94 KB instead of 1 MB for the whole book); makes the corpus reproducible on every PC without downloads. |
| 25.11.2026 | Training data is never committed, only the scripts that generate it | Training data quickly reaches gigabytes; the scripts keep it reproducible. |
| 25.11.2026 | Training data comes from labelled sources (DeepScores V2, synthetic data via Verovio), not from plain PDFs | Object detection needs bounding boxes; plain PDFs would require annotating thousands of symbols by hand. |
