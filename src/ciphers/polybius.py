"""Polybius square helpers for coordinate-based letter encoding."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

DEFAULT_POLYBIUS_ROWS = (
    "ABCDE",
    "FGHIK",
    "LMNOP",
    "QRSTU",
    "VWXYZ",
)
ALPHANUMERIC_POLYBIUS_ROWS = (
    "ABCDEF",
    "GHIJKL",
    "MNOPQR",
    "STUVWX",
    "YZ1234",
    "567890",
)

Coordinate = tuple[int, int]
CoordinateOrder = Literal["row-column", "column-row"]


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
    """Parse coordinate digit pairs from text with optional whitespace."""

    compact = "".join(character for character in encoded if not character.isspace())
    if not compact.isdigit() or len(compact) % 2 != 0:
        raise ValueError("Polybius coordinates must contain an even number of digits.")

    return [
        (int(compact[index]), int(compact[index + 1]))
        for index in range(0, len(compact), 2)
    ]


def _resolve_coordinate(
    coordinate: Coordinate,
    *,
    coordinate_order: CoordinateOrder,
) -> Coordinate:
    """Return a coordinate in row-column order for board lookup."""

    first, second = coordinate
    if coordinate_order == "row-column":
        return first, second
    if coordinate_order == "column-row":
        return second, first
    raise ValueError(f"Unsupported coordinate order: {coordinate_order!r}.")


def decode_polybius(
    encoded: str,
    *,
    rows: Sequence[str] = DEFAULT_POLYBIUS_ROWS,
    coordinate_order: CoordinateOrder = "row-column",
) -> str:
    """Decode coordinate pairs using a Polybius board."""

    board = _normalize_rows(rows)
    decoded: list[str] = []
    for coordinate in parse_coordinates(encoded):
        row, column = _resolve_coordinate(coordinate, coordinate_order=coordinate_order)
        if not 1 <= row <= len(board) or not 1 <= column <= len(board):
            first, second = coordinate
            raise ValueError(f"Coordinate {first}{second} is outside the Polybius board.")
        decoded.append(board[row - 1][column - 1])
    return "".join(decoded)


def encode_polybius(
    text: str,
    *,
    rows: Sequence[str] = DEFAULT_POLYBIUS_ROWS,
    separator: str = " ",
    coordinate_order: CoordinateOrder = "row-column",
) -> str:
    """Encode letters as coordinate pairs using a Polybius board."""

    board = _normalize_rows(rows)
    positions = {
        symbol: (row_index, column_index)
        for row_index, row in enumerate(board, start=1)
        for column_index, symbol in enumerate(row, start=1)
    }
    if "J" not in positions and "I" in positions:
        positions["J"] = positions["I"]

    encoded: list[str] = []
    for character in text.upper():
        if character.isspace():
            continue
        try:
            row, column = positions[character]
        except KeyError as error:
            raise ValueError(f"Character {character!r} is not on the Polybius board.") from error
        if coordinate_order == "row-column":
            encoded.append(f"{row}{column}")
        elif coordinate_order == "column-row":
            encoded.append(f"{column}{row}")
        else:
            raise ValueError(f"Unsupported coordinate order: {coordinate_order!r}.")
    return separator.join(encoded)


def trace_polybius_decode(
    encoded: str,
    *,
    rows: Sequence[str] = DEFAULT_POLYBIUS_ROWS,
    coordinate_order: CoordinateOrder = "row-column",
) -> list[tuple[str, str]]:
    """Return coordinate-to-letter mappings for a decoded clue."""

    coordinates = parse_coordinates(encoded)
    decoded = decode_polybius(encoded, rows=rows, coordinate_order=coordinate_order)
    return [
        (f"{row}{column}", letter)
        for (row, column), letter in zip(coordinates, decoded, strict=True)
    ]
