"""Minimal CLI entry point for chapter demos and playable levels."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.chapters import get_chapter, iter_chapters
from src.game.engine import GameEngine


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""

    parser = argparse.ArgumentParser(
        description="Run chapter demos and puzzle levels for Enigmatica."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List the available chapters.")

    demo_parser = subparsers.add_parser("demo", help="Show a chapter demo.")
    demo_parser.add_argument("chapter", help="Chapter code, for example c001.")

    play_parser = subparsers.add_parser("play", help="Play a chapter level.")
    play_parser.add_argument("chapter", help="Chapter code, for example c001.")

    return parser


def list_chapters() -> int:
    """Print the registered chapters."""

    print("Available chapters:")
    for chapter in iter_chapters():
        print(f"- {chapter.code}: {chapter.title}")
        print(f"  {chapter.description}")
    return 0


def run_demo(chapter_code: str) -> int:
    """Print a non-interactive chapter demo."""

    chapter = get_chapter(chapter_code)
    print(f"{chapter.code} - {chapter.title}")
    print(chapter.description)
    print()
    print(chapter.render_demo())
    return 0


def play_chapter(chapter_code: str) -> int:
    """Launch the text-based level loop for a chapter."""

    chapter = get_chapter(chapter_code)
    level = chapter.build_level()
    engine = GameEngine()
    result = engine.play_level(level)
    return 0 if result.completed else 1


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point used by both ``python -m`` and the console script."""

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "list":
            return list_chapters()
        if args.command == "demo":
            return run_demo(args.chapter)
        if args.command == "play":
            return play_chapter(args.chapter)
    except KeyError as error:
        parser.exit(status=1, message=f"{error}\n")

    parser.exit(status=1, message="Unknown command.\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
