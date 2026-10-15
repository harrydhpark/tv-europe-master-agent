/**
 * 2027 LG TV & Partner Growth Strategy - Core Application Logic
 * Supporting Hybrid Motion Video, Fullscreen Slideshow, Dual TTS, KO/EN Toggle
 */

// ===================================================================
// 1. Global State
// ===================================================================
let currentSlideIndex = 1;
let totalSlidesCount = 72;
let currentZoomLevel = 1.0;
let isScriptPanelOpen = true;
let isTocOpen = true;
let isPresentationMode = false;
let presentationCurrentSlide = 1;
let isSubtitlesOpen = true; // Live 2-line translucent subtitles enabled by default
let currentSlideSubtitleChunks = [];
let currentSubtitleChunkIndex = 0;
let subtitleTrackerTimer = null;
let subtitleStartTime = 0;
let subtitlePausedAt = 0;
let isSubtitleTrackingActive = false;

// Audio & Web Speech API State
let isSpeaking = false;
let currentSpeechUtterance = null;
const SPEECH_RATES = [0.85, 0.9, 1.0, 1.2];
let currentSpeechRate = parseFloat(localStorage.getItem('lge_prm_speech_rate')) || 0.85;
let currentScriptFontSize = 13.5;
let currentAppLang = 'ko';

// Interactive Dialogue State
let isDialoguePlaying = false;
let currentDialogueTurnIndex = 0;
let dialogueTimeoutId = null;

// Video-First Sequencing State (Slides 11, 12, etc.)
let isVideoFirstPlaying = false;
let activeVideoFirstEl = null;
let activeVideoFirstHandler = null;
let currentSpeakingSlideIndex = null;

// Split Narration Sequencing State (Slide 33: Intro Narration -> Video Sound Demo -> Follow-up Narration)
let splitNarrationPhase = 0; // 0: idle, 1: intro speech, 2: video sound demo, 3: follow-up speech
let activeSplitVideoEl = null;
let activeSplitVideoHandler = null;

function cleanupSplitNarration() {
  splitNarrationPhase = 0;
  if (activeSplitVideoEl && activeSplitVideoHandler) {
    activeSplitVideoEl.removeEventListener('ended', activeSplitVideoHandler);
    activeSplitVideoHandler = null;
  }
  activeSplitVideoEl = null;
}

// Programmatic slide transition & Auto-play flags
let isProgrammaticScrolling = false;
let programmaticScrollTimer = null;
let autoPlaySpeechTimer = null;
let presentationAutoPlayTimer = null;

function cleanupVideoFirst() {
  isVideoFirstPlaying = false;
  if (activeVideoFirstEl && activeVideoFirstHandler) {
    activeVideoFirstEl.removeEventListener('ended', activeVideoFirstHandler);
    activeVideoFirstHandler = null;
  }
  activeVideoFirstEl = null;
}

// Multilingual Dictionary
const I18N_DICT = {
  ko: {
    portalBack: "← 포털로 돌아가기",
    docTitle: "2027 LG TV & Partner Growth Strategy",
    prevBtn: "◀ 이전",
    nextBtn: "다음 ▶",
    tocToggle: "목차",
    panelToggle: "발표 설명창",
    modeToggle: "슬라이드쇼 모드",
    tabToc: "대목차 (TOC)",
    tabThumbs: "슬라이드",
    tocHeader: "3-PART AGENDA STRUCTURE",
    collapseAll: "전체 펼침/접힘",
    scriptPanelTitle: "슬라이드 발표 스크립트",
    ttsPlay: "음성 듣기",
    ttsStop: "음성 정지",
    ttsPlaying: "음성 재생 중...",
    ttsPaused: "일시 정지됨",
    ttsResume: "이어듣기",
    ttsSlideAudio: "음성 듣기 (A)",
    ttsSlidePause: "일시정지 (A)",
    ttsSlideResume: "이어듣기 (A)",
    speedToast: "나레이션 속도: ",
    copyBtn: "📋 복사",
    copiedToast: "📋 영문 발표 스크립트가 클립보드에 복사되었습니다.",
    speechLabel: "ENGLISH PRESENTATION SCRIPT",
    speechSubtag: "원문 발표 스피치",
    koGuideLabel: "국문 발표 대본 (스피치 가이드)",
    zoomReset: "화면 크기 맞춤",
    overlayNotes: "자막",
    overlayExit: "✕ 나가기 (ESC)",
    motionPlay: "모션 재생",
    motionPause: "모션 일시정지",
    motionReplay: "모션 다시보기"
  },
  en: {
    portalBack: "← Back to Portal",
    docTitle: "2027 LG TV & Partner Growth Strategy",
    prevBtn: "◀ Prev",
    nextBtn: "Next ▶",
    tocToggle: "Contents",
    panelToggle: "Presenter Script",
    modeToggle: "Slideshow",
    tabToc: "TOC",
    tabThumbs: "Slides",
    tocHeader: "3-PART AGENDA STRUCTURE",
    collapseAll: "Expand/Collapse All",
    scriptPanelTitle: "Slide Presentation Script",
    ttsPlay: "Play Audio",
    ttsStop: "Stop Audio",
    ttsPlaying: "Playing Speech Audio...",
    ttsPaused: "Playback Paused",
    ttsResume: "Resume",
    ttsSlideAudio: "Listen (A)",
    ttsSlidePause: "Pause (A)",
    ttsSlideResume: "Resume (A)",
    speedToast: "Narration Speed: ",
    copyBtn: "📋 Copy",
    copiedToast: "📋 English speech script copied to clipboard.",
    speechLabel: "ENGLISH PRESENTATION SCRIPT",
    speechSubtag: "Original Speech",
    koGuideLabel: "Korean Guide & Partner Notes",
    zoomReset: "Fit to Screen",
    overlayNotes: "Subtitles",
    overlayExit: "✕ Exit (ESC)",
    motionPlay: "Play Motion",
    motionPause: "Pause Motion",
    motionReplay: "Replay Motion"
  }
};

// ===================================================================
// 2. Lifecycle & Initialization
// ===================================================================
document.addEventListener('DOMContentLoaded', () => {
  initIframeMode();
  initPresentationData();
  initSpeechRate();
  initLanguage();
  setupEventListeners();
});

function initIframeMode() {
  try {
    if (window.self !== window.top || window.location.search.includes('embedded=true') || window.location.search.includes('auth_token=')) {
      document.documentElement.classList.add('in-iframe');
    }
  } catch (e) {
    document.documentElement.classList.add('in-iframe');
  }
}

function initPresentationData() {
  if (typeof presentationData === 'undefined' || !presentationData.slides) {
    console.warn('presentationData is not loaded yet.');
    return;
  }
  totalSlidesCount = presentationData.slides.length;

  const headerTotal = document.getElementById('header-total-count');
  const headerInput = document.getElementById('header-page-input');
  const overlayTotal = document.getElementById('overlay-total-num');
  const overlayScrubber = document.getElementById('overlay-scrubber');

  if (headerTotal) headerTotal.textContent = totalSlidesCount;
  if (headerInput) headerInput.max = totalSlidesCount;
  if (overlayTotal) overlayTotal.textContent = totalSlidesCount;
  if (overlayScrubber) overlayScrubber.max = totalSlidesCount;

  renderTOC();
  renderThumbs();
  renderSlideCards();
  renderScriptPanel(1);
  setupScrollSpy();
}

// ===================================================================
// 3. Multilingual Engine
// ===================================================================
function initLanguage() {
  const urlParams = new URLSearchParams(window.location.search);
  const paramLang = urlParams.get('lang');
  const savedLang = localStorage.getItem('lge_prm_lang_2027');
  const initialLang = (paramLang && (paramLang === 'en' || paramLang === 'ko')) ? paramLang : (savedLang || 'ko');
  setAppLanguage(initialLang, false);
}

function setAppLanguage(lang, persist = true) {
  currentAppLang = lang;
  if (persist) localStorage.setItem('lge_prm_lang_2027', lang);

  document.documentElement.setAttribute('data-lang', lang);
  const btnKo = document.getElementById('btnLangKo');
  const btnEn = document.getElementById('btnLangEn');
  if (btnKo) btnKo.classList.toggle('active', lang === 'ko');
  if (btnEn) btnEn.classList.toggle('active', lang === 'en');

  const t = I18N_DICT[lang] || I18N_DICT.ko;

  const docTitle = document.getElementById('doc-title');
  if (docTitle) docTitle.textContent = t.docTitle;

  const prevBtnText = document.getElementById('prev-btn-text');
  if (prevBtnText) prevBtnText.textContent = t.prevBtn;

  const nextBtnText = document.getElementById('next-btn-text');
  if (nextBtnText) nextBtnText.textContent = t.nextBtn;

  const tocToggleText = document.getElementById('toc-toggle-text');
  if (tocToggleText) tocToggleText.textContent = t.tocToggle;

  const panelToggleText = document.getElementById('panel-toggle-text');
  if (panelToggleText) panelToggleText.textContent = t.panelToggle;

  const modeToggleText = document.getElementById('mode-toggle-text');
  if (modeToggleText) modeToggleText.textContent = t.modeToggle;

  const tabTocText = document.getElementById('tab-toc-text');
  if (tabTocText) tabTocText.textContent = t.tabToc;

  const tabThumbsText = document.getElementById('tab-thumbs-text');
  if (tabThumbsText) tabThumbsText.textContent = t.tabThumbs;

  const scriptPanelTitle = document.getElementById('script-panel-header-title');
  if (scriptPanelTitle) scriptPanelTitle.textContent = t.scriptPanelTitle;

  const copyBtnText = document.getElementById('btn-copy-text');
  if (copyBtnText) copyBtnText.textContent = t.copyBtn;

  const labelGuideKo = document.getElementById('label-guide-ko');
  if (labelGuideKo) labelGuideKo.textContent = t.koGuideLabel;

  const overlayNotesLabel = document.getElementById('overlay-subtitles-label') || document.getElementById('overlay-notes-label');
  if (overlayNotesLabel) overlayNotesLabel.textContent = t.overlayNotes;

  const overlayExitBtn = document.getElementById('btn-overlay-close');
  if (overlayExitBtn) overlayExitBtn.textContent = t.overlayExit;

  const overlayPrevBtn = document.getElementById('overlay-prev-btn');
  if (overlayPrevBtn) overlayPrevBtn.textContent = t.prevBtn;

  const overlayNextBtn = document.getElementById('overlay-next-btn');
  if (overlayNextBtn) overlayNextBtn.textContent = t.nextBtn;

  const replayBtn = document.getElementById('btn-overlay-video-replay');
  if (replayBtn) replayBtn.textContent = '🔄 ' + t.motionReplay;

  renderTOC();
  renderScriptPanel(currentSlideIndex);

  const isCurrentlySpeaking = ('speechSynthesis' in window) && window.speechSynthesis.speaking;
  const isCurrentlyPaused = ('speechSynthesis' in window) && window.speechSynthesis.paused;
  updateTtsUi(isCurrentlySpeaking && !isCurrentlyPaused, isCurrentlyPaused);

  if (isPresentationMode && presentationData && presentationData.slides) {
    const slide = presentationData.slides.find(s => s.index === presentationCurrentSlide);
    if (slide && currentSlideSubtitleChunks[currentSubtitleChunkIndex]) {
      updateSubtitleDisplay(currentSlideSubtitleChunks[currentSubtitleChunkIndex].text);
    }
  }
}

