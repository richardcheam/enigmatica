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
    matrix_inverse_2x2,
    multiply_matrix_vector_2x2,
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
PUZZLE_03_MODULUS = len(DEFAULT_HILL_ALPHABET)
PUZZLE_03_INVERSE_KEY = matrix_inverse_2x2(PUZZLE_03_HILL_KEY, modulus=PUZZLE_03_MODULUS)
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
PUZZLE_03_EXAMPLE_BLOCK = "QB"
PUZZLE_03_EXAMPLE_VECTOR = (
    DEFAULT_HILL_ALPHABET.index(PUZZLE_03_EXAMPLE_BLOCK[0]),
    DEFAULT_HILL_ALPHABET.index(PUZZLE_03_EXAMPLE_BLOCK[1]),
)
PUZZLE_03_EXAMPLE_DECODED_VECTOR = multiply_matrix_vector_2x2(
    PUZZLE_03_INVERSE_KEY,
    PUZZLE_03_EXAMPLE_VECTOR,
    modulus=PUZZLE_03_MODULUS,
)
PUZZLE_03_EXAMPLE_DECODED_BLOCK = "".join(
    DEFAULT_HILL_ALPHABET[index] for index in PUZZLE_03_EXAMPLE_DECODED_VECTOR
)


def _format_positions(positions: tuple[int, ...]) -> str:
    """Return the chapter positions as two-digit values for display."""

    return " ".join(f"{position:02d}" for position in positions)


def _format_board_rows(rows: tuple[str, ...] | list[str]) -> str:
    """Return numbered rows for CLI display."""

    return "\n".join(f"{index:02d}: {row[:5]} {row[5:]}" for index, row in enumerate(rows, start=1))


def _format_block_trace(trace: list[tuple[str, str]]) -> str:
    """Return block mappings for display."""

    return "\n".join(f"  {cipher_block} -> {plain_block}" for cipher_block, plain_block in trace)


def _format_blocks(text: str) -> str:
    """Render text as space-separated bigrams."""

    return " ".join(text[index : index + 2] for index in range(0, len(text), 2))


def _format_matrix(matrix: tuple[tuple[int, int], tuple[int, int]]) -> str:
    """Render a 2x2 matrix for CLI display."""

    return "\n".join(f"  [{left:>2} {right:>2}]" for left, right in matrix)


def build_puzzle_01() -> Puzzle:
    """Build the first puzzle in chapter 1."""

    return Puzzle(
        id="c001-puzzle-01",
        title="Read the numbered letters",
        prompt=(
            f"Letters:   {PUZZLE_01_LETTER_STRIP}\n"
            f"Positions: {_format_positions(PUZZLE_01_POSITIONS)}\n"
            "\nRecover the hidden phrase."
        ),
        expected_answer=PUZZLE_01_FORMATTED_SOLUTION,
        hint="Treat the strip as 1-based indexed: 1=A, 2=R, 3=T, and so on.",
        metadata={
            "mechanic": "index-extraction",
            "chapter_puzzle_number": 1,
            "asset_path": "assets/chapters/c001/puzzle-01.png",
            "web_prompt": "Recover the hidden phrase.",
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
            f"Board:\n{_format_board_rows(PUZZLE_02_BOARD)}\n"
            f"Source clue: {' '.join(PUZZLE_02_SOURCE_CLUE)}\n"
            "\nRecover the hidden warning."
        ),
        expected_answer=PUZZLE_02_SOLUTION,
        hint="The two digits identify a position in the board.",
        metadata={
            "mechanic": "grid-extraction",
            "chapter_puzzle_number": 2,
            "asset_path": "assets/chapters/c001/puzzle-02.png",
            "web_prompt": "Recover the hidden warning.",
            "left_block": PUZZLE_02_LEFT_BLOCK,
            "right_block": PUZZLE_02_RIGHT_BLOCK,
            "source_clue": PUZZLE_02_SOURCE_CLUE,
            "board_coordinates": PUZZLE_02_BOARD_COORDINATES,
            "raw_solution": PUZZLE_02_SOLUTION,
        },
    )


def build_puzzle_03() -> Puzzle:
    """Build the third puzzle in chapter 1."""

    return Puzzle(
        id="c001-puzzle-03",
        title="Use the Hill-cipher inverse matrix",
        prompt=(
            "This chapter step uses a two-character Hill cipher over the alphabet "
            f"{DEFAULT_HILL_ALPHABET}.\n"
            "Medium mode gives you the inverse matrix, so you do not need to derive it yourself.\n"
            "Character values: A=0, B=1, ..., Z=25, 1=26, 2=27, 3=28, 4=29, 5=30\n"
            "Use this inverse matrix:\n"
            f"{_format_matrix(PUZZLE_03_INVERSE_KEY)}\n"
            "Treat each block XY as the column vector [x, y]^T, multiply modulo 31, then convert "
            "the result back into characters.\n"
            f"Ciphertext blocks: {_format_blocks(PUZZLE_03_CIPHERTEXT)}\n"
            "Decode all four blocks, join the plaintext, then remove the trailing filler character '3'."
        ),
        expected_answer=PUZZLE_03_SOLUTION,
        hint=(
            "Worked example: QB -> [16,1]. Applying the inverse matrix gives [12,8], which maps to MI."
        ),
        metadata={
            "mechanic": "hill-cipher-medium",
            "chapter_puzzle_number": 3,
            "asset_path": "assets/chapters/c001/puzzle-03.png",
            "web_prompt": (
                "Decode the ciphertext in two-character blocks with the supplied inverse matrix. "
                "Use A=0 through Z=25 and 1=26 through 5=30, multiplying modulo 31. "
                "Remove the trailing filler character after decoding."
            ),
            "alphabet": DEFAULT_HILL_ALPHABET,
            "pad_char": DEFAULT_PAD_CHAR,
            "mode": "medium",
            "ciphertext": PUZZLE_03_CIPHERTEXT,
            "key_matrix": PUZZLE_03_HILL_KEY,
            "inverse_key_matrix": PUZZLE_03_INVERSE_KEY,
            "example_block": PUZZLE_03_EXAMPLE_BLOCK,
            "example_vector": PUZZLE_03_EXAMPLE_VECTOR,
            "example_decoded_vector": PUZZLE_03_EXAMPLE_DECODED_VECTOR,
            "example_decoded_block": PUZZLE_03_EXAMPLE_DECODED_BLOCK,
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
            "Mechanic: medium-mode Hill cipher",
            "Character values: A=0..Z=25, 1=26..5=30",
            f"Inverse matrix:\n{_format_matrix(PUZZLE_03_INVERSE_KEY)}",
            f"Ciphertext blocks: {_format_blocks(PUZZLE_03_CIPHERTEXT)}",
            (
                "Worked example: "
                f"{PUZZLE_03_EXAMPLE_BLOCK} -> {list(PUZZLE_03_EXAMPLE_VECTOR)} -> "
                f"{list(PUZZLE_03_EXAMPLE_DECODED_VECTOR)} -> {PUZZLE_03_EXAMPLE_DECODED_BLOCK}"
            ),
            f"Full decode:\n{_format_block_trace(puzzle_03_trace)}",
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
