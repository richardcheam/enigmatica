"""Helpers for letter frequency analysis."""

from __future__ import annotations

from collections import Counter
from string import ascii_uppercase

from .utils import normalize_text


def letter_frequency(text: str) -> dict[str, int]:
    """Count letters in a piece of text."""

    normalized = normalize_text(text, keep_spaces=False)
    counts = Counter(char for char in normalized if char in ascii_uppercase)
    return dict(counts)


def ranked_letters(text: str) -> list[tuple[str, int]]:
    """Return letters sorted by descending frequency."""

    counts = letter_frequency(text)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))


def frequency_percentages(text: str) -> dict[str, float]:
    """Return percentage frequencies for the letters in text."""

    counts = letter_frequency(text)
    total = sum(counts.values())

    if total == 0:
        return {}

    return {
        letter: round((count / total) * 100, 2)
        for letter, count in sorted(counts.items())
    }