// ===================================================================
// 4. Slide Rendering & Motion Video Engine
// ===================================================================
function renderSlideCards() {
  const stack = document.getElementById('slides-card-stack');
  if (!stack || !presentationData) return;

  const t = I18N_DICT[currentAppLang] || I18N_DICT.ko;

  stack.innerHTML = presentationData.slides.map(slide => `
    <div class="slide-card ${slide.index === 1 ? 'active-slide' : ''}" id="slide-card-${slide.index}" data-slide-index="${slide.index}">
      <div class="slide-card-header">
        <div class="card-header-left">
          <span class="card-num-badge">SLIDE ${String(slide.index).padStart(2, '0')}</span>
          ${slide.origPptLabel ? `<span class="card-ppt-ref" title="원문 파워포인트 슬라이드 번호">[원문 ${slide.origPptLabel}]</span>` : ''}
          <span class="card-title">${escapeHtml(slide.title)}</span>
        </div>
        ${slide.hasVideo ? `
          <button class="btn-card-motion" onclick="toggleCardMotion(${slide.index})" id="btn-motion-${slide.index}" title="애니메이션 모션 비디오 재생">
            <span class="motion-icon" id="motion-icon-${slide.index}">▶</span>
            <span class="motion-text" id="motion-text-${slide.index}">${t.motionPlay}</span>
          </button>
        ` : ''}
      </div>
      <div class="slide-card-body" id="slide-card-body-${slide.index}">
        <img src="slides/${slide.image}" alt="${escapeHtml(slide.title)}" id="slide-img-${slide.index}" loading="lazy">
        ${slide.hasVideo ? `
          <video class="slide-card-video" id="slide-video-${slide.index}" src="${slide.videoUrl}" playsinline preload="none" onended="onCardVideoEnded(${slide.index})" style="display:none;"></video>
        ` : ''}
        ${slide.isDialogue ? `
          <div class="dialogue-live-overlay" id="dialogue-overlay-${slide.index}" style="display:none;">
            <div class="dialogue-live-pill speaker-ai" id="dialogue-pill-${slide.index}">
              <span class="pill-speaker-badge badge-ai" id="pill-badge-${slide.index}">LG AI</span>
              <span class="pill-text-content" id="pill-text-${slide.index}">Hi Yeni! Looking great today!</span>
            </div>
          </div>
        ` : ''}
      </div>
    </div>
  `).join('');
}

// Handler for when a card's motion video finishes playing (no loop)
function onCardVideoEnded(slideNum) {
  const btnEl = document.getElementById(`btn-motion-${slideNum}`);
  const iconEl = document.getElementById(`motion-icon-${slideNum}`);
  const textEl = document.getElementById(`motion-text-${slideNum}`);
  const t = I18N_DICT[currentAppLang] || I18N_DICT.ko;

  if (btnEl) btnEl.classList.remove('playing');
  if (iconEl) iconEl.textContent = '🔄';
  if (textEl) textEl.textContent = t.motionReplay;
}

// Hybrid Toggle between Static Image and Inline Video
function toggleCardMotion(slideNum, forceState) {
  const imgEl = document.getElementById(`slide-img-${slideNum}`);
  const videoEl = document.getElementById(`slide-video-${slideNum}`);
  const btnEl = document.getElementById(`btn-motion-${slideNum}`);
  const iconEl = document.getElementById(`motion-icon-${slideNum}`);
  const textEl = document.getElementById(`motion-text-${slideNum}`);
  const t = I18N_DICT[currentAppLang] || I18N_DICT.ko;

  if (!videoEl || !imgEl) return;

  if (forceState === true) {
    // Explicit force play (from TTS audio auto-start)
    imgEl.style.display = 'none';
    videoEl.style.display = 'block';
    if (videoEl.ended) {
      videoEl.currentTime = 0;
    }
    videoEl.play().catch(e => console.warn('Autoplay prevented:', e));
    if (btnEl) btnEl.classList.add('playing');
    if (iconEl) iconEl.textContent = '⏸';
    if (textEl) textEl.textContent = t.motionPause;
    return;
  }

  if (forceState === false) {
    // Explicit force pause
    videoEl.pause();
    if (btnEl) btnEl.classList.remove('playing');
    if (iconEl) iconEl.textContent = videoEl.ended ? '🔄' : '▶';
    if (textEl) textEl.textContent = videoEl.ended ? t.motionReplay : t.motionPlay;
    return;
  }

  // User clicked card motion button directly
  if (videoEl.style.display === 'none') {
    imgEl.style.display = 'none';
    videoEl.style.display = 'block';
    if (videoEl.ended) {
      videoEl.currentTime = 0;
    }
    videoEl.play().catch(e => console.warn('Autoplay prevented:', e));
    if (btnEl) btnEl.classList.add('playing');
    if (iconEl) iconEl.textContent = '⏸';
    if (textEl) textEl.textContent = t.motionPause;
  } else {
    if (videoEl.ended) {
      videoEl.currentTime = 0;
      videoEl.play().catch(e => console.warn('Autoplay prevented:', e));
      if (btnEl) btnEl.classList.add('playing');
      if (iconEl) iconEl.textContent = '⏸';
      if (textEl) textEl.textContent = t.motionPause;
    } else if (videoEl.paused) {
      videoEl.play();
      if (btnEl) btnEl.classList.add('playing');
      if (iconEl) iconEl.textContent = '⏸';
      if (textEl) textEl.textContent = t.motionPause;
    } else {
      videoEl.pause();
      if (btnEl) btnEl.classList.remove('playing');
      if (iconEl) iconEl.textContent = '▶';
      if (textEl) textEl.textContent = t.motionPlay;
    }
  }
}

function renderTOC() {
  const tree = document.getElementById('toc-tree');
  if (!tree || !presentationData) return;

  tree.innerHTML = presentationData.sections.map(sec => `
    <div class="toc-section-group" id="toc-sec-${sec.id}">
      <div class="toc-section-title" onclick="toggleTocGroup('${sec.id}')">
        <span>${escapeHtml(sec.title)}</span>
        <span class="toc-section-icon">▾</span>
      </div>
      <div class="toc-slide-list">
        ${sec.slideIndices.map(num => {
          const s = presentationData.slides.find(sl => sl.index === num);
          if (!s) return '';
          return `
            <a href="#slide-card-${s.index}" class="toc-item ${s.index === currentSlideIndex ? 'active' : ''}" onclick="onTocItemClick(event, ${s.index})">
              <span class="toc-item-num">${s.index}</span>
              <span class="toc-item-title">${escapeHtml(s.title)}</span>
              ${s.origPptLabel ? `<span class="toc-ppt-tag" title="원문 PPT 슬라이드 번호">${s.origPptLabel}</span>` : ''}
              ${s.hasVideo ? `<span class="toc-motion-indicator" title="모션 애니메이션 탑재">🎬</span>` : ''}
            </a>
          `;
        }).join('')}
      </div>
    </div>
  `).join('');
}

function renderThumbs() {
  const grid = document.getElementById('thumbs-grid');
  if (!grid || !presentationData) return;

  grid.innerHTML = presentationData.slides.map(s => `
    <div class="thumb-card ${s.index === 1 ? 'active' : ''}" id="thumb-${s.index}" onclick="scrollToSlide(${s.index}, true)">
      <img src="slides/${s.image}" alt="Slide ${s.index}" loading="lazy">
      ${s.hasVideo ? `<span class="thumb-motion-badge">MOTION</span>` : ''}
      <div class="thumb-label">${s.index}. ${escapeHtml(s.title)}${s.origPptLabel ? ` <span style="font-size:9px; color:#94A3B8; font-weight:normal;">(${s.origPptLabel})</span>` : ''}</div>
    </div>
  `).join('');
}

function toggleTocGroup(secId) {
  const grp = document.getElementById(`toc-sec-${secId}`);
  if (grp) grp.classList.toggle('collapsed');
}

function toggleAllTocSections() {
  const groups = document.querySelectorAll('.toc-section-group');
  const anyCollapsed = Array.from(groups).some(g => g.classList.contains('collapsed'));
  groups.forEach(g => g.classList.toggle('collapsed', !anyCollapsed));
}

function switchSidebarTab(tabName) {
  const tabToc = document.getElementById('tab-toc');
  const tabThumbs = document.getElementById('tab-thumbs');
  const contentToc = document.getElementById('content-toc');
  const contentThumbs = document.getElementById('content-thumbs');

  if (tabName === 'toc') {
    tabToc.classList.add('active');
    tabThumbs.classList.remove('active');
    contentToc.classList.add('active');
    contentThumbs.classList.remove('active');
  } else {
    tabToc.classList.remove('active');
    tabThumbs.classList.add('active');
    contentToc.classList.remove('active');
    contentThumbs.classList.add('active');
  }
}

