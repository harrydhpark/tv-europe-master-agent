/**
 * ============================================================================
 * AXIS Sales Portal <-> Antigravity Master Agent Live Bridge Client
 * ============================================================================
 * 1. Upgrades Sales Portal #searchInput into a Dual Search + AI Command Bar (Ctrl+K)
 * 2. Renders the Right-Side Slide-Over Drawer (#axisAgentDrawer)
 * 3. Connects to Antigravity Sidecar & Master Agent Bridge (http://localhost:5050)
 * 4. Streams live thinking/tool_calls from transcript.jsonl & displays Task/ deliverables
 * 5. Expands to 3-Column Fullscreen Master Agent Workspace on demand
 */
(function () {
  'use strict';

  const BRIDGE_BASE_URL = window.AXIS_BRIDGE_URL || 'http://localhost:5050';
  let bridgeOnline = false;
  let activeTaskId = null;
  let pollInterval = null;
  let mirrorInterval = null;
  let mirrorAutoPoll = true;
  let lastMarkdownReport = '';
  let lastTaskTrace = null;
  let suppressSearchFilter = false;
  let portalCardsFiltered = false;
  let isImeComposing = false;

  // Detect whether input in #searchInput is a natural-language AI prompt rather than a dashboard card keyword
  function isNaturalLanguagePrompt(text) {
    const t = (text || '').trim();
    if (!t) return false;
    if (/\s/.test(t)) return true;
    if (/\d{1,2}\s*월/.test(t)) return true;
    return /(영국|스위스|독일|프랑스|이탈리아|스페인|폴란드|네덜란드|베네룩스|오스트리아|체코|슬로바키아|헝가리|그리스|포르투갈|루마니아|스웨덴|노르딕|발틱|러시아|유럽|법인|지점|해줘|알려줘|확인|분석|비교|정리|진단|점유율|비중|손익|매출|영업이익|한계이익|추이|현황|보고서|리포트|시뮬레이션|만들어|작성|\?)/.test(t);
  }

  // Restore background Sales Portal dashboard cards WITHOUT mutating native HTMLInputElement.value
  // (Mutating input.value during Korean IME composition cancels the browser's IME buffer and causes jamo separation)
  function restorePortalCardsForPrompt(searchInput) {
    if (!searchInput || !portalCardsFiltered) return;
    portalCardsFiltered = false;
    suppressSearchFilter = true;
    try {
      Object.defineProperty(searchInput, 'value', {
        configurable: true,
        get: () => ''
      });
      searchInput.dispatchEvent(new Event('input', { bubbles: true }));
    } catch (e) {
    } finally {
      try { delete searchInput.value; } catch (e) {}
      suppressSearchFilter = false;
    }
  }
  function renderMarkdown(md) {
    if (!md) return '';
    if (window.marked && typeof window.marked.parse === 'function') {
      return window.marked.parse(md);
    }
    let html = String(md)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // Convert markdown tables
    const lines = html.split('\n');
    const out = [];
    let inTable = false;
    let tableRows = [];

    function flushTable() {
      if (!inTable || tableRows.length === 0) return;
      let t = '<table>';
      tableRows.forEach((row, idx) => {
        const cells = row
          .replace(/^\||\|$/g, '')
          .split('|')
          .map(c => c.trim());
        if (idx === 0) {
          t += '<thead><tr>' + cells.map(c => `<th>${c}</th>`).join('') + '</tr></thead><tbody>';
        } else if (idx === 1 && cells.every(c => /^[:\-]+$/.test(c))) {
          // separator row
        } else {
          t += '<tr>' + cells.map(c => `<td>${c}</td>`).join('') + '</tr>';
        }
      });
      t += '</tbody></table>';
      out.push(t);
      inTable = false;
      tableRows = [];
    }

    for (const line of lines) {
      if (/^\s*\|.+\|\s*$/.test(line)) {
        inTable = true;
        tableRows.push(line.trim());
      } else {
        if (inTable) flushTable();
        if (/^###\s+(.+)/.test(line)) {
          out.push(`<h3>${RegExp.$1}</h3>`);
        } else if (/^##\s+(.+)/.test(line)) {
          out.push(`<h2>${RegExp.$1}</h2>`);
        } else if (/^#\s+(.+)/.test(line)) {
          out.push(`<h2>${RegExp.$1}</h2>`);
        } else if (/^&gt;\s*(.+)/.test(line)) {
          out.push(`<blockquote>${RegExp.$1}</blockquote>`);
        } else if (/^\s*[-*]\s+(.+)/.test(line)) {
          out.push(`<li>${RegExp.$1}</li>`);
        } else if (/^---+$/.test(line.trim())) {
          out.push('<hr/>');
        } else if (line.trim().length === 0) {
          out.push('<br/>');
        } else {
          out.push(`<p>${line}</p>`);
        }
      }
    }
    if (inTable) flushTable();

    return out
      .join('\n')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/`([^`]+)`/g, '<code>$1</code>');
  }

  function injectBridgeStyles() {
    if (document.getElementById('axisPortalBridgeStyles')) return;
    const link = document.createElement('link');
    link.id = 'axisPortalBridgeStyles';
    link.rel = 'stylesheet';
    link.href = `${BRIDGE_BASE_URL}/axis_portal_bridge.css`;
    link.onerror = function () {
      // Fallback relative path if served locally
      link.href = 'axis_portal_bridge.css';
    };
    document.head.appendChild(link);
  }

  function ensureCommandBarAndDrawerDOM() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
      const wrapper = searchInput.closest('.search-box-wrapper');
      if (wrapper && !wrapper.classList.contains('axis-command-bar-enhanced')) {
        wrapper.classList.add('axis-command-bar-enhanced');
        searchInput.placeholder = '대시보드 검색 또는 AXIS Master Agent에게 작업 지시 (Enter / Ctrl+K)...';

        if (!document.getElementById('axisPromptRunBtn')) {
          const actionsDiv = document.createElement('div');
          actionsDiv.className = 'axis-cmd-actions';
          actionsDiv.innerHTML = `
            <span class="axis-kbd-hint" title="단축키 Ctrl+K">Ctrl+K</span>
            <button type="button" id="axisPromptRunBtn" class="axis-cmd-run-btn" title="입력한 프롬프트를 Antigravity AXIS Master Agent로 즉시 전송하여 자율 실행">
              <i class="ri-sparkling-2-fill"></i>
              <span id="axisPromptRunBtnText">AXIS AI 실행</span>
            </button>
            <button type="button" id="axisDrawerToggleBtn" class="axis-drawer-toggle-btn" title="우측 AXIS Master Agent 슬라이드 드로어 열기/닫기">
              <span class="axis-live-dot" id="axisLiveDot"></span>
              <i class="ri-robot-2-line"></i>
              <span id="axisDrawerToggleText">AI 드로어</span>
            </button>
          `;
          wrapper.appendChild(actionsDiv);
        }
      }
    }

    if (!document.getElementById('axisAgentDrawer')) {
      const container = document.createElement('div');
      container.innerHTML = `
        <div class="axis-drawer-backdrop" id="axisDrawerBackdrop"></div>
        <aside class="axis-agent-drawer" id="axisAgentDrawer" aria-label="AXIS Master Agent Workspace Drawer">
          <div class="axis-drawer-header">
            <div class="axis-drawer-title-row">
              <div class="axis-drawer-brand">
                <span class="axis-black-bar"></span>
                <div class="axis-brand-texts">
                  <div class="axis-brand-top">
                    <h3>AXIS Master AI Agent</h3>
                    <span class="axis-bridge-badge" id="axisBridgeStatusBadge">
                      <span class="axis-badge-dot"></span>
                      <span id="axisBridgeStatusText">Antigravity Sidecar 연결 확인중...</span>
                    </span>
                  </div>
                  <p>Sales Portal ↔ Antigravity <code>99. Master Agent</code> 실시간 자율 실행 &amp; 산출물 브릿지</p>
                </div>
              </div>
              <div class="axis-drawer-header-actions">
                <button type="button" class="axis-hdr-btn" id="axisExpandFullscreenBtn" title="3단 전체화면 마스터 에이전트 워크스페이스로 확장">
                  <i class="ri-fullscreen-line"></i>
                  <span>3단 전체화면</span>
                </button>
                <button type="button" class="axis-hdr-close" id="axisDrawerCloseBtn" title="드로어 닫기 (ESC)">
                  <i class="ri-close-line"></i>
                </button>
              </div>
            </div>

            <div class="axis-session-bar">
              <div class="axis-session-select-group">
                <label for="axisConversationSelect"><i class="ri-terminal-box-line"></i> Antigravity 세션:</label>
                <select id="axisConversationSelect" class="axis-conv-select">
                  <option value="">➕ 신규 Antigravity 세션 (Auto / Autonomous)</option>
                </select>
                <button type="button" class="axis-icon-mini-btn" id="axisRefreshSessionsBtn" title="Antigravity 세션 및 Task 목록 새로고침">
                  <i class="ri-refresh-line"></i>
                </button>
              </div>
              <div class="axis-auto-policy-tag" title="데이터 추출·산출물 생성·Task 폴더 아카이빙 전 과정 100% 무인 실행">
                <i class="ri-shield-flash-line"></i> 100% 무인 자율 실행
              </div>
            </div>

            <div class="axis-quick-prompts" id="axisQuickPrompts">
              <button type="button" class="axis-prompt-chip" data-prompt="스위스 법인 26년 누적 세그먼트별(OLED, MRGB, QNED) 및 주요 거래선별 순매출·한계이익률(MP%)·영업이익률(COI%)을 분석하고 산출물 리포트를 생성해줘">
                📊 스위스 세그먼트·거래선별 손익 분석
              </button>
              <button type="button" class="axis-prompt-chip" data-prompt="유럽 주요 법인별 최신 당월 및 누적(YTD) 순매출, 영업이익률(COI%), 유통 재고 주수(WOS) 현황을 종합 진단해줘">
                📦 유럽 법인별 손익·재고(WOS) 종합 진단
              </button>
              <button type="button" class="axis-prompt-chip" data-prompt="독일, 영국, 프랑스, 스위스 OLED TV 시장 점유율(LG vs 삼성 vs 소니) 최근 추이와 전략 시사점을 정리해줘">
                📈 주요국 OLED M/S 경쟁 현황 분석
              </button>
            </div>

            <div class="axis-drawer-tabs" role="tablist">
              <button type="button" class="axis-tab-btn active" data-tab="execution" id="axisTabBtnExecution">
                <i class="ri-flashlight-line"></i> 실시간 실행 &amp; 리포트
              </button>
              <button type="button" class="axis-tab-btn" data-tab="mirror" id="axisTabBtnMirror">
                <i class="ri-radar-line"></i> IDE 트랜스크립트 미러링
              </button>
              <button type="button" class="axis-tab-btn" data-tab="archives" id="axisTabBtnArchives">
                <i class="ri-folder-zip-line"></i> Task 산출물 보관함
              </button>
            </div>
          </div>

          <div class="axis-drawer-body">
            <div class="axis-tab-pane active" id="axisTabExecution">
              <div class="axis-active-prompt-card" id="axisActivePromptCard" style="display:none;">
                <div class="axis-prompt-label"><i class="ri-user-voice-line"></i> 지시한 프롬프트</div>
                <div class="axis-prompt-text" id="axisActivePromptText"></div>
              </div>

              <div class="axis-section-card" id="axisTimelineCard">
                <div class="axis-card-title-row">
                  <div class="axis-card-title"><span class="axis-mini-bar"></span>에이전트 추론 &amp; 도구 실행 타임라인</div>
                  <span class="axis-step-counter" id="axisStepCounter">대기중</span>
                </div>
                <div class="axis-timeline-list" id="axisTimelineList">
                  <div class="axis-empty-state">
                    <i class="ri-sparkling-2-line"></i>
                    <p>상단 커맨드 바(<code>Ctrl+K</code>) 또는 하단 입력창에 업무 지시 프롬프트를 입력하면<br><strong>Antigravity AXIS Master Agent</strong>가 즉시 원천 데이터를 분석하고 산출물을 생성합니다.</p>
                  </div>
                </div>
              </div>

              <div class="axis-section-card" id="axisDeliverablesCard" style="display:none;">
                <div class="axis-card-title-row">
                  <div class="axis-card-title"><span class="axis-mini-bar"></span>자동 생성 및 아카이빙된 산출물 (<code>Task/</code>)</div>
                  <span class="axis-step-counter completed" id="axisDeliverableFolderTag"></span>
                </div>
                <div class="axis-deliverables-grid" id="axisDeliverablesGrid"></div>
              </div>

              <div class="axis-section-card" id="axisReportCard" style="display:none;">
                <div class="axis-card-title-row">
                  <div class="axis-card-title"><span class="axis-mini-bar"></span>AXIS Master Agent 종합 실행 보고서</div>
                  <div class="axis-report-actions">
                    <button type="button" class="axis-icon-mini-btn" id="axisCopyReportBtn" title="마크다운 복사" style="width:auto;padding:0 8px;font-size:0.72rem;">
                      <i class="ri-file-copy-line"></i>&nbsp;복사
                    </button>
                  </div>
                </div>
                <div class="axis-markdown-body" id="axisMarkdownBody"></div>
              </div>
            </div>

            <div class="axis-tab-pane" id="axisTabMirror">
              <div class="axis-section-card">
                <div class="axis-card-title-row">
                  <div class="axis-card-title"><span class="axis-mini-bar"></span>Antigravity <code>transcript.jsonl</code> 실시간 미러링</div>
                  <button type="button" class="axis-icon-mini-btn" id="axisMirrorPollToggleBtn" style="width:auto;padding:0 8px;font-size:0.72rem;">
                    🔄 실시간 동기화 ON
                  </button>
                </div>
                <div class="axis-mirror-stream" id="axisMirrorStream">
                  <div class="axis-empty-state">상단 세션 선택기에서 Antigravity 세션을 선택하면 실시간 실행 로그가 표시됩니다.</div>
                </div>
              </div>
            </div>

            <div class="axis-tab-pane" id="axisTabArchives">
              <div class="axis-section-card">
                <div class="axis-card-title-row">
                  <div class="axis-card-title"><span class="axis-mini-bar"></span><code>99. Master Agent/Task</code> 실행 산출물 아카이브</div>
                  <button type="button" class="axis-icon-mini-btn" id="axisReloadArchivesBtn" style="width:auto;padding:0 8px;font-size:0.72rem;">
                    <i class="ri-refresh-line"></i>&nbsp;새로고침
                  </button>
                </div>
                <div class="axis-archive-list" id="axisArchiveList">
                  <div class="axis-empty-state">Task 아카이브 목록을 불러오는 중입니다...</div>
                </div>
              </div>
            </div>
          </div>

          <div class="axis-drawer-footer">
            <div class="axis-footer-input-wrap">
              <input
                type="text"
                id="axisDrawerPromptInput"
                placeholder="AXIS Master Agent에게 추가 작업 지시 또는 산출물 생성 요청 (Enter)..."
                autocomplete="off"
              />
              <button type="button" id="axisDrawerSendBtn" class="axis-drawer-send-btn">
                <i class="ri-send-plane-fill"></i>
                <span>실행</span>
              </button>
            </div>
          </div>
        </aside>
      `;
      document.body.appendChild(container);
    }
  }

  function openDrawer(tabName) {
    const drawer = document.getElementById('axisAgentDrawer');
    const backdrop = document.getElementById('axisDrawerBackdrop');
    if (drawer) drawer.classList.add('open');
    if (backdrop) backdrop.classList.add('open');
    if (tabName) switchDrawerTab(tabName);
    checkBridgeHealthAndSync();
  }

  function closeDrawer() {
    const drawer = document.getElementById('axisAgentDrawer');
    const backdrop = document.getElementById('axisDrawerBackdrop');
    if (drawer) drawer.classList.remove('open');
    if (backdrop) backdrop.classList.remove('open');
  }

  function switchDrawerTab(tabName) {
    document.querySelectorAll('.axis-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    document.getElementById('axisTabExecution')?.classList.toggle('active', tabName === 'execution');
    document.getElementById('axisTabMirror')?.classList.toggle('active', tabName === 'mirror');
    document.getElementById('axisTabArchives')?.classList.toggle('active', tabName === 'archives');

    if (tabName === 'mirror') loadMirrorTranscript();
    if (tabName === 'archives') loadRecentArchives();
  }

  async function checkBridgeHealthAndSync() {
    const statusText = document.getElementById('axisBridgeStatusText');
    const liveDot = document.getElementById('axisLiveDot');
    try {
      const res = await fetch(`${BRIDGE_BASE_URL}/api/health`, { method: 'GET' });
      if (res.ok) {
        bridgeOnline = true;
        if (statusText) statusText.textContent = 'Antigravity Sidecar Live (5050)';
        if (liveDot) liveDot.classList.remove('offline');
        loadConversationsList();
        loadRecentArchives();
        return true;
      }
    } catch (e) {}
    bridgeOnline = false;
    if (statusText) statusText.textContent = '로컬 브릿지 대기 (5050 서버 확인)';
    if (liveDot) liveDot.classList.add('offline');
    return false;
  }

  async function loadConversationsList() {
    const select = document.getElementById('axisConversationSelect');
    if (!select) return;
    try {
      const res = await fetch(`${BRIDGE_BASE_URL}/api/bridge/conversations?limit=12`);
      if (!res.ok) return;
      const data = await res.json();
      const convs = data.conversations || [];
      const currentVal = select.value;

      let defaultLabel = '➕ 신규 Antigravity 세션 (Auto / Autonomous)';
      if (convs.length > 0) {
        const latest = convs[0];
        select.dataset.latestConvId = latest.conversationId;
        const latestShort = latest.conversationId.slice(0, 8);
        const latestSnippet = (latest.lastPrompt || latest.firstPrompt || '활성 세션').slice(0, 26);
        defaultLabel = `➕ 자동 연결: 최근 활성 세션 [${latestShort}] ${latestSnippet.replace(/</g, '&lt;')}`;
      }

      const options = [`<option value="">${defaultLabel}</option>`];
      convs.forEach(c => {
        const shortId = c.conversationId.slice(0, 8);
        const label = `[${shortId}] ${(c.lastPrompt || c.firstPrompt || '세션').slice(0, 42)} (${c.stepCount} steps)`;
        options.push(`<option value="${c.conversationId}">${label.replace(/</g, '&lt;')}</option>`);
      });
      select.innerHTML = options.join('');
      if (currentVal) select.value = currentVal;

      // Immediately refresh Mirror stream if Mirror tab is active or waiting for session
      const mirrorPane = document.getElementById('axisTabMirror');
      const streamEl = document.getElementById('axisMirrorStream');
      if ((mirrorPane && mirrorPane.classList.contains('active')) ||
          (streamEl && streamEl.textContent.includes('세션을 찾는 중'))) {
        loadMirrorTranscript(true);
      }
    } catch (e) {}
  }

  async function loadMirrorTranscript(skipEnsureList) {
    const streamEl = document.getElementById('axisMirrorStream');
    const select = document.getElementById('axisConversationSelect');
    if (!streamEl) return;

    // Build top section for current Portal Bridge Task Trace (if any prompt was run)
    let taskTraceHtml = '';
    if (lastTaskTrace) {
      const tSteps = (lastTaskTrace.timeline || []).map(s => `
        <div class="axis-step-item ${s.status === 'running' ? 'running' : 'completed'}">
          <span class="axis-step-badge">PORTAL #${s.step || '✓'}</span>
          <div class="axis-step-desc">
            <strong>[${(s.agent || 'AXIS Master Agent').replace(/</g, '&lt;')}]</strong> ${(s.desc || '').replace(/</g, '&lt;')}
          </div>
        </div>
      `).join('');
      taskTraceHtml = `
        <div style="margin-bottom:10px;padding:10px 12px;background:#F0FDFA;border:1px solid #99F6E4;border-radius:8px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
            <span style="font-size:0.76rem;font-weight:700;color:#0F766E;">⚡ 포털 프롬프트 자율 실행 트레이스 (${lastTaskTrace.status === 'completed' ? '완료' : '실행중'})</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#0D9488;">${lastTaskTrace.taskId || ''}</span>
          </div>
          <div style="font-size:0.78rem;color:#0F172A;font-weight:600;margin-bottom:6px;">💬 "${(lastTaskTrace.query || '').replace(/</g, '&lt;')}"</div>
          <div style="display:flex;flex-direction:column;gap:6px;">${tSteps}</div>
        </div>
      `;
    }

    let convId = (select && select.value) || (select && select.dataset.latestConvId) || '';
    if (!convId && !skipEnsureList) {
      const ok = await checkBridgeHealthAndSync();
      if (ok) {
        await loadConversationsList();
        convId = (select && select.value) || (select && select.dataset.latestConvId) || '';
      }
    }

    if (!bridgeOnline) {
      streamEl.innerHTML = taskTraceHtml + `
        <div class="axis-empty-state" style="text-align:left;padding:16px;">
          <div style="font-weight:700;color:#B91C1C;margin-bottom:6px;">⚠️ 로컬 브릿지 데몬(Port 5050) 연결 대기 중</div>
          <p style="font-size:0.8rem;color:#475569;margin:0 0 10px;">
            Sales Portal(<code>file://</code>)에서 Antigravity 로컬 <code>transcript.jsonl</code>을 실시간 미러링하려면 <strong>Port 5050 브릿지 데몬</strong>이 실행 중이어야 합니다.
          </p>
          <div style="display:flex;gap:8px;flex-wrap:wrap;">
            <button type="button" id="axisRetryBridgeBtn" class="axis-cmd-run-btn" style="padding:6px 12px;font-size:0.76rem;">
              🔄 5050 브릿지 즉시 재연결
            </button>
          </div>
        </div>
      `;
      const retryBtn = document.getElementById('axisRetryBridgeBtn');
      if (retryBtn) {
        retryBtn.addEventListener('click', async () => {
          retryBtn.textContent = '연결 확인 중...';
          await checkBridgeHealthAndSync();
          await loadMirrorTranscript(true);
        });
      }
      return;
    }

    if (!convId) {
      streamEl.innerHTML = taskTraceHtml + `<div class="axis-empty-state">표시할 Antigravity 세션이 없습니다.</div>`;
      return;
    }

    try {
      const res = await fetch(`${BRIDGE_BASE_URL}/api/bridge/transcript/${encodeURIComponent(convId)}?maxSteps=35`);
      if (!res.ok) return;
      const data = await res.json();
      const steps = (data.steps || []).filter(s => s.thinking || (s.toolCalls && s.toolCalls.length > 0) || s.content);

      if (steps.length === 0) {
        streamEl.innerHTML = taskTraceHtml + `<div class="axis-empty-state">세션(${convId.slice(0, 8)})의 트랜스크립트가 비어 있습니다.</div>`;
        return;
      }

      const convHeaderHtml = `
        <div style="display:flex;align-items:center;justify-content:space-between;padding:4px 6px 8px;border-bottom:1px solid #E2E8F0;margin-bottom:8px;">
          <span style="font-size:0.75rem;font-weight:700;color:#334155;">🖥️ Antigravity IDE 활성 세션 (<code>${convId.slice(0, 8)}</code>)</span>
          <span style="font-size:0.72rem;color:#64748B;">총 ${data.totalLines || steps.length} 스텝 중 최근 ${Math.min(18, steps.length)}건</span>
        </div>
      `;

      streamEl.innerHTML = taskTraceHtml + convHeaderHtml + steps.slice(-18).map(s => {
        const toolsHtml = (s.toolCalls || []).map(tc =>
          `<div style="margin-top:4px;font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#0D9488;">🔧 [${tc.name}] ${tc.toolAction || tc.toolSummary || ''}</div>`
        ).join('');
        const thinkingHtml = s.thinking
          ? `<div style="font-size:0.76rem;color:#475569;margin-top:4px;">💭 ${s.thinking.replace(/</g, '&lt;').slice(0, 260)}</div>`
          : '';
        const contentHtml = s.content
          ? `<div style="font-size:0.78rem;color:#0F172A;margin-top:4px;font-weight:500;">${s.content.replace(/</g, '&lt;').slice(0, 240)}</div>`
          : '';

        return `
          <div class="axis-step-item ${s.status === 'DONE' ? 'completed' : 'running'}">
            <span class="axis-step-badge">#${s.stepIndex ?? '-'} ${s.type || ''}</span>
            <div class="axis-step-desc">
              ${contentHtml}
              ${thinkingHtml}
              ${toolsHtml}
            </div>
          </div>
        `;
      }).join('');
    } catch (e) {}
  }

  async function loadRecentArchives() {
    const listEl = document.getElementById('axisArchiveList');
    if (!listEl) return;
    try {
      const res = await fetch(`${BRIDGE_BASE_URL}/api/tasks/recent?limit=15`);
      if (!res.ok) return;
      const data = await res.json();
      const tasks = data.tasks || [];
      if (tasks.length === 0) {
        listEl.innerHTML = `<div class="axis-empty-state">아카이빙된 Task 폴더가 없습니다.</div>`;
        return;
      }

      listEl.innerHTML = tasks.map(t => {
        const delivs = (t.deliverables || []).map(d => {
          const icon = d.type === 'excel' ? 'ri-file-excel-2-line'
            : d.type === 'web' ? 'ri-window-line'
            : d.type === 'document' ? 'ri-file-word-2-line'
            : 'ri-markdown-line';
          return `
            <a class="axis-deliverable-item" href="${BRIDGE_BASE_URL}${d.url}" target="_blank" rel="noopener">
              <div class="axis-deliv-left">
                <i class="${icon} axis-deliv-icon"></i>
                <div>
                  <div class="axis-deliv-name">${d.name}</div>
                  <div class="axis-deliv-meta">${(d.sizeBytes / 1024).toFixed(1)} KB</div>
                </div>
              </div>
              <i class="ri-download-2-line" style="color:#64748B;"></i>
            </a>
          `;
        }).join('');

        return `
          <div class="axis-archive-card">
            <div class="axis-archive-card-hdr">
              <span class="axis-archive-folder">📁 ${t.folderName}</span>
              <span class="axis-step-counter completed">${(t.deliverables || []).length}개 산출물</span>
            </div>
            <div class="axis-archive-summary">${(t.summary || t.title || '').replace(/</g, '&lt;')}</div>
            <div class="axis-deliverables-grid">${delivs}</div>
          </div>
        `;
      }).join('');
    } catch (e) {}
  }

  function renderDeliverablesBox(taskArchive, deliverables) {
    const card = document.getElementById('axisDeliverablesCard');
    const grid = document.getElementById('axisDeliverablesGrid');
    const tag = document.getElementById('axisDeliverableFolderTag');
    if (!card || !grid) return;

    const files = (deliverables && deliverables.length > 0)
      ? deliverables
      : (taskArchive && taskArchive.deliverables ? taskArchive.deliverables : []);

    if (!files || files.length === 0) {
      card.style.display = 'none';
      return;
    }

    card.style.display = 'block';
    if (tag && taskArchive) {
      tag.textContent = `Task/${taskArchive.folderName}`;
    }

    grid.innerHTML = files.map(d => {
      const icon = d.type === 'excel' ? 'ri-file-excel-2-line'
        : d.type === 'web' ? 'ri-window-line'
        : d.type === 'document' ? 'ri-file-word-2-line'
        : 'ri-file-text-line';
      return `
        <a class="axis-deliverable-item" href="${BRIDGE_BASE_URL}${d.url}" target="_blank" rel="noopener">
          <div class="axis-deliv-left">
            <i class="${icon} axis-deliv-icon"></i>
            <div>
              <div class="axis-deliv-name" title="${d.name}">${d.name}</div>
              <div class="axis-deliv-meta">${(d.sizeBytes / 1024).toFixed(1)} KB · 클릭하여 열기/다운로드</div>
            </div>
          </div>
          <i class="ri-external-link-line" style="color:#0D9488;"></i>
        </a>
      `;
    }).join('');
  }

  async function executeAxisPrompt(rawPrompt) {
    const query = (rawPrompt || '').trim();
    if (!query) {
      openDrawer('execution');
      return;
    }

    const searchInput = document.getElementById('searchInput');
    if (searchInput && isNaturalLanguagePrompt(query)) {
      restorePortalCardsForPrompt(searchInput);
    }

    openDrawer('execution');

    const promptCard = document.getElementById('axisActivePromptCard');
    const promptText = document.getElementById('axisActivePromptText');
    const timelineList = document.getElementById('axisTimelineList');
    const stepCounter = document.getElementById('axisStepCounter');
    const reportCard = document.getElementById('axisReportCard');
    const markdownBody = document.getElementById('axisMarkdownBody');
    const delivCard = document.getElementById('axisDeliverablesCard');
    const select = document.getElementById('axisConversationSelect');

    if (promptCard && promptText) {
      promptCard.style.display = 'block';
      promptText.textContent = query;
    }
    if (delivCard) delivCard.style.display = 'none';
    if (reportCard) reportCard.style.display = 'none';

    if (stepCounter) {
      stepCounter.className = 'axis-step-counter running';
      stepCounter.textContent = '실행중 (Step 1/3)';
    }

    lastTaskTrace = {
      taskId: 'pending',
      query,
      status: 'running',
      timeline: [
        { step: 1, agent: 'Antigravity Sidecar & AXIS Master Agent', status: 'running', desc: '프롬프트를 수신하여 원천 데이터베이스(Parquet / NERP / GfK)를 스캔하고 있습니다...' }
      ]
    };

    if (timelineList) {
      timelineList.innerHTML = `
        <div class="axis-step-item running">
          <span class="axis-step-badge">STEP 1</span>
          <div class="axis-step-desc">
            <strong>Antigravity Sidecar &amp; AXIS Master Agent</strong>에 프롬프트를 전달하고 원천 데이터베이스(Parquet / NERP / GfK)를 스캔하고 있습니다...
          </div>
        </div>
      `;
    }

    const storedApiKey = localStorage.getItem('gemini_api_key') || localStorage.getItem('GEMINI_API_KEY') || '';
    const conversationId = select ? select.value : '';

    try {
      const res = await fetch(`${BRIDGE_BASE_URL}/api/bridge/task`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          apiKey: storedApiKey || undefined,
          conversationId: conversationId || undefined,
          executionMode: 'autonomous',
          source: 'sales_portal'
        })
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      activeTaskId = data.taskId;
      if (lastTaskTrace) lastTaskTrace.taskId = activeTaskId;

      if (pollInterval) clearInterval(pollInterval);
      pollInterval = setInterval(() => pollTaskStatus(activeTaskId), 900);
    } catch (err) {
      if (lastTaskTrace) {
        lastTaskTrace.status = 'offline';
        lastTaskTrace.timeline = [
          { step: '!', agent: 'Port 5050 Bridge Daemon', status: 'running', desc: '로컬 브릿지 서버(http://localhost:5050) 연결 대기 중입니다.' }
        ];
      }
      if (stepCounter) {
        stepCounter.className = 'axis-step-counter';
        stepCounter.textContent = '연결 안내';
      }
      if (timelineList) {
        timelineList.innerHTML = `
          <div class="axis-step-item">
            <span class="axis-step-badge">INFO</span>
            <div class="axis-step-desc">
              로컬 Antigravity Bridge 서버(<code>http://localhost:5050</code>)에 연결할 수 없습니다.<br>
              우측 상단 <strong>[3단 전체화면]</strong> 버튼을 누르면 클라우드/로컬 Master AI Agent 워크스페이스로 즉시 전환됩니다.
            </div>
          </div>
        `;
      }
    }
  }

  async function pollTaskStatus(taskId) {
    if (!taskId) return;
    const timelineList = document.getElementById('axisTimelineList');
    const stepCounter = document.getElementById('axisStepCounter');
    const reportCard = document.getElementById('axisReportCard');
    const markdownBody = document.getElementById('axisMarkdownBody');
    const select = document.getElementById('axisConversationSelect');

    try {
      const res = await fetch(`${BRIDGE_BASE_URL}/api/bridge/status/${encodeURIComponent(taskId)}`);
      if (!res.ok) return;
      const data = await res.json();

      if (data.status === 'running' && data.progress) {
        const p = data.progress;
        if (lastTaskTrace) {
          lastTaskTrace.status = 'running';
          lastTaskTrace.timeline = [
            ...(p.toolCalls || []).slice(-4).map((tc, i) => ({
              step: i + 1,
              agent: tc.name,
              status: 'completed',
              desc: tc.toolAction || tc.toolSummary || tc.name
            })),
            {
              step: p.step || 1,
              agent: p.currentAgent || 'AXIS Master Agent',
              status: 'running',
              desc: p.desc || '작업 수행 중...'
            }
          ];
        }

        if (stepCounter) {
          stepCounter.className = 'axis-step-counter running';
          stepCounter.textContent = `실행중 (Step ${p.step || 1}/${p.totalSteps || 3})`;
        }
        const toolsHtml = (p.toolCalls || []).slice(-4).map(tc => `
          <div class="axis-step-item completed">
            <span class="axis-step-badge">${tc.name}</span>
            <div class="axis-step-desc">${tc.toolAction || tc.toolSummary || tc.name}</div>
          </div>
        `).join('');

        if (timelineList) {
          timelineList.innerHTML = `
            ${toolsHtml}
            <div class="axis-step-item running">
              <span class="axis-step-badge">STEP ${p.step || 1}</span>
              <div class="axis-step-desc">
                <strong>[${p.currentAgent || 'AXIS Master Agent'}]</strong> ${p.desc || '작업 수행 중...'}
              </div>
            </div>
          `;
        }
      } else if (data.status === 'completed' && data.result) {
        clearInterval(pollInterval);
        pollInterval = null;

        const r = data.result;
        if (r.conversationId && select && !select.dataset.latestConvId) {
          select.dataset.latestConvId = r.conversationId;
        }
        if (lastTaskTrace) {
          lastTaskTrace.status = 'completed';
          lastTaskTrace.timeline = r.timeline || [];
        }

        if (stepCounter) {
          stepCounter.className = 'axis-step-counter completed';
          stepCounter.textContent = '100% 자율 실행 완료';
        }

        const steps = r.timeline || [];
        if (timelineList) {
          timelineList.innerHTML = steps.map(s => `
            <div class="axis-step-item completed">
              <span class="axis-step-badge">STEP ${s.step || '✓'}</span>
              <div class="axis-step-desc"><strong>[${s.agent || 'Agent'}]</strong> ${s.desc || ''}</div>
            </div>
          `).join('');
        }

        renderDeliverablesBox(r.taskArchive, r.deliverables);

        lastMarkdownReport = r.answerMarkdown || (r.artifact && r.artifact.markdown) || '';
        if (reportCard && markdownBody && lastMarkdownReport) {
          reportCard.style.display = 'block';
          markdownBody.innerHTML = renderMarkdown(lastMarkdownReport);
        }

        loadRecentArchives();
        loadMirrorTranscript(true);
      }
    } catch (e) {}
  }

  function expandToFullscreenMasterAgent() {
    closeDrawer();
    const searchInput = document.getElementById('searchInput');
    const drawerInput = document.getElementById('axisDrawerPromptInput');
    const promptVal = (drawerInput && drawerInput.value.trim()) || (searchInput && searchInput.value.trim()) || '';

    const targetUrl = bridgeOnline
      ? `${BRIDGE_BASE_URL}${promptVal ? `?q=${encodeURIComponent(promptVal)}` : ''}`
      : `https://master-agent-lge.web.app${promptVal ? `?q=${encodeURIComponent(promptVal)}` : ''}`;

    const overlay = document.getElementById('agentViewerOverlay');
    const iframe = document.getElementById('agentIframe');
    const mockContainer = document.getElementById('mockDashboardContainer');
    const viewerTitle = document.getElementById('viewerTitle');
    const viewerCategory = document.getElementById('viewerCategory');
    const externalLink = document.getElementById('viewerExternalLink');

    if (overlay && iframe) {
      if (viewerCategory) viewerCategory.textContent = 'AXIS Orchestrator';
      if (viewerTitle) viewerTitle.textContent = 'AXIS Master AI Agent (3단 통합 워크스페이스)';
      if (externalLink) externalLink.href = targetUrl;
      if (mockContainer) mockContainer.style.display = 'none';
      iframe.style.display = 'block';
      iframe.src = targetUrl;
      overlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    } else {
      window.open(targetUrl, '_blank');
    }
  }

  function bindEvents() {
    const searchInput = document.getElementById('searchInput');
    const runBtn = document.getElementById('axisPromptRunBtn');
    const toggleBtn = document.getElementById('axisDrawerToggleBtn');
    const closeBtn = document.getElementById('axisDrawerCloseBtn');
    const backdrop = document.getElementById('axisDrawerBackdrop');
    const expandBtn = document.getElementById('axisExpandFullscreenBtn');
    const drawerInput = document.getElementById('axisDrawerPromptInput');
    const drawerSendBtn = document.getElementById('axisDrawerSendBtn');
    const refreshBtn = document.getElementById('axisRefreshSessionsBtn');
    const reloadArchivesBtn = document.getElementById('axisReloadArchivesBtn');
    const copyReportBtn = document.getElementById('axisCopyReportBtn');
    const mirrorToggleBtn = document.getElementById('axisMirrorPollToggleBtn');
    const convSelect = document.getElementById('axisConversationSelect');

    // Prevent Sales Portal card filter from hiding all cards when typing a natural-language AI prompt
    // while strictly preserving Korean IME composition (never mutating input.value or firing synthetic events during composition)
    if (searchInput) {
      searchInput.addEventListener('compositionstart', () => {
        isImeComposing = true;
      });
      searchInput.addEventListener('compositionend', () => {
        isImeComposing = false;
        if (isNaturalLanguagePrompt(searchInput.value) && portalCardsFiltered) {
          restorePortalCardsForPrompt(searchInput);
        }
      });

      document.addEventListener('input', (e) => {
        if (e.target !== searchInput || suppressSearchFilter) return;
        if (isNaturalLanguagePrompt(searchInput.value)) {
          e.stopImmediatePropagation();
          e.stopPropagation();
          if (!e.isComposing && !isImeComposing && portalCardsFiltered) {
            restorePortalCardsForPrompt(searchInput);
          }
        } else {
          portalCardsFiltered = searchInput.value.trim().length > 0;
        }
      }, true);
    }

    if (runBtn && searchInput) {
      runBtn.addEventListener('click', () => {
        executeAxisPrompt(searchInput.value);
      });
    }

    if (searchInput) {
      searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.isComposing && !isImeComposing && e.keyCode !== 229 && searchInput.value.trim().length > 0) {
          e.preventDefault();
          executeAxisPrompt(searchInput.value);
        }
      });
    }

    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        const drawer = document.getElementById('axisAgentDrawer');
        if (drawer && drawer.classList.contains('open')) closeDrawer();
        else openDrawer();
      });
    }

    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    if (backdrop) backdrop.addEventListener('click', closeDrawer);
    if (expandBtn) expandBtn.addEventListener('click', expandToFullscreenMasterAgent);

    if (drawerSendBtn && drawerInput) {
      drawerSendBtn.addEventListener('click', () => {
        const val = drawerInput.value.trim();
        if (val) {
          executeAxisPrompt(val);
          drawerInput.value = '';
        }
      });
      drawerInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.isComposing && e.keyCode !== 229 && drawerInput.value.trim().length > 0) {
          e.preventDefault();
          executeAxisPrompt(drawerInput.value.trim());
          drawerInput.value = '';
        }
      });
    }

    document.querySelectorAll('.axis-prompt-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const prompt = chip.getAttribute('data-prompt');
        if (prompt) executeAxisPrompt(prompt);
      });
    });

    document.querySelectorAll('.axis-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        switchDrawerTab(btn.dataset.tab);
      });
    });

    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => {
        checkBridgeHealthAndSync();
        loadMirrorTranscript();
      });
    }

    if (reloadArchivesBtn) {
      reloadArchivesBtn.addEventListener('click', loadRecentArchives);
    }

    if (convSelect) {
      convSelect.addEventListener('change', () => {
        loadMirrorTranscript();
      });
    }

    if (copyReportBtn) {
      copyReportBtn.addEventListener('click', () => {
        if (lastMarkdownReport && navigator.clipboard) {
          navigator.clipboard.writeText(lastMarkdownReport);
          copyReportBtn.innerHTML = '<i class="ri-check-line"></i>&nbsp;복사됨';
          setTimeout(() => {
            copyReportBtn.innerHTML = '<i class="ri-file-copy-line"></i>&nbsp;복사';
          }, 1500);
        }
      });
    }

    if (mirrorToggleBtn) {
      mirrorToggleBtn.addEventListener('click', () => {
        mirrorAutoPoll = !mirrorAutoPoll;
        mirrorToggleBtn.textContent = mirrorAutoPoll ? '🔄 실시간 동기화 ON' : '⏸️ 동기화 일시정지';
      });
    }

    // Global Keyboard Shortcuts: Ctrl+K to focus Command Bar, ESC to close Drawer
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
      } else if (e.key === 'Escape') {
        const drawer = document.getElementById('axisAgentDrawer');
        if (drawer && drawer.classList.contains('open')) {
          closeDrawer();
        }
      }
    });

    // Periodic Mirror Poll when Mirror tab is active
    if (mirrorInterval) clearInterval(mirrorInterval);
    mirrorInterval = setInterval(() => {
      const drawer = document.getElementById('axisAgentDrawer');
      const mirrorPane = document.getElementById('axisTabMirror');
      if (drawer && drawer.classList.contains('open') && mirrorPane && mirrorPane.classList.contains('active') && mirrorAutoPoll) {
        loadMirrorTranscript();
      }
    }, 2500);
  }

  function init() {
    injectBridgeStyles();
    ensureCommandBarAndDrawerDOM();
    bindEvents();
    checkBridgeHealthAndSync();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
