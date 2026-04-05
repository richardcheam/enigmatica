"""Chapter 1 built as a sequence of puzzles inside one chapter."""

from __future__ import annotations

from src.chapters.base import Chapter
from src.ciphers.grid import combine_grid_blocks, extract_grid_text, trace_grid_extraction
from src.ciphers.hill import (
    DEFAULT_HILL_ALPHABET,
    DEFAULT_PAD_CHAR,
    block_mapping_trace,
    decode_hill,
    encode_hill,
)
from src.ciphers.indexing import extract_text, trace_extraction
from src.game.levels import Level
from src.game.puzzle import Puzzle

CHAPTER_CODE = "c001"
CHAPTER_TITLE = "Chapter 1: 12 HOURS LEFT TO LIVE"
PUZZLE_01_LETTER_STRIP = "ARTOYGDWEASOTUIBOVIAFFQKJI"
PUZZLE_01_POSITIONS = (6, 9, 3, 3, 4, 8, 4, 2, 24)
PUZZLE_01_RAW_SOLUTION = extract_text(PUZZLE_01_LETTER_STRIP, PUZZLE_01_POSITIONS)
PUZZLE_01_FORMATTED_SOLUTION = "Get To Work"
PUZZLE_02_LEFT_BLOCK = (
    "VL1NK",
    "QCOSF",
    "1MV1F",
    "TARM2",
    "KQWKX",
    "EU3FL",
    "MZXIY",
    "XYMHQ",
    "I1QOF",
    "443VL",
    "AWELB",
    "EAB2H",
)
PUZZLE_02_RIGHT_BLOCK = (
    "JOLQ3",
    "IA4K1",
    "PEGBZ",
    "5YFOX",
    "OAPPQ",
    "DYZPM",
    "OYZEX",
    "OUNGL",
    "BNDEH",
    "UPDME",
    "21NB2",
    "BUOJ3",
)
PUZZLE_02_BOARD = combine_grid_blocks(PUZZLE_02_LEFT_BLOCK, PUZZLE_02_RIGHT_BLOCK)
PUZZLE_02_SOURCE_CLUE = ("14", "34", "24", "69")
PUZZLE_02_BOARD_COORDINATES = ((1, 4), (3, 4), (2, 4), (9, 6))
PUZZLE_02_SOLUTION = extract_grid_text(PUZZLE_02_BOARD, PUZZLE_02_BOARD_COORDINATES)
PUZZLE_03_HILL_KEY = ((9, 4), (8, 23))
PUZZLE_03_CIPHERTEXT = encode_hill(
    "MISSION",
    PUZZLE_03_HILL_KEY,
    alphabet=DEFAULT_HILL_ALPHABET,
    pad_char=DEFAULT_PAD_CHAR,
)
PUZZLE_03_RAW_SOLUTION = decode_hill(
    PUZZLE_03_CIPHERTEXT,
    PUZZLE_03_HILL_KEY,
    alphabet=DEFAULT_HILL_ALPHABET,
    pad_char=DEFAULT_PAD_CHAR,
)
PUZZLE_03_SOLUTION = PUZZLE_03_RAW_SOLUTION.removesuffix(DEFAULT_PAD_CHAR)


def _format_positions(positions: tuple[int, ...]) -> str:
    """Return the chapter positions as two-digit values for display."""

    return " ".join(f"{position:02d}" for position in positions)


def _format_board_rows(rows: tuple[str, ...] | list[str]) -> str:
    """Return numbered rows for CLI display."""

    return "\n".join(f"{index:02d}: {row[:5]} {row[5:]}" for index, row in enumerate(rows, start=1))


def _format_block_trace(trace: list[tuple[str, str]]) -> str:
    """Return block mappings for display."""

    return "\n".join(f"  {cipher_block} -> {plain_block}" for cipher_block, plain_block in trace)


def build_puzzle_01() -> Puzzle:
    """Build the first puzzle in chapter 1."""

    return Puzzle(
        id="c001-puzzle-01",
        title="Read the numbered letters",
        prompt=(
            "A strip of letters appears above a row of numbers.\n"
            f"Letters:   {PUZZLE_01_LETTER_STRIP}\n"
            f"Positions: {_format_positions(PUZZLE_01_POSITIONS)}\n"
            "Use the numbers as direct indexes into the letter strip and enter the decoded phrase."
        ),
        expected_answer=PUZZLE_01_FORMATTED_SOLUTION,
        hint="Treat the strip as 1-based indexed: 1=A, 2=R, 3=T, and so on.",
        metadata={
            "mechanic": "index-extraction",
            "chapter_puzzle_number": 1,
            "asset_path": "assets/chapters/c001/puzzle-01.png",
            "letter_strip": PUZZLE_01_LETTER_STRIP,
            "positions": PUZZLE_01_POSITIONS,
            "raw_solution": PUZZLE_01_RAW_SOLUTION,
        },
    )


def build_puzzle_02() -> Puzzle:
    """Build the second puzzle in chapter 1."""

    return Puzzle(
        id="c001-puzzle-02",
        title="Find the warning in the board",
        prompt=(
            "A second clue uses a larger board reference.\n"
            f"Board:\n{_format_board_rows(PUZZLE_02_BOARD)}\n"
            f"Source clue: {' '.join(PUZZLE_02_SOURCE_CLUE)}\n"
            "Use the board to recover the four-letter warning."
        ),
        expected_answer=PUZZLE_02_SOLUTION,
        hint=(
            "Read the board as a grid. The first three letters sit on row 4 and spell T, R, A."
        ),
        metadata={
            "mechanic": "grid-extraction",
            "chapter_puzzle_number": 2,
            "asset_path": "assets/chapters/c001/puzzle-02.png",
            "left_block": PUZZLE_02_LEFT_BLOCK,
            "right_block": PUZZLE_02_RIGHT_BLOCK,
            "source_clue": PUZZLE_02_SOURCE_CLUE,
            "board_coordinates": PUZZLE_02_BOARD_COORDINATES,
            "raw_solution": PUZZLE_02_SOLUTION,
        },
    )