function onTocItemClick(e, slideNum) {
  e.preventDefault();
  scrollToSlide(slideNum, true);
}

function scrollToSlide(slideNum, autoPlay = true) {
  if (slideNum < 1 || slideNum > totalSlidesCount) return;

  // Mark programmatic scroll
  isProgrammaticScrolling = true;
  if (programmaticScrollTimer) clearTimeout(programmaticScrollTimer);
  programmaticScrollTimer = setTimeout(() => {
    isProgrammaticScrolling = false;
  }, 700);

  currentSlideIndex = slideNum;
  onSlideChanged(slideNum);

  // Cancel any pending speech timer from rapid clicks
  if (autoPlaySpeechTimer) clearTimeout(autoPlaySpeechTimer);

  if (autoPlay) {
    // Auto-play speech for the new target slide
    autoPlaySpeechTimer = setTimeout(() => {
      playCurrentSlideSpeech(true);
    }, 120);
  }
}

function goToPrevSlide() {
  if (currentSlideIndex > 1) {
    scrollToSlide(currentSlideIndex - 1, true);
  }
}

function goToNextSlide() {
  if (currentSlideIndex < totalSlidesCount) {
    scrollToSlide(currentSlideIndex + 1, true);
  }
}

function handlePageJump(val) {
  const num = parseInt(val, 10);
  if (num >= 1 && num <= totalSlidesCount) {
    scrollToSlide(num, true);
  } else {
    const input = document.getElementById('header-page-input');
    if (input) input.value = currentSlideIndex;
  }
}

function setupScrollSpy() {
  // In Single Slide Focus View, scroll-spy is not needed as inactive slides are hidden
}

function updateActiveSlideFromScroll() {
  // Single Slide Focus View
  return;
}

function onSlideChanged(slideNum) {
  // Pause any playing card videos on other slides
  document.querySelectorAll('.slide-card-video').forEach(v => {
    if (!v.paused) {
      v.pause();
      v.currentTime = 0;
    }
  });

  const input = document.getElementById('header-page-input');
  if (input) input.value = slideNum;

  const prevBtn = document.getElementById('btn-header-prev');
  const nextBtn = document.getElementById('btn-header-next');
  if (prevBtn) prevBtn.disabled = (slideNum <= 1);
  if (nextBtn) nextBtn.disabled = (slideNum >= totalSlidesCount);

  document.querySelectorAll('.toc-item').forEach(item => {
    const isCurrent = item.getAttribute('href') === `#slide-card-${slideNum}`;
    item.classList.toggle('active', isCurrent);
  });

  document.querySelectorAll('.thumb-card').forEach(th => {
    th.classList.toggle('active', th.id === `thumb-${slideNum}`);
  });

  document.querySelectorAll('.slide-card').forEach(c => {
    c.classList.toggle('active-slide', parseInt(c.dataset.slideIndex, 10) === slideNum);
  });

  const viewport = document.getElementById('slides-viewport');
  if (viewport) {
    viewport.scrollTop = 0;
    viewport.scrollLeft = 0;
  }

  renderScriptPanel(slideNum);
}

// ===================================================================
// 5. Presenter Script Panel & Web Speech API (TTS)
// ===================================================================
function renderScriptPanel(slideNum) {
  if (!presentationData || !presentationData.slides) return;
  const slide = presentationData.slides.find(s => s.index === slideNum);
  if (!slide) return;

  const slideBadge = document.getElementById('script-slide-badge');
  const secBadge = document.getElementById('script-section-badge');
  const motionBadge = document.getElementById('script-motion-badge');
  const titleEl = document.getElementById('script-slide-title');
  const subEl = document.getElementById('script-slide-subtitle');

  const sec = presentationData.sections.find(s => s.slideIndices.includes(slide.index));
  const secTag = sec ? sec.title.split('.')[0] : 'Part';

  if (slideBadge) {
    const origTag = slide.origPptLabel ? ` (${slide.origPptLabel})` : '';
    slideBadge.textContent = `SLIDE ${String(slide.index).padStart(2, '0')} / ${totalSlidesCount}${origTag}`;
  }
  if (secBadge) secBadge.textContent = secTag;
  if (motionBadge) motionBadge.style.display = slide.hasVideo ? 'inline-block' : 'none';
  if (titleEl) titleEl.textContent = slide.title;
  if (subEl) subEl.textContent = slide.subTitle || 'Executive Presentation Strategy';

  // English Speech / Dialogue View
  const enBox = document.getElementById('script-text-en');
  if (enBox) {
    if (slide.isDialogue && slide.dialogueTurns && slide.dialogueTurns.length > 0) {
      enBox.innerHTML = `
        <div class="dialogue-chat-container">
          ${slide.dialogueTurns.map(t => `
            <div class="dialogue-turn-item speaker-${t.speaker}" id="dialogue-turn-${t.turn}">
              <div class="turn-header">
                <div class="turn-speaker-tag tag-${t.speaker}">
                  <span class="active-pulse-indicator" style="display:none;" id="pulse-${t.turn}"></span>
                  <span>${escapeHtml(t.speakerNameEn)}</span>
                </div>
                <span class="turn-num-pill">Turn ${t.turn}/5</span>
              </div>
              <div class="turn-text-en">${escapeHtml(t.textEn)}</div>
            </div>
          `).join('')}
        </div>
      `;
    } else {
      const rawEn = slide.scriptEn || 'No presentation speech provided for this slide.';
      enBox.innerHTML = rawEn
        .split('\n')
        .filter(p => p.trim().length > 0)
        .map(p => `<p>${escapeHtml(p.trim())}</p>`)
        .join('');
    }
  }

  // Korean Guide (Hidden in English Mode)
  const koBoxContainer = document.getElementById('script-ko-box');
  if (koBoxContainer) {
    if (currentAppLang === 'en') {
      koBoxContainer.style.display = 'none';
    } else {
      koBoxContainer.style.display = 'block';
      const koBox = document.getElementById('script-text-ko');
      if (koBox) {
        if (slide.isDialogue && slide.dialogueTurns && slide.dialogueTurns.length > 0) {
          koBox.innerHTML = `
            <div class="dialogue-chat-container">
              ${slide.dialogueTurns.map(t => `
                <div class="dialogue-turn-item speaker-${t.speaker}" id="dialogue-turn-ko-${t.turn}">
                  <div class="turn-header">
                    <div class="turn-speaker-tag tag-${t.speaker}">
                      <span>${escapeHtml(t.speakerNameKo)}</span>
                    </div>
                    <span class="turn-num-pill">턴 ${t.turn}/5</span>
                  </div>
                  <div class="turn-text-ko" style="border-top:none; padding-top:0; margin-top:2px;">${escapeHtml(t.textKo)}</div>
                </div>
              `).join('')}
            </div>
          `;
        } else {
          const rawKo = slide.scriptKo || '해당 슬라이드의 국문 요약 및 파트너 상담 가이드가 준비 중입니다.';
          koBox.innerHTML = rawKo
            .split('\n')
            .filter(p => p.trim().length > 0)
            .map(p => {
              const trimmed = p.trim();
              if (trimmed === '[기능 사운드 시연]') {
                return `<div class="speech-demo-badge" style="display:inline-flex; align-items:center; gap:6px; margin:8px 0; padding:4px 12px; background:rgba(0,180,216,0.12); border:1px solid rgba(0,180,216,0.35); border-radius:16px; color:#00b4d8; font-weight:700; font-size:12px; letter-spacing:0.5px;"><span style="font-size:13px;">🎬</span> ${escapeHtml(trimmed)}</div>`;
              }
              return `<p>${escapeHtml(trimmed)}</p>`;
            })
            .join('');
        }
      }
    }
  }

  stopSpeech();
}

function toggleScriptPanel(forceState) {
  const mainBody = document.getElementById('main-body');
  const toggleBtn = document.getElementById('btn-script-panel-toggle');
  const collapseIcon = document.getElementById('collapse-icon');

  if (typeof forceState === 'boolean') {
    isScriptPanelOpen = forceState;
  } else {
    isScriptPanelOpen = !isScriptPanelOpen;
  }

  if (isScriptPanelOpen) {
    mainBody.classList.remove('script-collapsed');
    if (toggleBtn) toggleBtn.classList.add('active');
    if (collapseIcon) collapseIcon.textContent = '▶';
  } else {
    mainBody.classList.add('script-collapsed');
    if (toggleBtn) toggleBtn.classList.remove('active');
    if (collapseIcon) collapseIcon.textContent = '◀';
    stopSpeech();
  }
}

function toggleTocSidebar(forceState) {
  const mainBody = document.getElementById('main-body');
  const toggleBtn = document.getElementById('btn-toc-toggle');

  if (typeof forceState === 'boolean') {
    isTocOpen = forceState;
  } else {
    isTocOpen = !isTocOpen;
  }

  if (isTocOpen) {
    mainBody.classList.remove('toc-collapsed');
    if (toggleBtn) toggleBtn.classList.add('active');
  } else {
    mainBody.classList.add('toc-collapsed');
    if (toggleBtn) toggleBtn.classList.remove('active');
  }
}

