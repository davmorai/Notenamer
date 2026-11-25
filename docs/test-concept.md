# Test concept

| Level | What | Tool | When |
| --- | --- | --- | --- |
| Unit tests | Rule engine, staff geometry, metric | pytest | Every push (CI) |
| Integration tests | Pipeline on small known PDFs in `tests/fixtures/` | pytest | Every push (CI), from phase 4 |
| Evaluation | Accuracy on the test corpus against the MusicXML reference and Audiveris | `evaluate.py` | End of phases 0, 3 and 4 |
| Manual checks | Corpus spot checks, debug images, practice at the piano | By hand | As listed in each issue's Definition of Done |

Automated results are in the **Actions** tab of the repository and are not repeated here.
The test corpus is built with `uv run python scripts/build_corpus.py` and is never used for training.

## Protocol

Manual checks and evaluation runs only.

| Date | Commit | Test | Result | Notes |
| --- | --- | --- | --- | --- |
| 25.11.2026 | – | Chopin Op. 28 No. 4 conversion | Passed | Pickup + 25 measures, all measure lengths correct; measures 1, 4, 17 and 25 checked against the source. |
| 25.11.2026 | – | Visual spot check of all corpus PDFs against MusicXML | Open | Pending on the GPU PC after PDF export. |
