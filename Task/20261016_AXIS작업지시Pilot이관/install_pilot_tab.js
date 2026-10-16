const fs = require('fs');
const path = require('path');
const { syncPortalBridgeFiles } = require('./antigravity_sidecar_engine');

const ROOT_DIR = path.resolve(__dirname, '..');
const PORTAL_DIR = path.resolve(ROOT_DIR, '..', '00. TV Europe Sales Management Portal');

// 1. Clean main portal index.html (remove axis_portal_bridge.js / .css from main dashboard search bar)
const syncRes = syncPortalBridgeFiles();
console.log('[InstallPilot] Main portal index.html cleaned:', syncRes);

// 2. Build the Nav Button & Tab 7 Section HTML for AXIS_System_Architecture_Guide.html
const NAV_HTML = `<!-- AXIS_PILOT_NAV_START -->
            <button onclick="showTab('tab-prompt-pilot', this)" id="nav-btn-prompt-pilot" class="sidebar-item w-full flex items-center justify-between px-4 py-3 text-xs font-medium text-slate-300 transition-colors border-t border-slate-800/80 mt-1 pt-3.5">
                <span class="flex items-center space-x-3">
                    <span class="text-teal-400 font-mono font-bold">7.</span>
                    <span class="font-bold text-teal-300">AXIS 작업 지시 프롬프트(Pilot)</span>
                </span>
                <span class="px-1.5 py-0.5 rounded text-[9px] font-mono font-extrabold bg-teal-500/20 text-teal-300 border border-teal-500/40">PILOT</span>
            </button>
            <!-- AXIS_PILOT_NAV_END -->`;