// Web Speech API: Text-to-Speech (TTS)
function playCurrentSlideSpeech(forceRestart = false) {
  if (!('speechSynthesis' in window)) {
    showToast(currentAppLang === 'en' ? '⚠️ Speech synthesis is not supported in this browser.' : '⚠️ 현재 브라우저가 음성 재생을 지원하지 않습니다.');
    return;
  }

  const overlayVideo = document.getElementById('overlay-slide-video');
  const targetIndex = isPresentationMode ? presentationCurrentSlide : currentSlideIndex;
  const slide = presentationData.slides.find(s => s.index === targetIndex);

  if (!slide) return;

  if (currentSpeakingSlideIndex !== targetIndex) {
    forceRestart = true;
    currentSpeakingSlideIndex = targetIndex;
  }

  // Check if dialogue slide
  if (slide.isDialogue && slide.dialogueTurns && slide.dialogueTurns.length > 0) {
    cleanupVideoFirst();
    cleanupSplitNarration();
    playDialogueSpeech(slide, forceRestart);
    return;
  }

  // Check if split narration slide (Slide 33: Intro Narration -> Video Sound Demo -> Follow-up Narration)
  if (slide.splitNarration || slide.index === 33) {
    cleanupVideoFirst();
    playSplitNarrationSpeech(slide, forceRestart);
    return;
  }

  const isVideoFirst = Boolean(slide.videoFirst || slide.index === 11 || slide.index === 12);

  // Case 1: Video-First Slide (Slides 11 & 12 - Video plays completely before narration)
  if (isVideoFirst && slide.hasVideo) {
    const videoEl = isPresentationMode ? overlayVideo : document.getElementById(`slide-video-${slide.index}`);

    if (isVideoFirstPlaying && !forceRestart) {
      if (videoEl && !videoEl.paused) {
        // Pause preliminary video
        videoEl.pause();
        updateTtsUi(false, true);
        return;
      } else if (videoEl && videoEl.paused && !videoEl.ended) {
        // Resume preliminary video
        videoEl.play().catch(() => {});
        updateTtsUi(true, false);
        return;
      }
    }

    if (isSpeaking && !isVideoFirstPlaying && !forceRestart) {
      // Narration phase has already started; pause/resume TTS
      if (window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
        resumeSubtitleTracking();
        updateTtsUi(true, false);
        return;
      } else {
        window.speechSynthesis.pause();
        pauseSubtitleTracking();
        updateTtsUi(false, true);
        return;
      }
    }

    // Fresh start or forceRestart for Video-First slide
    cleanupVideoFirst();
    window.speechSynthesis.cancel();
    isSpeaking = true;
    isVideoFirstPlaying = true;
    updateTtsUi(true, false);

    if (videoEl) {
      activeVideoFirstEl = videoEl;
      if (!isPresentationMode) {
        toggleCardMotion(slide.index, true);
      }
      if (forceRestart || videoEl.ended || videoEl.paused) {
        videoEl.currentTime = 0;
        videoEl.play().catch(e => console.warn('Video autoplay prevented:', e));
      }

      activeVideoFirstHandler = () => {
        if (!isVideoFirstPlaying) return;
        cleanupVideoFirst();
        // Video finished completely! Now trigger the presenter's speech narration
        startSlideNarration(slide);
      };
      videoEl.addEventListener('ended', activeVideoFirstHandler, { once: true });
    } else {
      startSlideNarration(slide);
    }
    return;
  }

  // Case 2: Normal Slide TTS (non video-first)
  cleanupVideoFirst();

  if (isSpeaking && !forceRestart) {
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
      resumeSubtitleTracking();
      if (isPresentationMode && overlayVideo && !overlayVideo.ended) {
        overlayVideo.play().catch(() => {});
      } else if (!isPresentationMode && slide && slide.hasVideo) {
        toggleCardMotion(slide.index, true);
      }
      updateTtsUi(true, false);
      return;
    } else {
      window.speechSynthesis.pause();
      pauseSubtitleTracking();
      if (isPresentationMode && overlayVideo) {
        overlayVideo.pause();
      } else if (!isPresentationMode && slide && slide.hasVideo) {
        toggleCardMotion(slide.index, false);
      }
      updateTtsUi(false, true);
      return;
    }
  }

  startSlideNarration(slide);
}

function startSlideNarration(slide) {
  if (!slide || !slide.scriptEn) {
    isSpeaking = false;
    isVideoFirstPlaying = false;
    updateTtsUi(false, false);
    stopSubtitleTracking();
    clearSubtitleDisplay(true);
    return;
  }

  window.speechSynthesis.cancel();

  const cleanScript = (slide.scriptEn || '').replace(/\r\n/g, ' ').replace(/[\r\n]+/g, ' ').replace(/\s+/g, ' ').trim();

  // Prepare live 2-line subtitle chunks
  currentSlideSubtitleChunks = prepareSubtitleChunks(cleanScript, currentSpeechRate);
  currentSubtitleChunkIndex = 0;

  const utterance = new SpeechSynthesisUtterance(cleanScript);
  utterance.lang = 'en-US';
  utterance.rate = currentSpeechRate;
  utterance.pitch = 1.0;

  const voices = window.speechSynthesis.getVoices();
  const enVoice = voices.find(v => (v.lang === 'en-US' || v.lang === 'en-GB') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Microsoft') || v.name.includes('Samantha')));
  if (enVoice) utterance.voice = enVoice;

  const isVideoFirst = Boolean(slide.videoFirst || slide.index === 11 || slide.index === 12);
  const overlayVideo = document.getElementById('overlay-slide-video');

  utterance.onstart = () => {
    isSpeaking = true;
    isVideoFirstPlaying = false;
    updateTtsUi(true, false);

    // Start subtitle tracking
    startSubtitleTracking(slide);

    if (!isVideoFirst && slide.hasVideo) {
      if (isPresentationMode && overlayVideo) {
        if (overlayVideo.ended) overlayVideo.currentTime = 0;
        overlayVideo.play().catch(() => {});
      } else if (!isPresentationMode) {
        // Auto-play card motion video along with TTS speech
        toggleCardMotion(slide.index, true);
      }
    }
  };

  utterance.onboundary = (e) => {
    isSubtitleTrackingActive = true;
    if (e.charIndex !== undefined && e.charIndex >= 0) {
      boundaryEventCount++;
      hasValidBoundaryEvents = true;
      lastBoundaryEventTime = performance.now();
    }
    if (isPresentationMode && (e.name === 'word' || !e.name)) {
      const charIdx = e.charIndex;
      let foundIdx = currentSlideSubtitleChunks.findIndex(chunk => charIdx >= chunk.start && charIdx < chunk.end);
      if (foundIdx === -1 && currentSlideSubtitleChunks.length > 0) {
        for (let i = currentSlideSubtitleChunks.length - 1; i >= 0; i--) {
          if (charIdx >= currentSlideSubtitleChunks[i].start) {
            foundIdx = i;
            break;
          }
        }
      }
      if (foundIdx !== -1 && foundIdx !== currentSubtitleChunkIndex) {
        currentSubtitleChunkIndex = foundIdx;
        updateSubtitleDisplay(currentSlideSubtitleChunks[foundIdx].text);
      }
    }
  };

  utterance.onend = () => {
    isSpeaking = false;
    isVideoFirstPlaying = false;
    updateTtsUi(false, false);
    stopSubtitleTracking();
    clearSubtitleDisplay(true);
  };

  utterance.onerror = (e) => {
    console.warn('TTS playback error:', e);
    isSpeaking = false;
    isVideoFirstPlaying = false;
    updateTtsUi(false, false);
    stopSubtitleTracking();
    clearSubtitleDisplay(true);
  };

  currentSpeechUtterance = utterance;
  window.speechSynthesis.speak(utterance);
}

// Interactive Dialogue Speech Engine (AI vs Presenter back-and-forth)
function playDialogueSpeech(slide, forceRestart = false) {
  const overlayVideo = document.getElementById('overlay-slide-video');

  if (isSpeaking && !forceRestart) {
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
      if (isPresentationMode && overlayVideo && !overlayVideo.ended) {
        overlayVideo.play().catch(() => {});
      } else if (!isPresentationMode && slide.hasVideo) {
        toggleCardMotion(slide.index, true);
      }
      updateTtsUi(true, false);
      return;
    } else {
      window.speechSynthesis.pause();
      if (isPresentationMode && overlayVideo) {
        overlayVideo.pause();
      } else if (!isPresentationMode && slide.hasVideo) {
        toggleCardMotion(slide.index, false);
      }
      updateTtsUi(false, true);
      return;
    }
  }

  // Clear any existing dialogue timers and start fresh
  if (dialogueTimeoutId) {
    clearTimeout(dialogueTimeoutId);
    dialogueTimeoutId = null;
  }
  window.speechSynthesis.cancel();

  isSpeaking = true;
  isDialoguePlaying = true;
  currentDialogueTurnIndex = 0;
  updateTtsUi(true, false);

  if (isPresentationMode && overlayVideo && slide.hasVideo) {
    if (overlayVideo.ended) overlayVideo.currentTime = 0;
    overlayVideo.play().catch(() => {});
  } else if (!isPresentationMode && slide.hasVideo) {
    toggleCardMotion(slide.index, true);
  }

  speakNextDialogueTurn(slide);
}

function speakNextDialogueTurn(slide) {
  if (!isDialoguePlaying || !slide || !slide.dialogueTurns) return;

  if (currentDialogueTurnIndex >= slide.dialogueTurns.length) {
    onDialogueFinished(slide);
    return;
  }

  const turn = slide.dialogueTurns[currentDialogueTurnIndex];
  const voices = window.speechSynthesis.getVoices();

  // Voice selection: Natural human for presenter, distinct AI assistant for LG AI
  const presenterVoice = voices.find(v => (v.lang === 'en-US' || v.lang === 'en-GB') && 
    (v.name.includes('David') || v.name.includes('Guy') || v.name.includes('Natural') || v.name.includes('Google US English') || v.name.includes('Samantha'))) ||
    voices.find(v => v.lang.startsWith('en')) || null;

  const aiVoice = voices.find(v => (v.lang === 'en-US' || v.lang === 'en-GB') && 
    v !== presenterVoice &&
    (v.name.includes('Jenny') || v.name.includes('Aria') || v.name.includes('Zira') || v.name.includes('Google UK English Female') || v.name.includes('Victoria') || v.name.includes('Siri'))) ||
    voices.find(v => v.lang.startsWith('en') && v !== presenterVoice) ||
    presenterVoice;

  const utterance = new SpeechSynthesisUtterance(turn.textEn);
  utterance.lang = 'en-US';
  utterance.rate = currentSpeechRate;

  if (turn.speaker === 'ai') {
    if (aiVoice) utterance.voice = aiVoice;
    utterance.pitch = 1.15; // Friendly, clear AI tone
  } else {
    if (presenterVoice) utterance.voice = presenterVoice;
    utterance.pitch = 1.0;  // Standard natural human presenter pitch
  }

  utterance.onstart = () => {
    isSpeaking = true;
    updateTtsUi(true, false);
    updateDialogueVisuals(slide, turn);
  };

  utterance.onend = () => {
    if (!isDialoguePlaying) return;
    currentDialogueTurnIndex++;
    if (currentDialogueTurnIndex < slide.dialogueTurns.length) {
      dialogueTimeoutId = setTimeout(() => {
        speakNextDialogueTurn(slide);
      }, 400); // 0.4s natural breathing space between turns
    } else {
      onDialogueFinished(slide);
    }
  };

  utterance.onerror = (e) => {
    console.warn('Dialogue TTS error:', e);
    if (isDialoguePlaying) {
      currentDialogueTurnIndex++;
      if (currentDialogueTurnIndex < slide.dialogueTurns.length) {
        speakNextDialogueTurn(slide);
      } else {
        onDialogueFinished(slide);
      }
    }
  };

  currentSpeechUtterance = utterance;
  window.speechSynthesis.speak(utterance);
}

