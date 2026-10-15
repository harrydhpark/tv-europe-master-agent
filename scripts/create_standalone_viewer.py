import os

b64_path = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\scripts\excel_base64.txt"
with open(b64_path, "r", encoding="utf-8") as f:
    b64_excel = f.read().strip()

viewer_path = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\00. TV Europe Sales Management Portal\docs\scenario_01_result_viewer.html"

viewer_html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>시나리오 01 실전 답변 및 엑셀 결과 - AXIS Master AI Agent</title>
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Sans+KR:wght@300;400;500;700&family=Noto+Serif+KR:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..700&display=swap" rel="stylesheet">
    
    <!-- Icons -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    <link href="https://cdn.jsdelivr.net/npm/remixicon@4.3.0/fonts/remixicon.css" rel="stylesheet" />

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Inter', 'Noto Sans KR', 'sans-serif'],
                        headline: ['Source Serif 4', 'Noto Serif KR', 'serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    }},
                    colors: {{
                        primary: '#1B365D',
                        secondary: '#008080',
                    }}
                }}
            }}
        }}
    </script>

    <style>
        body {{
            background-color: #F8FAFC;
            color: #1E293B;
            font-family: 'Inter', 'Noto Sans KR', sans-serif;
            -webkit-font-smoothing: antialiased;
        }}
        .font-mono-num {{
            font-family: 'JetBrains Mono', monospace;
            font-variant-numeric: tabular-nums;
        }}
        /* Strict table header styles to completely prevent dark background text bug */
        table.custom-matrix-table th {{
            background-color: #1B365D !important;
            color: #FFFFFF !important;
            font-size: 0.72rem !important;
            font-weight: 700 !important;
            text-transform: none !important;
            letter-spacing: normal !important;
            border-bottom: 2px solid #0F2027 !important;
            line-height: 1.35 !important;
        }}
        table.custom-matrix-table th.th-highlight {{
            background-color: #244677 !important;
            color: #FFFFFF !important;
        }}
        table.custom-matrix-table td {{
            font-size: 0.72rem !important;
            border-color: #E2E8F0 !important;
        }}
    </style>
