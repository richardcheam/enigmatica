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
  completionModal: document.querySelector("#completionModal"),
  completionModalEyebrow: document.querySelector("#completionModalEyebrow"),
  completionModalTitle: document.querySelector("#completionModalTitle"),
  completionModalBody: document.querySelector("#completionModalBody"),
  completionModalPrimaryButton: document.querySelector("#completionModalPrimaryButton"),
  completionModalCloseButton: document.querySelector("#completionModalCloseButton"),
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
  const progressPuzzleIndex = activeChapter.puzzles.findIndex(
    (puzzle) => puzzle.id === state.progress.activePuzzleId,
  );
  const requestedPuzzleUnlocked =
    requestedPuzzleIndex >= 0 && requestedPuzzleIndex <= contiguousSolved;
  const progressPuzzleUnlocked =
    progressPuzzleIndex >= 0 && progressPuzzleIndex <= contiguousSolved;

  if (requestedPuzzleUnlocked) {
    state.activePuzzleId = requestedPuzzleId;
  } else if (progressPuzzleUnlocked) {
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
  elements.completionModalPrimaryButton.addEventListener("click", handleCompletionModalPrimary);
  elements.completionModalCloseButton.addEventListener("click", closeCompletionModal);
  elements.completionModal.addEventListener("click", (event) => {
    if (event.target === elements.completionModal) {
      closeCompletionModal();
    }
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !elements.completionModal.hidden) {
      closeCompletionModal();
    }
  });
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
      setContinueAvailability(true);
    } else {
      showStatus(copy.interface.chapterClearReplay, "success");
      setContinueAvailability(false);
      showChapterCompletionModal();
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
  if (isHidden) {
    renderHint(puzzle);
  } else {
    elements.hintBox.innerHTML = "";
  }
  elements.hintButton.textContent = isHidden ? copy.play.hideHint : copy.play.showHint;
}