function updateDialogueVisuals(slide, turn) {
  // 1. Script panel chat bubble highlights
  document.querySelectorAll('.dialogue-turn-item').forEach(el => {
    el.classList.remove('active-turn');
  });
  document.querySelectorAll('.active-pulse-indicator').forEach(el => {
    el.style.display = 'none';
  });

  const activeTurnItem = document.getElementById(`dialogue-turn-${turn.turn}`);
  if (activeTurnItem) {
    activeTurnItem.classList.add('active-turn');
    const pulse = document.getElementById(`pulse-${turn.turn}`);
    if (pulse) pulse.style.display = 'inline-block';
    activeTurnItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  const activeKoItem = document.getElementById(`dialogue-turn-ko-${turn.turn}`);
  if (activeKoItem) {
    activeKoItem.classList.add('active-turn');
  }

  // 2. Central Slide Live Subtitle Pill
  const pillOverlay = document.getElementById(`dialogue-overlay-${slide.index}`);
  const pill = document.getElementById(`dialogue-pill-${slide.index}`);
  const pillBadge = document.getElementById(`pill-badge-${slide.index}`);
  const pillText = document.getElementById(`pill-text-${slide.index}`);

  if (pillOverlay && pill) {
    if (turn.speaker === 'ai') {
      pillOverlay.style.display = 'flex';
      pill.className = `dialogue-live-pill visible speaker-ai`;
      if (pillBadge) {
        pillBadge.className = `pill-speaker-badge badge-ai`;
        pillBadge.textContent = 'LG AI';
      }
      if (pillText) {
        pillText.textContent = turn.pillCaption || turn.textEn;
      }
    } else {
      // PRESENTER: Hide slide subtitle completely
      pill.classList.remove('visible');
      pillOverlay.style.display = 'none';
    }
  }

  // 3. Fullscreen Overlay Dialogue Pill
  const overlayOverlay = document.getElementById('overlay-dialogue-overlay');
  const overlayPill = document.getElementById('overlay-dialogue-pill');
  const overlayBadge = document.getElementById('overlay-pill-badge');
  const overlayText = document.getElementById('overlay-pill-text');

  const shouldHideSubtitles = Boolean(slide && (slide.hideSubtitles || slide.index === 10));

  if (overlayOverlay && overlayPill) {
    if (isPresentationMode && turn.speaker === 'ai' && !shouldHideSubtitles) {
      overlayOverlay.style.display = 'flex';
      overlayPill.className = `dialogue-live-pill visible speaker-ai`;
      if (overlayBadge) {
        overlayBadge.className = `pill-speaker-badge badge-ai`;
        overlayBadge.textContent = 'LG AI';
      }
      if (overlayText) {
        overlayText.textContent = turn.pillCaption || turn.textEn;
      }
    } else {
      // PRESENTER or non-presentation mode or hidden for slide: Hide fullscreen subtitle
      overlayPill.classList.remove('visible');
      overlayOverlay.style.display = 'none';
    }
  }

  // Sync with live presentation subtitle bar
  if (isPresentationMode && isSubtitlesOpen && !shouldHideSubtitles) {
    const speakerPrefix = turn.speaker === 'ai' ? '[LG AI] ' : '';
    updateSubtitleDisplay(speakerPrefix + (turn.pillCaption || turn.textEn || ''));
  } else if (isPresentationMode && shouldHideSubtitles) {
    clearSubtitleDisplay(true);
  }
}

function onDialogueFinished(slide) {
  isSpeaking = false;
  isDialoguePlaying = false;
  currentDialogueTurnIndex = 0;
  updateTtsUi(false, false);
  clearSubtitleDisplay(true);

  document.querySelectorAll('.active-pulse-indicator').forEach(el => {
    el.style.display = 'none';
  });

  document.querySelectorAll('.dialogue-live-pill').forEach(p => {
    p.classList.remove('visible');
  });
  document.querySelectorAll('.dialogue-live-overlay').forEach(o => {
    o.style.display = 'none';
  });

  const ttsText = document.getElementById('tts-text');
  const t = I18N_DICT[currentAppLang] || I18N_DICT.ko;
  if (ttsText) ttsText.textContent = t.ttsPlay;
}

// ===================================================================
// 5.1 Split Narration Speech Engine (Slide 33: Intro Narration -> Video Sound Demo -> Follow-up Narration)
// ===================================================================
function playSplitNarrationSpeech(slide, forceRestart = false) {
  const overlayVideo = document.getElementById('overlay-slide-video');
  const videoEl = isPresentationMode ? overlayVideo : document.getElementById(`slide-video-${slide.index}`);

  if (isSpeaking && !forceRestart) {
    if (splitNarrationPhase === 1 || splitNarrationPhase === 3) {
      if (window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
        resumeSubtitleTracking();
        updateTtsUi(true, false);
        return;
      } else {
        window.speechSynthesis.pause();
        pauseSubtitleTracking();
        updateTtsUi(false, true);
        return;
      }
    } else if (splitNarrationPhase === 2) {
      if (videoEl && !videoEl.paused) {
        videoEl.pause();
        updateTtsUi(false, true);
        return;
      } else if (videoEl && videoEl.paused && !videoEl.ended) {
        videoEl.play().catch(() => {});
        updateTtsUi(true, false);
        return;
      }
    }
  }

  // Clear previous audio/video and start fresh
  cleanupSplitNarration();
  cleanupVideoFirst();
  window.speechSynthesis.cancel();
  stopSubtitleTracking();
  clearSubtitleDisplay(true);

  if (videoEl) {
    videoEl.pause();
    videoEl.currentTime = 0;
  }

  isSpeaking = true;
  updateTtsUi(true, false);

  startSplitIntroNarration(slide, videoEl);
}

function startSplitIntroNarration(slide, videoEl) {
  splitNarrationPhase = 1;
  const introText = (slide.scriptEnIntro || "AI Karaoke Mode brings a new level of fun to entertainment at home.").replace(/\r\n/g, ' ').replace(/[\r\n]+/g, ' ').replace(/\s+/g, ' ').trim();

  currentSlideSubtitleChunks = prepareSubtitleChunks(introText, currentSpeechRate);
  currentSubtitleChunkIndex = 0;

  // Initialize subtitle tracking immediately so subtitles show without delay
  startSubtitleTracking(slide, false, currentSlideSubtitleChunks);

  const utterance = new SpeechSynthesisUtterance(introText);
  utterance.lang = 'en-US';
  utterance.rate = currentSpeechRate;
  utterance.pitch = 1.0;

  const voices = window.speechSynthesis.getVoices();
  const enVoice = voices.find(v => (v.lang === 'en-US' || v.lang === 'en-GB') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Microsoft') || v.name.includes('Samantha')));
  if (enVoice) utterance.voice = enVoice;

  utterance.onstart = () => {
    if (splitNarrationPhase !== 1) return;
    isSpeaking = true;
    updateTtsUi(true, false);
  };

  utterance.onboundary = (e) => {
    if (splitNarrationPhase === 1 && isPresentationMode && (e.name === 'word' || !e.name)) {
      const charIdx = e.charIndex;
      const foundIdx = currentSlideSubtitleChunks.findIndex(chunk => charIdx >= chunk.start && charIdx < chunk.end);
      if (foundIdx !== -1 && foundIdx !== currentSubtitleChunkIndex) {
        currentSubtitleChunkIndex = foundIdx;
        updateSubtitleDisplay(currentSlideSubtitleChunks[foundIdx].text);
        if (isSubtitleTrackingActive && currentSlideSubtitleChunks[foundIdx]) {
          subtitleStartTime = performance.now() - currentSlideSubtitleChunks[foundIdx].startMs;
        }
      }
    }
  };

  utterance.onend = () => {
    if (splitNarrationPhase !== 1) return;
    // Phase 1 finished! Stop subtitles so the video demo screen is completely unoccluded
    stopSubtitleTracking();
    clearSubtitleDisplay(true);
    startSplitVideoDemo(slide, videoEl);
  };

  utterance.onerror = (e) => {
    console.warn('Split intro speech error:', e);
    if (splitNarrationPhase === 1) {
      stopSubtitleTracking();
      clearSubtitleDisplay(true);
      startSplitVideoDemo(slide, videoEl);
    }
  };

  currentSpeechUtterance = utterance;
  window.speechSynthesis.speak(utterance);
}

function startSplitVideoDemo(slide, videoEl) {
  splitNarrationPhase = 2;
  isSpeaking = true;
  updateTtsUi(true, false);

  const imgEl = isPresentationMode ? document.getElementById('overlay-slide-img') : document.getElementById(`slide-img-${slide.index}`);
  if (imgEl) imgEl.style.display = 'none';

  if (videoEl) {
    activeSplitVideoEl = videoEl;
    videoEl.style.display = 'block';
    if (!isPresentationMode) {
      toggleCardMotion(slide.index, true);
    }
    videoEl.currentTime = 0;
    videoEl.play().catch(e => console.warn('Video demo autoplay prevented:', e));

    activeSplitVideoHandler = () => {
      if (splitNarrationPhase !== 2) return;
      cleanupSplitNarration();
      // Video demo finished! Now proceed to Phase 3: Follow-up narration
      startSplitFollowupNarration(slide);
    };
    videoEl.addEventListener('ended', activeSplitVideoHandler, { once: true });
  } else {
    startSplitFollowupNarration(slide);
  }
}

function startSplitFollowupNarration(slide) {
  splitNarrationPhase = 3;
  const followupText = (slide.scriptEnFollowup || slide.scriptEn || '').replace(/\r\n/g, ' ').replace(/[\r\n]+/g, ' ').replace(/\s+/g, ' ').trim();

  currentSlideSubtitleChunks = prepareSubtitleChunks(followupText, currentSpeechRate);
  currentSubtitleChunkIndex = 0;

  // Initialize subtitle tracking immediately so followup subtitles show without delay
  startSubtitleTracking(slide, false, currentSlideSubtitleChunks);

  const utterance = new SpeechSynthesisUtterance(followupText);
  utterance.lang = 'en-US';
  utterance.rate = currentSpeechRate;
  utterance.pitch = 1.0;

  const voices = window.speechSynthesis.getVoices();
  const enVoice = voices.find(v => (v.lang === 'en-US' || v.lang === 'en-GB') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Microsoft') || v.name.includes('Samantha')));
  if (enVoice) utterance.voice = enVoice;

  utterance.onstart = () => {
    if (splitNarrationPhase !== 3) return;
    isSpeaking = true;
    updateTtsUi(true, false);
  };

  utterance.onboundary = (e) => {
    if (splitNarrationPhase === 3 && isPresentationMode && (e.name === 'word' || !e.name)) {
      const charIdx = e.charIndex;
      const foundIdx = currentSlideSubtitleChunks.findIndex(chunk => charIdx >= chunk.start && charIdx < chunk.end);
      if (foundIdx !== -1 && foundIdx !== currentSubtitleChunkIndex) {
        currentSubtitleChunkIndex = foundIdx;
        updateSubtitleDisplay(currentSlideSubtitleChunks[foundIdx].text);
        if (isSubtitleTrackingActive && currentSlideSubtitleChunks[foundIdx]) {
          subtitleStartTime = performance.now() - currentSlideSubtitleChunks[foundIdx].startMs;
        }
      }
    }
  };

  utterance.onend = () => {
    isSpeaking = false;
    cleanupSplitNarration();
    updateTtsUi(false, false);
    stopSubtitleTracking();
    clearSubtitleDisplay(true);
  };

  utterance.onerror = (e) => {
    console.warn('Split followup speech error:', e);
    isSpeaking = false;
    cleanupSplitNarration();
    updateTtsUi(false, false);
    stopSubtitleTracking();
    clearSubtitleDisplay(true);
  };

  currentSpeechUtterance = utterance;
  window.speechSynthesis.speak(utterance);
}

function stopSpeech() {
  if (autoPlaySpeechTimer) {
    clearTimeout(autoPlaySpeechTimer);
    autoPlaySpeechTimer = null;
  }
  if (presentationAutoPlayTimer) {
    clearTimeout(presentationAutoPlayTimer);
    presentationAutoPlayTimer = null;
  }
  if (dialogueTimeoutId) {
    clearTimeout(dialogueTimeoutId);
    dialogueTimeoutId = null;
  }
  isDialoguePlaying = false;
  currentDialogueTurnIndex = 0;

  cleanupVideoFirst();
  cleanupSplitNarration();
  stopSubtitleTracking();
  clearSubtitleDisplay(true);

  if ('speechSynthesis' in window && (isSpeaking || window.speechSynthesis.speaking)) {
    window.speechSynthesis.cancel();
  }
  isSpeaking = false;
  currentSpeakingSlideIndex = null;
  updateTtsUi(false, false);

  // Reset dialogue highlights
  document.querySelectorAll('.dialogue-turn-item').forEach(el => {
    el.classList.remove('active-turn');
  });
  document.querySelectorAll('.active-pulse-indicator').forEach(el => {
    el.style.display = 'none';
  });

  document.querySelectorAll('.dialogue-live-pill').forEach(p => {
    p.classList.remove('visible');
  });
  document.querySelectorAll('.dialogue-live-overlay').forEach(o => {
    o.style.display = 'none';
  });

  const targetIndex = isPresentationMode ? presentationCurrentSlide : currentSlideIndex;
  const slide = (typeof presentationData !== 'undefined' && presentationData.slides) ? presentationData.slides.find(s => s.index === targetIndex) : null;

  if (isPresentationMode) {
    const overlayVideo = document.getElementById('overlay-slide-video');
    if (overlayVideo) {
      overlayVideo.pause();
      overlayVideo.currentTime = 0;
    }
  } else if (slide && slide.hasVideo) {
    toggleCardMotion(slide.index, false);
  }
}

function updateTtsUi(playing, paused) {
  const playBtn = document.getElementById('btn-tts-play');
  const stopBtn = document.getElementById('btn-tts-stop');
  const ttsIcon = document.getElementById('tts-icon');
  const ttsText = document.getElementById('tts-text');
  const statusEl = document.getElementById('tts-status');

  const overlayTopBtn = document.getElementById('btn-overlay-tts-top');
  const overlayTopIcon = document.getElementById('overlay-tts-icon-top');
  const overlayTopText = document.getElementById('overlay-tts-text-top');
  const overlayTopStop = document.getElementById('btn-overlay-stop-top');

  const overlayBottomBtn = document.getElementById('btn-overlay-tts-bottom');
  const overlayBottomIcon = document.getElementById('overlay-tts-icon-bottom');
  const overlayBottomText = document.getElementById('overlay-tts-text-bottom');
  const overlayBottomStop = document.getElementById('btn-overlay-stop-bottom');

  const drawerTtsBtn = document.getElementById('drawer-tts-btn');
  const t = I18N_DICT[currentAppLang] || I18N_DICT.ko;

  if (playing && !paused) {
    if (playBtn) playBtn.classList.add('playing');
    if (stopBtn) stopBtn.style.display = 'inline-flex';
    if (ttsIcon) ttsIcon.textContent = '⏸';
    if (ttsText) ttsText.textContent = (currentAppLang === 'en' ? 'Pause' : '일시정지');
    if (statusEl) statusEl.textContent = t.ttsPlaying;

    if (overlayTopBtn) overlayTopBtn.classList.add('playing');
    if (overlayTopIcon) overlayTopIcon.textContent = '⏸';
    if (overlayTopText) overlayTopText.textContent = t.ttsSlidePause;
    if (overlayTopStop) overlayTopStop.style.display = 'inline-flex';

    if (overlayBottomBtn) overlayBottomBtn.classList.add('playing');
    if (overlayBottomIcon) overlayBottomIcon.textContent = '⏸';
    if (overlayBottomText) overlayBottomText.textContent = t.ttsSlidePause;
    if (overlayBottomStop) overlayBottomStop.style.display = 'inline-flex';

    if (drawerTtsBtn) {
      drawerTtsBtn.classList.add('playing');
      drawerTtsBtn.textContent = '⏸ ' + t.ttsSlidePause;
    }
  } else if (paused) {
    if (playBtn) playBtn.classList.remove('playing');
    if (stopBtn) stopBtn.style.display = 'inline-flex';
    if (ttsIcon) ttsIcon.textContent = '▶';
    if (ttsText) ttsText.textContent = t.ttsResume;
    if (statusEl) statusEl.textContent = t.ttsPaused;

    if (overlayTopBtn) overlayTopBtn.classList.remove('playing');
    if (overlayTopIcon) overlayTopIcon.textContent = '▶';
    if (overlayTopText) overlayTopText.textContent = t.ttsSlideResume;
    if (overlayTopStop) overlayTopStop.style.display = 'inline-flex';

    if (overlayBottomBtn) overlayBottomBtn.classList.remove('playing');
    if (overlayBottomIcon) overlayBottomIcon.textContent = '▶';
    if (overlayBottomText) overlayBottomText.textContent = t.ttsSlideResume;
    if (overlayBottomStop) overlayBottomStop.style.display = 'inline-flex';

    if (drawerTtsBtn) {
      drawerTtsBtn.classList.remove('playing');
      drawerTtsBtn.textContent = '▶ ' + t.ttsSlideResume;
    }
  } else {
    if (playBtn) playBtn.classList.remove('playing');
    if (stopBtn) stopBtn.style.display = 'none';
    if (ttsIcon) ttsIcon.textContent = '▶';
    if (ttsText) ttsText.textContent = t.ttsPlay;
    if (statusEl) statusEl.textContent = '';

    if (overlayTopBtn) overlayTopBtn.classList.remove('playing');
    if (overlayTopIcon) overlayTopIcon.textContent = '▶';
    if (overlayTopText) overlayTopText.textContent = t.ttsSlideAudio;
    if (overlayTopStop) overlayTopStop.style.display = 'none';

    if (overlayBottomBtn) overlayBottomBtn.classList.remove('playing');
    if (overlayBottomIcon) overlayBottomIcon.textContent = '▶';
    if (overlayBottomText) overlayBottomText.textContent = t.ttsSlideAudio;
    if (overlayBottomStop) overlayBottomStop.style.display = 'none';

    if (drawerTtsBtn) {
      drawerTtsBtn.classList.remove('playing');
      drawerTtsBtn.textContent = '▶ ' + t.ttsSlideAudio;
    }
  }
}

function initSpeechRate() {
  const savedRate = parseFloat(localStorage.getItem('lge_prm_speech_rate'));
  if (savedRate && SPEECH_RATES.includes(savedRate)) {
    currentSpeechRate = savedRate;
  } else {
    currentSpeechRate = 0.85;
  }
  updateSpeedLabels(currentSpeechRate);
}

function updateSpeedLabels(rate) {
  const labelText = rate === 1 ? '1.0x' : `${rate}x`;
  const labelIds = ['speed-label', 'speed-label-top', 'speed-label-bottom', 'speed-label-drawer'];
  labelIds.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = labelText;
  });
}

function cycleSpeechRate() {
  const currentIndex = SPEECH_RATES.indexOf(currentSpeechRate);
  const nextIndex = (currentIndex + 1) % SPEECH_RATES.length;
  currentSpeechRate = SPEECH_RATES[nextIndex];
  localStorage.setItem('lge_prm_speech_rate', currentSpeechRate);
  updateSpeedLabels(currentSpeechRate);

  const t = I18N_DICT[currentAppLang] || I18N_DICT.ko;
  showToast(`${t.speedToast}${currentSpeechRate}x`);

  // If audio is currently speaking, restart current slide speech at new rate immediately
  if (isSpeaking || (window.speechSynthesis && window.speechSynthesis.speaking)) {
    playCurrentSlideSpeech(true);
  }
}

function adjustScriptFontSize(delta) {
  currentScriptFontSize = Math.min(Math.max(11, currentScriptFontSize + delta), 20);
  document.documentElement.style.setProperty('--script-font-size', `${currentScriptFontSize}px`);
  showToast(currentAppLang === 'en' ? `Font Size: ${currentScriptFontSize}px` : `글자 크기: ${currentScriptFontSize}px`);
}

function copyCurrentScript() {
  const slide = presentationData.slides.find(s => s.index === currentSlideIndex);
  if (!slide) return;

  const t = I18N_DICT[currentAppLang] || I18N_DICT.ko;
  const origTag = slide.origPptLabel ? ` [원문 ${slide.origPptLabel}]` : '';
  const copyText = (currentAppLang === 'en')
    ? `[Slide ${slide.index}${origTag}] ${slide.title}\n\n[ENGLISH PRESENTATION SCRIPT]\n${slide.scriptEn || ''}`
    : `[Slide ${slide.index}${origTag}] ${slide.title}\n\n[ENGLISH PRESENTATION SCRIPT]\n${slide.scriptEn || ''}\n\n[국문 발표 대본 (스피치 가이드)]\n${slide.scriptKo || ''}`;

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(copyText).then(() => showToast(t.copiedToast));
  }
}

