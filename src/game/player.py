"""Minimal player state for tracking attempts and solved puzzles."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PlayerProgress:
    """State collected while a level is being played."""

    name: str = "Player"
    solved_puzzles: set[str] = field(default_factory=set)
    attempts_by_puzzle: dict[str, int] = field(default_factory=dict)

    def record_attempt(self, puzzle_id: str, *, solved: bool) -> None:
        """Store the attempt count and solved status for a puzzle."""

        self.attempts_by_puzzle[puzzle_id] = self.attempts_by_puzzle.get(puzzle_id, 0) + 1
        if solved:
            self.solved_puzzles.add(puzzle_id)
