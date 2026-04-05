"""Reusable Morse code encoding and decoding helpers."""

from __future__ import annotations

from typing import Final


MORSE_CODE_MAP: Final[dict[str, str]] = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "!": "-.-.--",
    "'": ".----.",
    "\"": ".-..-.",
    ":": "---...",
    ";": "-.-.-.",
    "(": "-.--.",
    ")": "-.--.-",
    "-": "-....-",
    "/": "-..-.",
    "@": ".--.-.",
    "=": "-...-",
}

REVERSE_MORSE_CODE_MAP: Final[dict[str, str]] = {
    code: char for char, code in MORSE_CODE_MAP.items()
}


def encode_morse(
    text: str,
    *,
    letter_separator: str = " ",
    word_separator: str = " / ",
    strict: bool = False,
) -> str:
    """Encode text into Morse code."""

    encoded_words: list[str] = []

    for word in text.upper().split():
        encoded_letters: list[str] = []

        for char in word:
            symbol = MORSE_CODE_MAP.get(char)
            if symbol is None:
                if strict:
                    raise ValueError(f"Unsupported character for Morse encoding: {char!r}")
                continue
            encoded_letters.append(symbol)

        if encoded_letters:
            encoded_words.append(letter_separator.join(encoded_letters))

    return word_separator.join(encoded_words)


def decode_morse(
    code: str,
    *,
    letter_separator: str = " ",
    word_separator: str = "/",
    strict: bool = False,
    unknown_symbol: str = "?",
) -> str:
    """Decode Morse code into plaintext."""

    normalized_code = code.strip().replace(" / ", "/")
    decoded_words: list[str] = []

    for word in normalized_code.split(word_separator):
        symbols = [symbol for symbol in word.strip().split(letter_separator) if symbol]
        if not symbols:
            continue

        decoded_letters: list[str] = []
        for symbol in symbols:
            letter = REVERSE_MORSE_CODE_MAP.get(symbol)
            if letter is None:
                if strict:
                    raise ValueError(f"Unsupported Morse symbol: {symbol!r}")
                letter = unknown_symbol
            decoded_letters.append(letter)

        decoded_words.append("".join(decoded_letters))

    return " ".join(decoded_words)