// ===================================================================
// 6. Presentation Slideshow Mode (with Motion Video Sync)
// ===================================================================
function togglePresentationMode() {
  if (isPresentationMode) {
    exitPresentationMode();
  } else {
    openPresentationAt(currentSlideIndex);
  }
}

function openPresentationAt(slideNum) {
  stopSpeech();
  isPresentationMode = true;
  presentationCurrentSlide = Math.min(Math.max(1, slideNum), totalSlidesCount);

  const overlay = document.getElementById('presentation-overlay');
  if (overlay) overlay.style.display = 'flex';

  const indicator = document.getElementById('overlay-subtitles-indicator');
  const toolBtn = document.getElementById('btn-overlay-subtitles-toggle');
  if (indicator) indicator.textContent = isSubtitlesOpen ? 'ON' : 'OFF';
  if (toolBtn) toolBtn.classList.toggle('active', isSubtitlesOpen);

  renderPresentationSlide();
}

function exitPresentationMode() {
  isPresentationMode = false;
  stopSpeech();

  const overlayVideo = document.getElementById('overlay-slide-video');
  if (overlayVideo) {
    overlayVideo.pause();
    overlayVideo.currentTime = 0;
  }

  const overlay = document.getElementById('presentation-overlay');
  if (overlay) overlay.style.display = 'none';

  clearSubtitleDisplay(true);

  scrollToSlide(presentationCurrentSlide, false);
}

