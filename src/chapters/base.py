"""Chapter metadata shared by the CLI and future game-level builders."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from src.game.levels import Level


@dataclass(frozen=True, slots=True)
class Chapter:
    """A chapter exposes both a human-readable demo and a reusable level builder."""

    code: str
    title: str
    description: str
    build_level: Callable[[], Level]
    render_demo: Callable[[], str]