const SECTION_HTML = `<!-- AXIS_PILOT_SECTION_START -->
        <!-- ==================== TAB 7: AXIS PROMPT PILOT ==================== -->
        <section id="tab-prompt-pilot" class="tab-content space-y-6">
            <style>
                .axis-exec-paper {
                    background: #FFFFFF;
                    border: 1px solid #CBD5E1;
                    border-radius: 14px;
                    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
                    overflow: hidden;
                    color: #0F172A;
                    font-family: 'Inter', 'Malgun Gothic', -apple-system, BlinkMacSystemFont, sans-serif;
                }
                .axis-exec-banner {
                    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
                    color: #FFFFFF;
                    padding: 24px 32px;
                    border-bottom: 3px solid #0D9488;
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    gap: 16px;
                    flex-wrap: wrap;
                }
                .axis-exec-meta {
                    background: #F8FAFC;
                    border-bottom: 1px solid #E2E8F0;
                    padding: 12px 32px;
                    font-size: 0.8rem;
                    color: #334155;
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                    align-items: center;
                }
                .axis-exec-body {
                    padding: 28px 32px 36px;
                    line-height: 1.7;
                    font-size: 0.9rem;
                    color: #1E293B;
                }
                .axis-exec-body h2 {
                    font-family: 'IBM Plex Sans', 'Malgun Gothic', sans-serif;
                    font-size: 1.2rem;
                    font-weight: 700;
                    color: #0F172A;
                    background: #F8FAFC;
                    border-left: 5px solid #0F172A;
                    padding: 10px 14px;
                    margin: 18px 0 14px;
                    border-radius: 0 8px 8px 0;
                }
                .axis-exec-body h2:first-child { margin-top: 0; }
                .axis-exec-body h3 {
                    font-family: 'IBM Plex Sans', 'Malgun Gothic', sans-serif;
                    font-size: 1.02rem;
                    font-weight: 700;
                    color: #0F172A;
                    border-left: 4px solid #0D9488;
                    padding-left: 10px;
                    margin: 24px 0 10px;
                }
                .axis-exec-body h4 {
                    font-size: 0.92rem;
                    font-weight: 700;
                    color: #0F172A;
                    margin: 16px 0 8px;
                }
                .axis-exec-body blockquote {
                    margin: 10px 0 18px;
                    padding: 12px 16px;
                    background: #F0FDFA;
                    border-left: 4px solid #0D9488;
                    border-radius: 0 8px 8px 0;
                    color: #134E4A;
                    font-size: 0.84rem;
                }
                .axis-exec-body blockquote p { margin: 0; }
                .axis-exec-body table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 12px 0 20px;
                    font-size: 0.82rem;
                    border: 1px solid #CBD5E1;
                }
                .axis-exec-body th {
                    background: #0F172A;
                    color: #FFFFFF;
                    padding: 9px 11px;
                    text-align: left;
                    font-weight: 700;
                    border: 1px solid #1E293B;
                    white-space: nowrap;
                }
                .axis-exec-body td {
                    padding: 8px 11px;
                    border: 1px solid #E2E8F0;
                    color: #0F172A;
                }
                .axis-exec-body tr:nth-child(even) td { background: #F8FAFC; }
                .axis-exec-body ul {
                    list-style-type: disc;
                    padding-left: 22px;
                    margin: 8px 0 16px;
                }
                .axis-exec-body li { margin-bottom: 6px; }
                .axis-exec-body code {
                    font-family: 'JetBrains Mono', monospace;
                    background: #F1F5F9;
                    color: #0F766E;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-size: 0.78rem;
                }
                .axis-exec-body hr {
                    border: 0;
                    border-top: 1px solid #E2E8F0;
                    margin: 24px 0 14px;
                }
                .axis-pilot-chip {
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    padding: 6px 12px;
                    border-radius: 999px;
                    font-size: 0.75rem;
                    font-weight: 600;
                    background: #F8FAFC;
                    color: #334155;
                    border: 1px solid #CBD5E1;
                    cursor: pointer;
                    transition: all 0.15s ease;
                }
                .axis-pilot-chip:hover {
                    background: #F0FDFA;
                    color: #0F766E;
                    border-color: #14B8A6;
                    transform: translateY(-1px);
                }
                .axis-copy-toast {
                    position: fixed;
                    bottom: 24px;
                    right: 24px;
                    background: #0F172A;
                    color: #5EEAD4;
                    border: 1px solid #14B8A6;
                    padding: 12px 18px;
                    border-radius: 10px;
                    font-size: 0.82rem;
                    font-weight: 700;
                    box-shadow: 0 12px 28px rgba(2, 6, 23, 0.35);
                    z-index: 9999;
                    opacity: 0;
                    pointer-events: none;
                    transition: opacity 0.2s ease;
                }
                .axis-copy-toast.show { opacity: 1; }
            </style>

            <!-- Top Status & Header Banner -->
            <div class="bg-slate-900 text-white rounded-2xl p-6 shadow-md border border-slate-800 relative overflow-hidden">
                <div class="relative z-10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                    <div>
                        <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-teal-500/20 border border-teal-500/40 text-teal-300 text-xs font-mono mb-2">
                            <span>PILOT WORKSPACE</span>
                            <span>•</span>
                            <span>ANTIGRAVITY SIDECAR DIRECT BRIDGE (PORT 5050)</span>
                        </div>
                        <h2 class="text-xl lg:text-2xl font-bold tracking-tight">7. AXIS 작업 지시 프롬프트 (Pilot)</h2>
                        <p class="text-slate-300 text-xs lg:text-sm mt-1">
                            프롬프트 한 줄로 15대 에이전트 원천 데이터베이스(Parquet·NERP·GfK)를 실시간 쿼리하고, <strong>가독성 높은 경영진 보고용 HTML 문서(Executive HTML Document)</strong>로 변환 및 즉시 복사(이메일/워드 서식 유지)할 수 있습니다.
                        </p>
                    </div>
                    <div class="flex flex-wrap items-center gap-2.5 shrink-0">
                        <span id="pilotBridgeStatusBadge" class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold bg-slate-800 text-slate-300 border border-slate-700">
                            <span id="pilotBridgeDot" class="w-2 h-2 rounded-full bg-amber-400"></span>
                            <span id="pilotBridgeStatusText">브릿지 확인 중...</span>
                        </span>
                        <select id="pilotSessionSelect" class="bg-slate-800 text-slate-200 text-xs rounded-lg px-3 py-1.5 border border-slate-700 focus:outline-none focus:border-teal-400" title="연결할 Antigravity 세션 선택">
                            <option value="">✨ 새 자율 실행 세션 (권장)</option>
                        </select>
                        <button type="button" onclick="window.axisPilotRefreshStatus()" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 hover:bg-slate-700 text-teal-300 border border-slate-700 transition">
                            🔄 연결 새로고침
                        </button>
                    </div>
                </div>
            </div>

            <!-- 1. Prompt Command Bar Card -->
            <div class="bg-white rounded-xl p-6 border border-slate-200 shadow-sm space-y-4">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-2">
                        <span class="w-2.5 h-2.5 rounded-full bg-teal-600"></span>
                        <h3 class="text-sm font-bold text-slate-900">AXIS Master Agent 작업 지시 프롬프트 입력</h3>
                    </div>
                    <span class="text-[11px] text-slate-500 font-mono">한글 IME 조합 보호 적용 • Enter 또는 우측 실행 버튼 클릭</span>
                </div>

                <div class="flex flex-col sm:flex-row gap-3">
                    <div class="relative flex-1">
                        <input
                            id="pilotPromptInput"
                            type="text"
                            autocomplete="off"
                            spellcheck="false"
                            placeholder="예: 9월 영국 수익성 분석 보고서 만들어줘 / 스위스 8월 제품군별 점유율 확인해줘"
                            class="w-full px-4 py-3.5 text-sm text-slate-900 bg-slate-50 border-2 border-slate-300 rounded-xl focus:outline-none focus:bg-white focus:border-teal-600 transition font-medium"
                        />
                    </div>
                    <button
                        id="pilotRunBtn"
                        type="button"
                        onclick="window.axisPilotRunPrompt()"
                        class="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-teal-700 text-white font-bold text-sm shadow-sm transition flex items-center justify-center gap-2 shrink-0 cursor-pointer"
                    >
                        <span>✨ AXIS AI 작업 실행</span>
                    </button>
                </div>

                <!-- Recommended One-Click Prompt Chips -->
                <div class="pt-1">
                    <div class="text-[11px] font-bold text-slate-500 mb-2">💡 원클릭 추천 실무 프롬프트 (클릭 시 즉시 실행):</div>
                    <div class="flex flex-wrap gap-2">
                        <button type="button" class="axis-pilot-chip" onclick="window.axisPilotQuickRun('9월 영국 수익성 분석 보고서 만들어줘')">🇬🇧 9월 영국 수익성 분석 보고서 만들어줘</button>
                        <button type="button" class="axis-pilot-chip" onclick="window.axisPilotQuickRun('스위스 8월 제품군별 점유율 확인해줘')">🇨🇭 스위스 8월 제품군별 점유율 확인해줘</button>
                        <button type="button" class="axis-pilot-chip" onclick="window.axisPilotQuickRun('독일 법인 8월 제품군별 손익 및 주요 거래선 수익성 분석 보고서 작성해줘')">🇩🇪 독일 8월 제품군·거래선별 손익 보고서</button>
                        <button type="button" class="axis-pilot-chip" onclick="window.axisPilotQuickRun('프랑스 법인 8월 세그먼트별 판매 비중과 유통재고(WOS) 진단해줘')">🇫🇷 프랑스 8월 세그먼트 비중 &amp; WOS 진단</button>
                        <button type="button" class="axis-pilot-chip" onclick="window.axisPilotQuickRun('스페인 법인 8월 제품군별 매출 비중 및 영업이익률(COI%) 분석해줘')">🇪🇸 스페인 8월 제품군별 매출·영업이익률 분석</button>
                        <button type="button" class="axis-pilot-chip" onclick="window.axisPilotQuickRun('베네룩스 법인 8월 주요 거래선별 차감율(SD%) 및 수익성 구조 분석해줘')">🇳🇱 베네룩스 주요 거래선별 차감율·수익성 분석</button>
                    </div>
                </div>
            </div>

            <!-- 2. Live Progress & Diagnostics Bar -->
            <div id="pilotProgressCard" class="bg-white rounded-xl p-5 border border-slate-200 shadow-sm space-y-3">
                <div class="flex flex-wrap items-center justify-between gap-2">
                    <div class="flex items-center gap-2.5">
                        <span id="pilotStepBadge" class="px-2.5 py-1 rounded-md text-xs font-mono font-bold bg-teal-50 text-teal-800 border border-teal-200">READY</span>
                        <span id="pilotStepDesc" class="text-xs font-semibold text-slate-700">프롬프트를 실행하면 Parquet 원천 쿼리 → AI 분석 → HTML·CSV 산출물 아카이빙이 자동 수행됩니다.</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <button type="button" onclick="window.axisPilotTogglePanel('pilotMirrorPanel')" class="px-2.5 py-1 rounded text-[11px] font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 transition">
                            📡 IDE 트랜스크립트 미러링 보기/접기
                        </button>
                        <button type="button" onclick="window.axisPilotTogglePanel('pilotArchivePanel')" class="px-2.5 py-1 rounded text-[11px] font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 transition">
                            📁 최근 Task 아카이브 산출물 목록
                        </button>
                    </div>
                </div>

                <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div id="pilotProgressBar" class="h-full bg-gradient-to-r from-teal-600 to-blue-600 transition-all duration-300" style="width: 0%"></div>
                </div>

                <!-- Deliverable File Chips -->
                <div id="pilotDeliverablesBar" class="flex flex-wrap items-center gap-2 pt-1"></div>

                <!-- Collapsible Panel 1: IDE Live Transcript Mirror -->
                <div id="pilotMirrorPanel" class="hidden mt-3 pt-3 border-t border-slate-200">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-xs font-bold text-slate-700">📡 Antigravity IDE 세션 실시간 트랜스크립트 (<code>transcript.jsonl</code>)</span>
                        <button type="button" onclick="window.axisPilotLoadMirror()" class="text-[11px] text-teal-700 font-bold hover:underline">🔄 즉시 갱신</button>
                    </div>
                    <div id="pilotMirrorBody" class="bg-slate-900 text-slate-200 rounded-lg p-3.5 font-mono text-xs max-h-60 overflow-y-auto space-y-2">
                        <div class="text-slate-400">상단 세션 드롭다운에서 세션을 선택하거나 작업을 실행하면 IDE 추론 내역이 표시됩니다.</div>
                    </div>
                </div>

                <!-- Collapsible Panel 2: Recent Task Archives -->
                <div id="pilotArchivePanel" class="hidden mt-3 pt-3 border-t border-slate-200">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-xs font-bold text-slate-700">📁 <code>99. Master Agent/Task</code> 자동 아카이빙 산출물 목록 (클릭 시 HTML 문서 뷰어에 로드)</span>
                        <button type="button" onclick="window.axisPilotLoadArchives()" class="text-[11px] text-teal-700 font-bold hover:underline">🔄 목록 새로고침</button>
                    </div>
                    <div id="pilotArchiveList" class="grid grid-cols-1 md:grid-cols-2 gap-2.5 max-h-64 overflow-y-auto"></div>
                </div>
            </div>

            <!-- 3. Executive HTML Document Viewer & Copy Toolbar -->
            <div id="pilotDocWorkspace" class="space-y-3">
                <div class="bg-slate-900 text-white px-5 py-3.5 rounded-xl flex flex-wrap items-center justify-between gap-3 shadow-sm">
                    <div class="flex items-center gap-3">
                        <span class="px-2.5 py-1 rounded bg-teal-500/20 border border-teal-500/40 text-teal-300 text-xs font-mono font-bold">HTML DOCUMENT VIEWER</span>
                        <div>
                            <div class="text-sm font-bold">가시성 강화 경영진 보고서 (Executive HTML Document)</div>
                            <div class="text-[11px] text-slate-400">표 테두리·다크슬레이트 헤더·우측 숫자 정렬이 적용된 HTML 문서입니다. 이메일이나 워드에 서식 그대로 붙여넣을 수 있습니다.</div>
                        </div>
                    </div>
                    <div class="flex flex-wrap items-center gap-2">
                        <button
                            type="button"
                            onclick="window.axisPilotCopyRichHtml()"
                            class="px-3.5 py-2 rounded-lg text-xs font-bold bg-teal-600 hover:bg-teal-500 text-white shadow-sm transition flex items-center gap-1.5 cursor-pointer"
                            title="표 테두리, 헤더 색상, 굵은 글씨 서식을 그대로 유지하여 이메일(Outlook)이나 MS Word에 붙여넣을 수 있도록 복사합니다."
                        >
                            <span>📋 서식 유지 복사 (이메일/워드용)</span>
                        </button>
                        <button
                            type="button"
                            onclick="window.axisPilotCopyPlainText()"
                            class="px-3.5 py-2 rounded-lg text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-100 border border-slate-700 transition flex items-center gap-1.5 cursor-pointer"
                            title="메모장이나 메신저에 붙여넣기 좋은 순수 텍스트만 복사합니다."
                        >
                            <span>📝 순수 텍스트 복사</span>
                        </button>
                        <button
                            type="button"
                            onclick="window.axisPilotOpenStandaloneHtml()"
                            class="px-3.5 py-2 rounded-lg text-xs font-bold bg-white hover:bg-slate-100 text-slate-900 transition flex items-center gap-1.5 cursor-pointer"
                            title="독립된 전체화면 HTML 보고서 새 창으로 열기 또는 인쇄/PDF 저장"
                        >
                            <span>🌐 독립 HTML 새 창 / 인쇄</span>
                        </button>
                    </div>
                </div>

                <!-- Rendered Executive HTML Document Paper -->
                <div id="pilotExecDocPaper" class="axis-exec-paper">
                    <div class="axis-exec-banner">
                        <div>
                            <div class="text-[11px] font-mono uppercase tracking-widest text-teal-300 font-bold mb-1">LGE EUROPE TV SALES STRATEGY • AXIS MASTER AI AGENT</div>
                            <h1 id="pilotDocTitle" class="text-lg lg:text-xl font-bold text-white m-0">🤖 AXIS Master Agent — Executive HTML 분석 보고서</h1>
                        </div>
                        <span id="pilotDocFolderBadge" class="px-3 py-1 rounded-full text-xs font-mono font-bold bg-teal-500/20 border border-teal-400 text-teal-200">
                            READY
                        </span>
                    </div>
                    <div class="axis-exec-meta">
                        <div><strong class="text-slate-900">지시 프롬프트:</strong> <span id="pilotDocQueryText">9월 영국 수익성 분석 보고서 만들어줘</span></div>
                        <div><strong class="text-slate-900">생성 시각:</strong> <span id="pilotDocTimeText">-</span></div>
                        <div><strong class="text-slate-900">연계 에이전트:</strong> <span id="pilotDocAgentsText">Master AI Agent, 05. TV P&amp;L Analysis (Parquet), 08. MS Trend (GfK)</span></div>
                    </div>
                    <div id="pilotDocBody" class="axis-exec-body">
                        <div class="text-slate-400 py-8 text-center text-sm">보고서 데이터를 불러오는 중입니다...</div>
                    </div>
                </div>
            </div>

            <div id="axisPilotToast" class="axis-copy-toast">클립보드에 복사되었습니다.</div>
        </section>
        <!-- AXIS_PILOT_SECTION_END -->`;

