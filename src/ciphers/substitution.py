"""Simple substitution cipher helpers for later chapters."""

from __future__ import annotations

from collections.abc import Mapping
from string import ascii_uppercase


def _normalize_mapping(mapping: Mapping[str, str]) -> dict[str, str]:
    normalized: dict[str, str] = {}

    for source, target in mapping.items():
        source_key = source.upper()
        target_value = target.upper()

        if len(source_key) != 1 or len(target_value) != 1:
            raise ValueError("Substitution mappings must use single characters.")

        normalized[source_key] = target_value

    return normalized


def apply_substitution(
    text: str,
    mapping: Mapping[str, str],
    *,
    preserve_case: bool = True,
) -> str:
    """Apply a substitution mapping to text."""

    normalized_mapping = _normalize_mapping(mapping)
    transformed: list[str] = []

    for char in text:
        replacement = normalized_mapping.get(char.upper(), char)
        if preserve_case and char.islower() and replacement in ascii_uppercase:
            transformed.append(replacement.lower())
        else:
            transformed.append(replacement)

    return "".join(transformed)


def invert_substitution(mapping: Mapping[str, str]) -> dict[str, str]:
    """Swap the keys and values of a substitution mapping."""

    normalized_mapping = _normalize_mapping(mapping)
    return {target: source for source, target in normalized_mapping.items()}


def is_complete_substitution(mapping: Mapping[str, str]) -> bool:
    """Return True when the mapping covers a full A-Z substitution alphabet."""

    normalized_mapping = _normalize_mapping(mapping)
    return (
        set(normalized_mapping.keys()) == set(ascii_uppercase)
        and len(set(normalized_mapping.values())) == len(ascii_uppercase)
    )


def rotation_mapping(shift: int) -> dict[str, str]:
    """Return a complete A-Z substitution mapping rotated by ``shift`` positions."""

    normalized_shift = shift % len(ascii_uppercase)
    return {
        letter: ascii_uppercase[(index + normalized_shift) % len(ascii_uppercase)]
        for index, letter in enumerate(ascii_uppercase)
    }


def decode_substitution(text: str, encryption_mapping: Mapping[str, str]) -> str:
    """Decode text produced with a plaintext-to-ciphertext substitution mapping."""

    return apply_substitution(text, invert_substitution(encryption_mapping))
