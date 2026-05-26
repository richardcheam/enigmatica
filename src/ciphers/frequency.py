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


def frequency_profile(
    text: str,
    *,
    limit: int | None = None,
) -> list[dict[str, int | float | str]]:
    """Return ranked symbol evidence suitable for display or candidate scoring."""

    ranked = ranked_letters(text)
    total = sum(count for _, count in ranked)
    if limit is not None:
        if limit < 1:
            raise ValueError("Frequency profile limit must be at least 1.")
        ranked = ranked[:limit]

    return [
        {
            "symbol": symbol,
            "count": count,
            "percentage": round((count / total) * 100, 2) if total else 0.0,
        }
        for symbol, count in ranked
    ]


def most_frequent_symbol(text: str) -> str | None:
    """Return the most common letter in text, or ``None`` when none exist."""

    ranked = ranked_letters(text)
    return ranked[0][0] if ranked else None
