"""Puzzle abstractions that can be reused by chapter demos and the future game."""

from __future__ import annotations

from typing import Any
from collections.abc import Callable
from dataclasses import dataclass, field

from src.ciphers.utils import normalize_text

AnswerValidator = Callable[[str], bool]


@dataclass(slots=True)
class Puzzle:
    """A single puzzle prompt with enough data for validation and hints."""

    id: str
    title: str
    prompt: str
    expected_answer: str | None = None
    validator: AnswerValidator | None = None
    hint: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def check_answer(self, answer: str) -> bool:
        """Validate a player's answer."""

        if self.validator is not None:
            return self.validator(answer)

        if self.expected_answer is None:
            raise ValueError("Puzzle requires either an expected answer or a validator.")

        return normalize_text(answer) == normalize_text(self.expected_answer)
