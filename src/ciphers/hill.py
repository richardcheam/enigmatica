"""Helpers for a simple 2x2 Hill cipher over a configurable alphabet."""

from __future__ import annotations

from collections.abc import Iterable
from string import ascii_uppercase

DEFAULT_HILL_ALPHABET = ascii_uppercase + "12345"
DEFAULT_PAD_CHAR = "3"
KeyMatrix = tuple[tuple[int, int], tuple[int, int]]


def normalize_hill_text(text: str, *, alphabet: str = DEFAULT_HILL_ALPHABET) -> str:
    """Return uppercase text filtered to characters supported by the alphabet."""

    allowed = set(alphabet)
    return "".join(char for char in text.upper() if char in allowed)


def hill_blocks(
    text: str,
    *,
    alphabet: str = DEFAULT_HILL_ALPHABET,
    pad_char: str = DEFAULT_PAD_CHAR,
) -> list[str]:
    """Split Hill-cipher text into two-character blocks."""

    normalized = normalize_hill_text(text, alphabet=alphabet)
    if pad_char not in alphabet:
        raise ValueError("Pad character must exist in the alphabet.")

    if len(normalized) % 2 == 1:
        normalized += pad_char

    return [normalized[index : index + 2] for index in range(0, len(normalized), 2)]


def modular_inverse(value: int, modulus: int) -> int:
    """Return the multiplicative inverse of ``value`` modulo ``modulus``."""

    value %= modulus

    for candidate in range(1, modulus):
        if (value * candidate) % modulus == 1:
            return candidate

    raise ValueError(f"{value} has no modular inverse modulo {modulus}.")


def matrix_determinant_2x2(matrix: KeyMatrix, *, modulus: int) -> int:
    """Return the determinant of a 2x2 matrix modulo ``modulus``."""

    (a, b), (c, d) = matrix
    return (a * d - b * c) % modulus


def matrix_inverse_2x2(matrix: KeyMatrix, *, modulus: int) -> KeyMatrix:
    """Return the modular inverse of a 2x2 matrix."""

    (a, b), (c, d) = matrix
    determinant = matrix_determinant_2x2(matrix, modulus=modulus)
    determinant_inverse = modular_inverse(determinant, modulus)

    return (
        ((d * determinant_inverse) % modulus, (-b * determinant_inverse) % modulus),
        ((-c * determinant_inverse) % modulus, (a * determinant_inverse) % modulus),
    )


def multiply_matrix_vector_2x2(
    matrix: KeyMatrix,
    vector: tuple[int, int],
    *,
    modulus: int,
) -> tuple[int, int]:
    """Multiply a 2x2 matrix by a 2x1 vector modulo ``modulus``."""

    (a, b), (c, d) = matrix
    x, y = vector
    return ((a * x + b * y) % modulus, (c * x + d * y) % modulus)


def multiply_matrices_2x2(
    left: KeyMatrix,
    right: KeyMatrix,
    *,
    modulus: int,
) -> KeyMatrix:
    """Multiply two 2x2 matrices modulo ``modulus``."""

    (a, b), (c, d) = left
    (e, f), (g, h) = right
    return (
        (((a * e) + (b * g)) % modulus, ((a * f) + (b * h)) % modulus),
        (((c * e) + (d * g)) % modulus, ((c * f) + (d * h)) % modulus),
    )


def encode_hill(
    plaintext: str,
    key: KeyMatrix,
    *,
    alphabet: str = DEFAULT_HILL_ALPHABET,
    pad_char: str = DEFAULT_PAD_CHAR,
) -> str:
    """Encode plaintext with a 2x2 Hill cipher."""

    alphabet_index = {char: index for index, char in enumerate(alphabet)}
    modulus = len(alphabet)
    encoded_blocks: list[str] = []

    for block in hill_blocks(plaintext, alphabet=alphabet, pad_char=pad_char):
        vector = (alphabet_index[block[0]], alphabet_index[block[1]])
        encoded_vector = multiply_matrix_vector_2x2(key, vector, modulus=modulus)
        encoded_blocks.append("".join(alphabet[index] for index in encoded_vector))

    return "".join(encoded_blocks)


def decode_hill(
    ciphertext: str,
    key: KeyMatrix,
    *,
    alphabet: str = DEFAULT_HILL_ALPHABET,
    pad_char: str = DEFAULT_PAD_CHAR,
    strip_padding: bool = False,
) -> str:
    """Decode ciphertext with a 2x2 Hill cipher."""

    inverse_key = matrix_inverse_2x2(key, modulus=len(alphabet))
    decoded = encode_hill(ciphertext, inverse_key, alphabet=alphabet, pad_char=pad_char)

    if strip_padding and decoded.endswith(pad_char):
        return decoded[:-1]

    return decoded


def derive_key_from_digraph_pairs(
    plaintext_blocks: tuple[str, str],
    ciphertext_blocks: tuple[str, str],
    *,
    alphabet: str = DEFAULT_HILL_ALPHABET,
) -> KeyMatrix:
    """Derive an encryption key from two plaintext/ciphertext digraph pairs."""

    if any(len(block) != 2 for block in (*plaintext_blocks, *ciphertext_blocks)):
        raise ValueError("Each digraph block must contain exactly two characters.")

    alphabet_index = {char: index for index, char in enumerate(alphabet)}
    modulus = len(alphabet)

    plaintext_matrix: KeyMatrix = (
        (
            alphabet_index[plaintext_blocks[0][0]],
            alphabet_index[plaintext_blocks[1][0]],
        ),
        (
            alphabet_index[plaintext_blocks[0][1]],
            alphabet_index[plaintext_blocks[1][1]],
        ),
    )
    ciphertext_matrix: KeyMatrix = (
        (
            alphabet_index[ciphertext_blocks[0][0]],
            alphabet_index[ciphertext_blocks[1][0]],
        ),
        (
            alphabet_index[ciphertext_blocks[0][1]],
            alphabet_index[ciphertext_blocks[1][1]],
        ),
    )

    plaintext_inverse = matrix_inverse_2x2(plaintext_matrix, modulus=modulus)
    return multiply_matrices_2x2(ciphertext_matrix, plaintext_inverse, modulus=modulus)


def block_mapping_trace(
    ciphertext: str,
    key: KeyMatrix,
    *,
    alphabet: str = DEFAULT_HILL_ALPHABET,
    pad_char: str = DEFAULT_PAD_CHAR,
    strip_padding: bool = False,
) -> list[tuple[str, str]]:
    """Return ``(cipher_block, plain_block)`` pairs for a ciphertext string."""

    cipher_blocks = hill_blocks(ciphertext, alphabet=alphabet, pad_char=pad_char)
    return [
        (
            block,
            decode_hill(
                block,
                key,
                alphabet=alphabet,
                pad_char=pad_char,
                strip_padding=strip_padding,
            ),
        )
        for block in cipher_blocks
    ]