def build_puzzle_03() -> Puzzle:
    """Build the third puzzle in chapter 1."""

    bigram_trace = block_mapping_trace(
        PUZZLE_03_CIPHERTEXT,
        PUZZLE_03_HILL_KEY,
        alphabet=DEFAULT_HILL_ALPHABET,
        pad_char=DEFAULT_PAD_CHAR,
    )

    return Puzzle(
        id="c001-puzzle-03",
        title="Use the Hill-cipher crib",
        prompt=(
            "The last clue in chapter 1 uses a two-character Hill cipher over the alphabet "
            f"{DEFAULT_HILL_ALPHABET}.\n"
            "You do not need to solve the matrix by hand for this game version.\n"
            "The playable puzzle uses a shorter adapted ciphertext generated from the recovered key.\n"
            "Recovered decoder crib:\n"
            f"{_format_block_trace(bigram_trace)}\n"
            f"Ciphertext: {PUZZLE_03_CIPHERTEXT}\n"
            "Read the plaintext blocks, then remove the trailing filler character if one remains."
        ),
        expected_answer=PUZZLE_03_SOLUTION,
        hint="The last plaintext block ends with the filler symbol '3', so drop it after decoding.",
        metadata={
            "mechanic": "hill-cipher-crib",
            "chapter_puzzle_number": 3,
            "asset_path": "assets/chapters/c001/puzzle-03.png",
            "alphabet": DEFAULT_HILL_ALPHABET,
            "pad_char": DEFAULT_PAD_CHAR,
            "adapted_for_gameplay": True,
            "ciphertext": PUZZLE_03_CIPHERTEXT,
            "key_matrix": PUZZLE_03_HILL_KEY,
            "raw_solution": PUZZLE_03_RAW_SOLUTION,
        },
    )


def build_puzzles() -> list[Puzzle]:
    """Build all puzzles currently implemented for chapter 1."""

    return [
        build_puzzle_01(),
        build_puzzle_02(),
        build_puzzle_03(),
    ]


def build_level() -> Level:
    """Build a playable level for the first chapter."""

    return Level(
        id="level-c001",
        title=CHAPTER_TITLE,
        description=(
            "Chapter 1 is modeled as a sequence of puzzle beats. It currently contains three "
            "implemented puzzles, with room for later chapter-1 puzzles to be added to the "
            "same level."
        ),
        puzzles=build_puzzles(),
        chapter_code=CHAPTER_CODE,
    )


def render_demo() -> str:
    """Render a short non-interactive preview of the chapter."""

    trace = trace_extraction(PUZZLE_01_LETTER_STRIP, PUZZLE_01_POSITIONS)
    puzzle_02_trace = trace_grid_extraction(PUZZLE_02_BOARD, PUZZLE_02_BOARD_COORDINATES)
    puzzle_03_trace = block_mapping_trace(
        PUZZLE_03_CIPHERTEXT,
        PUZZLE_03_HILL_KEY,
        alphabet=DEFAULT_HILL_ALPHABET,
        pad_char=DEFAULT_PAD_CHAR,
    )
    return "\n".join(
        [
            "Chapter structure: multi-puzzle level",
            f"Implemented puzzles: {len(build_puzzles())}",
            "",
            "Puzzle 1",
            "Mechanic: 1-based index extraction",
            f"Letters:   {PUZZLE_01_LETTER_STRIP}",
            f"Positions: {_format_positions(PUZZLE_01_POSITIONS)}",
            f"Trace:     {' '.join(f'{position:02d}->{letter}' for position, letter in trace)}",
            f"Decoded:   {PUZZLE_01_RAW_SOLUTION}",
            f"Answer:    {PUZZLE_01_FORMATTED_SOLUTION}",
            "",
            "Puzzle 2",
            "Mechanic: board-based grid extraction",
            f"Source clue: {' '.join(PUZZLE_02_SOURCE_CLUE)}",
            (
                "Board path: "
                + " ".join(
                    f"({column},{row})->{letter}"
                    for (column, row), letter in puzzle_02_trace
                )
            ),
            f"Decoded:   {PUZZLE_02_SOLUTION}",
            f"Answer:    {PUZZLE_02_SOLUTION}",
            "",
            "Puzzle 3",
            "Mechanic: game-friendly Hill cipher crib",
            f"Alphabet:  {DEFAULT_HILL_ALPHABET}",
            f"Ciphertext: {PUZZLE_03_CIPHERTEXT}",
            f"Trace:\n{_format_block_trace(puzzle_03_trace)}",
            f"Decoded:   {PUZZLE_03_RAW_SOLUTION}",
            f"Answer:    {PUZZLE_03_SOLUTION}",
            "",
            "Add later chapter-1 puzzles by creating build_puzzle_04() and appending it in build_puzzles().",
        ]
    )


CHAPTER = Chapter(
    code=CHAPTER_CODE,
    title=CHAPTER_TITLE,
    description=(
        "Chapter 1 now chains indexing, board extraction, and a guided Hill-cipher reveal."
    ),
    build_level=build_level,
    render_demo=render_demo,
)
