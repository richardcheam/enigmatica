# E N I G M A T I C A

Cipher experiments and puzzle-game scaffolding inspired by manga-style decoding challenges.

![Manga Cover](assets/horizontal-cover.png)

## Current structure

```text
assets/
├── chapters/   # source images and reference materials for each chapter
docs/
├── chapters/   # chapter notes, reasoning, and image references
scripts/
├── export_web_data.py  # exports static chapter data for the GitHub Pages frontend
├── build_pages_bundle.py  # stages a clean static bundle for GitHub Pages deployment
src/
├── chapters/   # chapter-specific demos and level builders
├── ciphers/    # reusable cipher and analysis logic
├── game/       # puzzle, player, level, and engine building blocks
└── main.py     # minimal CLI entry point
web/
├── app.js      # static game interface logic
├── game-data.json  # exported chapter data for the web app
└── styles.css  # frontend styling
```

## Quick start

```bash
uv sync
uv run enigmatica list
uv run enigmatica demo c001
uv run enigmatica play c001
python3 scripts/export_web_data.py
```

You can also run the module directly:

```bash
python3 -m src.main list
python3 -m src.main demo c001
python3 -m src.main play c001
```

## Design notes

- Cipher logic lives in `src/ciphers/` so chapters and the future game loop can share it.
- `src/ciphers/` can also hold reusable decoding helpers that are not strict classical ciphers, such as index-based extraction.
- Chapter files expose both a human-readable demo and a reusable `Level` builder, and each chapter can contain multiple puzzles.
- `docs/chapters/` acts as the project notebook for puzzle snapshots, reasoning, and game-design notes.
- `assets/chapters/` stores the corresponding source images or other visual references, ideally one file per puzzle.
- `scripts/export_web_data.py` turns Python chapter data into static JSON for the web interface.
- `index.html` plus `web/` provide a GitHub Pages-friendly frontend with local browser progress.
- The CLI is intentionally small today, but it already speaks in terms of chapters and levels so it can grow into a real game loop later.

## Web interface

```bash
UV_CACHE_DIR="$PWD/.uv-cache" uv run python scripts/export_web_data.py
uv run python -m http.server
```

- Open `http://localhost:8000` to preview the static frontend locally.
- The site reads `web/game-data.json`, which is generated from the Python chapter definitions.
- For GitHub Pages, serve the repository root so `index.html` is the entry point.

## GitHub Pages

This repo is set up to deploy publicly with GitHub Pages through GitHub Actions.

Workflow:

- `.github/workflows/deploy-pages.yml` runs on pushes to `main`
- `scripts/build_pages_bundle.py` regenerates `web/game-data.json`
- the workflow stages a clean `.site-dist/` bundle
- GitHub Pages deploys that static artifact

One-time GitHub setup:

1. Push this repo to GitHub.
2. Open `Settings -> Pages`.
3. Under `Build and deployment`, set `Source` to `GitHub Actions`.
4. Push to `main` again or run the workflow manually from the `Actions` tab.

Notes:

- The public site will be available at `https://richardcheam.github.io/enigmatica/` once Pages is enabled.
- Chapter note links on the public site are routed to the GitHub repository view rather than raw markdown files on Pages.
- If you change chapter data, the deployment workflow will rebuild the exported JSON automatically.

## uv environment

- Run `uv sync` to create `.venv` from `pyproject.toml`.
- Use `uv run ...` so you do not accidentally use a system `python3` that is too old for the project.
- If you like using `pyenv` or a local Python pin, keep a private `.python-version` file locally; it is intentionally not tracked.
