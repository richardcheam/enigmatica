"""Polybius square helpers for coordinate-based letter encoding."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

DEFAULT_POLYBIUS_ROWS = (
    "ABCDE",
    "FGHIK",
    "LMNOP",
    "QRSTU",
    "VWXYZ",
)

Coordinate = tuple[int, int]


def _normalize_rows(rows: Sequence[str]) -> tuple[str, ...]:
    """Validate and normalize a square Polybius board."""

    normalized = tuple(row.replace(" ", "").upper() for row in rows if row.strip())
    if not normalized:
        raise ValueError("Polybius board requires at least one row.")

    size = len(normalized)
    if any(len(row) != size for row in normalized):
        raise ValueError("Polybius board must be a square grid.")

    return normalized


def parse_coordinates(encoded: str) -> list[Coordinate]:
    """Parse row-column pairs from digits with optional whitespace."""

    compact = "".join(character for character in encoded if not character.isspace())
    if not compact.isdigit() or len(compact) % 2 != 0:
        raise ValueError("Polybius coordinates must contain an even number of digits.")

    return [
        (int(compact[index]), int(compact[index + 1]))
        for index in range(0, len(compact), 2)
    ]


def decode_polybius(
    encoded: str,
    *,
    rows: Sequence[str] = DEFAULT_POLYBIUS_ROWS,
) -> str:
    """Decode row-column coordinate pairs using a Polybius board."""

    board = _normalize_rows(rows)
    decoded: list[str] = []
    for row, column in parse_coordinates(encoded):
        if not 1 <= row <= len(board) or not 1 <= column <= len(board):
            raise ValueError(f"Coordinate {row}{column} is outside the Polybius board.")
        decoded.append(board[row - 1][column - 1])
    return "".join(decoded)


def encode_polybius(
    text: str,
    *,
    rows: Sequence[str] = DEFAULT_POLYBIUS_ROWS,
    separator: str = " ",
) -> str:
    """Encode letters as row-column coordinate pairs."""

    board = _normalize_rows(rows)
    positions = {
        symbol: (row_index, column_index)
        for row_index, row in enumerate(board, start=1)
        for column_index, symbol in enumerate(row, start=1)
    }
    positions["J"] = positions["I"]

    encoded: list[str] = []
    for character in text.upper():
        if character.isspace():
            continue
        try:
            row, column = positions[character]
        except KeyError as error:
            raise ValueError(f"Character {character!r} is not on the Polybius board.") from error
        encoded.append(f"{row}{column}")
    return separator.join(encoded)


def trace_polybius_decode(
    encoded: str,
    *,
    rows: Sequence[str] = DEFAULT_POLYBIUS_ROWS,
) -> list[tuple[str, str]]:
    """Return coordinate-to-letter mappings for a decoded clue."""

    coordinates = parse_coordinates(encoded)
    decoded = decode_polybius(encoded, rows=rows)
    return [
        (f"{row}{column}", letter)
        for (row, column), letter in zip(coordinates, decoded, strict=True)
    ]