function renderPresentationSlide() {
  const slide = presentationData.slides.find(s => s.index === presentationCurrentSlide);
  if (!slide) return;

  const imgEl = document.getElementById('overlay-slide-img');
  const videoEl = document.getElementById('overlay-slide-video');
  const replayBtn = document.getElementById('btn-overlay-video-replay');
  const titleEl = document.getElementById('overlay-slide-title');
  const currentNumEl = document.getElementById('overlay-current-num');
  const scrubber = document.getElementById('overlay-scrubber');

  const origTag = slide.origPptLabel ? ` (${slide.origPptLabel})` : '';
  if (titleEl) titleEl.textContent = `[${slide.index}/${totalSlidesCount}] ${slide.title}${origTag}`;
  if (currentNumEl) currentNumEl.textContent = slide.index;
  if (scrubber) scrubber.value = slide.index;

  const isSplitNarration = Boolean(slide.splitNarration || slide.index === 33);

  // Handle Motion Video in Slideshow
  if (slide.hasVideo && slide.videoUrl) {
    if (isSplitNarration) {
      // Slide 33: Show slide image with title & graphics during Phase 1 intro narration
      if (imgEl) {
        imgEl.style.display = 'block';
        imgEl.src = `slides/${slide.image}`;
      }
      if (videoEl) {
        videoEl.pause();
        videoEl.style.display = 'none';
        videoEl.src = slide.videoUrl;
        videoEl.currentTime = 0;
      }
    } else {
      if (imgEl) imgEl.style.display = 'none';
      if (videoEl) {
        videoEl.style.display = 'block';
        videoEl.src = slide.videoUrl;
        videoEl.currentTime = 0;
        videoEl.play().catch(e => console.warn('Video autoplay prevented:', e));
      }
    }
    if (replayBtn) replayBtn.style.display = 'block';
  } else {
    if (videoEl) {
      videoEl.pause();
      videoEl.style.display = 'none';
      videoEl.src = '';
    }
    if (imgEl) {
      imgEl.style.display = 'block';
      imgEl.src = `slides/${slide.image}`;
    }
    if (replayBtn) replayBtn.style.display = 'none';
  }

  const overlayDialogue = document.getElementById('overlay-dialogue-overlay');
  if (overlayDialogue) {
    overlayDialogue.style.display = 'none';
    const p = document.getElementById('overlay-dialogue-pill');
    if (p) p.classList.remove('visible');
  }

  // Live 2-line Subtitle Initialization
  stopSubtitleTracking();
  const isHiddenForSlide = Boolean(slide.hideSubtitles || slide.index === 10);
  let scriptForSubtitles = slide.scriptEn || '';
  if (isSplitNarration && slide.scriptEnIntro) {
    scriptForSubtitles = slide.scriptEnIntro;
  }
  const cleanScript = scriptForSubtitles.replace(/\r\n/g, ' ').replace(/[\r\n]+/g, ' ').replace(/\s+/g, ' ').trim();
  currentSlideSubtitleChunks = (cleanScript && !slide.isDialogue && !isHiddenForSlide) ? prepareSubtitleChunks(cleanScript, currentSpeechRate) : [];
  currentSubtitleChunkIndex = 0;

  const isVideoFirst = Boolean(slide.videoFirst || slide.index === 11 || slide.index === 12);
  if (isSubtitlesOpen && currentSlideSubtitleChunks.length > 0 && !isVideoFirst && !isHiddenForSlide) {
    updateSubtitleDisplay(currentSlideSubtitleChunks[0].text);
  } else {
    clearSubtitleDisplay(true);
  }

  // Auto-play speech when entering slide in presentation mode
  if (presentationAutoPlayTimer) clearTimeout(presentationAutoPlayTimer);
  presentationAutoPlayTimer = setTimeout(() => {
    playCurrentSlideSpeech(true);
  }, 100);
}

function replayOverlayVideo() {
  const videoEl = document.getElementById('overlay-slide-video');
  if (videoEl) {
    videoEl.currentTime = 0;
    videoEl.play().catch(() => {});
  }
}

function onOverlayVideoEnded() {
  const replayBtn = document.getElementById('btn-overlay-video-replay');
  if (replayBtn) replayBtn.style.display = 'block';
}

function splitSentenceIntoSubtitleChunks(s, maxLen = 115) {
  const trimmed = s.trim();
  if (!trimmed) return [];
  if (trimmed.length <= maxLen) return [trimmed];

  const parts = [];
  let remaining = trimmed;
  while (remaining.length > maxLen) {
    let breakIdx = -1;
    // Prefer punctuation break: comma, semicolon, colon, dash
    const punctMatch = remaining.slice(25, maxLen + 1).match(/.*([,;:\u2014\u2013\-])\s+/);
    if (punctMatch && punctMatch.index !== undefined) {
      breakIdx = 25 + punctMatch.index + punctMatch[0].length;
    } else {
      // Fallback: word boundary before maxLen
      const spaceIdx = remaining.lastIndexOf(' ', maxLen);
      if (spaceIdx > 25) {
        breakIdx = spaceIdx + 1;
      } else {
        const nextSpace = remaining.indexOf(' ', maxLen);
        breakIdx = nextSpace !== -1 ? nextSpace + 1 : remaining.length;
      }
    }

    // Prevent orphan trailing fragments (< 22 chars when sentence can fit within 135 chars)
    const remainingAfter = remaining.slice(breakIdx).trim();
    if (remainingAfter.length > 0 && remainingAfter.length < 22 && remaining.length <= 135) {
      parts.push(remaining);
      remaining = '';
      break;
    }

    const chunk = remaining.slice(0, breakIdx).trim();
    if (chunk) parts.push(chunk);
    remaining = remainingAfter;
  }
  if (remaining) parts.push(remaining);
  return parts;
}

function prepareSubtitleChunks(text, speechRate = 0.85) {
  if (!text) return [];

  // Normalize newlines, carriage returns, and multiple spaces
  const clean = text.replace(/\r\n/g, ' ').replace(/[\r\n]+/g, ' ').replace(/\s+/g, ' ').trim();

  // Split into sentences using lookbehind for terminal punctuation (. ! ?)
  const rawSentences = clean.split(/(?<=[.!?])\s+/);
  const chunks = [];
  let cursor = 0;

  for (const s of rawSentences) {
    const trimmed = s.trim();
    if (!trimmed) continue;

    const parts = splitSentenceIntoSubtitleChunks(trimmed, 115);
    for (const p of parts) {
      const pStart = clean.indexOf(p, cursor);
      const actualStart = pStart !== -1 ? pStart : cursor;
      const actualEnd = actualStart + p.length;
      cursor = actualEnd;

      chunks.push({
        text: p,
        start: actualStart,
        end: actualEnd
      });
    }
  }

  // Ensure contiguous ranges so no character index falls into a void
  for (let i = 0; i < chunks.length - 1; i++) {
    chunks[i].end = chunks[i + 1].start;
  }
  if (chunks.length > 0) {
    chunks[chunks.length - 1].end = clean.length;
  }

  // Calibrated Speech Engine (155 WPM conversational baseline with character/punctuation weights)
  const rate = Math.max(0.5, speechRate);
  const baseWordMs = 175 / rate;
  const charMs = 34 / rate;
  const commaMs = 110 / rate;
  const periodMs = 240 / rate;
  let accumulatedMs = 0;

  return chunks.map((chunk, idx) => {
    const words = chunk.text.split(/\s+/).filter(Boolean).length;
    const chars = chunk.text.length;
    const commaCount = (chunk.text.match(/[,;—]/g) || []).length;
    const periodCount = (chunk.text.match(/[.!?]/g) || []).length;

    const duration = Math.max(900, Math.round(
      words * baseWordMs +
      chars * charMs +
      commaCount * commaMs +
      periodCount * periodMs
    ));

    const startMs = accumulatedMs;
    const endMs = startMs + duration;
    accumulatedMs = endMs;

    return {
      index: idx,
      text: chunk.text,
      start: chunk.start,
      end: chunk.end,
      startMs,
      endMs,
      durationMs: duration
    };
  });
}

