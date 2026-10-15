import os
import re

html_path = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\00. TV Europe Sales Management Portal\docs\AXIS_System_Architecture_Guide.html"
b64_path = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\scripts\excel_base64.txt"

with open(b64_path, "r", encoding="utf-8") as f:
    b64_excel = f.read().strip()

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Exact drawer HTML with verbatim user request results (masked A~P subsidiaries)
drawer_html = f'''<!-- Real Agent Execution Result Section (Interactive Drawer) -->
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
                                            <span>실제 답변 결과 (원문 무편집)</span>
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
                                        <span class="text-[11px] text-slate-400 hidden sm:inline">예제 보안: A~P 법인 가명 처리</span>
                                        <button type="button" 
                                                onclick="downloadScenario01Excel()"
                                                class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center gap-1.5 shadow-sm transition-all hover:scale-105 active:scale-95">
                                            <span class="material-symbols-outlined text-sm">download</span>
                                            <span>엑셀 원본 다운로드 (.xlsx)</span>
                                        </button>
                                    </div>
                                </div>

                                <!-- Tab 1: Verbatim AI Answer (Unedited Exact Text with A~P Masking) -->
                                <div id="sc01-tab-report" class="p-6 space-y-6 text-xs text-slate-700 leading-relaxed font-sans">
                                    
                                    <!-- Lead intro paragraph -->
                                    <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
                                        <p class="text-[12.5px] text-slate-800 leading-relaxed">
                                            유럽 16개 전체 법인 및 유럽 본부(EU TTL)의 <strong>공식 마스터 KPI 실적 데이터(9/21W 주차 실적 반영, 9/28W 조회 기준)</strong>를 바탕으로, <strong>유통재고 주수(WOS) 기준 리스크 법인(6주 초과 또는 3주 미만)</strong>을 선별하고 각 법인의 OLED 신모델 비중을 다각도로 비교 분석한 결과입니다.
                                        </p>
                                        <div class="mt-2 text-[11px] text-slate-500 flex items-center gap-2">
                                            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                                            <span>* 대외비 보안 정책에 의거하여 실제 법인명은 <strong>A 법인 ~ P 법인</strong>으로 가명 처리된 실전 예제입니다.</span>
                                        </div>
                                    </div>

                                    <!-- Section 1: Executive Summary -->
                                    <div class="space-y-3">
                                        <h4 class="text-sm font-bold text-slate-900 flex items-center gap-2 border-b border-slate-200 pb-2">
                                            <span class="text-base">📌</span>
                                            <span>1. 핵심 요약 (Executive Summary)</span>
                                        </h4>
                                        <div class="space-y-2.5 pl-1">
                                            <div>
                                                <strong class="text-slate-900 block mb-1">유럽 본부(EU TTL) 총괄 재고 현황:</strong>
                                                <ul class="list-disc pl-5 space-y-1 text-slate-700">
                                                    <li>유럽 전체 유통재고는 <strong>654,669대</strong>, 전체 WOS는 <strong>7.31주</strong>(신모델 9.54주, 구모델 4.36주)입니다.</li>
                                                    <li>Q4 성수기(블랙프라이데이/사이버먼데이/크리스마스) 진입을 앞두고 8~9월 신모델 초도 집중 선적(Sell-in)에 따라 유통 내 신모델 재고가 빌드업되어 유럽 전체 평균 WOS가 6주를 상회하고 있습니다.</li>
                                                </ul>
                                            </div>

                                            <div class="pt-1">
                                                <strong class="text-slate-900 block mb-1">리스크 법인 분류 결과 (WOS &gt; 6주 또는 &lt; 3주):</strong>
                                                <ul class="list-disc pl-5 space-y-1.5 text-slate-700">
                                                    <li><strong class="text-rose-700">과다 재고 리스크 (&gt; 6.0주) 법인:</strong> 유럽 16개 법인 중 <strong>총 13개 법인</strong>
                                                        <ul class="list-circle pl-5 mt-1 space-y-1 text-slate-600">
                                                            <li><span class="font-bold text-rose-800">심각 과다 (&gt;10주):</span> <strong>A 법인 (12.62주)</strong> &rarr; 신모델 WOS가 무려 <strong>24.73주</strong>(약 6개월분)로 유럽 최고 위험군.</li>
                                                            <li><span class="font-bold text-amber-800">고위험군 (8~9주):</span> <strong>B 법인 (8.58주)</strong>, <strong>C 법인 (8.46주)</strong>, <strong>D 법인 (8.44주)</strong>, <strong>E 법인 (8.01주)</strong></li>
                                                            <li><span class="font-bold text-slate-700">주의군 (6~8주):</span> <strong>F 법인 (7.73주)</strong>, <strong>G 법인 (7.35주)</strong>, <strong>H 법인 (7.31주)</strong>, <strong>I 법인 (7.24주)</strong>, <strong>J 법인 (7.03주)</strong>, <strong>K 법인 (6.39주)</strong>, <strong>L 법인 (6.38주)</strong>, <strong>M 법인 (6.31주)</strong></li>
                                                        </ul>
                                                    </li>
                                                    <li><strong class="text-amber-700">재고 부족 결품 리스크 (&lt; 3.0주) 법인:</strong> <strong>0개 법인</strong> (전체 TV 기준 결품 우려 법인 없음)</li>
                                                    <li><strong class="text-emerald-700">정상 범위 (3.0~6.0주) 법인:</strong> <strong>총 3개 법인</strong> (<strong>P 법인 4.23주</strong>, <strong>O 법인 5.62주</strong>, <strong>N 법인 5.74주</strong>)</li>
                                                </ul>
                                            </div>

                                            <div class="pt-1">
                                                <strong class="text-slate-900 block mb-1">OLED 신모델 비중 특이사항:</strong>
                                                <ul class="list-disc pl-5 space-y-1 text-slate-700">
                                                    <li><strong>E 법인:</strong> 전체 TV 판매(Sell-out)의 <strong class="text-teal-800">29.4%</strong>가 OLED 신모델이며, 신모델 판매 중 OLED 비중이 <strong class="text-teal-800">44.1%</strong>에 달해 유럽 최고 수준의 프리미엄 장악력을 보이고 있습니다.</li>
                                                    <li><strong>A 법인:</strong> WOS는 12.6주로 극단적 과다이나, OLED 판매 중 신모델 비중(<strong>79.0%</strong>) 및 신모델 중 OLED 비중(<strong>50.8%</strong>)이 매우 우수하여 4분기 판촉 드라이브 시 빠른 회전이 가능합니다.</li>
                                                    <li><strong>F 법인:</strong> 전체 WOS 7.73주 중 신모델 판매 내 OLED 비중이 <strong class="text-rose-700">9.5%</strong>에 불과하며, 구모델 WOS도 <strong>7.65주</strong>로 높아 구모델 잔여 재고와 보급형 LCD 편중의 이중 리스크에 직면해 있습니다.</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Section 2: Full Matrix Table -->
                                    <div class="space-y-3">
                                        <div class="flex items-center justify-between border-b border-slate-200 pb-2">
                                            <h4 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                                                <span class="text-base">📊</span>
                                                <span>2. 유럽 전 법인 유통재고 WOS 리스크 및 OLED 신모델 비중 비교표</span>
                                            </h4>
                                            <span class="text-[11px] text-slate-500">기준 시점: 2026년 9월 최신 (9/21W 주차 반영) | WOS 내림차순 정렬</span>
                                        </div>

                                        <div class="overflow-x-auto border border-slate-200 rounded-lg shadow-2xs">
                                            <table class="w-full text-[11px] text-left border-collapse font-mono-num">
                                                <thead class="bg-[#1B365D] text-white font-bold text-center">
                                                    <tr class="divide-x divide-slate-700">
                                                        <th class="py-2 px-2 whitespace-nowrap">구분</th>
                                                        <th class="py-2 px-2 whitespace-nowrap">법인코드</th>
                                                        <th class="py-2 px-3 text-left whitespace-nowrap">법인명</th>
                                                        <th class="py-2 px-2.5 text-right whitespace-nowrap bg-[#152a48]">유통재고 WOS</th>
                                                        <th class="py-2 px-2.5 whitespace-nowrap">리스크 판정</th>
                                                        <th class="py-2 px-2.5 text-right whitespace-nowrap">유통재고 (대)</th>
                                                        <th class="py-2 px-2.5 text-right whitespace-nowrap">Sell-out (대)</th>
                                                        <th class="py-2 px-2.5 text-right whitespace-nowrap">OLED 신모델 (대)</th>
                                                        <th class="py-2 px-2.5 text-right whitespace-nowrap bg-[#224472]">① OLED 내 신모델 비중</th>
                                                        <th class="py-2 px-2.5 text-right whitespace-nowrap bg-[#224472]">② 신모델 내 OLED 비중</th>
                                                        <th class="py-2 px-2.5 text-right whitespace-nowrap bg-[#224472]">③ 전체 TV 내 OLED 신모델</th>
                                                        <th class="py-2 px-2.5 text-right whitespace-nowrap">신모델 WOS</th>
                                                        <th class="py-2 px-2.5 text-right whitespace-nowrap">구모델 WOS</th>
                                                    </tr>
                                                </thead>
                                                <tbody class="divide-y divide-slate-200">
                                                    <tr class="hover:bg-teal-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">A</td><td class="py-1.5 px-3 font-sans text-slate-800">A 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">12.62주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">29,906</td><td class="py-1.5 px-2.5 text-right">9,481</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,883</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">79.0%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">50.8%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">19.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">24.73주</td><td class="py-1.5 px-2.5 text-right text-slate-500">4.83주</td></tr>
                                                    <tr class="hover:bg-teal-50/50 bg-slate-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">B</td><td class="py-1.5 px-3 font-sans text-slate-800">B 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">8.58주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">22,458</td><td class="py-1.5 px-2.5 text-right">10,468</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,724</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">66.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">24.4%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">16.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">11.86주</td><td class="py-1.5 px-2.5 text-right text-slate-500">1.77주</td></tr>
                                                    <tr class="hover:bg-teal-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">C</td><td class="py-1.5 px-3 font-sans text-slate-800">C 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">8.46주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">49,241</td><td class="py-1.5 px-2.5 text-right">23,292</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">5,051</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">52.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">44.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">21.7%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">15.11주</td><td class="py-1.5 px-2.5 text-right text-slate-500">2.03주</td></tr>
                                                    <tr class="hover:bg-teal-50/50 bg-slate-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">D</td><td class="py-1.5 px-3 font-sans text-slate-800">D 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">8.44주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">44,396</td><td class="py-1.5 px-2.5 text-right">21,032</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">2,262</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">40.6%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">25.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">10.8%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">12.85주</td><td class="py-1.5 px-2.5 text-right text-slate-500">5.23주</td></tr>
                                                    <tr class="hover:bg-teal-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">E</td><td class="py-1.5 px-3 font-sans text-slate-800">E 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">8.01주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">77,793</td><td class="py-1.5 px-2.5 text-right">38,837</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">11,426</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">57.2%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">44.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">29.4%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">9.82주</td><td class="py-1.5 px-2.5 text-right text-slate-500">4.39주</td></tr>
                                                    <tr class="hover:bg-teal-50/50 bg-slate-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">F</td><td class="py-1.5 px-3 font-sans text-slate-800">F 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">7.73주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">91,671</td><td class="py-1.5 px-2.5 text-right">47,443</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">3,551</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">70.6%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">9.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">7.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">7.75주</td><td class="py-1.5 px-2.5 text-right text-rose-600 font-bold">7.65주</td></tr>
                                                    <tr class="hover:bg-teal-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">G</td><td class="py-1.5 px-3 font-sans text-slate-800">G 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">7.35주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">24,183</td><td class="py-1.5 px-2.5 text-right">13,157</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">2,149</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">37.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">55.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">16.3%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">18.45주</td><td class="py-1.5 px-2.5 text-right text-slate-500">2.77주</td></tr>
                                                    <tr class="hover:bg-teal-50/50 bg-slate-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">H</td><td class="py-1.5 px-3 font-sans text-slate-800">H 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">7.31주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">53,208</td><td class="py-1.5 px-2.5 text-right">29,116</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">3,360</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">36.3%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">30.2%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">11.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">10.50주</td><td class="py-1.5 px-2.5 text-right text-slate-500">5.34주</td></tr>
                                                    <tr class="hover:bg-teal-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">I</td><td class="py-1.5 px-3 font-sans text-slate-800">I 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">7.24주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">14,469</td><td class="py-1.5 px-2.5 text-right">7,991</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">486</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">36.8%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">15.7%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">6.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">12.32주</td><td class="py-1.5 px-2.5 text-right text-slate-500">4.03주</td></tr>
                                                    <tr class="hover:bg-teal-50/50 bg-slate-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">J</td><td class="py-1.5 px-3 font-sans text-slate-800">J 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">7.03주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">55,383</td><td class="py-1.5 px-2.5 text-right">31,501</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">3,177</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">70.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">22.4%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">10.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">8.96주</td><td class="py-1.5 px-2.5 text-right text-slate-500">5.45주</td></tr>
                                                    <tr class="hover:bg-teal-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">K</td><td class="py-1.5 px-3 font-sans text-slate-800">K 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">6.39주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">120,916</td><td class="py-1.5 px-2.5 text-right">75,696</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">8,425</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">65.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">16.0%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">11.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">7.58주</td><td class="py-1.5 px-2.5 text-right text-slate-500">3.67주</td></tr>
                                                    <tr class="hover:bg-teal-50/50 bg-slate-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">L</td><td class="py-1.5 px-3 font-sans text-slate-800">L 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">6.38주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">12,491</td><td class="py-1.5 px-2.5 text-right">7,830</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,116</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">64.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">44.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">14.3%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">9.39주</td><td class="py-1.5 px-2.5 text-right text-slate-500">4.96주</td></tr>
                                                    <tr class="hover:bg-teal-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">M</td><td class="py-1.5 px-3 font-sans text-slate-800">M 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/30">6.31주</td><td class="py-1.5 px-2 text-center text-rose-700 font-medium">과다재고</td><td class="py-1.5 px-2.5 text-right">7,681</td><td class="py-1.5 px-2.5 text-right">4,870</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">920</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">40.8%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">45.0%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">18.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">7.07주</td><td class="py-1.5 px-2.5 text-right text-slate-500">5.76주</td></tr>
                                                    <tr class="hover:bg-teal-50/50 bg-slate-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">N</td><td class="py-1.5 px-3 font-sans text-slate-800">N 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-emerald-700 bg-emerald-50/30">5.74주</td><td class="py-1.5 px-2 text-center text-emerald-700 font-medium">정상 (3~6주)</td><td class="py-1.5 px-2.5 text-right">26,296</td><td class="py-1.5 px-2.5 text-right">18,338</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">4,536</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">49.0%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">52.3%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">24.7%</td><td class="py-1.5 px-2.5 text-right text-slate-700">8.58주</td><td class="py-1.5 px-2.5 text-right text-slate-500">3.18주</td></tr>
                                                    <tr class="hover:bg-teal-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">O</td><td class="py-1.5 px-3 font-sans text-slate-800">O 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-emerald-700 bg-emerald-50/30">5.62주</td><td class="py-1.5 px-2 text-center text-emerald-700 font-medium">정상 (3~6주)</td><td class="py-1.5 px-2.5 text-right">17,888</td><td class="py-1.5 px-2.5 text-right">12,740</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,260</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">88.6%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">13.6%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">9.9%</td><td class="py-1.5 px-2.5 text-right text-slate-700">7.35주</td><td class="py-1.5 px-2.5 text-right text-slate-500">0.93주</td></tr>
                                                    <tr class="hover:bg-teal-50/50 bg-slate-50/50"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">P</td><td class="py-1.5 px-3 font-sans text-slate-800">P 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-emerald-700 bg-emerald-50/30">4.23주</td><td class="py-1.5 px-2 text-center text-emerald-700 font-medium">정상 (3~6주)</td><td class="py-1.5 px-2.5 text-right">6,691</td><td class="py-1.5 px-2.5 text-right">6,328</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">986</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">50.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">40.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700">15.6%</td><td class="py-1.5 px-2.5 text-right text-slate-700">3.57주</td><td class="py-1.5 px-2.5 text-right text-slate-500">4.64주</td></tr>
                                                    <tr class="bg-slate-200/90 font-bold border-t-2 border-slate-400"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-slate-800 text-white text-[10px]">본부</span></td><td class="py-2 px-2 text-center font-mono">EU</td><td class="py-2 px-3 font-sans text-slate-900">유럽 본부 (EU 총괄)</td><td class="py-2 px-2.5 text-right text-rose-800 font-mono text-xs">7.31주</td><td class="py-2 px-2 text-center text-rose-900 font-bold">과다재고 (>6주)</td><td class="py-2 px-2.5 text-right">654,669</td><td class="py-2 px-2.5 text-right">358,121</td><td class="py-2 px-2.5 text-right text-teal-900">52,312</td><td class="py-2 px-2.5 text-right text-teal-900">54.8%</td><td class="py-2 px-2.5 text-right text-teal-900">25.6%</td><td class="py-2 px-2.5 text-right text-teal-900">14.6%</td><td class="py-2 px-2.5 text-right text-rose-800">9.54주</td><td class="py-2 px-2.5 text-right text-slate-700">4.36주</td></tr>
                                                </tbody>
                                            </table>
                                        </div>

                                        <div class="p-3 rounded bg-slate-50 border border-slate-200 text-[11px] text-slate-600 space-y-1">
                                            <div class="font-bold text-slate-700">[OLED 신모델 비중 지표 정의]</div>
                                            <div><strong>① OLED 내 신모델 비중:</strong> OLED 신모델 Sell-out / 전체 OLED Sell-out (OLED 세대교체율 / NPI 진척도)</div>
                                            <div><strong>② 신모델 내 OLED 비중:</strong> OLED 신모델 Sell-out / 전체 TV 신모델 Sell-out (신모델 믹스 중 OLED 프리미엄 집중도)</div>
                                            <div><strong>③ 전체 TV 내 OLED 신모델:</strong> OLED 신모델 Sell-out / 전체 TV Sell-out (전체 판매 볼륨 대비 기여율)</div>
                                        </div>
                                    </div>

                                    <!-- Section 3: Deep Diagnostics (Verbatim) -->
                                    <div class="space-y-3">
                                        <h4 class="text-sm font-bold text-slate-900 flex items-center gap-2 border-b border-slate-200 pb-2">
                                            <span class="text-base">🔍</span>
                                            <span>3. 심층 진단 및 법인 유형별 리스크 분석</span>
                                        </h4>
                                        <div class="space-y-3 pl-1">
                                            <!-- Cluster A -->
                                            <div class="p-3.5 rounded-lg bg-rose-50/70 border border-rose-200 space-y-1.5">
                                                <div class="font-bold text-rose-900 flex items-center gap-1.5">
                                                    <span>🚨</span>
                                                    <span>유형 A: 극단적 신모델 과잉 선적형 (A 법인, C 법인, G 법인, D 법인)</span>
                                                </div>
                                                <div class="text-slate-700 space-y-1 pl-4">
                                                    <div><strong>A 법인:</strong> 전체 WOS 12.62주 중 신모델 WOS가 24.73주에 달해 유통 내 신모델 재고 체류가 매우 심각합니다. 다만 신모델 내 OLED 비중이 50.8%로 프리미엄 잠재력이 높으므로, 공급(Sell-in)을 즉시 동결하고 메이저 리테일러 중심의 가을 판촉을 통해 셀아웃 회전율을 높여야 합니다.</div>
                                                    <div><strong>G 법인 & C 법인:</strong> 신모델 WOS가 각각 18.45주, 15.11주로 매우 높습니다. 반면 구모델 WOS는 각각 2.77주, 2.03주로 사실상 구모델 재고 소진은 마무리되었으므로, 신모델 프로모션 집중 지원을 통한 유통 출하 속도 조절이 필요합니다.</div>
                                                </div>
                                            </div>

                                            <!-- Cluster B -->
                                            <div class="p-3.5 rounded-lg bg-teal-50/70 border border-teal-200 space-y-1.5">
                                                <div class="font-bold text-teal-900 flex items-center gap-1.5">
                                                    <span>💎</span>
                                                    <span>유형 B: 프리미엄 OLED 신모델 주도형 (E 법인, M 법인, N 법인)</span>
                                                </div>
                                                <div class="text-slate-700 space-y-1 pl-4">
                                                    <div><strong>E 법인:</strong> WOS 8.01주(신모델 9.82주)로 6주를 상회하나, 전체 판매의 29.4%가 OLED 신모델(월 11,426대)로 유럽 최대 규모입니다. 10~11월 성수기 수요 선점을 위한 유통 재고 사전 확보(Build-up) 성격이 강하며, 회전율이 뒷받침되어 실질 리스크는 통제 가능한 수준입니다.</div>
                                                    <div><strong>M 법인:</strong> 전체 WOS 6.31주(신모델 7.07주, 구모델 5.76주)로 안정적인 흐름이며, 신모델 중 OLED 비중이 <strong>45.0%</strong>로 고수익 모델 중심의 양호한 믹스를 유지하고 있습니다.</div>
                                                </div>
                                            </div>

                                            <!-- Cluster C -->
                                            <div class="p-3.5 rounded-lg bg-amber-50/70 border border-amber-200 space-y-1.5">
                                                <div class="font-bold text-amber-900 flex items-center gap-1.5">
                                                    <span>⚠️</span>
                                                    <span>유형 C: 구모델 정체 + 저가형 편중형 (F 법인, H 법인, I 법인)</span>
                                                </div>
                                                <div class="text-slate-700 space-y-1 pl-4">
                                                    <div><strong>F 법인:</strong> 전체 WOS가 7.73주인 상태에서 구모델 WOS가 7.65주(19,088대)로 여전히 구모델이 대량 체류하고 있습니다. 신모델 판매 중 OLED 비중도 <strong>9.5%</strong>에 그쳐, 구모델 클리어런스 판촉과 OLED 진열 전환이 가장 시급한 법인입니다.</div>
                                                    <div><strong>H 법인:</strong> 전체 WOS 7.31주, OLED 내 신모델 비중이 <strong>36.3%</strong>로 유럽 내 최저 수준(구모델 OLED 판매 비중이 63.7%)입니다. 2026년형 C4/B4 신모델로의 전환 속도가 지연되고 있습니다.</div>
                                                </div>
                                            </div>
                                        </div>
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
                                        <table class="w-full text-[11px] text-left border-collapse font-mono-num" id="sc01-excel-table">
                                            <thead class="sticky top-0 bg-[#1B365D] text-white z-10 font-bold text-center">
                                                <tr class="divide-x divide-slate-700">
                                                    <th class="py-2 px-2 whitespace-nowrap">구분</th>
                                                    <th class="py-2 px-2 whitespace-nowrap">법인코드</th>
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
                                            <tbody class="divide-y divide-slate-200" id="sc01-table-body">
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">A</td><td class="py-1.5 px-3 font-sans text-slate-800">A 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">12.62주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">29,906</td><td class="py-1.5 px-2.5 text-right">22,931</td><td class="py-1.5 px-2.5 text-right">9,481</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,883</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">79.0%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">50.8%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">19.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">24.73주</td><td class="py-1.5 px-2.5 text-right text-slate-500">4.83주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">B</td><td class="py-1.5 px-3 font-sans text-slate-800">B 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">8.58주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">22,458</td><td class="py-1.5 px-2.5 text-right">20,956</td><td class="py-1.5 px-2.5 text-right">10,468</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,724</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">66.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">24.4%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">16.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">11.86주</td><td class="py-1.5 px-2.5 text-right text-slate-500">1.77주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">C</td><td class="py-1.5 px-3 font-sans text-slate-800">C 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">8.46주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">49,241</td><td class="py-1.5 px-2.5 text-right">43,217</td><td class="py-1.5 px-2.5 text-right">23,292</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">5,051</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">52.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">44.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">21.7%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">15.11주</td><td class="py-1.5 px-2.5 text-right text-slate-500">2.03주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">D</td><td class="py-1.5 px-3 font-sans text-slate-800">D 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">8.44주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">44,396</td><td class="py-1.5 px-2.5 text-right">28,501</td><td class="py-1.5 px-2.5 text-right">21,032</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">2,262</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">40.6%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">25.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">10.8%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">12.85주</td><td class="py-1.5 px-2.5 text-right text-slate-500">5.23주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">E</td><td class="py-1.5 px-3 font-sans text-slate-800">E 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">8.01주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">77,793</td><td class="py-1.5 px-2.5 text-right">63,588</td><td class="py-1.5 px-2.5 text-right">38,837</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">11,426</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">57.2%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">44.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">29.4%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">9.82주</td><td class="py-1.5 px-2.5 text-right text-slate-500">4.39주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">F</td><td class="py-1.5 px-3 font-sans text-slate-800">F 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">7.73주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">91,671</td><td class="py-1.5 px-2.5 text-right">72,583</td><td class="py-1.5 px-2.5 text-right">47,443</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">3,551</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">70.6%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">9.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">7.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">7.75주</td><td class="py-1.5 px-2.5 text-right text-rose-600 font-bold">7.65주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">G</td><td class="py-1.5 px-3 font-sans text-slate-800">G 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">7.35주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">24,183</td><td class="py-1.5 px-2.5 text-right">17,743</td><td class="py-1.5 px-2.5 text-right">13,157</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">2,149</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">37.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">55.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">16.3%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">18.45주</td><td class="py-1.5 px-2.5 text-right text-slate-500">2.77주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">H</td><td class="py-1.5 px-3 font-sans text-slate-800">H 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">7.31주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">53,208</td><td class="py-1.5 px-2.5 text-right">29,204</td><td class="py-1.5 px-2.5 text-right">29,116</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">3,360</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">36.3%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">30.2%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">11.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">10.50주</td><td class="py-1.5 px-2.5 text-right text-slate-500">5.34주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">I</td><td class="py-1.5 px-3 font-sans text-slate-800">I 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">7.24주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">14,469</td><td class="py-1.5 px-2.5 text-right">9,543</td><td class="py-1.5 px-2.5 text-right">7,991</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">486</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">36.8%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">15.7%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">6.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">12.32주</td><td class="py-1.5 px-2.5 text-right text-slate-500">4.03주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">J</td><td class="py-1.5 px-3 font-sans text-slate-800">J 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">7.03주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">55,383</td><td class="py-1.5 px-2.5 text-right">31,787</td><td class="py-1.5 px-2.5 text-right">31,501</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">3,177</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">70.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">22.4%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">10.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">8.96주</td><td class="py-1.5 px-2.5 text-right text-slate-500">5.45주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">K</td><td class="py-1.5 px-3 font-sans text-slate-800">K 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">6.39주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">120,916</td><td class="py-1.5 px-2.5 text-right">99,763</td><td class="py-1.5 px-2.5 text-right">75,696</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">8,425</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">65.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">16.0%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">11.1%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">7.58주</td><td class="py-1.5 px-2.5 text-right text-slate-500">3.67주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk bg-slate-50/50" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">L</td><td class="py-1.5 px-3 font-sans text-slate-800">L 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">6.38주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">12,491</td><td class="py-1.5 px-2.5 text-right">5,891</td><td class="py-1.5 px-2.5 text-right">7,830</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,116</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">64.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">44.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">14.3%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">9.39주</td><td class="py-1.5 px-2.5 text-right text-slate-500">4.96주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-risk" data-status="risk"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">M</td><td class="py-1.5 px-3 font-sans text-slate-800">M 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-700 bg-rose-50/40">6.31주</td><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">과다재고 (>6주)</span></td><td class="py-1.5 px-2.5 text-right">7,681</td><td class="py-1.5 px-2.5 text-right">3,615</td><td class="py-1.5 px-2.5 text-right">4,870</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">920</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">40.8%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">45.0%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">18.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-rose-600">7.07주</td><td class="py-1.5 px-2.5 text-right text-slate-500">5.76주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-safe bg-slate-50/50" data-status="safe"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">N</td><td class="py-1.5 px-3 font-sans text-slate-800">N 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-emerald-700 bg-emerald-50/40">5.74주</td><td class="py-1.5 px-2 text-center text-emerald-700 font-medium">정상 (3~6주)</td><td class="py-1.5 px-2.5 text-right">26,296</td><td class="py-1.5 px-2.5 text-right">18,626</td><td class="py-1.5 px-2.5 text-right">18,338</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">4,536</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">49.0%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">52.3%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">24.7%</td><td class="py-1.5 px-2.5 text-right text-slate-700">8.58주</td><td class="py-1.5 px-2.5 text-right text-slate-500">3.18주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-safe" data-status="safe"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">O</td><td class="py-1.5 px-3 font-sans text-slate-800">O 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-emerald-700 bg-emerald-50/40">5.62주</td><td class="py-1.5 px-2 text-center text-emerald-700 font-medium">정상 (3~6주)</td><td class="py-1.5 px-2.5 text-right">17,888</td><td class="py-1.5 px-2.5 text-right">17,087</td><td class="py-1.5 px-2.5 text-right">12,740</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">1,260</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">88.6%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">13.6%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">9.9%</td><td class="py-1.5 px-2.5 text-right text-slate-700">7.35주</td><td class="py-1.5 px-2.5 text-right text-slate-500">0.93주</td></tr>
                                                <tr class="hover:bg-teal-50/50 transition-colors sc01-row-safe bg-slate-50/50" data-status="safe"><td class="py-1.5 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td><td class="py-1.5 px-2 text-center font-bold font-mono">P</td><td class="py-1.5 px-3 font-sans text-slate-800">P 법인</td><td class="py-1.5 px-2.5 text-right font-bold text-emerald-700 bg-emerald-50/40">4.23주</td><td class="py-1.5 px-2 text-center text-emerald-700 font-medium">정상 (3~6주)</td><td class="py-1.5 px-2.5 text-right">6,691</td><td class="py-1.5 px-2.5 text-right">2,173</td><td class="py-1.5 px-2.5 text-right">6,328</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-800">986</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">50.9%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">40.5%</td><td class="py-1.5 px-2.5 text-right font-bold text-teal-700 bg-teal-50/30">15.6%</td><td class="py-1.5 px-2.5 text-right text-slate-700">3.57주</td><td class="py-1.5 px-2.5 text-right text-slate-500">4.64주</td></tr>
                                                <tr class="bg-slate-200/90 font-bold border-t-2 border-slate-400"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-slate-800 text-white text-[10px]">본부</span></td><td class="py-2 px-2 text-center font-mono">EU</td><td class="py-2 px-3 font-sans text-slate-900">유럽 본부 (EU 총괄)</td><td class="py-2 px-2.5 text-right text-rose-800 font-mono text-xs">7.31주</td><td class="py-2 px-2 text-center text-rose-900 font-bold">과다재고 (>6주)</td><td class="py-2 px-2.5 text-right">654,669</td><td class="py-2 px-2.5 text-right">487,207</td><td class="py-2 px-2.5 text-right">358,121</td><td class="py-2 px-2.5 text-right text-teal-900">52,312</td><td class="py-2 px-2.5 text-right text-teal-900">54.8%</td><td class="py-2 px-2.5 text-right text-teal-900">25.6%</td><td class="py-2 px-2.5 text-right text-teal-900">14.6%</td><td class="py-2 px-2.5 text-right text-rose-800">9.54주</td><td class="py-2 px-2.5 text-right text-slate-700">4.36주</td></tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    <div class="text-[10.5px] text-slate-500 flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-slate-100">
                                        <span>* 기준: 2026년 9월 (9/21W 주차 실적 기준, 9/28W 조회). 대외비 보호를 위해 법인명 A~P 법인으로 가명 처리됨.</span>
                                        <button type="button" onclick="downloadScenario01Excel()" class="text-emerald-700 font-bold hover:underline flex items-center gap-1">
                                            <span class="material-symbols-outlined text-xs">file_download</span>
                                            <span>가명화 적용 Excel 파일 (.xlsx) 다운로드</span>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>'''

# Replace existing drawer component in html
pattern_existing = r'<!-- Real Agent Execution Result Section \(Interactive Drawer\) -->[\s\S]*?<!-- Scenario 2:'
if 'id="sc01-result-drawer"' in html:
    html = re.sub(pattern_existing, drawer_html + "\n                    </div>\n\n                    <!-- Scenario 2:", html, count=1)
    print("Replaced existing drawer with masked verbatim version.")
else:
    target_pattern = r'(<!-- Live Actionable Prompt Chip -->[\s\S]*?content_copy</span>\s*</div>\s*</div>)'
    html = re.sub(target_pattern, r'\1' + "\n\n" + drawer_html, html, count=1)
    print("Injected masked verbatim drawer into Scenario 01.")

# Update the Base64 constant in JavaScript
pattern_js_b64 = r'const SC01_EXCEL_BASE64 = "[^"]*";'
replacement_js_b64 = f'const SC01_EXCEL_BASE64 = "{b64_excel}";'
html = re.sub(pattern_js_b64, replacement_js_b64, html)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully updated AXIS_System_Architecture_Guide.html with verbatim masked output and new Base64 excel!")
