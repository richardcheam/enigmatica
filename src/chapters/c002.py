"""Chapter 2 built around a Polybius checkerboard puzzle."""

from __future__ import annotations

from src.chapters.base import Chapter
from src.ciphers.polybius import (
    DEFAULT_POLYBIUS_ROWS,
    decode_polybius,
    encode_polybius,
    trace_polybius_decode,
)
from src.game.levels import Level
from src.game.puzzle import Puzzle

CHAPTER_CODE = "c002"
CHAPTER_TITLE = "Chapter 2"
PUZZLE_01_SOURCE_DIGITS = "631121213224"
PUZZLE_01_ANSWER = "RABBIT"
PUZZLE_01_PLAYABLE_COORDINATES = encode_polybius(PUZZLE_01_ANSWER)
PUZZLE_01_DECODED = decode_polybius(PUZZLE_01_PLAYABLE_COORDINATES)


def _format_board(rows: tuple[str, ...]) -> str:
    """Return the checkerboard with coordinate labels for CLI display."""

    header = "    1 2 3 4 5"
    body = [
        f"{row_index}:  {' '.join(row)}"
        for row_index, row in enumerate(rows, start=1)
    ]
    return "\n".join([header, *body])


def build_puzzle_01() -> Puzzle:
    """Build the Polybius checkerboard puzzle."""

    return Puzzle(
        id="c002-puzzle-01",
        title="Read the Polybius checkerboard",
        prompt=(
            "A Polybius checkerboard stores each letter as two digits: row first, then column.\n"
            f"Board:\n{_format_board(DEFAULT_POLYBIUS_ROWS)}\n"
            f"Playable coordinate clue: {PUZZLE_01_PLAYABLE_COORDINATES}\n"
            "Decode the coordinate pairs and enter the recovered word."
        ),
        expected_answer=PUZZLE_01_ANSWER,
        hint="Start with 42: row 4, column 2 points to R.",
        metadata={
            "mechanic": "polybius-square",
            "chapter_puzzle_number": 1,
            "asset_path": "assets/chapters/c002/puzzle-01.png",
            "rule_asset_path": "assets/chapters/c002/rule-puzzle-01.png",
            "board_rows": DEFAULT_POLYBIUS_ROWS,
            "source_digits": PUZZLE_01_SOURCE_DIGITS,
            "playable_coordinates": PUZZLE_01_PLAYABLE_COORDINATES,
            "raw_solution": PUZZLE_01_DECODED,
            "source_discrepancy": (
                "The supplied cropped digit clue does not decode to RABBIT using the "
                "shown standard checkerboard. The playable clue uses verified coordinates."
            ),
        },
    )


def build_puzzles() -> list[Puzzle]:
    """Build all currently implemented puzzles for chapter 2."""

    return [build_puzzle_01()]


def build_level() -> Level:
    """Build the playable level for chapter 2."""

    return Level(
        id="level-c002",
        title=CHAPTER_TITLE,
        description="Chapter 2 introduces Polybius checkerboard coordinate decoding.",
        puzzles=build_puzzles(),
        chapter_code=CHAPTER_CODE,
    )


def render_demo() -> str:
    """Render a non-interactive preview of the chapter mechanic."""

    trace = trace_polybius_decode(PUZZLE_01_PLAYABLE_COORDINATES)
    return "\n".join(
        [
            "Chapter structure: single-puzzle level",
            "Mechanic: Polybius checkerboard",
            "",
            _format_board(DEFAULT_POLYBIUS_ROWS),
            "",
            f"Playable clue: {PUZZLE_01_PLAYABLE_COORDINATES}",
            f"Trace: {' '.join(f'{coordinate}->{letter}' for coordinate, letter in trace)}",
            f"Answer: {PUZZLE_01_DECODED}",
            "",
            f"Source crop digits retained for documentation: {PUZZLE_01_SOURCE_DIGITS}",
            "Note: those source digits do not decode to RABBIT under the displayed board.",
        ]
    )


CHAPTER = Chapter(
    code=CHAPTER_CODE,
    title=CHAPTER_TITLE,
    description="Chapter 2 introduces a Polybius checkerboard puzzle with row-column decoding.",
    build_level=build_level,
    render_demo=render_demo,
)