function advanceToNextPuzzle() {
  const chapter = getActiveChapter();
  if (!state.progress.solvedPuzzleIds.includes(state.activePuzzleId)) {
    showStatus(copy.interface.solveBeforeContinue, "error");
    setContinueAvailability(false);
    return;
  }

  const currentIndex = chapter.puzzles.findIndex((puzzle) => puzzle.id === state.activePuzzleId);
  const nextPuzzle = chapter.puzzles[currentIndex + 1];

  if (!nextPuzzle) {
    showStatus(copy.interface.chapterClearSoon, "success");
    setContinueAvailability(false);
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
  elements.completionModalEyebrow.textContent = copy.modal.eyebrow;
  elements.completionModalCloseButton.textContent = copy.modal.stayHere;
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
    setContinueAvailability(hasNextPuzzle());
  } else {
    showStatus(copy.interface.ready, "neutral");
    setContinueAvailability(false);
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

function renderHint(puzzle) {
  elements.hintBox.innerHTML = "";

  const hintCopy = document.createElement("p");
  hintCopy.className = "hint-copy";
  hintCopy.textContent = puzzle.metadata.web_hint || puzzle.hint;
  elements.hintBox.append(hintCopy);

  if (puzzle.metadata.hint_mechanic_asset_path && puzzle.metadata.hint_mechanic_asset_exists) {
    elements.hintBox.append(
      renderPuzzleImage(
        puzzle.metadata.hint_mechanic_asset_path,
        `${puzzle.title} hint mechanic reference`,
        copy.play.mechanicSnapshot || "Mechanic Reference",
      ),
    );
  }

  if (puzzle.metadata.hint_rule_asset_path && puzzle.metadata.hint_rule_asset_exists) {
    elements.hintBox.append(
      renderPuzzleImage(
        puzzle.metadata.hint_rule_asset_path,
        `${puzzle.title} hint rule reference`,
        copy.play.ruleSnapshot,
      ),
    );
  }

  const hintClue = renderHintClue(puzzle);
  if (hintClue) {
    elements.hintBox.append(hintClue);
  }
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

function renderFrequencyChart(profile) {
  const highestCount = profile[0]?.count ?? 1;
  return profile
    .map(
      (row) => `
        <div class="frequency-row">
          <span class="frequency-symbol">${row.symbol}</span>
          <span class="frequency-bar-track">
            <span class="frequency-bar" style="width: ${(row.count / highestCount) * 100}%"></span>
          </span>
          <span class="frequency-count">${row.count}</span>
        </div>
      `,
    )
    .join("");
}

function renderHintClue(puzzle) {
  const panel = document.createElement("div");
  panel.className = "hint-clue";

  if (puzzle.metadata.hint_clue === "grid-extraction") {
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

  if (puzzle.metadata.hint_clue === "frequency-profile") {
    panel.innerHTML = `
      <span class="label">${copy.play.clueFrequencyChart}</span>
      <div class="frequency-chart">${renderFrequencyChart(puzzle.metadata.frequency_profile)}</div>
    `;
    return panel;
  }

  if (puzzle.metadata.hint_clue === "known-mappings") {
    panel.innerHTML = `
      <span class="label">${copy.play.clueStartingMappings}</span>
      <div class="mapping-chips">
        ${puzzle.metadata.known_mappings
          .map(([cipherSymbol, plainSymbol]) => `<span>${cipherSymbol} &rarr; ${plainSymbol}</span>`)
          .join("")}
      </div>
    `;
    return panel;
  }

  return null;
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

  if (mechanic === "morse-code") {
    panel.innerHTML = `
      <div class="clue-grid">
        <div>
          <span class="label">${copy.play.clueTransmission}</span>
          <div class="morse-block">${puzzle.metadata.encoded_message}</div>
        </div>
      </div>
    `;
    return panel;
  }

  if (mechanic === "frequency-analysis") {
    const hasFrequency = puzzle.metadata.frequency_profile && puzzle.metadata.frequency_profile.length > 0;
    panel.innerHTML = `
      <div class="clue-grid">
        <div>
          <span class="label">${copy.play.clueEncryptedMessage}</span>
          <div class="cipher-message">${puzzle.metadata.ciphertext}</div>
        </div>
        ${hasFrequency ? `
        <div>
          <span class="label">${copy.play.clueFrequencyChart}</span>
          <div class="frequency-chart">${renderFrequencyChart(puzzle.metadata.frequency_profile)}</div>
        </div>` : ""}
      </div>
    `;
    return panel;
  }

  if (mechanic === "guided-substitution") {
    const hasFrequency = puzzle.metadata.frequency_profile && puzzle.metadata.frequency_profile.length > 0;
    panel.innerHTML = `
      <div class="clue-grid">
        <div>
          <span class="label">${copy.play.clueEncryptedMessage}</span>
          <div class="cipher-message">${puzzle.metadata.ciphertext}</div>
        </div>
        ${hasFrequency ? `
        <div>
          <span class="label">${copy.play.clueFrequencyChart}</span>
          <div class="frequency-chart">${renderFrequencyChart(puzzle.metadata.frequency_profile)}</div>
        </div>` : ""}
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
  elements.hintBox.innerHTML = "";
  elements.hintButton.textContent = copy.play.showHint;
  setContinueAvailability(false);
  closeCompletionModal();
}

function setContinueAvailability(available) {
  elements.continueButton.hidden = !available;
  elements.continueButton.disabled = !available;
}

function showChapterCompletionModal() {
  const chapter = getActiveChapter();
  const chapterIndex = state.data.chapters.findIndex((item) => item.code === chapter.code);
  const nextChapter = state.data.chapters[chapterIndex + 1] ?? null;
  const canAdvance =
    nextChapter && shared.isChapterUnlocked(state.data, nextChapter.code, state.progress);

  elements.completionModalTitle.textContent = `${chapter.title} Complete`;
  elements.completionModalBody.textContent = canAdvance
    ? copy.modal.nextUnlocked
    : copy.modal.allComplete;
  elements.completionModalPrimaryButton.textContent = canAdvance
    ? copy.modal.advance
    : copy.modal.returnHome;
  elements.completionModalPrimaryButton.dataset.chapterCode = canAdvance ? nextChapter.code : "";
  elements.completionModal.hidden = false;
  document.body.classList.add("has-modal");
  elements.completionModalPrimaryButton.focus();
}

function closeCompletionModal() {
  elements.completionModal.hidden = true;
  document.body.classList.remove("has-modal");
}

function handleCompletionModalPrimary() {
  const nextChapterCode = elements.completionModalPrimaryButton.dataset.chapterCode;
  if (nextChapterCode) {
    window.location.href = shared.buildPlayUrl(nextChapterCode);
    return;
  }

  window.location.href = "./index.html";
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
