import os
import re

html_path = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\00. TV Europe Sales Management Portal\docs\AXIS_System_Architecture_Guide.html"
b64_path = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\scripts\excel_base64.txt"

with open(b64_path, "r", encoding="utf-8") as f:
    b64_excel = f.read().strip()

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Let's inspect where to insert
target_pattern = r'(<!-- Live Actionable Prompt Chip -->[\s\S]*?content_copy</span>\s*</div>\s*</div>)'

component_html = f'''<!-- Live Actionable Prompt Chip -->
                        <div class="bg-slate-50 p-3.5 rounded-lg border border-slate-200">
                            <div class="text-[11px] font-bold text-slate-600 mb-1.5 flex items-center justify-between">
                                <span>마스터 에이전트 실전 질의 프롬프트 (클릭 시 복사)</span>
                                <span class="text-[10px] text-teal-600 font-semibold">One-Click Copy</span>
                            </div>
                            <div class="prompt-chip p-2.5 rounded bg-white border border-slate-200 text-xs font-mono text-slate-800 flex items-center justify-between shadow-sm" onclick="copyPrompt('유럽 전 법인 중 유통재고 주수(WOS)가 6주를 초과하거나 3주 미만인 리스크 법인 목록과 해당 법인의 OLED 신모델 비중을 표로 비교 요약해줘')">
                                <span>"유럽 전 법인 중 WOS 6주 초과 또는 3주 미만 리스크 법인 목록과 OLED 신모델 비중 요약해줘"</span>
                                <span class="material-symbols-outlined text-sm text-slate-400">content_copy</span>
                            </div>
                        </div>

                        <!-- Real Agent Execution Result Section (Interactive Drawer) -->
                        <div class="mt-3 pt-3 border-t border-slate-200/80">
                            <button type="button" 
                                    id="sc01-toggle-btn"
                                    onclick="toggleScenario01Result()"
                                    class="w-full py-2.5 px-4 rounded-lg bg-gradient-to-r from-teal-50 to-emerald-50 hover:from-teal-100 hover:to-emerald-100 border border-teal-200 text-teal-900 text-xs font-bold flex items-center justify-between transition-all shadow-sm group">
                                <span class="flex items-center gap-2">
                                    <span class="w-6 h-6 rounded-md bg-teal-600 text-white flex items-center justify-center material-symbols-outlined text-sm shadow-xs group-hover:rotate-12 transition-transform">smart_toy</span>
                                    <span class="font-headline text-sm font-bold text-slate-800">마스터 에이전트 실전 답변 및 엑셀 결과 보기 (Live Execution Output)</span>
                                    <span class="px-2 py-0.5 rounded-full bg-emerald-600 text-white text-[10px] font-semibold tracking-wide">실행 완료 (5초)</span>
                                </span>
                                <span class="flex items-center gap-1.5 text-xs text-teal-700 font-semibold">
                                    <span id="sc01-toggle-text">답변 & 엑셀 열기</span>
                                    <span class="material-symbols-outlined text-lg transition-transform duration-200" id="sc01-toggle-icon">expand_more</span>
                                </span>
                            </button>

                            <!-- Expandable Result Drawer Container -->
                            <div id="sc01-result-drawer" class="hidden mt-3 rounded-xl border border-teal-200/80 bg-white shadow-md overflow-hidden transition-all duration-300">
                                
                                <!-- Drawer Top Bar (Tabs & Download) -->
                                <div class="bg-slate-900 px-4 py-3 flex flex-wrap items-center justify-between gap-3 border-b border-slate-800">
                                    <div class="flex items-center gap-2">
                                        <button type="button" 
                                                id="sc01-btn-tab-report"
                                                onclick="switchScenario01Tab('report')"
                                                class="px-3.5 py-1.5 rounded-lg text-xs font-bold bg-teal-600 text-white shadow-xs flex items-center gap-1.5 transition-all">
                                            <span class="material-symbols-outlined text-sm">chat</span>
                                            <span>AI 분석 보고서 (총평 & 리스크 진단)</span>
                                        </button>
                                        <button type="button" 
                                                id="sc01-btn-tab-sheet"
                                                onclick="switchScenario01Tab('sheet')"
                                                class="px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-1.5 transition-all">
                                            <span class="material-symbols-outlined text-sm">table_view</span>
                                            <span>엑셀 데이터 시트 뷰어 (16개 법인 매트릭스)</span>
                                        </button>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <span class="text-[11px] text-slate-400 hidden sm:inline">참조: 06. KPI Sheet (9/21W 주차 실적)</span>
                                        <button type="button" 
                                                onclick="downloadScenario01Excel()"
                                                class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center gap-1.5 shadow-sm transition-all hover:scale-105 active:scale-95">
                                            <span class="material-symbols-outlined text-sm">download</span>
                                            <span>엑셀 원본 다운로드 (.xlsx)</span>
                                        </button>
                                    </div>
                                </div>

                                <!-- Tab 1: AI Analysis Report -->
                                <div id="sc01-tab-report" class="p-5 space-y-5">
                                    <!-- Agent Header Info -->
                                    <div class="p-3.5 rounded-lg bg-slate-50 border border-slate-200 flex flex-wrap items-center justify-between gap-2 text-xs">
                                        <div class="flex items-center gap-2">
                                            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                                            <span class="font-bold text-slate-800">TV Europe Master AI Agent 실행 리포트</span>
                                            <span class="text-slate-400">|</span>
                                            <span class="text-slate-600">소요 시간: <strong class="text-teal-700 font-mono">4.8초</strong></span>
                                            <span class="text-slate-400">|</span>
                                            <span class="text-slate-600">질의 일시: <strong class="text-slate-700">2026-10-03 (최신 9/21W 주차 실적 기반)</strong></span>
                                        </div>
                                        <div class="flex items-center gap-1 text-[11px] text-slate-500">
                                            <span class="material-symbols-outlined text-xs text-teal-600">verified</span>
                                            <span>Auto-Archived: <code>20261003_유통재고WOS_OLED비중</code></span>
                                        </div>
                                    </div>

                                    <!-- 4 KPI Metrics Card Grid -->
                                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                                        <div class="p-3.5 rounded-lg bg-slate-50 border border-slate-200 space-y-1">
                                            <div class="text-[11px] text-slate-500 font-medium">유럽 본부(EU TTL) 평균 WOS</div>
                                            <div class="text-xl font-bold font-mono text-slate-900">7.31<span class="text-xs font-normal text-slate-500 ml-0.5">주</span></div>
                                            <div class="text-[10px] text-slate-500">신모델 9.54주 / 구모델 4.36주</div>
                                        </div>
                                        <div class="p-3.5 rounded-lg bg-rose-50 border border-rose-200 space-y-1">
                                            <div class="text-[11px] text-rose-700 font-bold flex items-center gap-1">
                                                <span class="material-symbols-outlined text-xs">warning</span>
                                                <span>과다재고 리스크 (>6주)</span>
                                            </div>
                                            <div class="text-xl font-bold font-mono text-rose-700">13<span class="text-xs font-normal text-rose-600 ml-0.5">개 법인</span></div>
                                            <div class="text-[10px] text-rose-600">루마니아(12.6주), 체코(8.6주) 등</div>
                                        </div>
                                        <div class="p-3.5 rounded-lg bg-amber-50 border border-amber-200 space-y-1">
                                            <div class="text-[11px] text-amber-800 font-medium">재고부족 리스크 (<3주)</div>
                                            <div class="text-xl font-bold font-mono text-amber-800">0<span class="text-xs font-normal text-amber-700 ml-0.5">개 법인</span></div>
                                            <div class="text-[10px] text-amber-700">전체 TV 기준 결품 우려 없음</div>
                                        </div>
                                        <div class="p-3.5 rounded-lg bg-emerald-50 border border-emerald-200 space-y-1">
                                            <div class="text-[11px] text-emerald-800 font-medium">정상 범위 (3~6주)</div>
                                            <div class="text-xl font-bold font-mono text-emerald-800">3<span class="text-xs font-normal text-emerald-700 ml-0.5">개 법인</span></div>
                                            <div class="text-[10px] text-emerald-700">오스트리아(4.2), 포르투갈(5.6), 베네룩스(5.7)</div>
                                        </div>
                                    </div>

                                    <!-- Deep Diagnostic 3 Clusters -->
                                    <div class="space-y-3">
                                        <h4 class="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                                            <span class="material-symbols-outlined text-teal-600 text-sm">troubleshoot</span>
                                            <span>리스크 법인 3대 유형 심층 진단 및 실무 액션 플랜</span>
                                        </h4>
                                        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                                            <!-- Cluster A -->
                                            <div class="p-3.5 rounded-lg bg-rose-50/70 border border-rose-200 space-y-2">
                                                <div class="font-bold text-rose-900 flex items-center justify-between">
                                                    <span>🚨 유형 A: 신모델 과잉 선적형</span>
                                                    <span class="px-1.5 py-0.5 rounded bg-rose-200/80 text-[10px] text-rose-800">심각 리스크</span>
                                                </div>
                                                <p class="text-slate-700 leading-relaxed text-[11.5px]">
                                                    <strong>루마니아(12.6주), 폴란드(7.4주), 프랑스(8.5주)</strong>: 전체 WOS 대비 <strong>신모델 WOS가 15~25주</strong>에 달해 유통 내 신모델 재고가 과도하게 정체되어 있습니다. 반면 구모델 WOS는 2~4주로 이미 소진 완료되었으므로, <strong>본사 추가 출하를 즉각 동결하고 메이저 리테일러 신모델 셀아웃 판촉에 집중</strong>해야 합니다.
                                                </p>
                                            </div>
                                            <!-- Cluster B -->
                                            <div class="p-3.5 rounded-lg bg-teal-50/70 border border-teal-200 space-y-2">
                                                <div class="font-bold text-teal-900 flex items-center justify-between">
                                                    <span>💎 유형 B: 프리미엄 OLED 주도형</span>
                                                    <span class="px-1.5 py-0.5 rounded bg-teal-200/80 text-[10px] text-teal-800">전략적 비축</span>
                                                </div>
                                                <p class="text-slate-700 leading-relaxed text-[11.5px]">
                                                    <strong>독일(8.0주), 스위스(6.3주), 베네룩스(5.7주)</strong>: WOS가 6~8주 수준이나, 전체 판매 중 <strong>OLED 신모델 비중이 20~29%</strong>에 달하며 신모델 중 OLED 비중이 44~52%로 유럽 내 최고 수준입니다. IFA 직후 Q4 성수기를 선점하기 위한 전략적 재고 빌드업으로 실질 회전 리스크는 낮습니다.
                                                </p>
                                            </div>
                                            <!-- Cluster C -->
                                            <div class="p-3.5 rounded-lg bg-amber-50/70 border border-amber-200 space-y-2">
                                                <div class="font-bold text-amber-900 flex items-center justify-between">
                                                    <span>⚠️ 유형 C: 구모델 정체 + 저가형 편중</span>
                                                    <span class="px-1.5 py-0.5 rounded bg-amber-200/80 text-[10px] text-amber-800">이중 리스크</span>
                                                </div>
                                                <p class="text-slate-700 leading-relaxed text-[11.5px]">
                                                    <strong>스페인(7.7주), 이탈리아(7.3주), 그리스(7.2주)</strong>: 신모델 판매 내 OLED 비중이 <strong>9~30%</strong>에 불과하며 보급형 LCD에 편중되어 있습니다. 특히 스페인은 <strong>구모델 WOS도 7.65주(1.9만대)</strong>로 여전히 높아 구모델 긴급 클리어런스와 OLED 진열 개선이 병행되어야 합니다.
                                                </p>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Guide Note -->
                                    <div class="p-3 rounded-lg bg-slate-50 border border-slate-200 text-[11px] text-slate-600 flex items-center justify-between flex-wrap gap-2">
                                        <div class="flex items-center gap-1.5">
                                            <span class="material-symbols-outlined text-xs text-teal-600">info</span>
                                            <span><strong>OLED 신모델 3대 지표 정의:</strong> ① OLED 내 신모델비중(OLED 세대교체율) | ② 신모델 내 OLED비중(프리미엄 믹스율) | ③ 전체 TV 내 OLED신모델(전체 볼륨 기여율)</span>
                                        </div>
                                        <button type="button" onclick="switchScenario01Tab('sheet')" class="text-teal-700 font-bold hover:underline flex items-center gap-0.5">
                                            <span>전체 16개국 엑셀 매트릭스 표 보기</span>
                                            <span class="material-symbols-outlined text-xs">arrow_forward</span>
                                        </button>
                                    </div>
                                </div>

                                <!-- Tab 2: Interactive Excel Data Sheet View -->
                                <div id="sc01-tab-sheet" class="hidden p-5 space-y-4">
                                    <!-- Sheet Control Bar -->
                                    <div class="flex flex-wrap items-center justify-between gap-3 text-xs">
                                        <div class="flex items-center gap-1.5">
                                            <span class="text-slate-500 font-medium">필터:</span>
                                            <button type="button" 
                                                    id="sc01-filter-all"
                                                    onclick="filterScenario01Grid('all')" 
                                                    class="px-2.5 py-1 rounded bg-slate-900 text-white font-bold text-xs shadow-2xs">전체 (17)</button>
                                            <button type="button" 
                                                    id="sc01-filter-risk"
                                                    onclick="filterScenario01Grid('risk')" 
                                                    class="px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium text-xs">과다재고 리스크 (13)</button>
                                            <button type="button" 
                                                    id="sc01-filter-safe"
                                                    onclick="filterScenario01Grid('safe')" 
                                                    class="px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium text-xs">정상 (3)</button>
                                        </div>
                                        <div class="text-[11px] text-slate-500 flex items-center gap-2">
                                            <span class="px-2 py-0.5 rounded bg-slate-100 border border-slate-200 font-mono">시트명: 리스크법인_WOS_OLED요약</span>
                                            <span>단위: 수량(대), WOS(주), 비중(%)</span>
                                        </div>
                                    </div>

                                    <!-- Table Container -->
                                    <div class="overflow-x-auto border border-slate-200 rounded-lg shadow-2xs max-h-[460px] overflow-y-auto">
                                        <table class="w-full text-[11px] text-left border-collapse" id="sc01-excel-table">
                                            <thead class="sticky top-0 bg-[#1B365D] text-white z-10 font-bold">
                                                <tr class="divide-x divide-slate-700 text-center">
                                                    <th class="py-2 px-2.5 whitespace-nowrap">구분</th>
                                                    <th class="py-2 px-2 whitespace-nowrap">법인</th>
                                                    <th class="py-2 px-3 text-left whitespace-nowrap">법인명</th>
                                                    <th class="py-2 px-2.5 text-right whitespace-nowrap bg-[#152a48]">유통재고 WOS</th>
                                                    <th class="py-2 px-2.5 whitespace-nowrap">재고 리스크 판정</th>
                                                    <th class="py-2 px-2.5 text-right whitespace-nowrap">유통재고(대)</th>
                                                    <th class="py-2 px-2.5 text-right whitespace-nowrap">신모델 재고(대)</th>
                                                    <th class="py-2 px-2.5 text-right whitespace-nowrap">Sell-out(대)</th>
                                                    <th class="py-2 px-2.5 text-right whitespace-nowrap">OLED 신모델(대)</th>
                                                    <th class="py-2 px-2.5 text-right whitespace-nowrap bg-[#224472]">① OLED 내 신모델</th>
                                                    <th class="py-2 px-2.5 text-right whitespace-nowrap bg-[#224472]">② 신모델 내 OLED</th>
                                                    <th class="py-2 px-2.5 text-right whitespace-nowrap bg-[#224472]">③ 전체TV 내 OLED신</th>
                                                    <th class="py-2 px-2.5 text-right whitespace-nowrap">신모델 WOS</th>
                                                    <th class="py-2 px-2.5 text-right whitespace-nowrap">구모델 WOS</th>
                                                </tr>
                                            </thead>
                                            <tbody class="divide-y divide-slate-200 font-mono-num" id="sc01-table-body">
                                                <!-- Row: LGERO -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGERO</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">루마니아 (LGERO)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">12.62주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">29,906</td>
                                                    <td class="py-1.5 px-2.5 text-right">22,931</td>
                                                    <td class="py-1.5 px-2.5 text-right">9,481</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,883</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">79.0%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">50.8%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">19.9%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">24.73주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">4.83주</td>
                                                </tr>
                                                <!-- Row: LGECK -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGECK</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">체코/슬로바키아 (LGECK)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">8.58주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">22,458</td>
                                                    <td class="py-1.5 px-2.5 text-right">20,956</td>
                                                    <td class="py-1.5 px-2.5 text-right">10,468</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,724</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">66.1%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">24.4%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">16.5%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">11.86주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">1.77주</td>
                                                </tr>
                                                <!-- Row: LGEFS -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGEFS</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">프랑스 (LGEFS)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">8.46주</td>
                                                    <td class="py-1.5 px-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">49,241</td>
                                                    <td class="py-1.5 px-2.5 text-right">43,217</td>
                                                    <td class="py-1.5 px-2.5 text-right">23,292</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">5,051</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">52.1%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">44.1%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">21.7%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">15.11주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">2.03주</td>
                                                </tr>
                                                <!-- Row: LGESW -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGESW</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">스웨덴/노르딕 (LGESW)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">8.44주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">44,396</td>
                                                    <td class="py-1.5 px-2.5 text-right">28,501</td>
                                                    <td class="py-1.5 px-2.5 text-right">21,032</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">2,262</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">40.6%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">25.5%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">10.8%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">12.85주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">5.23주</td>
                                                </tr>
                                                <!-- Row: LGEDG -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGEDG</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">독일 (LGEDG)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">8.01주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">77,793</td>
                                                    <td class="py-1.5 px-2.5 text-right">63,588</td>
                                                    <td class="py-1.5 px-2.5 text-right">38,837</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">11,426</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">57.2%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">44.1%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">29.4%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">9.82주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">4.39주</td>
                                                </tr>
                                                <!-- Row: LGEES -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGEES</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">스페인 (LGEES)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">7.73주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">91,671</td>
                                                    <td class="py-1.5 px-2.5 text-right">72,583</td>
                                                    <td class="py-1.5 px-2.5 text-right">47,443</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">3,551</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">70.6%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">9.5%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">7.5%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">7.75주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-rose-600 font-bold">7.65주</td>
                                                </tr>
                                                <!-- Row: LGEPL -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGEPL</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">폴란드 (LGEPL)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">7.35주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">24,183</td>
                                                    <td class="py-1.5 px-2.5 text-right">17,743</td>
                                                    <td class="py-1.5 px-2.5 text-right">13,157</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">2,149</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">37.9%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">55.9%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">16.3%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">18.45주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">2.77주</td>
                                                </tr>
                                                <!-- Row: LGEIS -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGEIS</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">이탈리아 (LGEIS)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">7.31주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">53,208</td>
                                                    <td class="py-1.5 px-2.5 text-right">29,204</td>
                                                    <td class="py-1.5 px-2.5 text-right">29,116</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">3,360</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">36.3%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">30.2%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">11.5%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">10.50주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">5.34주</td>
                                                </tr>
                                                <!-- Row: LGEHS -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGEHS</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">그리스 (LGEHS)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">7.24주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">14,469</td>
                                                    <td class="py-1.5 px-2.5 text-right">9,543</td>
                                                    <td class="py-1.5 px-2.5 text-right">7,991</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">486</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">36.8%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">15.7%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">6.1%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">12.32주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">4.03주</td>
                                                </tr>
                                                <!-- Row: LGEMK -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGEMK</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">헝가리 (LGEMK)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">7.03주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">55,383</td>
                                                    <td class="py-1.5 px-2.5 text-right">31,787</td>
                                                    <td class="py-1.5 px-2.5 text-right">31,501</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">3,177</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">70.5%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">22.4%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">10.1%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">8.96주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">5.45주</td>
                                                </tr>
                                                <!-- Row: LGEUK -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGEUK</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">영국 (LGEUK)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">6.39주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">120,916</td>
                                                    <td class="py-1.5 px-2.5 text-right">99,763</td>
                                                    <td class="py-1.5 px-2.5 text-right">75,696</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">8,425</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">65.5%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">16.0%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">11.1%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">7.58주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">3.67주</td>
                                                </tr>
                                                <!-- Row: LGELA -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGELA</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">라트비아/발틱 (LGELA)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">6.38주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">12,491</td>
                                                    <td class="py-1.5 px-2.5 text-right">5,891</td>
                                                    <td class="py-1.5 px-2.5 text-right">7,830</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,116</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">64.9%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">44.5%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">14.3%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">9.39주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">4.96주</td>
                                                </tr>
                                                <!-- Row: Swiss -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">Swiss</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">스위스 (Swiss)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">6.31주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">7,681</td>
                                                    <td class="py-1.5 px-2.5 text-right">3,615</td>
                                                    <td class="py-1.5 px-2.5 text-right">4,870</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">920</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">40.8%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">45.0%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">18.9%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-rose-600">7.07주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">5.76주</td>
                                                </tr>
                                                <!-- Row: LGEBN (Safe) -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-safe bg-slate-50/50" data-status="safe">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGEBN</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">베네룩스 (LGEBN)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-emerald-700 bg-emerald-50/40">5.74주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상 (3~6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">26,296</td>
                                                    <td class="py-1.5 px-2.5 text-right">18,626</td>
                                                    <td class="py-1.5 px-2.5 text-right">18,338</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">4,536</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">49.0%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">52.3%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">24.7%</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-700">8.58주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">3.18주</td>
                                                </tr>
                                                <!-- Row: LGEPT (Safe) -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-safe" data-status="safe">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGEPT</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">포르투갈 (LGEPT)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-emerald-700 bg-emerald-50/40">5.62주</td>
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상 (3~6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">17,888</td>
                                                    <td class="py-1.5 px-2.5 text-right">17,087</td>
                                                    <td class="py-1.5 px-2.5 text-right">12,740</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,260</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">88.6%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">13.6%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">9.9%</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-700">7.35주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">0.93주</td>
                                                </tr>
                                                <!-- Row: LGEAG (Safe) -->
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-safe bg-slate-50/50" data-status="safe">
                                                    <td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td>
                                                    <td class="py-1.5 px-2 text-center font-bold font-mono">LGEAG</td>
                                                    <td class="py-1.5 px-3 text-left font-sans text-slate-800">오스트리아 (LGEAG)</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-emerald-700 bg-emerald-50/40">4.23주</td>
                                                    <td class="py-1.5 px-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상 (3~6주)</span></td>
                                                    <td class="py-1.5 px-2.5 text-right">6,691</td>
                                                    <td class="py-1.5 px-2.5 text-right">2,173</td>
                                                    <td class="py-1.5 px-2.5 text-right">6,328</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-800">986</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">50.9%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">40.5%</td>
                                                    <td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">15.6%</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-700">3.57주</td>
                                                    <td class="py-1.5 px-2.5 text-right text-slate-500">4.64주</td>
                                                </tr>
                                                <!-- Row: EU Total -->
                                                <tr class="bg-slate-200/90 font-bold border-t-2 border-slate-400">
                                                    <td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-slate-800 text-white text-[10px]">본부 TTL</span></td>
                                                    <td class="py-2 px-2 text-center font-mono">EU</td>
                                                    <td class="py-2 px-3 text-left font-sans text-slate-900">유럽 본부 (EU TTL)</td>
                                                    <td class="py-2 px-2.5 text-right text-rose-800 font-mono text-xs">7.31주</td>
                                                    <td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-200 text-rose-900 text-[10px]">과다재고 (>6주)</span></td>
                                                    <td class="py-2 px-2.5 text-right">654,669</td>
                                                    <td class="py-2 px-2.5 text-right">487,207</td>
                                                    <td class="py-2 px-2.5 text-right">358,121</td>
                                                    <td class="py-2 px-2.5 text-right text-teal-900">52,312</td>
                                                    <td class="py-2 px-2.5 text-right text-teal-900">54.8%</td>
                                                    <td class="py-2 px-2.5 text-right text-teal-900">25.6%</td>
                                                    <td class="py-2 px-2.5 text-right text-teal-900">14.6%</td>
                                                    <td class="py-2 px-2.5 text-right text-rose-800">9.54주</td>
                                                    <td class="py-2 px-2.5 text-right text-slate-700">4.36주</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    <div class="text-[10.5px] text-slate-500 flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-slate-100">
                                        <span>* 기준: 2026년 9월 (9/21W 주차 실적 기준, 9/28W 조회). 출처: 06. KPI Sheet (26년_유럽+CIS_KPI_2026.xlsx)</span>
                                        <button type="button" onclick="downloadScenario01Excel()" class="text-emerald-700 font-bold hover:underline flex items-center gap-1">
                                            <span class="material-symbols-outlined text-xs">file_download</span>
                                            <span>서식 및 수식이 완비된 Excel 파일 (.xlsx) 다운로드</span>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>'''