</head>
<body class="bg-slate-50 min-h-screen pb-16">

    <!-- Top Fixed Navigation Bar -->
    <header class="sticky top-0 z-50 bg-[#051c2c] text-white border-b border-slate-700/80 shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between gap-4">
            
            <!-- Left: Back Button & Context Info -->
            <div class="flex items-center gap-3">
                <button type="button" 
                        onclick="returnToGuide()"
                        class="px-3 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold flex items-center gap-1.5 transition-all shadow-xs hover:scale-105 active:scale-95 group">
                    <span class="material-symbols-outlined text-base group-hover:-translate-x-0.5 transition-transform">arrow_back</span>
                    <span>가이드로 돌아가기</span>
                </button>
                <div class="h-4 w-px bg-slate-700 hidden sm:block"></div>
                <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded bg-teal-900/80 text-teal-300 text-[10px] font-bold border border-teal-700/60 hidden md:inline">실전 질의 시나리오 01</span>
                    <h1 class="text-sm font-bold text-white tracking-tight truncate">주간 유통재고 주수(WOS) 리스크 진단 & OLED 신모델 비중 실전 답변</h1>
                </div>
            </div>

            <!-- Right: Actions -->
            <div class="flex items-center gap-2">
                <button type="button" 
                        onclick="downloadScenarioExcel()"
                        class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center gap-1.5 shadow-sm transition-all hover:scale-105 active:scale-95">
                    <span class="material-symbols-outlined text-sm">download</span>
                    <span class="hidden sm:inline">엑셀 원본 다운로드 (.xlsx)</span>
                    <span class="sm:hidden">엑셀 (.xlsx)</span>
                </button>
                <button type="button" 
                        onclick="window.print()"
                        class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-medium flex items-center gap-1 transition-all border border-slate-700">
                    <span class="material-symbols-outlined text-sm">print</span>
                    <span class="hidden md:inline">인쇄 / PDF</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 pt-6 space-y-6">
        
        <!-- Breadcrumb & Title Banner -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-6 space-y-3">
            <div class="flex items-center gap-2 text-xs text-slate-500">
                <span>AXIS 시스템 가이드</span>
                <span class="material-symbols-outlined text-xs">chevron_right</span>
                <span>6. 실무 활용 방안 & 시나리오</span>
                <span class="material-symbols-outlined text-xs">chevron_right</span>
                <span class="font-bold text-teal-700">시나리오 01 실전 답변 상세 결과</span>
            </div>
            <div class="flex flex-wrap items-center justify-between gap-3">
                <div>
                    <h2 class="text-xl font-headline font-bold text-slate-900">주간 권역/법인별 출하 진척률 및 유통 재고 주수(WOS) 점검 실전 결과</h2>
                    <p class="text-xs text-slate-600 mt-1">마스터 에이전트에게 실제 질의하여 산출된 AI 총괄 브리핑 및 유럽 16개국 전수 정밀 매트릭스 표 원문입니다.</p>
                </div>
                <div class="flex items-center gap-2 text-xs bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span class="text-slate-600">소요 시간: <strong class="text-teal-700 font-mono">4.8초</strong></span>
                    <span class="text-slate-300">|</span>
                    <span class="text-slate-600">기준: <strong class="text-slate-800">9/21W 주차 실적 (06. KPI Sheet)</strong></span>
                </div>
            </div>

            <!-- Original Query Chip -->
            <div class="p-3 rounded-lg bg-teal-50/50 border border-teal-100 flex items-center justify-between text-xs font-mono text-slate-800 gap-2">
                <div class="flex items-center gap-2 truncate">
                    <span class="px-2 py-0.5 rounded bg-teal-600 text-white text-[10px] font-bold font-sans">실전 질의</span>
                    <span class="truncate">"유럽 전 법인 중 WOS 6주 초과 또는 3주 미만 리스크 법인 목록과 OLED 신모델 비중 요약해줘"</span>
                </div>
                <span class="px-2 py-0.5 rounded bg-slate-200/80 text-slate-700 text-[10px] font-sans font-medium whitespace-nowrap">예제 보안: A~P 법인 가명 처리</span>
            </div>
        </div>

        <!-- Section 1: Executive Summary -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-6 space-y-4">
            <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2 border-b border-slate-100 pb-3">
                <span class="text-base">📌</span>
                <span>1. 핵심 요약 (Executive Summary)</span>
            </h3>
            
            <div class="space-y-4 text-xs text-slate-700 leading-relaxed">
                <div class="space-y-1.5">
                    <strong class="text-slate-900 block font-bold text-[13px]">유럽 본부(EU TTL) 총괄 재고 현황:</strong>
                    <ul class="list-disc pl-5 space-y-1">
                        <li>유럽 전체 유통재고는 <strong>654,669대</strong>, 전체 WOS는 <strong>7.31주</strong>(신모델 9.54주, 구모델 4.36주)입니다.</li>
                        <li>Q4 성수기(블랙프라이데이/사이버먼데이/크리스마스) 진입을 앞두고 8~9월 신모델 초도 집중 선적(Sell-in)에 따라 유통 내 신모델 재고가 빌드업되어 유럽 전체 평균 WOS가 6주를 상회하고 있습니다.</li>
                    </ul>
                </div>

                <div class="space-y-2 pt-2 border-t border-slate-100">
                    <strong class="text-slate-900 block font-bold text-[13px]">리스크 법인 분류 결과 (WOS &gt; 6주 또는 &lt; 3주):</strong>
                    <ul class="list-disc pl-5 space-y-2">
                        <li><strong class="text-rose-700 font-bold">과다 재고 리스크 (&gt; 6.0주) 법인:</strong> 유럽 16개 법인 중 <strong>총 13개 법인</strong>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-2.5 mt-2">
                                <div class="p-3 rounded-lg bg-rose-50/70 border border-rose-200 space-y-1">
                                    <div class="font-bold text-rose-900 flex items-center justify-between text-[11px]">
                                        <span>🚨 심각 과다 (&gt;10주)</span>
                                        <span class="px-1.5 py-0.2 rounded bg-rose-200 text-rose-800 text-[10px]">최고위험</span>
                                    </div>
                                    <p class="text-[11.5px] text-slate-700"><strong>A 법인 (12.62주)</strong> &rarr; 신모델 WOS가 무려 <strong>24.73주</strong>(약 6개월분)로 유럽 최고 위험군.</p>
                                </div>
                                <div class="p-3 rounded-lg bg-amber-50/70 border border-amber-200 space-y-1">
                                    <div class="font-bold text-amber-900 text-[11px]">⚠️ 고위험군 (8~9주)</div>
                                    <p class="text-[11.5px] text-slate-700"><strong>B 법인 (8.58주)</strong>, <strong>C 법인 (8.46주)</strong>, <strong>D 법인 (8.44주)</strong>, <strong>E 법인 (8.01주)</strong></p>
                                </div>
                                <div class="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-1">
                                    <div class="font-bold text-slate-800 text-[11px]">📋 주의군 (6~8주)</div>
                                    <p class="text-[11.5px] text-slate-700"><strong>F 법인 (7.73주)</strong>, <strong>G 법인 (7.35주)</strong>, <strong>H 법인 (7.31주)</strong>, <strong>I 법인 (7.24주)</strong>, <strong>J 법인 (7.03주)</strong>, <strong>K 법인 (6.39주)</strong>, <strong>L 법인 (6.38주)</strong>, <strong>M 법인 (6.31주)</strong></p>
                                </div>
                            </div>
                        </li>
                        <li><strong class="text-amber-700 font-bold">재고 부족 결품 리스크 (&lt; 3.0주) 법인:</strong> <strong>0개 법인</strong> (전체 TV 기준 결품 우려 법인 없음)</li>
                        <li><strong class="text-emerald-700 font-bold">정상 범위 (3.0~6.0주) 법인:</strong> <strong>총 3개 법인</strong> (<strong>P 법인 4.23주</strong>, <strong>O 법인 5.62주</strong>, <strong>N 법인 5.74주</strong>)</li>
                    </ul>
                </div>

                <div class="space-y-1.5 pt-2 border-t border-slate-100">
                    <strong class="text-slate-900 block font-bold text-[13px]">OLED 신모델 비중 특이사항:</strong>
                    <ul class="list-disc pl-5 space-y-1">
                        <li><strong>E 법인:</strong> 전체 TV 판매(Sell-out)의 <strong class="text-teal-800 font-bold">29.4%</strong>가 OLED 신모델이며, 신모델 판매 중 OLED 비중이 <strong class="text-teal-800 font-bold">44.1%</strong>에 달해 유럽 최고 수준의 프리미엄 장악력을 보이고 있습니다.</li>
                        <li><strong>A 법인:</strong> WOS는 12.6주로 극단적 과다이나, OLED 판매 중 신모델 비중(<strong>79.0%</strong>) 및 신모델 중 OLED 비중(<strong>50.8%</strong>)이 매우 우수하여 4분기 판촉 드라이브 시 빠른 회전이 가능합니다.</li>
                        <li><strong>F 법인:</strong> 전체 WOS 7.73주 중 신모델 판매 내 OLED 비중이 <strong class="text-rose-700 font-bold">9.5%</strong>에 불과하며, 구모델 WOS도 <strong>7.65주</strong>로 높아 구모델 잔여 재고와 보급형 LCD 편중의 이중 리스크에 직면해 있습니다.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Section 2: Full Matrix Table -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-6 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
                <div>
                    <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                        <span class="text-base">📊</span>
                        <span>2. 유럽 전 법인 유통재고 WOS 리스크 및 OLED 신모델 비중 비교표</span>
                    </h3>
                    <p class="text-[11px] text-slate-500 mt-0.5">기준 시점: 2026년 9월 최신 (9/21W 주차 실판매·유통재고 반영, 9/28W 조회 기준) | WOS 내림차순 정렬</p>
                </div>
                <!-- Filter Chips -->
                <div class="flex items-center gap-1.5 text-xs">
                    <span class="text-slate-500 font-medium">필터:</span>
                    <button type="button" id="btn-filter-all" onclick="filterTable('all')" class="px-2.5 py-1 rounded bg-slate-900 text-white font-bold text-xs shadow-2xs">전체 (17)</button>
                    <button type="button" id="btn-filter-risk" onclick="filterTable('risk')" class="px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium text-xs">과다재고 리스크 (13)</button>
                    <button type="button" id="btn-filter-safe" onclick="filterTable('safe')" class="px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium text-xs">정상 (3)</button>
                </div>
            </div>

            <!-- Table Container (Strict styles, NO black background text bug) -->
            <div class="overflow-x-auto border border-slate-200 rounded-lg shadow-2xs">
                <table class="w-full text-left border-collapse custom-matrix-table font-mono-num">
                    <thead>
                        <tr class="divide-x divide-slate-700 text-center">
                            <th class="py-2.5 px-2 whitespace-nowrap">구분</th>
                            <th class="py-2.5 px-2 whitespace-nowrap">법인코드</th>
                            <th class="py-2.5 px-3 text-left whitespace-nowrap font-sans">법인명</th>
                            <th class="py-2.5 px-3 text-right whitespace-nowrap th-highlight">유통재고 WOS</th>
                            <th class="py-2.5 px-2.5 whitespace-nowrap">리스크 판정</th>
                            <th class="py-2.5 px-2.5 text-right whitespace-nowrap">유통재고 (대)</th>
                            <th class="py-2.5 px-2.5 text-right whitespace-nowrap">Sell-out (대)</th>
                            <th class="py-2.5 px-2.5 text-right whitespace-nowrap">OLED 신모델 (대)</th>
                            <th class="py-2.5 px-2.5 text-right whitespace-nowrap th-highlight">① OLED 내 신모델 비중</th>
                            <th class="py-2.5 px-2.5 text-right whitespace-nowrap th-highlight">② 신모델 내 OLED 비중</th>
                            <th class="py-2.5 px-2.5 text-right whitespace-nowrap th-highlight">③ 전체 TV 내 OLED 신모델</th>
                            <th class="py-2.5 px-2.5 text-right whitespace-nowrap">신모델 WOS</th>
                            <th class="py-2.5 px-2.5 text-right whitespace-nowrap">구모델 WOS</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200" id="matrix-tbody">
                        <tr class="hover:bg-teal-50/50 transition-colors" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">A</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">A 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">12.62주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">29,906</td><td class="py-2 px-2.5 text-right">9,481</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">1,883</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">79.0%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">50.8%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">19.9%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">24.73주</td><td class="py-2 px-2.5 text-right text-slate-500">4.83주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors bg-slate-50/50" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">B</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">B 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">8.58주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">22,458</td><td class="py-2 px-2.5 text-right">10,468</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">1,724</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">66.1%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">24.4%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">16.5%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">11.86주</td><td class="py-2 px-2.5 text-right text-slate-500">1.77주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">C</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">C 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">8.46주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">49,241</td><td class="py-2 px-2.5 text-right">23,292</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">5,051</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">52.1%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">44.1%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">21.7%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">15.11주</td><td class="py-2 px-2.5 text-right text-slate-500">2.03주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors bg-slate-50/50" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">D</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">D 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">8.44주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">44,396</td><td class="py-2 px-2.5 text-right">21,032</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">2,262</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">40.6%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">25.5%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">10.8%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">12.85주</td><td class="py-2 px-2.5 text-right text-slate-500">5.23주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">E</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">E 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">8.01주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">77,793</td><td class="py-2 px-2.5 text-right">38,837</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">11,426</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">57.2%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">44.1%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">29.4%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">9.82주</td><td class="py-2 px-2.5 text-right text-slate-500">4.39주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors bg-slate-50/50" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">F</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">F 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">7.73주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">91,671</td><td class="py-2 px-2.5 text-right">47,443</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">3,551</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">70.6%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">9.5%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">7.5%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">7.75주</td><td class="py-2 px-2.5 text-right text-rose-600 font-bold">7.65주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">G</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">G 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">7.35주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">24,183</td><td class="py-2 px-2.5 text-right">13,157</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">2,149</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">37.9%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">55.9%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">16.3%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">18.45주</td><td class="py-2 px-2.5 text-right text-slate-500">2.77주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors bg-slate-50/50" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">H</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">H 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">7.31주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">53,208</td><td class="py-2 px-2.5 text-right">29,116</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">3,360</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">36.3%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">30.2%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">11.5%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">10.50주</td><td class="py-2 px-2.5 text-right text-slate-500">5.34주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">I</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">I 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">7.24주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">14,469</td><td class="py-2 px-2.5 text-right">7,991</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">486</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">36.8%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">15.7%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">6.1%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">12.32주</td><td class="py-2 px-2.5 text-right text-slate-500">4.03주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors bg-slate-50/50" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">J</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">J 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">7.03주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">55,383</td><td class="py-2 px-2.5 text-right">31,501</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">3,177</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">70.5%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">22.4%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">10.1%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">8.96주</td><td class="py-2 px-2.5 text-right text-slate-500">5.45주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">K</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">K 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">6.39주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">120,916</td><td class="py-2 px-2.5 text-right">75,696</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">8,425</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">65.5%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">16.0%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">11.1%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">7.58주</td><td class="py-2 px-2.5 text-right text-slate-500">3.67주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors bg-slate-50/50" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">L</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">L 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">6.38주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">12,491</td><td class="py-2 px-2.5 text-right">7,830</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">1,116</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">64.9%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">44.5%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">14.3%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">9.39주</td><td class="py-2 px-2.5 text-right text-slate-500">4.96주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors" data-status="risk"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold text-[10px]">★ 리스크</span></td><td class="py-2 px-2 text-center font-bold font-mono">M</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">M 법인</td><td class="py-2 px-3 text-right font-bold text-rose-700 bg-rose-50/40">6.31주</td><td class="py-2 px-2.5 text-center text-rose-700 font-medium">과다재고</td><td class="py-2 px-2.5 text-right">7,681</td><td class="py-2 px-2.5 text-right">4,870</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">920</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">40.8%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">45.0%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">18.9%</td><td class="py-2 px-2.5 text-right font-bold text-rose-600">7.07주</td><td class="py-2 px-2.5 text-right text-slate-500">5.76주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors bg-slate-50/50" data-status="safe"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td><td class="py-2 px-2 text-center font-bold font-mono">N</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">N 법인</td><td class="py-2 px-3 text-right font-bold text-emerald-700 bg-emerald-50/40">5.74주</td><td class="py-2 px-2.5 text-center text-emerald-700 font-medium">정상 (3~6주)</td><td class="py-2 px-2.5 text-right">26,296</td><td class="py-2 px-2.5 text-right">18,338</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">4,536</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">49.0%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">52.3%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">24.7%</td><td class="py-2 px-2.5 text-right text-slate-700">8.58주</td><td class="py-2 px-2.5 text-right text-slate-500">3.18주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors" data-status="safe"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td><td class="py-2 px-2 text-center font-bold font-mono">O</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">O 법인</td><td class="py-2 px-3 text-right font-bold text-emerald-700 bg-emerald-50/40">5.62주</td><td class="py-2 px-2.5 text-center text-emerald-700 font-medium">정상 (3~6주)</td><td class="py-2 px-2.5 text-right">17,888</td><td class="py-2 px-2.5 text-right">12,740</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">1,260</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">88.6%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">13.6%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">9.9%</td><td class="py-2 px-2.5 text-right text-slate-700">7.35주</td><td class="py-2 px-2.5 text-right text-slate-500">0.93주</td></tr>
                        <tr class="hover:bg-teal-50/50 transition-colors bg-slate-50/50" data-status="safe"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">정상</span></td><td class="py-2 px-2 text-center font-bold font-mono">P</td><td class="py-2 px-3 font-sans text-slate-800 font-medium">P 법인</td><td class="py-2 px-3 text-right font-bold text-emerald-700 bg-emerald-50/40">4.23주</td><td class="py-2 px-2.5 text-center text-emerald-700 font-medium">정상 (3~6주)</td><td class="py-2 px-2.5 text-right">6,691</td><td class="py-2 px-2.5 text-right">6,328</td><td class="py-2 px-2.5 text-right font-bold text-teal-800">986</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">50.9%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">40.5%</td><td class="py-2 px-2.5 text-right font-bold text-teal-700 bg-teal-50/20">15.6%</td><td class="py-2 px-2.5 text-right text-slate-700">3.57주</td><td class="py-2 px-2.5 text-right text-slate-500">4.64주</td></tr>
                        <tr class="bg-slate-200/90 font-bold border-t-2 border-slate-400"><td class="py-2 px-2 text-center"><span class="px-1.5 py-0.5 rounded bg-slate-800 text-white text-[10px]">본부</span></td><td class="py-2 px-2 text-center font-mono">EU</td><td class="py-2 px-3 font-sans text-slate-900 font-bold">유럽 본부 (EU 총괄)</td><td class="py-2 px-3 text-right text-rose-800 font-mono text-xs">7.31주</td><td class="py-2 px-2.5 text-center text-rose-900 font-bold">과다재고 (>6주)</td><td class="py-2 px-2.5 text-right">654,669</td><td class="py-2 px-2.5 text-right">358,121</td><td class="py-2 px-2.5 text-right text-teal-900 font-bold">52,312</td><td class="py-2 px-2.5 text-right text-teal-900 font-bold">54.8%</td><td class="py-2 px-2.5 text-right text-teal-900 font-bold">25.6%</td><td class="py-2 px-2.5 text-right text-teal-900 font-bold">14.6%</td><td class="py-2 px-2.5 text-right text-rose-800">9.54주</td><td class="py-2 px-2.5 text-right text-slate-700">4.36주</td></tr>
                    </tbody>
                </table>
            </div>

            <!-- Definitions Box -->
            <div class="p-3.5 rounded-lg bg-slate-50 border border-slate-200 text-xs text-slate-600 space-y-1">
                <div class="font-bold text-slate-800 text-[12px] flex items-center gap-1.5 mb-1">
                    <span class="material-symbols-outlined text-sm text-teal-600">info</span>
                    <span>[OLED 신모델 비중 지표 정의]</span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-2 text-[11.5px]">
                    <div class="p-2 rounded bg-white border border-slate-200">
                        <strong class="text-teal-800">① OLED 내 신모델 비중:</strong>
                        <p class="mt-0.5 text-slate-600">OLED 신모델 Sell-out / 전체 OLED Sell-out<br><span class="text-slate-400 font-mono text-[10.5px]">(OLED 세대교체율 / NPI 진척도)</span></p>
                    </div>
                    <div class="p-2 rounded bg-white border border-slate-200">
                        <strong class="text-teal-800">② 신모델 내 OLED 비중:</strong>
                        <p class="mt-0.5 text-slate-600">OLED 신모델 Sell-out / 전체 TV 신모델 Sell-out<br><span class="text-slate-400 font-mono text-[10.5px]">(신모델 믹스 중 OLED 프리미엄 집중도)</span></p>
                    </div>
                    <div class="p-2 rounded bg-white border border-slate-200">
                        <strong class="text-teal-800">③ 전체 TV 내 OLED 신모델:</strong>
                        <p class="mt-0.5 text-slate-600">OLED 신모델 Sell-out / 전체 TV Sell-out<br><span class="text-slate-400 font-mono text-[10.5px]">(전체 판매 볼륨 대비 기여율)</span></p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Section 3: Deep Diagnostics -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-xs p-6 space-y-4">
            <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2 border-b border-slate-100 pb-3">
                <span class="text-base">🔍</span>
                <span>3. 심층 진단 및 법인 유형별 리스크 분석</span>
            </h3>

            <div class="space-y-3.5 text-xs text-slate-700 leading-relaxed">
                <!-- Cluster A -->
                <div class="p-4 rounded-xl bg-rose-50/70 border border-rose-200 space-y-2">
                    <div class="font-bold text-rose-900 flex items-center justify-between text-xs">
                        <span class="flex items-center gap-1.5">
                            <span>🚨</span>
                            <span>유형 A: 극단적 신모델 과잉 선적형 (A 법인, C 법인, G 법인, D 법인)</span>
                        </span>
                        <span class="px-2 py-0.5 rounded bg-rose-200 text-rose-800 font-bold text-[10px]">공급 동결 & 셀아웃 촉진</span>
                    </div>
                    <div class="space-y-1.5 pl-5 text-[12px] text-slate-700">
                        <p><strong>A 법인:</strong> 전체 WOS 12.62주 중 <strong>신모델 WOS가 24.73주</strong>에 달해 유통 내 신모델 재고 체류가 매우 심각합니다. 다만 신모델 내 OLED 비중이 50.8%로 프리미엄 잠재력이 높으므로, <strong>공급(Sell-in)을 즉시 동결하고 메이저 리테일러 중심의 가을 판촉을 통해 셀아웃 회전율을 높여야 합니다.</strong></p>
                        <p><strong>G 법인 & C 법인:</strong> 신모델 WOS가 각각 <strong>18.45주, 15.11주</strong>로 매우 높습니다. 반면 구모델 WOS는 각각 2.77주, 2.03주로 사실상 구모델 재고 소진은 마무리되었으므로, <strong>신모델 프로모션 집중 지원을 통한 유통 출하 속도 조절</strong>이 필요합니다.</p>
                    </div>
                </div>

                <!-- Cluster B -->
                <div class="p-4 rounded-xl bg-teal-50/70 border border-teal-200 space-y-2">
                    <div class="font-bold text-teal-900 flex items-center justify-between text-xs">
                        <span class="flex items-center gap-1.5">
                            <span>💎</span>
                            <span>유형 B: 프리미엄 OLED 신모델 주도형 (E 법인, M 법인, N 법인)</span>
                        </span>
                        <span class="px-2 py-0.5 rounded bg-teal-200 text-teal-800 font-bold text-[10px]">전략적 사전 확보</span>
                    </div>
                    <div class="space-y-1.5 pl-5 text-[12px] text-slate-700">
                        <p><strong>E 법인:</strong> WOS 8.01주(신모델 9.82주)로 6주를 상회하나, 전체 판매의 <strong>29.4%가 OLED 신모델(월 11,426대)</strong>로 유럽 최대 규모입니다. 10~11월 성수기 수요 선점을 위한 유통 재고 사전 확보(Build-up) 성격이 강하며, 회전율이 뒷받침되어 실질 리스크는 통제 가능한 수준입니다.</p>
                        <p><strong>M 법인:</strong> 전체 WOS 6.31주(신모델 7.07주, 구모델 5.76주)로 안정적인 흐름이며, 신모델 중 OLED 비중이 <strong>45.0%</strong>로 고수익 모델 중심의 양호한 믹스를 유지하고 있습니다.</p>
                    </div>
                </div>

                <!-- Cluster C -->
                <div class="p-4 rounded-xl bg-amber-50/70 border border-amber-200 space-y-2">
                    <div class="font-bold text-amber-900 flex items-center justify-between text-xs">
                        <span class="flex items-center gap-1.5">
                            <span>⚠️</span>
                            <span>유형 C: 구모델 정체 + 저가형 편중형 (F 법인, H 법인, I 법인)</span>
                        </span>
                        <span class="px-2 py-0.5 rounded bg-amber-200 text-amber-800 font-bold text-[10px]">구모델 긴급 정리</span>
                    </div>
                    <div class="space-y-1.5 pl-5 text-[12px] text-slate-700">
                        <p><strong>F 법인:</strong> 전체 WOS가 7.73주인 상태에서 <strong>구모델 WOS가 7.65주(19,088대)</strong>로 여전히 구모델이 대량 체류하고 있습니다. 신모델 판매 중 OLED 비중도 <strong>9.5%</strong>에 그쳐, <strong>구모델 클리어런스 판촉과 OLED 진열 전환</strong>이 가장 시급한 법인입니다.</p>
                        <p><strong>H 법인:</strong> 전체 WOS 7.31주, OLED 내 신모델 비중이 <strong>36.3%</strong>로 유럽 내 최저 수준(구모델 OLED 판매 비중이 63.7%)입니다. 2026년형 C4/B4 신모델로의 전환 속도가 지연되고 있습니다.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Bottom Return Bar -->
        <div class="pt-4 flex items-center justify-between">
            <button type="button" 
                    onclick="returnToGuide()"
                    class="px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold flex items-center gap-2 shadow-sm transition-all hover:scale-105 active:scale-95">
                <span class="material-symbols-outlined text-sm">arrow_back</span>
                <span>가이드로 돌아가기 (시나리오 목록)</span>
            </button>
            <button type="button" 
                    onclick="downloadScenarioExcel()"
                    class="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center gap-2 shadow-sm transition-all hover:scale-105 active:scale-95">
                <span class="material-symbols-outlined text-sm">file_download</span>
                <span>전체 16개국 가명화 엑셀 파일 (.xlsx) 다운로드</span>
            </button>
        </div>
    </main>

    <script>
        // Return to guide handler
        function returnToGuide() {{
            if (window.opener && !window.opener.closed) {{
                try {{
                    window.opener.focus();
                    window.close();
                    return;
                }} catch (e) {{
                    // Fallback to navigation
                }}
            }}
            window.location.href = 'AXIS_System_Architecture_Guide.html#tab-scenarios';
        }}

        // Filter Matrix Table
        function filterTable(type) {{
            const rows = document.querySelectorAll('#matrix-tbody tr');
            const btnAll = document.getElementById('btn-filter-all');
            const btnRisk = document.getElementById('btn-filter-risk');
            const btnSafe = document.getElementById('btn-filter-safe');

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

        // Base64 Excel download
        const SCENARIO_EXCEL_B64 = "{b64_excel}";
        function downloadScenarioExcel() {{
            try {{
                const byteCharacters = atob(SCENARIO_EXCEL_B64);
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
    </script>
</body>
</html>
'''

with open(viewer_path, "w", encoding="utf-8") as f:
    f.write(viewer_html)

print("Created standalone viewer page successfully at:", viewer_path)
