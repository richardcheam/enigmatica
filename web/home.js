const shared = window.EnigmaticaShared;
const copy = window.EnigmaticaSiteCopy;

const state = {
  data: null,
  progress: shared.loadProgress(),
};

const elements = {
  brandName: document.querySelector("#brandName"),
  brandSubtitle: document.querySelector("#brandSubtitle"),
  coverImage: document.querySelector("#coverImage"),
  topbarPlayButton: document.querySelector("#topbarPlayButton"),
  heroPlayButton: document.querySelector("#heroPlayButton"),
  heroContinueButton: document.querySelector("#heroContinueButton"),
  overallProgress: document.querySelector("#overallProgress"),
  chapterCountLabel: document.querySelector("#chapterCountLabel"),
  chapterList: document.querySelector("#chapterList"),
  resetProgressButton: document.querySelector("#resetProgressButton"),
  homeVolumeLabel: document.querySelector("#homeVolumeLabel"),
  homeHeroTitle: document.querySelector("#homeHeroTitle"),
  homeHeroCopy: document.querySelector("#homeHeroCopy"),
  heroKicker: document.querySelector("#heroKicker"),
  heroCaption: document.querySelector("#heroCaption"),
  homeAboutEyebrow: document.querySelector("#homeAboutEyebrow"),
  homeAboutTitle: document.querySelector("#homeAboutTitle"),
  homeAboutCopy: document.querySelector("#homeAboutCopy"),
  homeHowEyebrow: document.querySelector("#homeHowEyebrow"),
  featureTitle01: document.querySelector("#featureTitle01"),
  featureBody01: document.querySelector("#featureBody01"),
  featureTitle02: document.querySelector("#featureTitle02"),
  featureBody02: document.querySelector("#featureBody02"),
  featureTitle03: document.querySelector("#featureTitle03"),
  featureBody03: document.querySelector("#featureBody03"),
  chaptersEyebrow: document.querySelector("#chaptersEyebrow"),
};

boot();

async function boot() {
  try {
    state.data = await shared.loadGameData();
    bindEvents();
    render();
  } catch (error) {
    console.error(error);
  }
}

function bindEvents() {
  elements.topbarPlayButton.addEventListener("click", () => {
    window.location.href = getPrimaryPlayUrl();
  });

  elements.heroPlayButton.addEventListener("click", () => {
    window.location.href = getPrimaryPlayUrl();
  });

  elements.heroContinueButton.addEventListener("click", () => {
    window.location.href = getPrimaryPlayUrl();
  });

  elements.resetProgressButton.addEventListener("click", resetProgress);
}

function render() {
  renderStaticCopy();
  renderCover();
  renderProgress();
  renderButtons();
  renderChapterList();
}

function renderStaticCopy() {
  elements.brandName.textContent = copy.common.brandName;
  elements.brandSubtitle.textContent = copy.common.homeBrandSubtitle;
  elements.resetProgressButton.textContent = copy.common.resetProgress;
  elements.homeVolumeLabel.textContent = copy.home.volumeLabel;
  elements.homeHeroTitle.textContent = copy.home.heroTitle;
  elements.homeHeroCopy.textContent = copy.home.heroCopy;
  elements.heroKicker.textContent = copy.home.heroKicker;
  elements.heroCaption.textContent = copy.home.heroCaption;
  elements.homeAboutEyebrow.textContent = copy.home.aboutEyebrow;
  elements.homeAboutTitle.textContent = copy.home.aboutTitle;
  elements.homeAboutCopy.textContent = copy.home.aboutCopy;
  elements.homeHowEyebrow.textContent = copy.home.howEyebrow;
  elements.chaptersEyebrow.textContent = copy.home.chaptersEyebrow;

  elements.featureTitle01.textContent = copy.home.featureCards[0].title;
  elements.featureBody01.textContent = copy.home.featureCards[0].body;
  elements.featureTitle02.textContent = copy.home.featureCards[1].title;
  elements.featureBody02.textContent = copy.home.featureCards[1].body;
  elements.featureTitle03.textContent = copy.home.featureCards[2].title;
  elements.featureBody03.textContent = copy.home.featureCards[2].body;
}

function renderCover() {
  if (state.data.app.cover_image_path) {
    elements.coverImage.src = `./${state.data.app.cover_image_path}`;
  }
}

function renderProgress() {
  const summary = shared.getProgressSummary(state.data, state.progress);
  elements.overallProgress.textContent = `${summary.solvedCount} / ${summary.totalCount} ${copy.common.solved}`;
}

function renderButtons() {
  const summary = shared.getProgressSummary(state.data, state.progress);
  elements.topbarPlayButton.textContent = summary.hasSolvedPuzzles
    ? copy.common.continue
    : copy.common.play;
  elements.heroPlayButton.textContent = summary.hasSolvedPuzzles
    ? copy.home.resumeInteractive
    : copy.home.startInteractive;
  elements.heroContinueButton.textContent = copy.home.continueChapter;
  elements.heroContinueButton.hidden = !summary.hasSolvedPuzzles;
}

function renderChapterList() {
  elements.chapterCountLabel.textContent = `${state.data.chapters.length} ${copy.common.total}`;
  elements.chapterList.innerHTML = "";

  for (const chapter of state.data.chapters) {
    const solvedCount = chapter.puzzles.filter((puzzle) =>
      state.progress.solvedPuzzleIds.includes(puzzle.id),
    ).length;

    const item = document.createElement("div");
    item.className = `chapter-item${chapter.code === state.progress.activeChapterCode ? " is-active" : ""}`;

    const button = document.createElement("button");
    button.type = "button";
    button.className = "chapter-button";
    button.innerHTML = `
      <strong>${chapter.code.toUpperCase()} · ${chapter.title}</strong>
      <span>${chapter.description}</span>
      <div class="chapter-meta">
        <span class="chapter-pill">${solvedCount} / ${chapter.puzzles.length} ${copy.common.solved}</span>
        <span class="subtle-label">${chapter.puzzles.length} ${copy.common.puzzles}</span>
      </div>
      <span class="chapter-cta">${solvedCount > 0 ? copy.home.continueChapterCard : copy.home.openChapter}</span>
    `;

    button.addEventListener("click", () => {
      window.location.href = shared.buildPlayUrl(chapter.code);
    });

    item.append(button);
    elements.chapterList.append(item);
  }
}

function getPrimaryPlayUrl() {
  const requestedChapterCode =
    state.progress.activeChapterCode || state.data.chapters[0]?.code || null;

  return shared.buildPlayUrl(requestedChapterCode);
}

function resetProgress() {
  const confirmed = window.confirm(copy.interface.confirmReset);
  if (!confirmed) {
    return;
  }

  state.progress = { solvedPuzzleIds: [], activeChapterCode: null, activePuzzleId: null };
  shared.saveProgress(state.progress);
  render();
}
