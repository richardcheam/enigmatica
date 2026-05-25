"""Export chapter data from Python into static JSON for the web frontend."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_URL = "https://github.com/richardcheam/enigmatica"
DEFAULT_BRANCH = "main"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chapters import iter_chapters


def _to_json_value(value: Any) -> Any:
    """Convert nested Python objects into JSON-safe values."""

    if isinstance(value, dict):
        return {str(key): _to_json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_json_value(item) for item in value]
    return value


def build_payload() -> dict[str, Any]:
    """Build the static payload consumed by the frontend."""

    chapters: list[dict[str, Any]] = []

    for chapter in iter_chapters():
        level = chapter.build_level()
        chapter_note_path = f"docs/chapters/{chapter.code}.md"
        note_exists = (ROOT / chapter_note_path).exists()
        chapter_note_url = (
            f"{REPOSITORY_URL}/blob/{DEFAULT_BRANCH}/{chapter_note_path}"
            if note_exists
            else None
        )
        puzzles: list[dict[str, Any]] = []

        for puzzle in level.puzzles:
            metadata = _to_json_value(puzzle.metadata)
            for key, asset_path in tuple(metadata.items()):
                if key.endswith("_asset_path"):
                    exists_key = f"{key.removesuffix('_path')}_exists"
                    metadata[exists_key] = bool(asset_path and (ROOT / asset_path).exists())

            puzzles.append(
                {
                    "id": puzzle.id,
                    "title": puzzle.title,
                    "prompt": puzzle.prompt,
                    "expected_answer": puzzle.expected_answer,
                    "hint": puzzle.hint,
                    "metadata": metadata,
                }
            )

        chapters.append(
            {
                "code": chapter.code,
                "title": chapter.title,
                "description": chapter.description,
                "level_id": level.id,
                "chapter_note_path": chapter_note_path if note_exists else None,
                "chapter_note_url": chapter_note_url,
                "puzzles": puzzles,
            }
        )

    return {
        "app": {
            "title": "Enigmatica",
            "tagline": "Decode the manga, one chapter at a time.",
            "repository_url": REPOSITORY_URL,
            "cover_image_path": (
                "assets/horizontal-cover.png"
                if (ROOT / "assets/horizontal-cover.png").exists()
                else "assets/vertical-cover.png"
                if (ROOT / "assets/vertical-cover.png").exists()
                else "assets/cover.png"
                if (ROOT / "assets/cover.png").exists()
                else None
            ),
        },
        "chapters": chapters,
    }


def main() -> int:
    """Write the exported payload to the static web directory."""

    output_path = ROOT / "web" / "game-data.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
