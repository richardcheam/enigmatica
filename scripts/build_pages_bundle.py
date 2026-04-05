"""Build a clean static bundle for GitHub Pages deployment."""

from __future__ import annotations

import shutil
from pathlib import Path

from export_web_data import ROOT, main as export_web_data_main

DIST_DIR = ROOT / ".site-dist"
FILES_TO_COPY = ["index.html", "play.html"]
DIRS_TO_COPY = ["assets", "web"]


def _reset_dist_dir() -> None:
    """Remove any previous build output and recreate the bundle directory."""

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)


def _copy_static_files() -> None:
    """Copy only the files required by the public static site."""

    for relative_path in FILES_TO_COPY:
        source = ROOT / relative_path
        if source.exists():
            destination = DIST_DIR / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    for relative_path in DIRS_TO_COPY:
        source = ROOT / relative_path
        if source.exists():
            shutil.copytree(
                source,
                DIST_DIR / relative_path,
                ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"),
            )


def _write_pages_markers() -> None:
    """Write GitHub Pages marker files directly into the bundle."""

    (DIST_DIR / ".nojekyll").write_text("", encoding="utf-8")


def main() -> int:
    """Export fresh game data and stage the GitHub Pages bundle."""

    export_web_data_main()
    _reset_dist_dir()
    _copy_static_files()
    _write_pages_markers()
    print(f"Built {DIST_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
