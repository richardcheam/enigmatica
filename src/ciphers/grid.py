"""Helpers for grid-based extraction puzzles."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

Coordinate = tuple[int, int]


def normalize_grid_rows(rows: Sequence[str]) -> list[str]:
    """Return compact uppercase rows for a character grid."""

    normalized_rows: list[str] = []
    expected_width: int | None = None

    for row in rows:
        compact_row = row.replace(" ", "").upper()
        if not compact_row:
            continue

        if expected_width is None:
            expected_width = len(compact_row)
        elif len(compact_row) != expected_width:
            raise ValueError("Grid rows must all have the same width.")

        normalized_rows.append(compact_row)

    if not normalized_rows:
        raise ValueError("Grid must contain at least one non-empty row.")

    return normalized_rows


def combine_grid_blocks(left_rows: Sequence[str], right_rows: Sequence[str]) -> list[str]:
    """Combine two equal-height grid blocks into one continuous grid."""

    if len(left_rows) != len(right_rows):
        raise ValueError("Grid blocks must have the same number of rows.")

    return [
        f"{left.replace(' ', '').upper()}{right.replace(' ', '').upper()}"
        for left, right in zip(left_rows, right_rows, strict=True)
    ]


def extract_grid_symbols(
    rows: Sequence[str],
    coordinates: Iterable[Coordinate],
    *,
    one_based: bool = True,
) -> list[str]:
    """Return symbols found at ``(column, row)`` coordinates."""

    normalized_rows = normalize_grid_rows(rows)
    row_count = len(normalized_rows)
    column_count = len(normalized_rows[0])
    offset = 1 if one_based else 0
    extracted: list[str] = []

    for column, row in coordinates:
        column_index = column - offset
        row_index = row - offset

        if not 0 <= row_index < row_count:
            raise IndexError(f"Row {row} is out of range for a grid with {row_count} rows.")
        if not 0 <= column_index < column_count:
            raise IndexError(
                f"Column {column} is out of range for a grid with {column_count} columns."
            )

        extracted.append(normalized_rows[row_index][column_index])

    return extracted


def extract_grid_text(
    rows: Sequence[str],
    coordinates: Iterable[Coordinate],
    *,
    one_based: bool = True,
    separator: str = "",
) -> str:
    """Join extracted grid symbols into a string."""

    return separator.join(extract_grid_symbols(rows, coordinates, one_based=one_based))


def trace_grid_extraction(
    rows: Sequence[str],
    coordinates: Iterable[Coordinate],
    *,
    one_based: bool = True,
) -> list[tuple[Coordinate, str]]:
    """Return ``((column, row), symbol)`` pairs for display and reasoning."""

    coordinate_list = list(coordinates)
    extracted = extract_grid_symbols(rows, coordinate_list, one_based=one_based)
    return list(zip(coordinate_list, extracted, strict=True))
