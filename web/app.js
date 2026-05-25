const shared = window.EnigmaticaShared;
const copy = window.EnigmaticaSiteCopy;
const params = new URLSearchParams(window.location.search);

const state = {
  data: null,
  progress: shared.loadProgress(),
  activeChapterCode: null,
  activePuzzleId: null,
};

const elements = {
  brandName: document.querySelector("#brandName"),
  brandSubtitle: document.querySelector("#brandSubtitle"),
  homeLink: document.querySelector("#homeLink"),
  overallProgress: document.querySelector("#overallProgress"),
  chapterProgressLabel: document.querySelector("#chapterProgressLabel"),
  playModeEyebrow: document.querySelector("#playModeEyebrow"),
  playChapterTitle: document.querySelector("#playChapterTitle"),
  playChapterDescription: document.querySelector("#playChapterDescription"),
  chapterNotesLink: document.querySelector("#chapterNotesLink"),
  puzzleFlowEyebrow: document.querySelector("#puzzleFlowEyebrow"),
  puzzleFlowLabel: document.querySelector("#puzzleFlowLabel"),
  puzzleNav: document.querySelector("#puzzleNav"),
  puzzleEyebrow: document.querySelector("#puzzleEyebrow"),
  puzzleTitle: document.querySelector("#puzzleTitle"),
  mechanicChip: document.querySelector("#mechanicChip"),
  puzzleMedia: document.querySelector("#puzzleMedia"),
  puzzleClue: document.querySelector("#puzzleClue"),
  instructionEyebrow: document.querySelector("#instructionEyebrow"),
  puzzlePrompt: document.querySelector("#puzzlePrompt"),
  answerForm: document.querySelector("#answerForm"),
  answerLabel: document.querySelector("#answerLabel"),
  answerInput: document.querySelector("#answerInput"),
  submitButton: document.querySelector("#submitButton"),
  hintButton: document.querySelector("#hintButton"),
  continueButton: document.querySelector("#continueButton"),
  hintBox: document.querySelector("#hintBox"),
  statusBox: document.querySelector("#statusBox"),
  resetProgressButton: document.querySelector("#resetProgressButton"),
};

boot();

async function boot() {
  try {
    state.data = await shared.loadGameData();
    hydrateDefaults();
    bindEvents();
    render();
  } catch (error) {
    showStatus(copy.interface.dataLoadError, "error");
    console.error(error);
  }
}

function hydrateDefaults() {
  const chapters = state.data.chapters;
  const requestedChapterCode = params.get("chapter");
  const requestedChapterCandidate = shared.getChapterByCode(state.data, requestedChapterCode);
  const requestedChapter =
    requestedChapterCandidate &&
    shared.isChapterUnlocked(state.data, requestedChapterCandidate.code, state.progress)
      ? requestedChapterCandidate
      : null;
  const fallbackChapter = shared.getResumeChapter(state.data, state.progress) || chapters[0] || null;
  const activeChapter = requestedChapter || fallbackChapter;

  state.activeChapterCode = activeChapter?.code ?? null;
  if (!activeChapter) {
    state.activePuzzleId = null;
    return;
  }

  const requestedPuzzleId = params.get("puzzle");
  const firstAvailablePuzzleId = shared.getFirstAvailablePuzzleId(activeChapter, state.progress);
  const contiguousSolved = shared.getContiguousSolvedCount(activeChapter, state.progress);
  const requestedPuzzleIndex = activeChapter.puzzles.findIndex(
    (puzzle) => puzzle.id === requestedPuzzleId,
  );
  const requestedPuzzleUnlocked =
    requestedPuzzleIndex >= 0 && requestedPuzzleIndex <= contiguousSolved;

  if (requestedPuzzleUnlocked) {
    state.activePuzzleId = requestedPuzzleId;
  } else if (
    state.progress.activePuzzleId &&
    activeChapter.puzzles.some((puzzle) => puzzle.id === state.progress.activePuzzleId)
  ) {
    state.activePuzzleId = state.progress.activePuzzleId;
  } else {
    state.activePuzzleId = firstAvailablePuzzleId;
  }

  saveProgress();
  syncUrl();
}

function bindEvents() {
  elements.answerForm.addEventListener("submit", handleAnswerSubmit);
  elements.hintButton.addEventListener("click", toggleHint);
  elements.continueButton.addEventListener("click", advanceToNextPuzzle);
  elements.resetProgressButton.addEventListener("click", resetProgress);
}

