"""Helpers for index-based extraction puzzles."""

from __future__ import annotations

from collections.abc import Iterable, Sequence


def extract_symbols(
    symbols: Sequence[str] | str,
    positions: Iterable[int],
    *,
    one_based: bool = True,
) -> list[str]:
    """Return the symbols found at the requested positions."""

    symbol_list = list(symbols)
    offset = 1 if one_based else 0
    extracted: list[str] = []

    for position in positions:
        index = position - offset
        if index < 0 or index >= len(symbol_list):
            raise IndexError(
                f"Position {position} is out of range for a sequence of length {len(symbol_list)}."
            )
        extracted.append(symbol_list[index])

    return extracted


def extract_text(
    symbols: Sequence[str] | str,
    positions: Iterable[int],
    *,
    one_based: bool = True,
    separator: str = "",
) -> str:
    """Join extracted symbols into a single string."""

    return separator.join(extract_symbols(symbols, positions, one_based=one_based))


def trace_extraction(
    symbols: Sequence[str] | str,
    positions: Iterable[int],
    *,
    one_based: bool = True,
) -> list[tuple[int, str]]:
    """Return ``(position, symbol)`` pairs for explanation and hint output."""

    position_list = list(positions)
    extracted = extract_symbols(symbols, position_list, one_based=one_based)
    return list(zip(position_list, extracted, strict=True))
