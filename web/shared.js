(function bootstrapShared(windowObject) {
  const DATA_URL = "./web/game-data.json";
  const STORAGE_KEY = "enigmatica-progress-v1";

  async function loadGameData() {
    const response = await fetch(DATA_URL);
    if (!response.ok) {
      throw new Error(`Failed to load data: ${response.status}`);
    }
    return response.json();
  }

  function loadProgress() {
    try {
      const raw = windowObject.localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return { solvedPuzzleIds: [], activeChapterCode: null, activePuzzleId: null };
      }

      const parsed = JSON.parse(raw);
      return {
        solvedPuzzleIds: Array.isArray(parsed.solvedPuzzleIds) ? parsed.solvedPuzzleIds : [],
        activeChapterCode: parsed.activeChapterCode ?? null,
        activePuzzleId: parsed.activePuzzleId ?? null,
      };
    } catch {
      return { solvedPuzzleIds: [], activeChapterCode: null, activePuzzleId: null };
    }
  }

  function saveProgress(progress) {
    windowObject.localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }

  function normalizeText(text) {
    return text
      .toUpperCase()
      .replace(/[^A-Z0-9\s]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function formatMechanicLabel(mechanic) {
    return mechanic
      .split("-")
      .map((chunk) => chunk[0].toUpperCase() + chunk.slice(1))
      .join(" ");
  }

  function chunkPairs(text) {
    return text.match(/.{1,2}/g)?.join(" ") ?? text;
  }

  function combineGridBlocks(leftRows, rightRows) {
    return leftRows.map((row, index) => `${row}${rightRows[index]}`);
  }

  function formatMatrix(matrix) {
    return matrix
      .map((row) => `  [${String(row[0]).padStart(2, " ")} ${String(row[1]).padStart(2, " ")}]`)
      .join("\n");
  }

  function getChapterByCode(data, chapterCode) {
    return data.chapters.find((chapter) => chapter.code === chapterCode) ?? null;
  }

  function getContiguousSolvedCount(chapter, progress) {
    let count = 0;
    for (const puzzle of chapter.puzzles) {
      if (!progress.solvedPuzzleIds.includes(puzzle.id)) {
        break;
      }
      count += 1;
    }
    return count;
  }

  function getFirstAvailablePuzzleId(chapter, progress) {
    const contiguousSolved = getContiguousSolvedCount(chapter, progress);
    return chapter.puzzles[Math.min(contiguousSolved, chapter.puzzles.length - 1)].id;
  }

  function getProgressSummary(data, progress) {
    const allPuzzles = data.chapters.flatMap((chapter) => chapter.puzzles);
    const solvedCount = allPuzzles.filter((puzzle) =>
      progress.solvedPuzzleIds.includes(puzzle.id),
    ).length;

    return {
      solvedCount,
      totalCount: allPuzzles.length,
      hasSolvedPuzzles: solvedCount > 0,
    };
  }

  function buildPlayUrl(chapterCode, puzzleId = null) {
    const params = new URLSearchParams();
    if (chapterCode) {
      params.set("chapter", chapterCode);
    }
    if (puzzleId) {
      params.set("puzzle", puzzleId);
    }

    const suffix = params.toString();
    return suffix ? `./play.html?${suffix}` : "./play.html";
  }

  windowObject.EnigmaticaShared = {
    DATA_URL,
    loadGameData,
    loadProgress,
    saveProgress,
    normalizeText,
    formatMechanicLabel,
    chunkPairs,
    combineGridBlocks,
    formatMatrix,
    getChapterByCode,
    getContiguousSolvedCount,
    getFirstAvailablePuzzleId,
    getProgressSummary,
    buildPlayUrl,
  };
})(window);