function handleAnswerSubmit(event) {
  event.preventDefault();

  const puzzle = getActivePuzzle();
  const answer = elements.answerInput.value.trim();
  if (!answer) {
    showStatus(copy.interface.typeAnswerFirst, "error");
    return;
  }

  if (shared.normalizeText(answer) === shared.normalizeText(puzzle.expected_answer ?? "")) {
    state.progress.solvedPuzzleIds = Array.from(
      new Set([...state.progress.solvedPuzzleIds, puzzle.id]),
    );
    saveProgress();
    render();

    if (hasNextPuzzle()) {
      showStatus(copy.interface.correctUnlock, "success");
      elements.continueButton.hidden = false;
    } else {
      showStatus(copy.interface.chapterClearReplay, "success");
      elements.continueButton.hidden = true;
    }
    return;
  }

  showStatus(copy.interface.incorrect, "error");
}

function toggleHint() {
  const puzzle = getActivePuzzle();
  if (!puzzle?.hint) {
    showStatus(copy.interface.noHint, "neutral");
    return;
  }

  const isHidden = elements.hintBox.hidden;
  elements.hintBox.hidden = !isHidden;
  elements.hintBox.textContent = puzzle.hint;
  elements.hintButton.textContent = isHidden ? copy.play.hideHint : copy.play.showHint;
}

