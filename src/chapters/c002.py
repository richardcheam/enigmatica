"""Chapter 2 puzzles built around an alphanumeric checkerboard."""

from __future__ import annotations

from src.chapters.base import Chapter
from src.ciphers.polybius import (
    ALPHANUMERIC_POLYBIUS_ROWS,
    decode_polybius,
    trace_polybius_decode,
)
from src.game.levels import Level
from src.game.puzzle import Puzzle

CHAPTER_CODE = "c002"
CHAPTER_TITLE = "Chapter 2: 3 HOURS LEFT TO LIVE"
PUZZLE_01_SOURCE_DIGITS = "631121213224"
PUZZLE_01_COORDINATE_ORDER = "column-row"
PUZZLE_01_SOLUTION = decode_polybius(
    PUZZLE_01_SOURCE_DIGITS,
    rows=ALPHANUMERIC_POLYBIUS_ROWS,
    coordinate_order=PUZZLE_01_COORDINATE_ORDER,
)
PUZZLE_02_SOURCE_DIGITS = "31433141122336422214115131115154654222"
PUZZLE_02_COORDINATE_ORDER = "row-column"
PUZZLE_02_RAW_SOLUTION = decode_polybius(
    PUZZLE_02_SOURCE_DIGITS,
    rows=ALPHANUMERIC_POLYBIUS_ROWS,
    coordinate_order=PUZZLE_02_COORDINATE_ORDER,
)
PUZZLE_02_FORMATTED_SOLUTION = "MUM'S BIRTHDAY MAY 29TH"


def _format_board(rows: tuple[str, ...]) -> str:
    """Return the six-by-six checkerboard for CLI display."""

    header = "    1 2 3 4 5 6"
    body = [
        f"{row_index}:  {' '.join(row)}"
        for row_index, row in enumerate(rows, start=1)
    ]
    return "\n".join([header, *body])


def _cli_prompt(encoded: str, instruction: str) -> str:
    """Render only the source clue before a terminal player requests help."""

    return (
        f"Digit string: {encoded}\n"
        f"\n{instruction}"
    )


def _cli_hint(coordinate_order: str) -> str:
    """Render the checkerboard rule only after a player asks for a hint."""

    direction = {
        "column-row": "read a pair as column first, then row.",
        "row-column": "read a pair as row first, then column.",
    }[coordinate_order]
    return f"Use this reference board:\n{_format_board(ALPHANUMERIC_POLYBIUS_ROWS)}\n{direction}"


def build_puzzle_01() -> Puzzle:
    """Build the rabbit checkerboard puzzle from the source panels."""

    return Puzzle(
        id="c002-puzzle-01",
        title="Decode the digit string",
        prompt=_cli_prompt(PUZZLE_01_SOURCE_DIGITS, "Recover the hidden word."),
        expected_answer=PUZZLE_01_SOLUTION,
        hint=_cli_hint(PUZZLE_01_COORDINATE_ORDER),
        metadata={
            "mechanic": "alphanumeric-checkerboard",
            "chapter_puzzle_number": 1,
            "asset_path": "assets/chapters/c002/puzzle-01.png",
            "hint_mechanic_asset_path": "assets/chapters/c002/polybius-checkerboard.png",
            "hint_rule_asset_path": "assets/chapters/c002/puzzle-01-rule.png",
            "web_prompt": "Recover the hidden word.",
            "web_hint": "Use the revealed board. For this clue, read each pair as column first, then row.",
            "image_only_clue": True,
            "board_rows": ALPHANUMERIC_POLYBIUS_ROWS,
            "source_digits": PUZZLE_01_SOURCE_DIGITS,
            "coordinate_order": PUZZLE_01_COORDINATE_ORDER,
            "raw_solution": PUZZLE_01_SOLUTION,
        },
    )


def build_puzzle_02() -> Puzzle:
    """Build the longer checkerboard message from the source panel."""

    return Puzzle(
        id="c002-puzzle-02",
        title="Decode the written message",
        prompt=_cli_prompt(PUZZLE_02_SOURCE_DIGITS, "Recover the hidden message."),
        expected_answer=PUZZLE_02_FORMATTED_SOLUTION,
        hint=_cli_hint(PUZZLE_02_COORDINATE_ORDER),
        metadata={
            "mechanic": "alphanumeric-checkerboard",
            "chapter_puzzle_number": 2,
            "asset_path": "assets/chapters/c002/puzzle-02.png",
            "hint_rule_asset_path": "assets/chapters/c002/puzzle-01-rule.png",
            "web_prompt": "Recover the hidden message.",
            "web_hint": "Use the revealed board. For this clue, read each pair as row first, then column.",
            "image_only_clue": True,
            "board_rows": ALPHANUMERIC_POLYBIUS_ROWS,
            "source_digits": PUZZLE_02_SOURCE_DIGITS,
            "coordinate_order": PUZZLE_02_COORDINATE_ORDER,
            "raw_solution": PUZZLE_02_RAW_SOLUTION,
        },
    )


def build_puzzles() -> list[Puzzle]:
    """Build all currently implemented puzzles for chapter 2."""

    return [build_puzzle_01(), build_puzzle_02()]


def build_level() -> Level:
    """Build the playable level for chapter 2."""

    return Level(
        id="level-c002",
        title=CHAPTER_TITLE,
        description=(
            "Chapter 2 introduces a six-by-six checkerboard that can encode letters "
            "and digits as coordinate pairs."
        ),
        puzzles=build_puzzles(),
        chapter_code=CHAPTER_CODE,
    )


def render_demo() -> str:
    """Render a non-interactive preview of the chapter puzzles."""

    first_trace = trace_polybius_decode(
        PUZZLE_01_SOURCE_DIGITS,
        rows=ALPHANUMERIC_POLYBIUS_ROWS,
        coordinate_order=PUZZLE_01_COORDINATE_ORDER,
    )
    second_trace = trace_polybius_decode(
        PUZZLE_02_SOURCE_DIGITS,
        rows=ALPHANUMERIC_POLYBIUS_ROWS,
        coordinate_order=PUZZLE_02_COORDINATE_ORDER,
    )
    return "\n".join(
        [
            "Chapter structure: two-puzzle level",
            "Mechanic: alphanumeric checkerboard",
            "",
            _format_board(ALPHANUMERIC_POLYBIUS_ROWS),
            "",
            f"Puzzle 1 clue: {PUZZLE_01_SOURCE_DIGITS}",
            f"Trace: {' '.join(f'{coordinate}->{letter}' for coordinate, letter in first_trace)}",
            f"Answer: {PUZZLE_01_SOLUTION}",
            "",
            f"Puzzle 2 clue: {PUZZLE_02_SOURCE_DIGITS}",
            f"Trace: {' '.join(f'{coordinate}->{letter}' for coordinate, letter in second_trace)}",
            f"Answer: {PUZZLE_02_FORMATTED_SOLUTION}",
        ]
    )


CHAPTER = Chapter(
    code=CHAPTER_CODE,
    title=CHAPTER_TITLE,
    description=(
        "Chapter 2 introduces a six-by-six checkerboard and two coordinate-decoding puzzles."
    ),
    build_level=build_level,
    render_demo=render_demo,
)