const SCRIPT_HTML = `<!-- AXIS_PILOT_SCRIPT_START -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
        (function () {
            const SIDECAR_ORIGIN = (window.location.port === '5050') ? window.location.origin : 'http://127.0.0.1:5050';
            let currentStandaloneHtmlUrl = '';
            let currentRawMarkdown = '';
            let activeTaskPollTimer = null;

            function showPilotToast(msg) {
                const t = document.getElementById('axisPilotToast');
                if (!t) return;
                t.textContent = msg;
                t.classList.add('show');
                setTimeout(() => t.classList.remove('show'), 2700);
            }

            // Simple fallback markdown-to-HTML converter in case CDN marked is blocked
            function parseMarkdownToHtml(md) {
                if (!md) return '';
                if (window.marked && typeof window.marked.parse === 'function') {
                    return window.marked.parse(md);
                }
                // Minimal table & heading parser fallback
                return md
                    .replace(/^### (.*)$/gm, '<h3>$1</h3>')
                    .replace(/^## (.*)$/gm, '<h2>$1</h2>')
                    .replace(/^#### (.*)$/gm, '<h4>$1</h4>')
                    .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                    .replace(/\\n/g, '<br/>');
            }

            // Apply inline styles to tables, headers, and blockquotes so Rich Copy to Outlook/Word keeps full styling
            function applyExecutiveInlineStyles(rootEl) {
                if (!rootEl) return;
                rootEl.querySelectorAll('h2').forEach(el => {
                    el.setAttribute('style', 'font-family: Malgun Gothic, IBM Plex Sans, Arial, sans-serif; font-size: 14.5pt; font-weight: bold; color: #0F172A; background-color: #F8FAFC; border-left: 5px solid #0F172A; padding: 8px 12px; margin: 16px 0 10px 0;');
                });
                rootEl.querySelectorAll('h3').forEach(el => {
                    el.setAttribute('style', 'font-family: Malgun Gothic, IBM Plex Sans, Arial, sans-serif; font-size: 11.5pt; font-weight: bold; color: #0F172A; border-left: 4px solid #0D9488; padding-left: 8px; margin: 18px 0 8px 0;');
                });
                rootEl.querySelectorAll('h4').forEach(el => {
                    el.setAttribute('style', 'font-family: Malgun Gothic, Arial, sans-serif; font-size: 10.5pt; font-weight: bold; color: #0F172A; margin: 12px 0 6px 0;');
                });
                rootEl.querySelectorAll('blockquote').forEach(el => {
                    el.setAttribute('style', 'font-family: Malgun Gothic, Arial, sans-serif; font-size: 9.5pt; background-color: #F0FDFA; border-left: 4px solid #0D9488; padding: 10px 14px; margin: 10px 0 14px 0; color: #134E4A;');
                });
                rootEl.querySelectorAll('ul').forEach(el => {
                    el.setAttribute('style', 'font-family: Malgun Gothic, Arial, sans-serif; font-size: 10pt; color: #1E293B; padding-left: 20px; margin: 8px 0 14px 0;');
                });
                rootEl.querySelectorAll('li').forEach(el => {
                    el.setAttribute('style', 'margin-bottom: 5px; line-height: 1.6;');
                });
                rootEl.querySelectorAll('table').forEach(tbl => {
                    tbl.setAttribute('style', 'width: 100%; border-collapse: collapse; margin: 12px 0 18px 0; font-family: Malgun Gothic, Arial, sans-serif; font-size: 9.5pt; border: 1px solid #CBD5E1;');
                    const rows = tbl.querySelectorAll('tr');
                    rows.forEach((tr, rIdx) => {
                        const isTotal = /합계|Total/i.test(tr.innerText || '');
                        tr.querySelectorAll('th').forEach((th, cIdx) => {
                            const align = cIdx === 0 ? 'left' : 'right';
                            th.setAttribute('style', 'background-color: #0F172A; color: #FFFFFF; padding: 8px 10px; border: 1px solid #1E293B; font-weight: bold; text-align: ' + align + '; white-space: nowrap;');
                        });
                        tr.querySelectorAll('td').forEach((td, cIdx) => {
                            const txt = (td.innerText || '').trim();
                            const isNum = cIdx > 0 && (/^[\\$\\+\\-]?[0-9,]+(\\.[0-9]+)?(%|%p|대|주|건|위)?$/.test(txt) || txt === '-');
                            const bg = isTotal ? '#E2E8F0' : (rIdx % 2 === 0 ? '#F8FAFC' : '#FFFFFF');
                            const fw = isTotal ? 'bold' : 'normal';
                            const align = isNum ? 'right' : 'left';
                            let color = '#0F172A';
                            if (/^\\+[0-9]/.test(txt)) color = '#0F766E';
                            if (/^\\-[0-9]/.test(txt)) color = '#B91C1C';
                            td.setAttribute('style', 'background-color: ' + bg + '; color: ' + color + '; padding: 7px 10px; border: 1px solid #CBD5E1; text-align: ' + align + '; font-weight: ' + fw + ';');
                        });
                    });
                });
            }

            function renderExecutiveDocument({ query, answerMarkdown, folderName, completedAt, dispatchedAgents, deliverables }) {
                currentRawMarkdown = answerMarkdown || '';
                const bodyEl = document.getElementById('pilotDocBody');
                const titleEl = document.getElementById('pilotDocTitle');
                const badgeEl = document.getElementById('pilotDocFolderBadge');
                const queryEl = document.getElementById('pilotDocQueryText');
                const timeEl = document.getElementById('pilotDocTimeText');
                const agentsEl = document.getElementById('pilotDocAgentsText');
                const delivBar = document.getElementById('pilotDeliverablesBar');

                const headingMatch = (answerMarkdown || '').match(/^##\\s+(.+)$/m);
                if (titleEl) {
                    titleEl.textContent = headingMatch ? headingMatch[1].trim() : ('🤖 AXIS 전략 분석 리포트 — ' + (query || '자동 생성 문서'));
                }
                if (badgeEl) badgeEl.textContent = folderName || 'EXECUTIVE HTML';
                if (queryEl) queryEl.textContent = query || '-';
                if (timeEl) timeEl.textContent = (completedAt || new Date().toISOString()).slice(0, 19).replace('T', ' ');
                if (agentsEl) {
                    agentsEl.textContent = Array.isArray(dispatchedAgents) && dispatchedAgents.length > 0
                        ? dispatchedAgents.join(', ')
                        : 'Master AI Agent, 05. TV P&L Analysis (Parquet), 08. MS Trend (GfK)';
                }

                if (bodyEl) {
                    bodyEl.innerHTML = parseMarkdownToHtml(answerMarkdown || '');
                    applyExecutiveInlineStyles(bodyEl);
                }

                // Deliverable download chips
                currentStandaloneHtmlUrl = '';
                if (delivBar) {
                    const files = Array.isArray(deliverables) ? deliverables : [];
                    if (files.length === 0) {
                        delivBar.innerHTML = '';
                    } else {
                        delivBar.innerHTML = '<span class="text-[11px] font-bold text-slate-600 mr-1">📦 생성된 산출물 파일:</span>' +
                            files.map(f => {
                                const rawUrl = f.url || f.webUrl || '';
                                const fullUrl = rawUrl.startsWith('http') ? rawUrl : (SIDECAR_ORIGIN + rawUrl);
                                if ((f.name || '').endsWith('.html')) currentStandaloneHtmlUrl = fullUrl;
                                const icon = (f.name || '').endsWith('.html') ? '🌐' : ((f.name || '').endsWith('.csv') || (f.name || '').endsWith('.xlsx') ? '📊' : '📝');
                                return '<a href="' + fullUrl + '" target="_blank" rel="noopener" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-bold bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 transition">' +
                                    icon + ' ' + f.name + '</a>';
                            }).join('');
                    }
                }
            }

            // Copy as Rich HTML (for Outlook / MS Word / Notion paste with table borders & colors preserved)
            window.axisPilotCopyRichHtml = async function () {
                const paperEl = document.getElementById('pilotExecDocPaper');
                if (!paperEl) return;
                try {
                    const clone = paperEl.cloneNode(true);
                    applyExecutiveInlineStyles(clone);
                    const htmlStr = clone.outerHTML;
                    const plainStr = paperEl.innerText;
                    if (navigator.clipboard && window.ClipboardItem) {
                        const item = new ClipboardItem({
                            'text/html': new Blob([htmlStr], { type: 'text/html' }),
                            'text/plain': new Blob([plainStr], { type: 'text/plain' })
                        });
                        await navigator.clipboard.write([item]);
                        showPilotToast('✅ 서식 유지 HTML 문서가 복사되었습니다! (이메일·워드에 Ctrl+V로 표 서식 그대로 붙여넣기 가능)');
                        return;
                    }
                    await navigator.clipboard.writeText(plainStr);
                    showPilotToast('✅ 문서 텍스트가 클립보드에 복사되었습니다.');
                } catch (e) {
                    try {
                        const sel = window.getSelection();
                        const range = document.createRange();
                        range.selectNodeContents(paperEl);
                        sel.removeAllRanges();
                        sel.addRange(range);
                        document.execCommand('copy');
                        sel.removeAllRanges();
                        showPilotToast('✅ 서식 유지 문서가 클립보드에 복사되었습니다!');
                    } catch (err) {
                        showPilotToast('⚠️ 복사에 실패했습니다.');
                    }
                }
            };

            // Copy as Plain Text
            window.axisPilotCopyPlainText = async function () {
                const bodyEl = document.getElementById('pilotDocBody');
                if (!bodyEl) return;
                try {
                    await navigator.clipboard.writeText(bodyEl.innerText);
                    showPilotToast('✅ 순수 텍스트가 클립보드에 복사되었습니다!');
                } catch (e) {
                    showPilotToast('⚠️ 텍스트 복사에 실패했습니다.');
                }
            };

            // Open standalone archived HTML report or print
            window.axisPilotOpenStandaloneHtml = function () {
                if (currentStandaloneHtmlUrl) {
                    window.open(currentStandaloneHtmlUrl, '_blank', 'noopener');
                    return;
                }
                const paperEl = document.getElementById('pilotExecDocPaper');
                if (!paperEl) return;
                const win = window.open('', '_blank');
                if (!win) return;
                win.document.write('<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><title>AXIS Executive HTML Report</title></head><body style="margin:24px;background:#F8FAFC;">' + paperEl.outerHTML + '</body></html>');
                win.document.close();
            };

            // Toggle collapsible diagnostic panels
            window.axisPilotTogglePanel = function (panelId) {
                const el = document.getElementById(panelId);
                if (!el) return;
                el.classList.toggle('hidden');
                if (!el.classList.contains('hidden')) {
                    if (panelId === 'pilotMirrorPanel') window.axisPilotLoadMirror();
                    if (panelId === 'pilotArchivePanel') window.axisPilotLoadArchives();
                }
            };

            // Refresh Bridge Health & Sessions
            window.axisPilotRefreshStatus = async function () {
                const dot = document.getElementById('pilotBridgeDot');
                const txt = document.getElementById('pilotBridgeStatusText');
                const sel = document.getElementById('pilotSessionSelect');
                try {
                    const res = await fetch(SIDECAR_ORIGIN + '/api/health', { cache: 'no-store' });
                    const data = await res.json();
                    if (data && (data.ok || data.status === 'online')) {
                        if (dot) dot.className = 'w-2 h-2 rounded-full bg-teal-400';
                        if (txt) txt.textContent = 'Antigravity Sidecar 연결됨 (Port 5050)';
                    }
                } catch (e) {
                    if (dot) dot.className = 'w-2 h-2 rounded-full bg-rose-400';
                    if (txt) txt.textContent = 'Port 5050 오프라인 (start_sidecar_bridge.js 실행 필요)';
                }

                try {
                    const sRes = await fetch(SIDECAR_ORIGIN + '/api/bridge/conversations?limit=10', { cache: 'no-store' });
                    const sData = await sRes.json();
                    if (sel && sData && Array.isArray(sData.conversations)) {
                        const prevVal = sel.value;
                        sel.innerHTML = '<option value="">✨ 새 자율 실행 세션 (권장)</option>' +
                            sData.conversations.map(c => {
                                const shortId = (c.conversationId || '').slice(0, 8);
                                const label = (c.lastPrompt || c.firstPrompt || '세션').slice(0, 38);
                                return '<option value="' + c.conversationId + '">[' + shortId + '] ' + label.replace(/</g, '&lt;') + '</option>';
                            }).join('');
                        if (prevVal) sel.value = prevVal;
                    }
                } catch (e) {}
            };

            // Load live IDE transcript mirror
            window.axisPilotLoadMirror = async function () {
                const box = document.getElementById('pilotMirrorBody');
                const sel = document.getElementById('pilotSessionSelect');
                if (!box) return;
                try {
                    let convId = sel ? sel.value : '';
                    if (!convId) {
                        const sRes = await fetch(SIDECAR_ORIGIN + '/api/bridge/conversations?limit=1', { cache: 'no-store' });
                        const sData = await sRes.json();
                        if (sData?.conversations?.[0]) convId = sData.conversations[0].conversationId;
                    }
                    if (!convId) {
                        box.innerHTML = '<div class="text-slate-400">활성화된 Antigravity 세션을 찾을 수 없습니다.</div>';
                        return;
                    }
                    const tRes = await fetch(SIDECAR_ORIGIN + '/api/bridge/transcript/' + encodeURIComponent(convId) + '?maxSteps=20', { cache: 'no-store' });
                    const tData = await tRes.json();
                    const steps = tData?.steps || tData?.transcript?.steps || [];
                    if (steps.length === 0) {
                        box.innerHTML = '<div class="text-slate-400">세션(' + convId.slice(0, 8) + ') 트랜스크립트 내역이 비어 있습니다.</div>';
                        return;
                    }
                    box.innerHTML = steps.slice(-10).map(st => {
                        const tools = (st.toolCalls || []).map(tc => '<span class="px-1.5 py-0.5 rounded bg-teal-900 text-teal-300 mr-1">🔧 ' + tc.name + ' (' + (tc.toolSummary || '') + ')</span>').join('');
                        const txt = (st.content || st.thinking || '').slice(0, 220).replace(/</g, '&lt;');
                        return '<div class="border-b border-slate-800 pb-1.5">' +
                            '<div class="text-[10px] text-slate-400">#' + st.stepIndex + ' [' + st.type + '] ' + (st.status || '') + '</div>' +
                            (tools ? '<div class="my-1">' + tools + '</div>' : '') +
                            (txt ? '<div class="text-slate-200">' + txt + '</div>' : '') +
                            '</div>';
                    }).join('');
                } catch (e) {
                    box.innerHTML = '<div class="text-rose-400">트랜스크립트 조회 실패: ' + e.message + '</div>';
                }
            };

            // Load recent archived tasks & allow clicking any task to view its HTML report
            window.axisPilotLoadArchives = async function () {
                const listEl = document.getElementById('pilotArchiveList');
                try {
                    const res = await fetch(SIDECAR_ORIGIN + '/api/tasks/recent?limit=8', { cache: 'no-store' });
                    const data = await res.json();
                    const tasks = data?.tasks || [];
                    if (listEl) {
                        if (tasks.length === 0) {
                            listEl.innerHTML = '<div class="text-xs text-slate-400">아카이빙된 Task가 없습니다.</div>';
                        } else {
                            listEl.innerHTML = tasks.map(t => {
                                const htmlFile = (t.files || []).find(f => (f.name || '').endsWith('.html'));
                                const htmlUrl = htmlFile ? (SIDECAR_ORIGIN + htmlFile.url) : '';
                                return '<div class="p-3 rounded-lg border border-slate-200 bg-slate-50 hover:bg-teal-50/40 hover:border-teal-300 transition flex items-center justify-between gap-2">' +
                                    '<div class="min-w-0">' +
                                    '<div class="text-xs font-bold text-slate-900 truncate">📁 ' + t.folderName + '</div>' +
                                    '<div class="text-[11px] text-slate-500 truncate">' + (t.summary || t.title || '').replace(/</g, '&lt;') + '</div>' +
                                    '</div>' +
                                    (htmlUrl ? '<a href="' + htmlUrl + '" target="_blank" class="px-2.5 py-1 rounded text-[11px] font-bold bg-white border border-slate-300 text-slate-800 hover:bg-slate-900 hover:text-white shrink-0">🌐 HTML 열기</a>' : '') +
                                    '</div>';
                            }).join('');
                        }
                    }
                } catch (e) {}
            };

            // Quick run helper from sample chips
            window.axisPilotQuickRun = function (promptText) {
                const input = document.getElementById('pilotPromptInput');
                if (input) input.value = promptText;
                window.axisPilotRunPrompt(promptText);
            };

            // Execute Prompt via Port 5050 Bridge
            window.axisPilotRunPrompt = async function (overrideQuery) {
                const input = document.getElementById('pilotPromptInput');
                const query = (typeof overrideQuery === 'string' && overrideQuery.trim())
                    ? overrideQuery.trim()
                    : (input ? input.value.trim() : '');

                if (!query) {
                    showPilotToast('⚠️ 실행할 작업 지시 프롬프트를 입력해 주세요.');
                    if (input) input.focus();
                    return;
                }

                const runBtn = document.getElementById('pilotRunBtn');
                const stepBadge = document.getElementById('pilotStepBadge');
                const stepDesc = document.getElementById('pilotStepDesc');
                const progBar = document.getElementById('pilotProgressBar');
                const sel = document.getElementById('pilotSessionSelect');

                if (runBtn) {
                    runBtn.disabled = true;
                    runBtn.innerHTML = '<span>⏳ AI 분석 및 HTML 문서 생성 중...</span>';
                }
                if (stepBadge) {
                    stepBadge.textContent = 'STEP 1/3 • DISPATCHING';
                    stepBadge.className = 'px-2.5 py-1 rounded-md text-xs font-mono font-bold bg-blue-50 text-blue-800 border border-blue-200';
                }
                if (stepDesc) stepDesc.textContent = 'Antigravity AXIS Master Agent로 프롬프트를 전송하고 원천 Parquet DB를 쿼리하고 있습니다...';
                if (progBar) progBar.style.width = '28%';

                if (activeTaskPollTimer) clearInterval(activeTaskPollTimer);

                try {
                    const reqRes = await fetch(SIDECAR_ORIGIN + '/api/bridge/task', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            query,
                            conversationId: sel ? (sel.value || null) : null,
                            executionMode: 'autonomous_full',
                            source: 'axis_architecture_guide_pilot'
                        })
                    });
                    const reqData = await reqRes.json();
                    if (!reqData || !reqData.taskId) {
                        throw new Error(reqData?.error || '작업 ID 생성 실패');
                    }

                    const taskId = reqData.taskId;
                    let pollTicks = 0;

                    activeTaskPollTimer = setInterval(async () => {
                        pollTicks++;
                        try {
                            const stRes = await fetch(SIDECAR_ORIGIN + '/api/bridge/status/' + encodeURIComponent(taskId), { cache: 'no-store' });
                            const stData = await stRes.json();

                            if (stData.status === 'running' || stData.status === 'processing' || stData.status === 'queued' || stData.status === 'pending') {
                                const p = stData.progress || {};
                                const pct = Math.min(90, 30 + (p.step || 1) * 22);
                                if (progBar) progBar.style.width = pct + '%';
                                if (stepBadge) stepBadge.textContent = 'STEP ' + (p.step || 1) + '/' + (p.totalSteps || 3) + ' • ' + (p.currentAgent || 'WORKING');
                                if (stepDesc) stepDesc.textContent = p.desc || '원천 데이터 쿼리 및 HTML 보고서 합성 중...';
                            } else if (stData.status === 'completed' && (stData.result || stData.data)) {
                                clearInterval(activeTaskPollTimer);
                                activeTaskPollTimer = null;
                                const d = stData.result || stData.data;

                                if (progBar) progBar.style.width = '100%';
                                if (stepBadge) {
                                    stepBadge.textContent = 'COMPLETED • HTML READY';
                                    stepBadge.className = 'px-2.5 py-1 rounded-md text-xs font-mono font-bold bg-teal-50 text-teal-800 border border-teal-200';
                                }
                                if (stepDesc) {
                                    stepDesc.textContent = '✅ 분석 완료! 아래 Executive HTML 문서 뷰어에서 확인하거나 [서식 유지 복사] 버튼으로 즉시 복사하세요.';
                                }
                                if (runBtn) {
                                    runBtn.disabled = false;
                                    runBtn.innerHTML = '<span>✨ AXIS AI 작업 실행</span>';
                                }

                                renderExecutiveDocument({
                                    query,
                                    answerMarkdown: d.answerMarkdown || d.artifact?.markdown || '',
                                    folderName: d.taskArchive?.folderName || 'COMPLETED',
                                    completedAt: d.completedAt,
                                    dispatchedAgents: d.dispatchedAgents,
                                    deliverables: d.deliverables || d.taskArchive?.deliverables || []
                                });
                                window.axisPilotLoadArchives();
                            }
                        } catch (pollErr) {}

                        if (pollTicks > 90) {
                            clearInterval(activeTaskPollTimer);
                            activeTaskPollTimer = null;
                            if (runBtn) {
                                runBtn.disabled = false;
                                runBtn.innerHTML = '<span>✨ AXIS AI 작업 실행</span>';
                            }
                            if (stepBadge) stepBadge.textContent = 'TIMEOUT';
                            if (stepDesc) stepDesc.textContent = '⚠️ 응답 대기 시간이 초과되었습니다. 다시 시도해 주세요.';
                        }
                    }, 700);
                } catch (err) {
                    if (runBtn) {
                        runBtn.disabled = false;
                        runBtn.innerHTML = '<span>✨ AXIS AI 작업 실행</span>';
                    }
                    if (stepBadge) {
                        stepBadge.textContent = 'ERROR';
                        stepBadge.className = 'px-2.5 py-1 rounded-md text-xs font-mono font-bold bg-rose-50 text-rose-800 border border-rose-200';
                    }
                    if (stepDesc) stepDesc.textContent = '⚠️ 실행 오류: ' + err.message;
                }
            };

            // Attach Korean IME-safe Enter listener to #pilotPromptInput
            document.addEventListener('DOMContentLoaded', () => {
                const input = document.getElementById('pilotPromptInput');
                if (input) {
                    let isComposing = false;
                    input.addEventListener('compositionstart', () => { isComposing = true; });
                    input.addEventListener('compositionend', () => { isComposing = false; });
                    input.addEventListener('keydown', (e) => {
                        if (e.key === 'Enter' && !isComposing && !e.isComposing && e.keyCode !== 229) {
                            e.preventDefault();
                            window.axisPilotRunPrompt();
                        }
                    });
                }

                // Initialize status & run default sample report so viewer is populated immediately
                window.axisPilotRefreshStatus();
                window.axisPilotLoadArchives();
                setTimeout(() => {
                    const defaultPrompt = '9월 영국 수익성 분석 보고서 만들어줘';
                    if (input && !input.value) input.value = defaultPrompt;
                    window.axisPilotRunPrompt(defaultPrompt);
                }, 300);
            });

            // Upgrade copyPrompt(text) from Tab 3 so clicking an example prompt also opens Tab 7 Pilot and fills the input
            const origCopyPrompt = window.copyPrompt;
            window.copyPrompt = function (text) {
                if (typeof origCopyPrompt === 'function') {
                    try { origCopyPrompt(text); } catch (e) {}
                }
                const navBtn = document.getElementById('nav-btn-prompt-pilot');
                const input = document.getElementById('pilotPromptInput');
                if (input) input.value = text;
                if (typeof window.showTab === 'function' && navBtn) {
                    window.showTab('tab-prompt-pilot', navBtn);
                    showPilotToast('✨ 7. AXIS 작업 지시 프롬프트(Pilot) 탭으로 프롬프트를 가져왔습니다!');
                }
            };
        })();
    </script>
    <!-- AXIS_PILOT_SCRIPT_END -->`;

