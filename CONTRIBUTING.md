# Contributing

How work is organized in this repository.

## Workflow

1. Every change starts from an issue. Issues are numbered in order (0.1, 0.2, …) and grouped by milestone, one milestone per phase.
2. Move the card to **In Progress** on the project board and create a branch from `main`:
   `feat/…`, `fix/…`, `data/…`, `docs/…` or `chore/…`
3. Commit with [Conventional Commits](https://www.conventionalcommits.org/): `feat: …`, `fix: …`, `docs: …`, `data: …`, `chore: …`
4. Open a pull request whose description contains `Closes #<issue>`. Merging closes the issue and moves the card to Done.
5. An issue is done when its Definition of Done is met; a phase is done when its gate is met.
6. Add notable changes to the `[Unreleased]` section of [CHANGELOG.md](CHANGELOG.md) in the same pull request.

## Before opening a pull request

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## Code and files

- Code, comments, docs and commits are in English.
- Logic lives in `src/notenamer/`; files in `scripts/` are thin entry points that call it.
- All text files are UTF-8 without BOM, with CRLF line endings (enforced by `.gitattributes` and `.editorconfig`).
- Scores in `data/raw/` and model weights are never committed. Openly licensed scores go into `data/external/`, with attribution.
