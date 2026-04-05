"""Small text utilities used across cipher modules."""

from __future__ import annotations

from collections import Counter
from string import ascii_uppercase


def normalize_text(text: str, *, keep_spaces: bool = True) -> str:
    """Return uppercase alphanumeric text with optional single-space separators."""

    normalized: list[str] = []

    for char in text.upper():
        if char in ascii_uppercase or char.isdigit():
            normalized.append(char)
        elif keep_spaces and char.isspace():
            if normalized and normalized[-1] != " ":
                normalized.append(" ")

    return "".join(normalized).strip()


def chunk_text(text: str, size: int) -> list[str]:
    """Split text into fixed-size chunks."""

    if size < 1:
        raise ValueError("Chunk size must be at least 1.")

    return [text[index : index + size] for index in range(0, len(text), size)]


def count_symbols(text: str) -> dict[str, int]:
    """Count non-space symbols in a string."""

    return dict(Counter(char for char in text if not char.isspace()))