function advanceToNextPuzzle() {
  const chapter = getActiveChapter();
  const currentIndex = chapter.puzzles.findIndex((puzzle) => puzzle.id === state.activePuzzleId);
  const nextPuzzle = chapter.puzzles[currentIndex + 1];

  if (!nextPuzzle) {
    showStatus(copy.interface.chapterClearSoon, "success");
    elements.continueButton.hidden = true;
    return;
  }

  state.activePuzzleId = nextPuzzle.id;
  saveProgress();
  syncUrl();
  resetPuzzlePanels();
  render();
  elements.answerInput.focus();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function resetProgress() {
  const confirmed = window.confirm(copy.interface.confirmReset);
  if (!confirmed) {
    return;
  }

  state.progress = {
    solvedPuzzleIds: [],
    activeChapterCode: null,
    activePuzzleId: null,
  };
  const chapter = shared.getResumeChapter(state.data, state.progress);
  state.activeChapterCode = chapter?.code ?? null;
  state.activePuzzleId = chapter
    ? shared.getFirstAvailablePuzzleId(chapter, state.progress)
    : null;
  saveProgress();
  syncUrl();
  resetPuzzlePanels();
  render();
  showStatus(copy.interface.progressReset, "neutral");
}

function render() {
  renderStaticCopy();
  renderProgress();
  renderPlayStage();
  renderPuzzleNav();
  renderPuzzle();
}

function renderStaticCopy() {
  elements.brandName.textContent = copy.common.brandName;
  elements.brandSubtitle.textContent = copy.common.playBrandSubtitle;
  elements.homeLink.textContent = copy.common.home;
  elements.resetProgressButton.textContent = copy.common.resetProgress;
  elements.playModeEyebrow.textContent = copy.play.modeEyebrow;
  elements.chapterNotesLink.textContent = copy.common.notesLink;
  elements.puzzleFlowEyebrow.textContent = copy.play.flowEyebrow;
  elements.instructionEyebrow.textContent = copy.play.instructionEyebrow;
  elements.answerLabel.textContent = copy.play.answerLabel;
  elements.submitButton.textContent = copy.play.submit;
  elements.hintButton.textContent = copy.play.showHint;
  elements.continueButton.textContent = copy.play.continue;
}

function renderProgress() {
  const summary = shared.getProgressSummary(state.data, state.progress);
  elements.overallProgress.textContent = `${summary.solvedCount} / ${summary.totalCount} ${copy.common.solved}`;

  const chapter = getActiveChapter();
  const chapterSolvedCount = chapter.puzzles.filter((puzzle) =>
    state.progress.solvedPuzzleIds.includes(puzzle.id),
  ).length;
  elements.chapterProgressLabel.textContent = `${chapterSolvedCount} / ${chapter.puzzles.length} ${copy.common.solved}`;
}

function renderPlayStage() {
  const chapter = getActiveChapter();
  elements.playChapterTitle.textContent = chapter.title;
  elements.playChapterDescription.textContent = chapter.description;
  elements.puzzleFlowLabel.textContent = `${chapter.puzzles.length} sequential ${copy.play.puzzleFallback.toLowerCase()}${chapter.puzzles.length === 1 ? "" : "s"}`;

  if (chapter.chapter_note_url || chapter.chapter_note_path) {
    elements.chapterNotesLink.href = chapter.chapter_note_url || `./${chapter.chapter_note_path}`;
    elements.chapterNotesLink.hidden = false;
  } else {
    elements.chapterNotesLink.hidden = true;
  }
}

function renderPuzzleNav() {
  const chapter = getActiveChapter();
  const contiguousSolved = shared.getContiguousSolvedCount(chapter, state.progress);
  elements.puzzleNav.innerHTML = "";

  chapter.puzzles.forEach((puzzle, index) => {
    const solved = state.progress.solvedPuzzleIds.includes(puzzle.id);
    const unlocked = index <= contiguousSolved;
    const active = puzzle.id === state.activePuzzleId;

    const wrapper = document.createElement("div");
    wrapper.className = [
      "puzzle-step",
      active ? "is-active" : "",
      !unlocked ? "is-locked" : "",
    ]
      .filter(Boolean)
      .join(" ");

    const button = document.createElement("button");
    button.type = "button";
    button.className = "puzzle-step-button";
    button.disabled = !unlocked;
    button.innerHTML = `
      <span>
        <span class="puzzle-step-index">${copy.play.puzzleFallback} ${String(index + 1).padStart(2, "0")}</span>
        <span class="puzzle-step-title">${puzzle.title}</span>
      </span>
      <span class="puzzle-step-state">${solved ? copy.play.stateSolved : unlocked ? copy.play.stateOpen : copy.play.stateLocked}</span>
    `;
    button.addEventListener("click", () => {
      if (!unlocked) {
        return;
      }

      state.activePuzzleId = puzzle.id;
      saveProgress();
      syncUrl();
      resetPuzzlePanels();
      render();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    wrapper.append(button);
    elements.puzzleNav.append(wrapper);
  });
}

function renderPuzzle() {
  const chapter = getActiveChapter();
  const puzzle = getActivePuzzle();
  const index = chapter.puzzles.findIndex((item) => item.id === puzzle.id);
  const solved = state.progress.solvedPuzzleIds.includes(puzzle.id);

  elements.puzzleEyebrow.textContent = `${copy.play.puzzleFallback} ${index + 1} of ${chapter.puzzles.length}`;
  elements.puzzleTitle.textContent = puzzle.title;
  elements.mechanicChip.textContent = shared.formatMechanicLabel(puzzle.metadata.mechanic);
  elements.puzzlePrompt.textContent = puzzle.metadata.web_prompt || puzzle.prompt;
  elements.answerInput.value = "";
  elements.answerInput.placeholder = solved
    ? copy.play.answerPlaceholderSolved
    : copy.play.answerPlaceholder;

  elements.puzzleMedia.innerHTML = "";
  renderPuzzleImages(puzzle).forEach((imageFrame) => elements.puzzleMedia.append(imageFrame));

  elements.puzzleClue.innerHTML = "";
  const mechanicClue = renderMechanicClue(puzzle);
  elements.puzzleClue.hidden = mechanicClue === null;
  if (mechanicClue) {
    elements.puzzleClue.append(mechanicClue);
  }

  if (solved) {
    showStatus(copy.interface.solvedReplay, "success");
    elements.continueButton.hidden = !hasNextPuzzle();
  } else {
    showStatus(copy.interface.ready, "neutral");
    elements.continueButton.hidden = true;
  }
}

function renderPuzzleImages(puzzle) {
  const images = [];
  if (puzzle.metadata.mechanic_asset_path && puzzle.metadata.mechanic_asset_exists) {
    images.push(
      renderPuzzleImage(
        puzzle.metadata.mechanic_asset_path,
        `${puzzle.title} mechanic reference`,
        copy.play.mechanicSnapshot || "Mechanic Reference",
      ),
    );
  }

  if (puzzle.metadata.rule_asset_path && puzzle.metadata.rule_asset_exists) {
    images.push(
      renderPuzzleImage(puzzle.metadata.rule_asset_path, `${puzzle.title} rule reference`, copy.play.ruleSnapshot),
    );
  }

  if (puzzle.metadata.asset_path && puzzle.metadata.asset_exists) {
    images.push(
      renderPuzzleImage(puzzle.metadata.asset_path, puzzle.title, copy.play.sourceSnapshot),
    );
  }

  return images;
}

function renderPuzzleImage(assetPath, altText, label) {
  const frame = document.createElement("div");
  frame.className = "puzzle-image-frame";
  frame.innerHTML = `
    <span class="puzzle-image-label">${label}</span>
    <img src="./${assetPath}" alt="${altText}" />
  `;
  return frame;
}

function renderMechanicClue(puzzle) {
  if (puzzle.metadata.image_only_clue) {
    return null;
  }

  const mechanic = puzzle.metadata.mechanic;
  const panel = document.createElement("div");
  panel.className = "clue-panel";

  if (mechanic === "index-extraction") {
    panel.innerHTML = `
      <div class="clue-grid">
        <div>
          <span class="label">${copy.play.clueLetterStrip}</span>
          <div class="mono-block">${puzzle.metadata.letter_strip}</div>
        </div>
        <div>
          <span class="label">${copy.play.cluePositions}</span>
          <div class="mono-block">${puzzle.metadata.positions.map((value) => String(value).padStart(2, "0")).join(" ")}</div>
        </div>
      </div>
    `;
    return panel;
  }

  if (mechanic === "grid-extraction") {
    const rows = shared.combineGridBlocks(
      puzzle.metadata.left_block,
      puzzle.metadata.right_block,
    );
    panel.innerHTML = `
      <div class="clue-grid">
        <div>
          <span class="label">${copy.play.clueBoardReference}</span>
          <pre class="board-pre">${rows
            .map((row, index) => `${String(index + 1).padStart(2, "0")}: ${row.slice(0, 5)} ${row.slice(5)}`)
            .join("\n")}</pre>
        </div>
        <div>
          <span class="label">${copy.play.clueSourceClue}</span>
          <div class="mono-block">${puzzle.metadata.source_clue.join(" ")}</div>
        </div>
      </div>
    `;
    return panel;
  }

  if (mechanic === "hill-cipher-medium") {
    panel.innerHTML = `
      <div class="matrix-layout">
        <div class="matrix-card">
          <span class="label">${copy.play.clueAlphabet}</span>
          ${puzzle.metadata.alphabet}
        </div>
        <div class="matrix-card">
          <span class="label">${copy.play.clueInverseMatrix}</span>
${shared.formatMatrix(puzzle.metadata.inverse_key_matrix)}
        </div>
        <div class="matrix-card">
          <span class="label">${copy.play.clueCiphertextBlocks}</span>
          ${shared.chunkPairs(puzzle.metadata.ciphertext)}
        </div>
      </div>
    `;
    return panel;
  }

  if (mechanic === "polybius-square") {
    panel.innerHTML = `
      <div class="clue-grid">
        <div>
          <span class="label">${copy.play.cluePolybiusBoard}</span>
          <pre class="board-pre">    1 2 3 4 5
${puzzle.metadata.board_rows
  .map((row, index) => `${index + 1}:  ${row.split("").join(" ")}`)
  .join("\n")}</pre>
        </div>
        <div>
          <span class="label">${copy.play.cluePlayableCoordinates}</span>
          <div class="mono-block">${puzzle.metadata.playable_coordinates}</div>
        </div>
      </div>
    `;
    return panel;
  }

  panel.innerHTML = `<div class="prompt-block"><p>${puzzle.metadata.web_prompt || puzzle.prompt}</p></div>`;
  return panel;
}

function showStatus(message, tone = "neutral") {
  elements.statusBox.textContent = message;
  elements.statusBox.className = `status-box is-${tone}`;
}

function resetPuzzlePanels() {
  elements.hintBox.hidden = true;
  elements.hintBox.textContent = "";
  elements.hintButton.textContent = copy.play.showHint;
  elements.continueButton.hidden = true;
}

function hasNextPuzzle() {
  const chapter = getActiveChapter();
  const currentIndex = chapter.puzzles.findIndex((puzzle) => puzzle.id === state.activePuzzleId);
  return currentIndex >= 0 && currentIndex < chapter.puzzles.length - 1;
}

function getActiveChapter() {
  return shared.getChapterByCode(state.data, state.activeChapterCode);
}

function getActivePuzzle() {
  const chapter = getActiveChapter();
  return chapter.puzzles.find((puzzle) => puzzle.id === state.activePuzzleId) || chapter.puzzles[0];
}

function saveProgress() {
  state.progress.activeChapterCode = state.activeChapterCode;
  state.progress.activePuzzleId = state.activePuzzleId;
  shared.saveProgress(state.progress);
}

function syncUrl() {
  const nextUrl = shared.buildPlayUrl(state.activeChapterCode, state.activePuzzleId);
  window.history.replaceState({}, "", nextUrl);
}
