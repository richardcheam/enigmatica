"""Minimal CLI-friendly game engine that can grow into a fuller loop later."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .levels import Level
from .player import PlayerProgress

InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


@dataclass(slots=True)
class PlayResult:
    """Summary returned after a level has been played."""

    level_id: str
    solved_count: int
    total_puzzles: int
    completed: bool


class GameEngine:
    """A small text engine that reuses the same puzzle objects as the chapter demos."""

    def __init__(self, *, input_fn: InputFn = input, output_fn: OutputFn = print) -> None:
        self.input_fn = input_fn
        self.output_fn = output_fn

    def play_level(
        self,
        level: Level,
        *,
        player: PlayerProgress | None = None,
    ) -> PlayResult:
        """Play all puzzles in a level until completion or early exit."""

        progress = player or PlayerProgress()
        solved_count = 0

        self.output_fn(level.title)
        self.output_fn(level.description)
        self.output_fn("Type your answer, or use 'hint' or 'quit'.")

        for index, puzzle in enumerate(level.puzzles, start=1):
            self.output_fn("")
            self.output_fn(f"Puzzle {index}/{level.puzzle_count}: {puzzle.title}")
            self.output_fn(puzzle.prompt)

            while True:
                answer = self.input_fn("> ").strip()

                if answer.lower() in {"quit", "exit"}:
                    return PlayResult(
                        level_id=level.id,
                        solved_count=solved_count,
                        total_puzzles=level.puzzle_count,
                        completed=False,
                    )

                if answer.lower() == "hint":
                    if puzzle.hint:
                        self.output_fn(f"Hint: {puzzle.hint}")
                    else:
                        self.output_fn("No hint is available for this puzzle.")
                    continue

                solved = puzzle.check_answer(answer)
                progress.record_attempt(puzzle.id, solved=solved)

                if solved:
                    solved_count += 1
                    self.output_fn("Correct.")
                    break

                self.output_fn("Not quite. Try again, or type 'hint'.")

        self.output_fn("")
        self.output_fn(f"Level complete: {solved_count}/{level.puzzle_count} puzzles solved.")
        return PlayResult(
            level_id=level.id,
            solved_count=solved_count,
            total_puzzles=level.puzzle_count,
            completed=True,
        )
