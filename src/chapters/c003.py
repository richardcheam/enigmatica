"""Chapter 3 game-original puzzles inspired by Morse code and frequency analysis."""

from __future__ import annotations

from src.chapters.base import Chapter
from src.ciphers.frequency import frequency_profile
from src.ciphers.morse import decode_morse, encode_morse
from src.ciphers.substitution import (
    apply_substitution,
    decode_substitution,
    rotation_mapping,
)
from src.game.levels import Level
from src.game.puzzle import Puzzle

CHAPTER_CODE = "c003"
CHAPTER_TITLE = "Chapter 3: 5 MINUTES LEFT TO LIVE"

PUZZLE_01_MESSAGE = "HURRY"
PUZZLE_01_MORSE = encode_morse(PUZZLE_01_MESSAGE)
PUZZLE_01_SOLUTION = decode_morse(PUZZLE_01_MORSE)

PUZZLE_02_PLAINTEXT = (
    "THE SAME LETTER APPEARS OFTEN IN ENGLISH. THE MESSAGE OPENS WHEN YOU TEST COMMON WORDS. "
    "REPORT CODE: EAST GATE."
)
PUZZLE_02_ENCRYPTION_MAPPING = rotation_mapping(3)
PUZZLE_02_CIPHERTEXT = apply_substitution(PUZZLE_02_PLAINTEXT, PUZZLE_02_ENCRYPTION_MAPPING)
PUZZLE_02_PROFILE = frequency_profile(PUZZLE_02_CIPHERTEXT, limit=10)
PUZZLE_03_DECODED_MESSAGE = decode_substitution(
    PUZZLE_02_CIPHERTEXT,
    PUZZLE_02_ENCRYPTION_MAPPING,
)
PUZZLE_03_SOLUTION = "EAST GATE"


def _format_frequency_profile(profile: list[dict[str, int | float | str]]) -> str:
    """Format ranked frequency evidence for terminal play."""

    return "\n".join(
        f"  {row['symbol']}: {row['count']:>2} ({row['percentage']:>5.2f}%)"
        for row in profile
    )


def build_puzzle_01() -> Puzzle:
    """Build the Morse-code introduction puzzle."""

    return Puzzle(
        id="c003-puzzle-01",
        title="Read the urgent signal",
        prompt=f"Morse transmission:\n{PUZZLE_01_MORSE}\n\nDecode the single word.",
        expected_answer=PUZZLE_01_SOLUTION,
        hint="Use the Morse-code reference below. Decode each space-separated character.",
        metadata={
            "mechanic": "morse-code",
            "chapter_puzzle_number": 1,
            "hint_mechanic_asset_path": "assets/chapters/c003/morse-code.png",
            "web_prompt": "Decode the transmitted word.",
            "encoded_message": PUZZLE_01_MORSE,
            "raw_solution": PUZZLE_01_SOLUTION,
            "game_original": True,
        },
    )


def build_puzzle_02() -> Puzzle:
    """Build the substitution decoding puzzle."""

    return Puzzle(
        id="c003-puzzle-02",
        title="Decode the encrypted message",
        prompt=(
            f"Encrypted message:\n{PUZZLE_02_CIPHERTEXT}\n\n"
            "Decode the full message."
        ),
        expected_answer=PUZZLE_03_SOLUTION,
        hint=(
            f"Ranked letter counts:\n{_format_frequency_profile(PUZZLE_02_PROFILE)}\n\n"
            "Clue 1 — In English, E is the most common letter. H appears most often in the "
            "encrypted message, so H likely stands for E.\n"
            "Clue 2 — WKH appears as a word. THE is the most common three-letter word "
            "in English (W->T, K->H, H->E).\n"
            "Both clues point to a Caesar cipher: shift each letter back by 3."
        ),
        metadata={
            "mechanic": "frequency-analysis",
            "chapter_puzzle_number": 2,
            "ciphertext": PUZZLE_02_CIPHERTEXT,
            "web_prompt": "Decode the encrypted message to find the report code at the end.",
            "web_hint": (
                "Clue 1 — In English, E is the most common letter.\n"
                "Clue 2 — WKH appears as a word, so think of the most common three-letter word in English.\n"
                "Both clues point to a Caesar cipher. Recap: a Caesar cipher shifts each letter by a fixed amount."
            ),
            "frequency_profile": PUZZLE_02_PROFILE,
            "known_mappings": (("W", "T")),
            "hint_clue": "known-mappings",
            "decoded_message": PUZZLE_03_DECODED_MESSAGE,
            "raw_solution": PUZZLE_03_SOLUTION,
            "game_original": True,
        },
    )


def build_puzzles() -> list[Puzzle]:
    """Build all game-original puzzles inspired by chapter 3."""

    return [build_puzzle_01(), build_puzzle_02()]


def build_level() -> Level:
    """Build the playable level for chapter 3."""

    return Level(
        id="level-c003",
        title=CHAPTER_TITLE,
        description=(
            "Decode a Morse signal, then crack a Caesar cipher to uncover the report code."
        ),
        puzzles=build_puzzles(),
        chapter_code=CHAPTER_CODE,
    )


def render_demo() -> str:
    """Render a terminal preview of the chapter techniques."""

    return "\n".join(
        [
            "Chapter adaptation: game-original puzzles based on named techniques",
            "",
            "Puzzle 1 - Morse code",
            f"Transmission: {PUZZLE_01_MORSE}",
            f"Decoded: {PUZZLE_01_SOLUTION}",
            "",
            "Puzzle 2 - Substitution decode",
            f"Ciphertext: {PUZZLE_02_CIPHERTEXT}",
            f"Starting lead: H -> E, WKH -> THE (Caesar shift 3)",
            f"Decoded: {PUZZLE_03_DECODED_MESSAGE}",
            "",
            f"Report code from message: {PUZZLE_03_SOLUTION}",
        ]
    )


CHAPTER = Chapter(
    code=CHAPTER_CODE,
    title=CHAPTER_TITLE,
    description=(
        "Chapter 3: decode a Morse signal then crack a Caesar cipher to find the report code."
    ),
    build_level=build_level,
    render_demo=render_demo,
)
