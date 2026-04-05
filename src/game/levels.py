"""Level objects group puzzles into a unit the game engine can play."""

from __future__ import annotations

from dataclasses import dataclass

from .puzzle import Puzzle


@dataclass(slots=True)
class Level:
    """A lightweight container for one or more puzzles."""

    id: str
    title: str
    description: str
    puzzles: list[Puzzle]
    chapter_code: str | None = None

    def __post_init__(self) -> None:
        if not self.puzzles:
            raise ValueError("A level must contain at least one puzzle.")

    @property
    def puzzle_count(self) -> int:
        """Return the number of puzzles in this level."""

        return len(self.puzzles)