function injectPilotIntoGuide(guidePath) {
  if (!fs.existsSync(guidePath)) return false;
  let html = fs.readFileSync(guidePath, 'utf8');

  // Remove any previous injections for clean idempotent update
  html = html.replace(/<!-- AXIS_PILOT_NAV_START -->[\s\S]*?<!-- AXIS_PILOT_NAV_END -->\s*/g, '');
  html = html.replace(/<!-- AXIS_PILOT_SECTION_START -->[\s\S]*?<!-- AXIS_PILOT_SECTION_END -->\s*/g, '');
  html = html.replace(/<!-- AXIS_PILOT_SCRIPT_START -->[\s\S]*?<!-- AXIS_PILOT_SCRIPT_END -->\s*/g, '');

  // 1. Inject NAV_HTML right after the 6. 보안 구성 & 거버넌스 button inside #sidebar-nav
  const navTargetRegex = /(<button\s+onclick="showTab\('tab-security',\s*this\)"[\s\S]*?<\/button>)/i;
  if (navTargetRegex.test(html)) {
    html = html.replace(navTargetRegex, `$1\n            ${NAV_HTML}`);
  } else {
    html = html.replace(/<\/nav>/i, `    ${NAV_HTML}\n        </nav>`);
  }

  // 2. Inject SECTION_HTML right before </main>
  html = html.replace(/<\/main>/i, `\n${SECTION_HTML}\n    </main>`);

  // 3. Inject SCRIPT_HTML right before </body>
  html = html.replace(/<\/body>/i, `\n${SCRIPT_HTML}\n</body>`);

  fs.writeFileSync(guidePath, html, 'utf8');
  return true;
}

const guideTargets = [
  path.join(PORTAL_DIR, 'docs', 'AXIS_System_Architecture_Guide.html'),
  path.join(PORTAL_DIR, 'public', 'docs', 'AXIS_System_Architecture_Guide.html'),
  path.join(ROOT_DIR, 'public', 'docs', 'AXIS_System_Architecture_Guide.html')
];

for (const gp of guideTargets) {
  if (injectPilotIntoGuide(gp)) {
    console.log('[InstallPilot] Updated guide:', gp);
  }
}