# Check if component already injected
if 'id="sc01-result-drawer"' in html:
    print("Component already injected, updating existing section...")
    pattern_existing = r'<!-- Live Actionable Prompt Chip -->[\s\S]*?<!-- Scenario 2:'
    html = re.sub(pattern_existing, component_html + "\n                    </div>\n\n                    <!-- Scenario 2:", html, count=1)
else:
    print("Injecting new component into Scenario 01...")
    html = re.sub(target_pattern, component_html, html, count=1)

# Now check for JavaScript helper functions
js_code = f'''
    // Scenario 01 Live Execution Result Helpers
    const SC01_EXCEL_BASE64 = "{b64_excel}";

    function toggleScenario01Result() {{
        const drawer = document.getElementById('sc01-result-drawer');
        const icon = document.getElementById('sc01-toggle-icon');
        const text = document.getElementById('sc01-toggle-text');
        if (!drawer) return;

        const isHidden = drawer.classList.contains('hidden');
        if (isHidden) {{
            drawer.classList.remove('hidden');
            if (icon) icon.style.transform = 'rotate(180deg)';
            if (text) text.textContent = '답변 & 엑셀 접기';
        }} else {{
            drawer.classList.add('hidden');
            if (icon) icon.style.transform = 'rotate(0deg)';
            if (text) text.textContent = '답변 & 엑셀 열기';
        }}
    }}

    function switchScenario01Tab(tabName) {{
        const tabReport = document.getElementById('sc01-tab-report');
        const tabSheet = document.getElementById('sc01-tab-sheet');
        const btnReport = document.getElementById('sc01-btn-tab-report');
        const btnSheet = document.getElementById('sc01-btn-tab-sheet');

        if (tabName === 'report') {{
            if (tabReport) tabReport.classList.remove('hidden');
            if (tabSheet) tabSheet.classList.add('hidden');
            if (btnReport) {{
                btnReport.className = "px-3.5 py-1.5 rounded-lg text-xs font-bold bg-teal-600 text-white shadow-xs flex items-center gap-1.5 transition-all";
            }}
            if (btnSheet) {{
                btnSheet.className = "px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-1.5 transition-all";
            }}
        }} else {{
            if (tabReport) tabReport.classList.add('hidden');
            if (tabSheet) tabSheet.classList.remove('hidden');
            if (btnReport) {{
                btnReport.className = "px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-1.5 transition-all";
            }}
            if (btnSheet) {{
                btnSheet.className = "px-3.5 py-1.5 rounded-lg text-xs font-bold bg-teal-600 text-white shadow-xs flex items-center gap-1.5 transition-all";
            }}
        }}
    }}

    function filterScenario01Grid(type) {{
        const rows = document.querySelectorAll('#sc01-table-body tr');
        const btnAll = document.getElementById('sc01-filter-all');
        const btnRisk = document.getElementById('sc01-filter-risk');
        const btnSafe = document.getElementById('sc01-filter-safe');

        [btnAll, btnRisk, btnSafe].forEach(b => {{
            if (b) b.className = "px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium text-xs";
        }});

        if (type === 'all' && btnAll) btnAll.className = "px-2.5 py-1 rounded bg-slate-900 text-white font-bold text-xs shadow-2xs";
        if (type === 'risk' && btnRisk) btnRisk.className = "px-2.5 py-1 rounded bg-rose-600 text-white font-bold text-xs shadow-2xs";
        if (type === 'safe' && btnSafe) btnSafe.className = "px-2.5 py-1 rounded bg-emerald-600 text-white font-bold text-xs shadow-2xs";

        rows.forEach(r => {{
            const status = r.getAttribute('data-status');
            if (!status) return; // total row always show
            if (type === 'all') {{
                r.style.display = '';
            }} else if (type === 'risk') {{
                r.style.display = (status === 'risk') ? '' : 'none';
            }} else if (type === 'safe') {{
                r.style.display = (status === 'safe') ? '' : 'none';
            }}
        }});
    }}

    function downloadScenario01Excel() {{
        try {{
            const byteCharacters = atob(SC01_EXCEL_BASE64);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {{
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }}
            const byteArray = new Uint8Array(byteNumbers);
            const blob = new Blob([byteArray], {{ type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }});
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = '유럽_법인별_유통재고WOS_OLED신모델비중_요약.xlsx';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(link.href);
        }} catch (e) {{
            alert('엑셀 다운로드 중 오류가 발생했습니다: ' + e.message);
        }}
    }}
'''

if 'function toggleScenario01Result' not in html:
    # Append before </script> at the bottom
    last_script_idx = html.rfind('</script>')
    if last_script_idx != -1:
        html = html[:last_script_idx] + js_code + "\n" + html[last_script_idx:]
        print("Injected JS helper functions into HTML.")
else:
    # Replace existing JS function block if needed
    print("JS helper functions already present, replacing...")
    pattern_js = r'// Scenario 01 Live Execution Result Helpers[\s\S]*?function downloadScenario01Excel\(\) \{[\s\S]*?\}\s*\}'
    html = re.sub(pattern_js, js_code.strip(), html)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully updated AXIS_System_Architecture_Guide.html with Live Execution Result & Excel Viewer!")
