"""Chapter registry used by the CLI and future level selection systems."""

from __future__ import annotations

from .base import Chapter
from .c001 import CHAPTER as C001
from .c002 import CHAPTER as C002
from .c003 import CHAPTER as C003

CHAPTERS: dict[str, Chapter] = {
    C001.code: C001,
    C002.code: C002,
    C003.code: C003,
}


def get_chapter(code: str) -> Chapter:
    """Return a chapter by code."""

    try:
        return CHAPTERS[code.lower()]
    except KeyError as error:
        known_codes = ", ".join(sorted(CHAPTERS))
        raise KeyError(f"Unknown chapter {code!r}. Available chapters: {known_codes}") from error


def iter_chapters() -> list[Chapter]:
    """Return all registered chapters in code order."""

    return [CHAPTERS[code] for code in sorted(CHAPTERS)]