let lastBoundaryEventTime = 0;
let hasValidBoundaryEvents = false;
let boundaryEventCount = 0;

function startSubtitleTracking(slide, forceRestart = false, customChunks = null) {
  stopSubtitleTracking();

  if (!slide || (!slide.scriptEn && !customChunks) || slide.isDialogue || slide.hideSubtitles || slide.index === 10) {
    if (slide && (slide.hideSubtitles || slide.index === 10)) {
      clearSubtitleDisplay(true);
    }
    return;
  }

  if (customChunks && customChunks.length > 0) {
    currentSlideSubtitleChunks = customChunks;
  } else {
    const cleanScript = (slide.scriptEn || '').replace(/\r\n/g, ' ').replace(/[\r\n]+/g, ' ').replace(/\s+/g, ' ').trim();
    currentSlideSubtitleChunks = prepareSubtitleChunks(cleanScript, currentSpeechRate);
  }
  currentSubtitleChunkIndex = 0;

  if (currentSlideSubtitleChunks.length === 0) return;

  if (isPresentationMode && isSubtitlesOpen) {
    updateSubtitleDisplay(currentSlideSubtitleChunks[0].text);
  }

  subtitleStartTime = performance.now();
  lastBoundaryEventTime = 0;
  hasValidBoundaryEvents = false;
  boundaryEventCount = 0;
  isSubtitleTrackingActive = true;

  subtitleTrackerTimer = setInterval(() => {
    if (!isSpeaking || window.speechSynthesis.paused) return;

    const now = performance.now();

    // If onboundary is actively driving subtitles (events received within the last 1200ms),
    // let onboundary maintain 100% authority.
    if (hasValidBoundaryEvents && (now - lastBoundaryEventTime < 1200)) {
      return;
    }

    // High-Precision Hybrid Clock Fallback (runs immediately from t=0 if no boundary events, or takes over if stream paused/ended)
    const elapsed = now - subtitleStartTime;

    let targetIdx = currentSlideSubtitleChunks.findIndex(c => elapsed >= c.startMs && elapsed < c.endMs);
    if (targetIdx === -1) {
      if (elapsed >= currentSlideSubtitleChunks[currentSlideSubtitleChunks.length - 1].endMs) {
        targetIdx = currentSlideSubtitleChunks.length - 1;
      } else {
        for (let i = currentSlideSubtitleChunks.length - 1; i >= 0; i--) {
          if (elapsed >= currentSlideSubtitleChunks[i].startMs) {
            targetIdx = i;
            break;
          }
        }
      }
    }

    if (targetIdx !== -1 && targetIdx !== currentSubtitleChunkIndex) {
      currentSubtitleChunkIndex = targetIdx;
      if (isPresentationMode && isSubtitlesOpen) {
        updateSubtitleDisplay(currentSlideSubtitleChunks[targetIdx].text);
      }
    }
  }, 50);
}

function pauseSubtitleTracking() {
  if (isSubtitleTrackingActive) {
    subtitlePausedAt = performance.now();
  }
}

function resumeSubtitleTracking() {
  if (isSubtitleTrackingActive && subtitlePausedAt > 0) {
    const pauseDuration = performance.now() - subtitlePausedAt;
    subtitleStartTime += pauseDuration;
    subtitlePausedAt = 0;
  }
}

function stopSubtitleTracking() {
  if (subtitleTrackerTimer) {
    clearInterval(subtitleTrackerTimer);
    subtitleTrackerTimer = null;
  }
  isSubtitleTrackingActive = false;
  subtitlePausedAt = 0;
  subtitleStartTime = 0;
}

function updateSubtitleDisplay(text) {
  const bar = document.getElementById('presentation-subtitle-bar');
  const textEl = document.getElementById('subtitle-text');
  if (!bar || !textEl) return;

  const currentSlide = (presentationData && presentationData.slides) ? presentationData.slides.find(s => s.index === presentationCurrentSlide) : null;
  const isHiddenForSlide = Boolean(currentSlide && (currentSlide.hideSubtitles || currentSlide.index === 10));

  if (!isSubtitlesOpen || !text || !text.trim() || isHiddenForSlide || splitNarrationPhase === 2) {
    bar.classList.remove('visible');
    return;
  }

  textEl.textContent = text.trim();
  bar.classList.add('visible');
}

function clearSubtitleDisplay(hideBar = false) {
  const bar = document.getElementById('presentation-subtitle-bar');
  const textEl = document.getElementById('subtitle-text');
  if (textEl) textEl.textContent = '';
  if (bar && hideBar) bar.classList.remove('visible');
}

function togglePresentationSubtitles(forceState) {
  if (typeof forceState === 'boolean') {
    isSubtitlesOpen = forceState;
  } else {
    isSubtitlesOpen = !isSubtitlesOpen;
  }

  const bar = document.getElementById('presentation-subtitle-bar');
  const indicator = document.getElementById('overlay-subtitles-indicator');
  const toolBtn = document.getElementById('btn-overlay-subtitles-toggle');

  if (indicator) indicator.textContent = isSubtitlesOpen ? 'ON' : 'OFF';
  if (toolBtn) toolBtn.classList.toggle('active', isSubtitlesOpen);

  if (isSubtitlesOpen) {
    const currentSlide = (presentationData && presentationData.slides) ? presentationData.slides.find(s => s.index === presentationCurrentSlide) : null;
    const isHiddenForSlide = Boolean(currentSlide && (currentSlide.hideSubtitles || currentSlide.index === 10));
    if (!isHiddenForSlide) {
      if (currentSlideSubtitleChunks && currentSlideSubtitleChunks[currentSubtitleChunkIndex]) {
        updateSubtitleDisplay(currentSlideSubtitleChunks[currentSubtitleChunkIndex].text);
      } else {
        if (bar) bar.classList.add('visible');
      }
    } else {
      if (bar) bar.classList.remove('visible');
    }
  } else {
    if (bar) bar.classList.remove('visible');
  }
}

function prevPresentationSlide() {
  if (presentationCurrentSlide > 1) {
    presentationCurrentSlide--;
    stopSpeech();
    renderPresentationSlide();
  }
}

function nextPresentationSlide() {
  if (presentationCurrentSlide < totalSlidesCount) {
    presentationCurrentSlide++;
    stopSpeech();
    renderPresentationSlide();
  }
}

function onOverlayScrubberChange(val) {
  presentationCurrentSlide = parseInt(val, 10);
  stopSpeech();
  renderPresentationSlide();
}

// ===================================================================
// 7. Global Keyboard Event Listeners
// ===================================================================
function setupEventListeners() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
  }

  window.addEventListener('keydown', (e) => {
    if (document.activeElement && (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA')) {
      if (e.key === 'Escape') document.activeElement.blur();
      return;
    }

    if (isPresentationMode) {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextPresentationSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevPresentationSlide();
      } else if (e.key === 'Home') {
        e.preventDefault();
        presentationCurrentSlide = 1;
        stopSpeech();
        renderPresentationSlide();
      } else if (e.key === 'End') {
        e.preventDefault();
        presentationCurrentSlide = totalSlidesCount;
        stopSpeech();
        renderPresentationSlide();
      } else if (e.key === 'a' || e.key === 'A') {
        e.preventDefault();
        playCurrentSlideSpeech();
      } else if (e.key === 'n' || e.key === 'N') {
        e.preventDefault();
        togglePresentationSubtitles();
      } else if (e.key === 'Escape') {
        e.preventDefault();
        exitPresentationMode();
      }
      return;
    }

    // Normal Viewer Mode
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      goToPrevSlide();
    } else if (e.key === 'ArrowRight' || e.key === 'PageDown') {
      e.preventDefault();
      goToNextSlide();
    } else if (e.key === 'a' || e.key === 'A') {
      e.preventDefault();
      playCurrentSlideSpeech();
    } else if (e.key === 's' || e.key === 'S') {
      e.preventDefault();
      toggleScriptPanel();
    } else if (e.key === 't' || e.key === 'T' || e.key === 'm' || e.key === 'M') {
      e.preventDefault();
      toggleTocSidebar();
    } else if (e.key === 'p' || e.key === 'P') {
      e.preventDefault();
      togglePresentationMode();
    }
  });
}

function adjustZoom(delta) {
  currentZoomLevel = Math.min(Math.max(0.6, currentZoomLevel + delta), 2.0);
  applyZoom();
}

function resetZoom() {
  currentZoomLevel = 1.0;
  applyZoom();
}

function applyZoom() {
  const stack = document.getElementById('slides-card-stack');
  const badge = document.getElementById('zoom-level-badge');
  if (stack) stack.style.transform = `scale(${currentZoomLevel})`;
  if (stack) stack.style.transformOrigin = 'center center';
  if (badge) badge.textContent = `${Math.round(currentZoomLevel * 100)}%`;
}

let toastTimer = null;
function showToast(message) {
  const toast = document.getElementById('app-toast');
  if (!toast) return;
  toast.textContent = message;
  toast.style.display = 'block';
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toast.style.display = 'none'; }, 2400);
}

function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
