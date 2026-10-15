# -*- coding: utf-8 -*-
"""
build_swiss_4p_report.py
Generates the Swiss TV 3-Year P&L & 4P Strategy Executive Interactive Web Report (2024~2026.08 YTD).
Theme: Premium Dark Slate with LGE Crimson Red accents (Global Design System standard).
"""

import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
json_data_path = os.path.join(base_dir, "cache", "scratch_swiss_3y_result.json")
datamart_path = os.path.join(base_dir, "cache", "pnl_datamart.json")
output_html_path = os.path.join(base_dir, "Swiss_TV_4P_Strategy_Report_2024_2026.html")

print("Loading data...")
with open(json_data_path, "r", encoding="utf-8") as f:
    data_3y = json.load(f)

with open(datamart_path, "r", encoding="utf-8") as f:
    datamart = json.load(f)

waterfall_data = datamart["DATA"]["standard"]["waterfall"]
ytd_trend_data = datamart["DATA"]["standard"]["pnl_structure_new"]["ytd_trend"]
cost_stack_data = datamart["DATA"]["standard"]["pnl_structure_new"]["cost_structure_stack"]["ytd_compare"]

# Embed structured JSON directly in the HTML for interactive charts and filters
embedded_data = {
    "summary": data_3y["summary_by_year"],
    "segment": data_3y["blu_by_year"],
    "account": data_3y["acc_by_year"],
    "inch": data_3y["inch_by_year"],
    "waterfall": waterfall_data,
    "cost_stack": cost_stack_data,
    "ytd_trend": ytd_trend_data
}

html_content = f"""<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>스위스 법인 TV 손익 분석 및 4P 전략 보고서 (2024 ~ 2026.08 YTD)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              red: '#A50034',
              hover: '#E6004C',
              light: '#FFD6E0',
              dark: '#7A0026'
            }},
            slate: {{
              850: '#161F30',
              900: '#0F172A',
              950: '#0B0F19'
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    body {{
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }}
    .custom-scrollbar::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scrollbar::-webkit-scrollbar-track {{
      background: #111827;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{
      background: #374151;
      border-radius: 3px;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
      background: #4B5563;
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen custom-scrollbar antialiased selection:bg-brand-red selection:text-white">

  <!-- Top Navigation Bar -->
  <header class="sticky top-0 z-50 bg-slate-900/90 backdrop-blur border-b border-slate-800 px-6 py-3.5 flex items-center justify-between">
    <div class="flex items-center space-x-4">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-red to-rose-600 flex items-center justify-center shadow-lg shadow-brand-red/20">
        <i class="fa-solid fa-chart-line text-white text-lg"></i>
      </div>
      <div>
        <div class="flex items-center space-x-2">
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-brand-red/20 text-brand-light border border-brand-red/30">LG Europe TV AX</span>
          <span class="text-xs font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300">Swiss Branch (스위스 지점)</span>
        </div>
        <h1 class="text-lg font-black tracking-tight text-white mt-0.5">스위스 TV 손익(P&L) 심층 분석 및 4P 혁신 개선 과제</h1>
      </div>
    </div>
    <div class="flex items-center space-x-3 text-xs text-slate-400">
      <span class="flex items-center space-x-1.5 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60">
        <i class="fa-regular fa-calendar text-brand-light"></i>
        <span>비교 대상: 2024~2026년 1~8월 누적 (Jan-Aug YTD)</span>
      </span>
      <span class="flex items-center space-x-1.5 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60">
        <i class="fa-solid fa-scale-balanced text-emerald-400"></i>
        <span>회계 기준: Standard P&L (공식 결산)</span>
      </span>
      <button onclick="window.print()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg transition border border-slate-700 flex items-center space-x-1.5">
        <i class="fa-solid fa-print"></i>
        <span>보고서 인쇄/PDF</span>
      </button>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-6 py-6 space-y-6">

    <!-- Tab Navigation Buttons -->
    <div class="flex items-center space-x-2 border-b border-slate-800 pb-2">
      <button onclick="switchTab('tab-overview')" id="btn-tab-overview" class="tab-btn px-4 py-2.5 rounded-xl font-bold text-sm transition flex items-center space-x-2 bg-brand-red text-white shadow-lg shadow-brand-red/20">
        <i class="fa-solid fa-chart-pie"></i>
        <span>1. 경영진 요약 & 3개년 손익 추이</span>
      </button>
      <button onclick="switchTab('tab-4p-diagnostic')" id="btn-tab-4p-diagnostic" class="tab-btn px-4 py-2.5 rounded-xl font-medium text-sm transition flex items-center space-x-2 text-slate-400 hover:text-white hover:bg-slate-800/60">
        <i class="fa-solid fa-magnifying-glass-chart"></i>
        <span>2. 4P 영역별 심층 데이터 진단</span>
      </button>
      <button onclick="switchTab('tab-4p-action')" id="btn-tab-4p-action" class="tab-btn px-4 py-2.5 rounded-xl font-medium text-sm transition flex items-center space-x-2 text-slate-400 hover:text-white hover:bg-slate-800/60">
        <i class="fa-solid fa-bullseye"></i>
        <span>3. 4P 전략 로드맵 & 핵심 실행 과제</span>
      </button>
      <button onclick="switchTab('tab-simulator')" id="btn-tab-simulator" class="tab-btn px-4 py-2.5 rounded-xl font-medium text-sm transition flex items-center space-x-2 text-slate-400 hover:text-white hover:bg-slate-800/60">
        <i class="fa-solid fa-sliders"></i>
        <span>4. 유통 마진 개선 시뮬레이터 & 피벗 탐색기</span>
      </button>
    </div>

    <!-- ========================================== -->
    <!-- TAB 1: Executive Summary & 3Y P&L Overview -->
    <!-- ========================================== -->
    <section id="tab-overview" class="tab-pane space-y-6">
      
      <!-- Executive Alert Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <!-- Qty Card -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4.5 relative overflow-hidden shadow-sm">
          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">누적 판매 수량</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-bold">YoY +9.4%</span>
          </div>
          <div class="mt-2 flex items-baseline space-x-2">
            <span class="text-3xl font-black text-white">41,239</span>
            <span class="text-xs text-slate-400">대</span>
          </div>
          <div class="mt-2 text-xs text-slate-400 flex items-center justify-between border-t border-slate-800/80 pt-2">
            <span>'24: 41,510대</span>
            <span class="text-slate-600">→</span>
            <span>'25: 37,697대</span>
            <span class="text-slate-600">→</span>
            <span class="text-emerald-400 font-bold">'26: 41,239대</span>
          </div>
        </div>

        <!-- Net Sales Card -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4.5 relative overflow-hidden shadow-sm">
          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Net Sales (매출액)</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-bold">YoY +7.1%</span>
          </div>
          <div class="mt-2 flex items-baseline space-x-2">
            <span class="text-3xl font-black text-white">$36.08M</span>
            <span class="text-xs text-slate-400">($36,077K)</span>
          </div>
          <div class="mt-2 text-xs text-slate-400 flex items-center justify-between border-t border-slate-800/80 pt-2">
            <span>'24: $31.27M</span>
            <span class="text-slate-600">→</span>
            <span>'25: $33.67M</span>
            <span class="text-slate-600">→</span>
            <span class="text-emerald-400 font-bold">'26: $36.08M</span>
          </div>
        </div>

        <!-- ASP Card -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4.5 relative overflow-hidden shadow-sm">
          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">출하 평균 단가 (ASP)</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-400 font-bold">YoY -$18.3 (-2.1%)</span>
          </div>
          <div class="mt-2 flex items-baseline space-x-2">
            <span class="text-3xl font-black text-white">$874.8</span>
            <span class="text-xs text-slate-400">/대</span>
          </div>
          <div class="mt-2 text-xs text-slate-400 flex items-center justify-between border-t border-slate-800/80 pt-2">
            <span>'24: $753.4</span>
            <span class="text-slate-600">→</span>
            <span class="text-emerald-400">'25: $893.2</span>
            <span class="text-slate-600">→</span>
            <span class="text-rose-400 font-bold">'26: $874.8</span>
          </div>
        </div>

        <!-- COI Card -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4.5 relative overflow-hidden shadow-sm">
          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">영업이익 (COI & COI%)</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-bold">YoY +$1,297K</span>
          </div>
          <div class="mt-2 flex items-baseline space-x-2">
            <span class="text-3xl font-black text-emerald-400">13.78%</span>
            <span class="text-xs text-slate-300 font-bold">($4,972K)</span>
          </div>
          <div class="mt-2 text-xs text-slate-400 flex items-center justify-between border-t border-slate-800/80 pt-2">
            <span>'24: 2.27% ($711K)</span>
            <span class="text-slate-600">→</span>
            <span>'25: 10.91% ($3,675K)</span>
            <span class="text-slate-600">→</span>
            <span class="text-emerald-400 font-bold">'26: 13.78%</span>
          </div>
        </div>
      </div>

      <!-- Strategic Narrative Box -->
      <div class="bg-gradient-to-r from-slate-900 via-slate-900/90 to-brand-dark/20 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 rounded-lg bg-brand-red/20 text-brand-light flex items-center justify-center shrink-0 mt-0.5">
            <i class="fa-solid fa-bullhorn text-sm"></i>
          </div>
          <div class="space-y-2 text-sm leading-relaxed">
            <h3 class="font-bold text-white text-base">경영진 핵심 시사점 (Executive Key Takeaways)</h3>
            <p class="text-slate-300">
              스위스 TV 사업은 2024년 영업이익률 2.27%($711K)의 저수익 국면에서 2025년 10.91%($3,675K), 2026년 8월 누적 <strong class="text-emerald-400">13.78%($4,972K)</strong>로 구조적 흑자 기조를 확립했습니다. 
              이러한 질적 성장은 <strong class="text-white">OLED/QNED 고부가 믹스 전환</strong> 및 <strong class="text-white">재료비율의 구조적 하향 안정화(64.7% → 56.5%)</strong>가 견인했습니다.
            </p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 text-xs">
              <div class="bg-slate-950/60 p-3 rounded-xl border border-rose-500/20">
                <span class="font-bold text-rose-400 flex items-center space-x-1.5">
                  <i class="fa-solid fa-triangle-exclamation"></i>
                  <span>수익성 위협 리스크 1: 출하 판가 침하 & 원가 의존 한계</span>
                </span>
                <p class="text-slate-400 mt-1">
                  2026년 들어 ASP가 $893에서 $875로 -$18.3 하락했으며, 순수 판가 효과(Price Effect)가 -$653K로 작용했습니다. 원가 절감 효과(+$1,615K)가 판가 침하를 상쇄하고 있으나 원가 추가 절감 여력이 소진될 경우 이익률 급락 리스크가 상존합니다.
                </p>
              </div>
              <div class="bg-slate-950/60 p-3 rounded-xl border border-amber-500/20">
                <span class="font-bold text-amber-400 flex items-center space-x-1.5">
                  <i class="fa-solid fa-store-slash"></i>
                  <span>수익성 위협 리스크 2: 대형 양판 유통(MSH/FUST) 적자 고착화</span>
                </span>
                <p class="text-slate-400 mt-1">
                  MSH(MediaMarkt)는 매출 비중 18.5%($6.66M)에도 불구하고 <strong class="text-rose-400">COI -6.5%(-$430K 적자, SD% 38.0%)</strong>를 기록하고 있으며, FUST 역시 <strong class="text-rose-400">COI -4.3%(-$100K 적자)</strong>로 출하할수록 마진이 훼손되는 심각한 출혈 유통 구조를 노정하고 있습니다.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Row: Waterfall YoY Bridge & Multi-year P&L Stack -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Waterfall Bridge -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-bold text-white text-base flex items-center space-x-2">
                <i class="fa-solid fa-arrow-trend-up text-brand-light"></i>
                <span>'25년 vs '26년 영업이익(COI) 증감 Waterfall Bridge</span>
              </h3>
              <p class="text-xs text-slate-400 mt-0.5">단위: K$ (1~8월 누적 기준 YoY 변동 요인 분석)</p>
            </div>
            <span class="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 font-semibold border border-slate-700">Net +$1,297K</span>
          </div>
          <div class="h-64">
            <canvas id="chartWaterfall"></canvas>
          </div>
          <div class="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-800 text-center text-xs">
            <div class="bg-slate-950/40 p-2 rounded-lg">
              <span class="text-slate-400 block">원가 절감 기여</span>
              <span class="text-emerald-400 font-bold text-sm">+ $1,615K</span>
            </div>
            <div class="bg-slate-950/40 p-2 rounded-lg">
              <span class="text-slate-400 block">판가 하락 훼손</span>
              <span class="text-rose-400 font-bold text-sm">- $653K</span>
            </div>
            <div class="bg-slate-950/40 p-2 rounded-lg">
              <span class="text-slate-400 block">판매량 증가 기여</span>
              <span class="text-emerald-400 font-bold text-sm">+ $345K</span>
            </div>
          </div>
        </div>

        <!-- 3-Year Trend & Cost Stack -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-bold text-white text-base flex items-center space-x-2">
                <i class="fa-solid fa-layer-group text-sky-400"></i>
                <span>3개년 손익 원가 구조 및 한계이익(MP%) 변화</span>
              </h3>
              <p class="text-xs text-slate-400 mt-0.5">매출액 대비 재료비, 판관비, 한계이익률 비중 추이</p>
            </div>
            <span class="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20">재료비율 -8.2%p 개선</span>
          </div>
          <div class="h-64">
            <canvas id="chartCostStack"></canvas>
          </div>
          <div class="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-800 text-center text-xs">
            <div class="bg-slate-950/40 p-2 rounded-lg">
              <span class="text-slate-400 block">'24 재료비율</span>
              <span class="text-slate-300 font-bold text-sm">64.67%</span>
            </div>
            <div class="bg-slate-950/40 p-2 rounded-lg">
              <span class="text-slate-400 block">'25 재료비율</span>
              <span class="text-slate-300 font-bold text-sm">57.54%</span>
            </div>
            <div class="bg-slate-950/40 p-2 rounded-lg">
              <span class="text-slate-400 block">'26 재료비율</span>
              <span class="text-emerald-400 font-bold text-sm">56.46%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 3-Year P&L Statement Comprehensive Table -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm overflow-hidden">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="font-bold text-white text-base flex items-center space-x-2">
              <i class="fa-solid fa-table-list text-brand-light"></i>
              <span>3개년 표준 손익계산서 비교 (2024 ~ 2026.08 YTD)</span>
            </h3>
            <p class="text-xs text-slate-400 mt-0.5">단위: 금액 K$ (USD), 수량 대, 비율 %</p>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-slate-800/80 text-slate-300 border-b border-slate-700 font-semibold">
                <th class="py-3 px-4">손익 계정 항목</th>
                <th class="py-3 px-4 text-right">2024 1~8월</th>
                <th class="py-3 px-4 text-right">2025 1~8월</th>
                <th class="py-3 px-4 text-right">2026 1~8월</th>
                <th class="py-3 px-4 text-right text-emerald-400">YoY 증감 ('26 vs '25)</th>
                <th class="py-3 px-4 text-right text-sky-400">2개년 증감 ('26 vs '24)</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800 text-slate-200">
              <tr class="hover:bg-slate-800/40">
                <td class="py-2.5 px-4 font-semibold text-slate-300">판매 수량 (Qty, 대)</td>
                <td class="py-2.5 px-4 text-right">41,510</td>
                <td class="py-2.5 px-4 text-right">37,697</td>
                <td class="py-2.5 px-4 text-right font-bold text-white">41,239</td>
                <td class="py-2.5 px-4 text-right text-emerald-400 font-semibold">+3,542 (+9.4%)</td>
                <td class="py-2.5 px-4 text-right text-slate-400">-271 (-0.7%)</td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="py-2.5 px-4 font-semibold text-slate-300">Gross Sales (총매출)</td>
                <td class="py-2.5 px-4 text-right">$42,278K</td>
                <td class="py-2.5 px-4 text-right">$44,332K</td>
                <td class="py-2.5 px-4 text-right font-bold text-white">$47,425K</td>
                <td class="py-2.5 px-4 text-right text-emerald-400 font-semibold">+$3,093K (+7.0%)</td>
                <td class="py-2.5 px-4 text-right text-sky-400">+$5,147K (+12.2%)</td>
              </tr>
              <tr class="hover:bg-slate-800/40 text-rose-300">
                <td class="py-2.5 px-4 pl-8">(-) Sales Deduction (매출차감)</td>
                <td class="py-2.5 px-4 text-right">$11,005K</td>
                <td class="py-2.5 px-4 text-right">$10,662K</td>
                <td class="py-2.5 px-4 text-right font-bold">$11,348K</td>
                <td class="py-2.5 px-4 text-right text-rose-400 font-semibold">+$686K (+6.4%)</td>
                <td class="py-2.5 px-4 text-right text-rose-400">+$343K (+3.1%)</td>
              </tr>
              <tr class="hover:bg-slate-800/40 bg-slate-850/40">
                <td class="py-2 px-4 pl-12 text-slate-400">└ 매출차감률 (S/D%)</td>
                <td class="py-2 px-4 text-right text-slate-300">26.03%</td>
                <td class="py-2 px-4 text-right text-slate-300">24.05%</td>
                <td class="py-2 px-4 text-right font-bold text-emerald-400">23.93%</td>
                <td class="py-2 px-4 text-right text-emerald-400">-0.12%p</td>
                <td class="py-2 px-4 text-right text-emerald-400">-2.10%p</td>
              </tr>
              <tr class="hover:bg-slate-800/40 bg-slate-800/50 font-bold">
                <td class="py-3 px-4 text-white">Net Sales (순매출액)</td>
                <td class="py-3 px-4 text-right text-slate-200">$31,273K</td>
                <td class="py-3 px-4 text-right text-slate-200">$33,670K</td>
                <td class="py-3 px-4 text-right text-emerald-400 text-sm">$36,077K</td>
                <td class="py-3 px-4 text-right text-emerald-400">+$2,407K (+7.1%)</td>
                <td class="py-3 px-4 text-right text-sky-400">+$4,804K (+15.4%)</td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="py-2.5 px-4 font-semibold text-slate-300">출하 단가 (ASP, $)</td>
                <td class="py-2.5 px-4 text-right">$753.4</td>
                <td class="py-2.5 px-4 text-right text-emerald-400 font-bold">$893.2</td>
                <td class="py-2.5 px-4 text-right font-bold text-rose-400">$874.8</td>
                <td class="py-2.5 px-4 text-right text-rose-400 font-semibold">-$18.3 (-2.1%)</td>
                <td class="py-2.5 px-4 text-right text-emerald-400">+$121.5 (+16.1%)</td>
              </tr>
              <tr class="hover:bg-slate-800/40 text-slate-300">
                <td class="py-2.5 px-4 pl-8">(-) 재료비 (Material Cost)</td>
                <td class="py-2.5 px-4 text-right">$20,225K (64.7%)</td>
                <td class="py-2.5 px-4 text-right">$19,375K (57.5%)</td>
                <td class="py-2.5 px-4 text-right font-semibold">$20,368K (56.5%)</td>
                <td class="py-2.5 px-4 text-right text-emerald-400 font-semibold">-1.08%p 개선</td>
                <td class="py-2.5 px-4 text-right text-emerald-400">-8.21%p 개선</td>
              </tr>
              <tr class="hover:bg-slate-800/40 text-slate-300">
                <td class="py-2.5 px-4 pl-8">(-) COGS (매출원가 합계)</td>
                <td class="py-2.5 px-4 text-right">$22,096K (70.7%)</td>
                <td class="py-2.5 px-4 text-right">$21,204K (63.0%)</td>
                <td class="py-2.5 px-4 text-right font-semibold">$20,922K (58.0%)</td>
                <td class="py-2.5 px-4 text-right text-emerald-400 font-semibold">-4.99%p 개선</td>
                <td class="py-2.5 px-4 text-right text-emerald-400">-12.67%p 개선</td>
              </tr>
              <tr class="hover:bg-slate-800/40 bg-slate-850/40 font-bold">
                <td class="py-3 px-4 text-white">Marginal Profit (한계이익, MP)</td>
                <td class="py-3 px-4 text-right text-slate-200">$9,409K (30.1%)</td>
                <td class="py-3 px-4 text-right text-slate-200">$12,656K (37.6%)</td>
                <td class="py-3 px-4 text-right text-emerald-400 text-sm">$14,354K (39.8%)</td>
                <td class="py-3 px-4 text-right text-emerald-400">+$1,698K (+2.2%p)</td>
                <td class="py-3 px-4 text-right text-sky-400">+$4,945K (+9.7%p)</td>
              </tr>
              <tr class="hover:bg-slate-800/40 text-slate-300">
                <td class="py-2.5 px-4 pl-8">(-) SG&A (판관비 합계)</td>
                <td class="py-2.5 px-4 text-right">$8,466K (27.1%)</td>
                <td class="py-2.5 px-4 text-right">$8,791K (26.1%)</td>
                <td class="py-2.5 px-4 text-right font-semibold text-rose-300">$10,183K (28.2%)</td>
                <td class="py-2.5 px-4 text-right text-rose-400 font-semibold">+$1,392K (+2.1%p)</td>
                <td class="py-2.5 px-4 text-right text-rose-400">+$1,717K (+1.1%p)</td>
              </tr>
              <tr class="hover:bg-slate-800/40 bg-emerald-950/30 border-t-2 border-emerald-500/50 font-black">
                <td class="py-3.5 px-4 text-white text-sm">Operating Income (영업이익, COI)</td>
                <td class="py-3.5 px-4 text-right text-slate-300">$711K</td>
                <td class="py-3.5 px-4 text-right text-slate-300">$3,675K</td>
                <td class="py-3.5 px-4 text-right text-emerald-400 text-base">$4,972K</td>
                <td class="py-3.5 px-4 text-right text-emerald-400 text-sm">+$1,297K (+35.3%)</td>
                <td class="py-3.5 px-4 text-right text-sky-400 text-sm">+$4,261K (7.0배)</td>
              </tr>
              <tr class="hover:bg-slate-800/40 bg-emerald-950/20 font-black">
                <td class="py-2.5 px-4 pl-8 text-emerald-300">└ 영업이익률 (COI%)</td>
                <td class="py-2.5 px-4 text-right text-slate-300">2.27%</td>
                <td class="py-2.5 px-4 text-right text-slate-300">10.91%</td>
                <td class="py-2.5 px-4 text-right text-emerald-400 text-sm">13.78%</td>
                <td class="py-2.5 px-4 text-right text-emerald-400 font-bold">+2.87%p</td>
                <td class="py-2.5 px-4 text-right text-sky-400 font-bold">+11.51%p</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </section>

    <!-- ========================================== -->
    <!-- TAB 2: 4P Diagnostic Breakdown            -->
    <!-- ========================================== -->
    <section id="tab-4p-diagnostic" class="tab-pane hidden space-y-6">

      <!-- 4P Matrix Header Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <!-- 1. Product -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 border-t-4 border-t-indigo-500">
          <div class="flex items-center space-x-2 text-indigo-400 font-bold text-sm">
            <i class="fa-solid fa-tv"></i>
            <span>Product (제품 믹스)</span>
          </div>
          <div class="mt-2 text-xs text-slate-300 leading-relaxed">
            • <strong>OLED 매출 비중 66.8%</strong>로 안정적 수익 지탱.<br>
            • <strong>QNED 볼륨 급증(9.7K)</strong>했으나 ASP $581로 하락.<br>
            • <strong>MRGB 런칭 안착</strong>(COI 17.9% 고마진 검증).
          </div>
        </div>

        <!-- 2. Price -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 border-t-4 border-t-rose-500">
          <div class="flex items-center space-x-2 text-rose-400 font-bold text-sm">
            <i class="fa-solid fa-tag"></i>
            <span>Price (가격 & 할인)</span>
          </div>
          <div class="mt-2 text-xs text-slate-300 leading-relaxed">
            • '26년 <strong>순수 판가 효과 -$653K</strong> 훼손 발생.<br>
            • QNED <strong>S/D% 26.2%</strong>로 급상승(+5.7%p).<br>
            • 전체 S/D%는 23.9%로 전년 동기 수준 유지.
          </div>
        </div>

        <!-- 3. Place -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 border-t-4 border-t-amber-500">
          <div class="flex items-center space-x-2 text-amber-400 font-bold text-sm">
            <i class="fa-solid fa-network-wired"></i>
            <span>Place (유통 채널)</span>
          </div>
          <div class="mt-2 text-xs text-slate-300 leading-relaxed">
            • <strong>MSH(MediaMarkt) COI -6.5%</strong>(-$430K 적자 심각).<br>
            • <strong>FUST COI -4.3%</strong>(-$100K 3개년 적자 고착).<br>
            • <strong>Alltron/EP 등 총판 초고수익</strong>(COI 24~26%).
          </div>
        </div>

        <!-- 4. Promotion -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 border-t-4 border-t-emerald-500">
          <div class="flex items-center space-x-2 text-emerald-400 font-bold text-sm">
            <i class="fa-solid fa-bullhorn"></i>
            <span>Promotion (판촉 효율)</span>
          </div>
          <div class="mt-2 text-xs text-slate-300 leading-relaxed">
            • 저마진 채널에 <strong>리베이트 38% 집중 투입</strong> 왜곡.<br>
            • 실판매 연계 없는 Sell-In 보조금 누수 잔존.<br>
            • 성과급형 Sell-Out 프로모션 전환 시급.
          </div>
        </div>
      </div>

      <!-- Diagnostic Detail 1: Product & Price Analysis -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Segment Performance Table -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
          <h3 class="font-bold text-white text-base mb-3 flex items-center space-x-2">
            <i class="fa-solid fa-layer-group text-indigo-400"></i>
            <span>세그먼트(Segment)별 3개년 실적 및 수익성 추이</span>
          </h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border-collapse">
              <thead>
                <tr class="bg-slate-800/80 text-slate-300 border-b border-slate-700 font-semibold">
                  <th class="py-2.5 px-3">세그먼트</th>
                  <th class="py-2.5 px-3 text-right">2026 수량</th>
                  <th class="py-2.5 px-3 text-right">2026 매출</th>
                  <th class="py-2.5 px-3 text-right">ASP</th>
                  <th class="py-2.5 px-3 text-right">S/D%</th>
                  <th class="py-2.5 px-3 text-right">COI%</th>
                  <th class="py-2.5 px-3 text-right">COI 금액</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800 text-slate-200">
                <tr class="hover:bg-slate-800/40">
                  <td class="py-2 px-3 font-bold text-purple-400 flex items-center space-x-1.5">
                    <span class="w-2 h-2 rounded-full bg-purple-500"></span>
                    <span>OLED</span>
                  </td>
                  <td class="py-2 px-3 text-right">20,940</td>
                  <td class="py-2 px-3 text-right font-semibold">$24.10M</td>
                  <td class="py-2 px-3 text-right text-rose-300 font-semibold">$1,151</td>
                  <td class="py-2 px-3 text-right">24.4%</td>
                  <td class="py-2 px-3 text-right text-emerald-400 font-bold">9.4%</td>
                  <td class="py-2 px-3 text-right text-emerald-400 font-bold">$2,272K</td>
                </tr>
                <tr class="hover:bg-slate-800/40">
                  <td class="py-2 px-3 font-bold text-sky-400 flex items-center space-x-1.5">
                    <span class="w-2 h-2 rounded-full bg-sky-500"></span>
                    <span>QNED</span>
                  </td>
                  <td class="py-2 px-3 text-right">9,695</td>
                  <td class="py-2 px-3 text-right font-semibold">$5.63M</td>
                  <td class="py-2 px-3 text-right text-slate-300">$581</td>
                  <td class="py-2 px-3 text-right text-rose-400 font-bold">26.2%</td>
                  <td class="py-2 px-3 text-right text-slate-300">7.7%</td>
                  <td class="py-2 px-3 text-right text-slate-300">$436K</td>
                </tr>
                <tr class="hover:bg-slate-800/40">
                  <td class="py-2 px-3 font-bold text-emerald-400 flex items-center space-x-1.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <span>MRGB</span>
                  </td>
                  <td class="py-2 px-3 text-right">647</td>
                  <td class="py-2 px-3 text-right font-semibold">$0.58M</td>
                  <td class="py-2 px-3 text-right text-emerald-300 font-semibold">$890</td>
                  <td class="py-2 px-3 text-right">22.5%</td>
                  <td class="py-2 px-3 text-right text-emerald-400 font-bold">17.9%</td>
                  <td class="py-2 px-3 text-right text-emerald-400 font-bold">$103K</td>
                </tr>
                <tr class="hover:bg-slate-800/40">
                  <td class="py-2 px-3 font-bold text-amber-400 flex items-center space-x-1.5">
                    <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                    <span>UHD</span>
                  </td>
                  <td class="py-2 px-3 text-right">7,709</td>
                  <td class="py-2 px-3 text-right font-semibold">$3.79M</td>
                  <td class="py-2 px-3 text-right text-slate-300">$491</td>
                  <td class="py-2 px-3 text-right text-emerald-400">17.6%</td>
                  <td class="py-2 px-3 text-right text-emerald-400 font-bold">11.6%</td>
                  <td class="py-2 px-3 text-right text-emerald-400 font-bold">$441K</td>
                </tr>
                <tr class="hover:bg-slate-800/40">
                  <td class="py-2 px-3 font-bold text-slate-400 flex items-center space-x-1.5">
                    <span class="w-2 h-2 rounded-full bg-slate-500"></span>
                    <span>FHD</span>
                  </td>
                  <td class="py-2 px-3 text-right">2,248</td>
                  <td class="py-2 px-3 text-right font-semibold">$0.97M</td>
                  <td class="py-2 px-3 text-right text-slate-400">$430</td>
                  <td class="py-2 px-3 text-right">22.3%</td>
                  <td class="py-2 px-3 text-right text-slate-300">3.2%</td>
                  <td class="py-2 px-3 text-right text-slate-300">$31K</td>
                </tr>
                <tr class="hover:bg-slate-800/40 bg-slate-850/60 font-semibold">
                  <td class="py-2 px-3 text-slate-400">Others(조정)</td>
                  <td class="py-2 px-3 text-right">-</td>
                  <td class="py-2 px-3 text-right">$1.02M</td>
                  <td class="py-2 px-3 text-right">-</td>
                  <td class="py-2 px-3 text-right">-</td>
                  <td class="py-2 px-3 text-right text-emerald-400">-</td>
                  <td class="py-2 px-3 text-right text-emerald-400">$1,690K</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="mt-3 text-xs text-slate-400 p-3 bg-slate-950/40 rounded-xl border border-slate-800">
            <strong class="text-indigo-400">시사점:</strong> OLED는 스위스 전체 이익의 약 46%를 홀로 창출하는 절대적 캐시카우이나 '25년 대비 ASP가 -$76.4 하락했습니다. QNED는 수량 확대 과정에서 S/D%가 26.2%로 과도하게 치솟아 마진 방어 장치가 필요합니다.
          </div>
        </div>

        <!-- Segment Share Chart -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
          <h3 class="font-bold text-white text-base mb-1 flex items-center space-x-2">
            <i class="fa-solid fa-chart-pie text-indigo-400"></i>
            <span>2026년 8월 누적 세그먼트별 매출 비중 (Sales Share)</span>
          </h3>
          <p class="text-xs text-slate-400 mb-4">Total Net Sales: $36.08M</p>
          <div class="h-60">
            <canvas id="chartSegmentShare"></canvas>
          </div>
        </div>
      </div>

      <!-- Diagnostic Detail 2: Place & Promotion Analysis (Account Profitability & Rebate Gap) -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="font-bold text-white text-base flex items-center space-x-2">
              <i class="fa-solid fa-network-wired text-amber-400"></i>
              <span>주요 유통 채널별 손익 성적표 (Channel P&L Scorecard)</span>
            </h3>
            <p class="text-xs text-slate-400 mt-0.5">2026년 1~8월 누적 기준: 매출 비중, ASP, 매출차감률(S/D%), 영업이익률(COI%) 비교</p>
          </div>
          <div class="flex items-center space-x-2">
            <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">초고수익 채널 (Alltron, EP)</span>
            <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">위험 적자 채널 (MSH, FUST)</span>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-slate-800/80 text-slate-300 border-b border-slate-700 font-semibold">
                <th class="py-3 px-3">유통 거래선</th>
                <th class="py-3 px-3 text-right">판매 수량</th>
                <th class="py-3 px-3 text-right">매출액 (Net Sales)</th>
                <th class="py-3 px-3 text-right">매출 비중</th>
                <th class="py-3 px-3 text-right">출하 ASP</th>
                <th class="py-3 px-3 text-right">매출차감률 (S/D%)</th>
                <th class="py-3 px-3 text-right">한계이익률 (MP%)</th>
                <th class="py-3 px-3 text-right">영업이익률 (COI%)</th>
                <th class="py-3 px-3 text-right">영업이익 금액</th>
                <th class="py-3 px-3 text-center">진단 등급</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800 text-slate-200">
              <!-- Conforama -->
              <tr class="hover:bg-slate-800/40">
                <td class="py-2.5 px-3 font-bold text-white">Conforama</td>
                <td class="py-2.5 px-3 text-right">13,124대</td>
                <td class="py-2.5 px-3 text-right font-semibold">$8,681K</td>
                <td class="py-2.5 px-3 text-right font-bold text-slate-300">24.1% (1위)</td>
                <td class="py-2.5 px-3 text-right">$662</td>
                <td class="py-2.5 px-3 text-right text-slate-300">21.6%</td>
                <td class="py-2.5 px-3 text-right text-slate-300">38.9%</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-bold">12.9%</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-bold">+$1,122K</td>
                <td class="py-2.5 px-3 text-center"><span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">건전 볼륨</span></td>
              </tr>
              <!-- MSH (MediaMarkt) -->
              <tr class="hover:bg-slate-800/40 bg-rose-950/20 border-l-4 border-l-rose-500">
                <td class="py-2.5 px-3 font-bold text-rose-300 flex items-center space-x-1.5">
                  <i class="fa-solid fa-triangle-exclamation text-rose-400"></i>
                  <span>MSH (MediaMarkt)</span>
                </td>
                <td class="py-2.5 px-3 text-right">8,722대</td>
                <td class="py-2.5 px-3 text-right font-semibold text-rose-200">$6,657K</td>
                <td class="py-2.5 px-3 text-right font-bold text-rose-300">18.5% (2위)</td>
                <td class="py-2.5 px-3 text-right text-slate-300">$763</td>
                <td class="py-2.5 px-3 text-right text-rose-400 font-black">38.0%</td>
                <td class="py-2.5 px-3 text-right text-rose-300">26.2%</td>
                <td class="py-2.5 px-3 text-right text-rose-400 font-black">-6.5%</td>
                <td class="py-2.5 px-3 text-right text-rose-400 font-black">-$430K (적자)</td>
                <td class="py-2.5 px-3 text-center"><span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-black">심각 위험</span></td>
              </tr>
              <!-- Alltron -->
              <tr class="hover:bg-slate-800/40 bg-emerald-950/20 border-l-4 border-l-emerald-500">
                <td class="py-2.5 px-3 font-bold text-emerald-300 flex items-center space-x-1.5">
                  <i class="fa-solid fa-gem text-emerald-400"></i>
                  <span>Alltron (총판)</span>
                </td>
                <td class="py-2.5 px-3 text-right">4,416대</td>
                <td class="py-2.5 px-3 text-right font-semibold">$5,136K</td>
                <td class="py-2.5 px-3 text-right font-bold text-slate-300">14.2%</td>
                <td class="py-2.5 px-3 text-right text-emerald-300 font-bold">$1,163</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-bold">4.0%</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-bold">46.5%</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-black">26.3%</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-black">+$1,351K</td>
                <td class="py-2.5 px-3 text-center"><span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-black">최고 효자</span></td>
              </tr>
              <!-- EP -->
              <tr class="hover:bg-slate-800/40 bg-emerald-950/20 border-l-4 border-l-emerald-500">
                <td class="py-2.5 px-3 font-bold text-emerald-300 flex items-center space-x-1.5">
                  <i class="fa-solid fa-gem text-emerald-400"></i>
                  <span>EP (전문점)</span>
                </td>
                <td class="py-2.5 px-3 text-right">3,981대</td>
                <td class="py-2.5 px-3 text-right font-semibold">$4,885K</td>
                <td class="py-2.5 px-3 text-right font-bold text-slate-300">13.5%</td>
                <td class="py-2.5 px-3 text-right text-emerald-300 font-bold">$1,227</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-bold">5.9%</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-bold">44.7%</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-black">23.8%</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-black">+$1,163K</td>
                <td class="py-2.5 px-3 text-center"><span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-black">최고 효자</span></td>
              </tr>
              <!-- Online -->
              <tr class="hover:bg-slate-800/40">
                <td class="py-2.5 px-3 font-bold text-white">Online (D2C 자사몰)</td>
                <td class="py-2.5 px-3 text-right">2,999대</td>
                <td class="py-2.5 px-3 text-right font-semibold">$3,428K</td>
                <td class="py-2.5 px-3 text-right font-bold text-slate-300">9.5%</td>
                <td class="py-2.5 px-3 text-right text-slate-200">$1,143</td>
                <td class="py-2.5 px-3 text-right text-slate-300">21.8%</td>
                <td class="py-2.5 px-3 text-right text-emerald-400">41.3%</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-bold">15.4%</td>
                <td class="py-2.5 px-3 text-right text-emerald-400 font-bold">+$527K</td>
                <td class="py-2.5 px-3 text-center"><span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">고성장</span></td>
              </tr>
              <!-- Interdiscount -->
              <tr class="hover:bg-slate-800/40">
                <td class="py-2.5 px-3 font-bold text-slate-300">Interdiscount</td>
                <td class="py-2.5 px-3 text-right">3,375대</td>
                <td class="py-2.5 px-3 text-right font-semibold">$2,670K</td>
                <td class="py-2.5 px-3 text-right font-bold text-slate-300">7.4%</td>
                <td class="py-2.5 px-3 text-right text-slate-300">$791</td>
                <td class="py-2.5 px-3 text-right text-amber-400 font-bold">32.9%</td>
                <td class="py-2.5 px-3 text-right text-slate-300">33.4%</td>
                <td class="py-2.5 px-3 text-right text-slate-300 font-bold">2.8%</td>
                <td class="py-2.5 px-3 text-right text-slate-300 font-bold">+$74K</td>
                <td class="py-2.5 px-3 text-center"><span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold">저마진 경계</span></td>
              </tr>
              <!-- FUST -->
              <tr class="hover:bg-slate-800/40 bg-rose-950/20 border-l-4 border-l-rose-500">
                <td class="py-2.5 px-3 font-bold text-rose-300 flex items-center space-x-1.5">
                  <i class="fa-solid fa-triangle-exclamation text-rose-400"></i>
                  <span>FUST</span>
                </td>
                <td class="py-2.5 px-3 text-right">3,228대</td>
                <td class="py-2.5 px-3 text-right font-semibold text-rose-200">$2,343K</td>
                <td class="py-2.5 px-3 text-right font-bold text-rose-300">6.5%</td>
                <td class="py-2.5 px-3 text-right text-slate-300">$726</td>
                <td class="py-2.5 px-3 text-right text-rose-400 font-black">38.3%</td>
                <td class="py-2.5 px-3 text-right text-rose-300">28.8%</td>
                <td class="py-2.5 px-3 text-right text-rose-400 font-black">-4.3%</td>
                <td class="py-2.5 px-3 text-right text-rose-400 font-black">-$100K (적자)</td>
                <td class="py-2.5 px-3 text-center"><span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-black">만성 적자</span></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-4 p-4 bg-slate-950/60 rounded-xl border border-slate-800 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div>
            <h4 class="font-bold text-amber-400 flex items-center space-x-1.5 mb-1">
              <i class="fa-solid fa-chart-column"></i>
              <span>양극화 원인 1: 리베이트(S/D%) 요율의 극단적 편차</span>
            </h4>
            <p class="text-slate-300 leading-relaxed">
              Alltron과 EP는 출하 ASP가 $1,160~$1,230 수준으로 높은 반면, S/D%는 <strong>4.0%~5.9%</strong>에 불과하여 건강한 프리미엄 시장을 형성하고 있습니다. 반면 MSH와 FUST는 ASP가 $720~$760 수준임에도 S/D%가 <strong>38.0%~38.3%</strong>에 달해 유통의 판가 인하를 법인 마진으로 메워주고 있습니다.
            </p>
          </div>
          <div>
            <h4 class="font-bold text-rose-400 flex items-center space-x-1.5 mb-1">
              <i class="fa-solid fa-hand-holding-dollar"></i>
              <span>양극화 원인 2: 적자 채널 2사(MSH+FUST)의 연간 마진 누수액</span>
            </h4>
            <p class="text-slate-300 leading-relaxed">
              MSH(-$430K)와 FUST(-$100K) 단 2개 채널에서만 8개월간 <strong class="text-rose-400">-$530K의 순영업손실</strong>이 발생했습니다. 이 두 채널의 S/D%를 25% 수준으로만 정상화해도 스위스 법인 영업이익은 즉각 +$1,170K 추가 증가(COI 13.8% → 17.0%)할 수 있는 잠재력을 보유하고 있습니다.
            </p>
          </div>
        </div>
      </div>

    </section>

    <!-- ========================================== -->
    <!-- TAB 3: 4P Strategic Roadmap & Action Items -->
    <!-- ========================================== -->
    <section id="tab-4p-action" class="tab-pane hidden space-y-6">

      <!-- Strategic Framework Header -->
      <div class="bg-gradient-to-r from-brand-dark/40 via-slate-900 to-slate-900 border border-brand-red/30 rounded-2xl p-6 shadow-sm">
        <div class="flex items-center space-x-3 mb-2">
          <span class="w-8 h-8 rounded-lg bg-brand-red text-white flex items-center justify-center font-black text-sm">4P</span>
          <h2 class="text-xl font-black text-white">스위스 TV 손익 턴어라운드 및 고수익 체질화 4P 전략 로드맵</h2>
        </div>
        <p class="text-slate-300 text-sm leading-relaxed">
          스위스 시장은 높은 구매력을 보유한 고소득 국가로서, 가격 출혈 경쟁을 지양하고 <strong>프리미엄 믹스 고도화</strong>와 <strong>유통 채널 정상화</strong>를 통해 영업이익률 15% 이상을 상시 달성할 수 있는 최적의 체질을 갖추고 있습니다. 아래 4대 축의 실행 과제를 추진합니다.
        </p>
      </div>

      <!-- 4P Strategic Pillars -->
      <div class="space-y-6">

        <!-- 1. PRODUCT STRATEGY -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 relative overflow-hidden shadow-sm">
          <div class="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div class="flex items-center space-x-3">
              <span class="px-3 py-1 rounded-lg bg-indigo-500/20 text-indigo-400 font-black text-sm border border-indigo-500/30">PRODUCT</span>
              <h3 class="font-bold text-white text-base">OLED 초대형 프리미엄 고착화 & QNED 라인업 재정립</h3>
            </div>
            <span class="text-xs px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-300 font-semibold">목표: OLED ASP $1,200선 회복 & 믹스 마진 +1.5%p</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-indigo-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-1"></i>
                <span>OLED 65형 이상 초대형 비중 50% 돌파</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • <strong>현상:</strong> 2026년 OLED 수량은 20.9K로 성장했으나 55형 이하 비중 확대로 ASP가 $1,227 → $1,151로 하락.<br>
                • <strong>실행 과제:</strong> 65형 및 77/83형 C/G 시리즈 공급 우선 배정 및 프리미엄 번들링 프로모션(사운드바 무상/할인 결합)을 집중 전개하여 인치당 평균 판가 견인.
              </p>
            </div>

            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-indigo-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-2"></i>
                <span>QNED 미니LED 중심 고수익 라인업 전환</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • <strong>현상:</strong> QNED 수량이 9.7K대로 급증했으나 ASP $581, S/D% 26.2%로 엔트리급 중심 판매로 변질.<br>
                • <strong>실행 과제:</strong> 저가 QNED80 계열 공급 쿼터를 통제하고 고수익 미니LED QNED85/90 이상 모델의 마케팅 펀드를 신설하여 QNED 본연의 프리미엄 포지셔닝 회복.
              </p>
            </div>

            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-indigo-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-3"></i>
                <span>MRGB / 라이프스타일 스케일업</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • <strong>현상:</strong> 2026년 신규 런칭한 MRGB는 647대 판매, COI% 17.9%($103K)로 초고마진 입증.<br>
                • <strong>실행 과제:</strong> 스위스 고소득 인테리어 수요층을 겨냥해 StanbyME, Posé, Easel 등 라이프스타일 및 MRGB 라인업 전시 매장을 연내 120개점으로 2배 확대.
              </p>
            </div>
          </div>
        </div>

        <!-- 2. PRICE STRATEGY -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 relative overflow-hidden shadow-sm">
          <div class="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div class="flex items-center space-x-3">
              <span class="px-3 py-1 rounded-lg bg-rose-500/20 text-rose-400 font-black text-sm border border-rose-500/30">PRICE</span>
              <h3 class="font-bold text-white text-base">판가 하한선(Floor Price) 가이드라인 엄격 통제</h3>
            </div>
            <span class="text-xs px-2.5 py-1 rounded-full bg-rose-500/10 text-rose-300 font-semibold">목표: 판가 하락(Price Effect -$653K) 완전 방어</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-rose-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-1"></i>
                <span>Minimum Advertised Price (MAP) 제도 도입</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • 대형 양판점의 온라인 상 무분별한 덤핑 가격 노출을 차단하기 위해 유통 계약서 내 MAP 가이드라인을 의무화.<br>
                • 규정 위반 유통에 대해 마케팅 지원금 지급을 자동 유예하는 삼진아웃 페널티 시스템 가동.
              </p>
            </div>

            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-rose-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-2"></i>
                <span>원가 절감분의 판가 인하 전이 차단</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • 2026년 재료비 절감분(+$1,615K) 중 상당액이 유통 판촉비로 흡수되어 실질 판가 하락으로 연결됨.<br>
                • 본사 원가 절감 시 법인 출하가 인하를 동결하고, 절감 마진을 법인 영업이익 유보금으로 확보하는 가격 결정 프로세스 구축.
              </p>
            </div>

            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-rose-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-3"></i>
                <span>채널별 전용 모델(Derivation) 분리</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • 동일 모델이 가격 비교 사이트(Toppreise 등)에서 무한 최저가 경쟁을 벌이지 않도록 대형 양판점(MSH/Conforama)과 전문 총판(Alltron/EP) 전용 스펙 이원화 운영.
              </p>
            </div>
          </div>
        </div>

        <!-- 3. PLACE STRATEGY -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 relative overflow-hidden shadow-sm">
          <div class="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div class="flex items-center space-x-3">
              <span class="px-3 py-1 rounded-lg bg-amber-500/20 text-amber-400 font-black text-sm border border-amber-500/30">PLACE</span>
              <h3 class="font-bold text-white text-base">적자 유통(MSH / FUST) 정상화 & 고수익 전문 채널 볼륨 확대</h3>
            </div>
            <span class="text-xs px-2.5 py-1 rounded-full bg-amber-500/10 text-amber-300 font-semibold">목표: 적자 채널 흑자 전환 (+ $600K 개선)</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-amber-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-1"></i>
                <span>MSH / FUST 비상 수익성 개선 TF 가동</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • <strong>핵심 조치:</strong> S/D%를 현행 38% 수준에서 상한선(Cap) 28% 이하로 강제 제한.<br>
                • 유통 마진 보전용 사후 보상금을 전면 중단하고, 최소 영업이익률(COI% +2% 이상) 미달 모델은 출하를 즉각 중단(Stop-Shipment).
              </p>
            </div>

            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-amber-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-2"></i>
                <span>Alltron / EP 고수익 총판 공급 우선권 부여</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • Alltron(COI 26.3%), EP(COI 23.8%)는 합산 $10.0M 매출과 $2.51M의 영업이익을 창출하는 핵심 기반.<br>
                • 신제품 출시 시 2~4주간 독점 선공급 혜택 및 연간 목표 달성 시 분기 성과 인센티브(Rebate 2%)를 설계하여 총판 충성도 극대화.
              </p>
            </div>

            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-amber-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-3"></i>
                <span>자사몰(Online D2C) 매출 비중 15%로 확대</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • 자사몰 실적: 매출 $3.43M, ASP $1,143, COI 15.4%로 유통 마진 누수 없는 고수익 채널.<br>
                • 프리미엄 설치 서비스(Wall-Mount 무료), 추가 보증 3년 제공 등 D2C 전용 밸류 프로포지션을 강화하여 유통 의존도를 축소.
              </p>
            </div>
          </div>
        </div>

        <!-- 4. PROMOTION STRATEGY -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 relative overflow-hidden shadow-sm">
          <div class="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div class="flex items-center space-x-3">
              <span class="px-3 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 font-black text-sm border border-emerald-500/30">PROMOTION</span>
              <h3 class="font-bold text-white text-base">Sell-In 일괄 리베이트 축소 & 실판매(Sell-Out) 연동형 전환</h3>
            </div>
            <span class="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-300 font-semibold">목표: S/D% 23.9% → 21.0%로 축소 (연간 $1.0M 절감)</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-emerald-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-1"></i>
                <span>Trade Term(Sell-In 기본 계약) 삭감</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • 실질 판매와 무관하게 유통 입점 조건으로 일괄 공제되는 Sell-In 리베이트 요율을 현행 대비 2~3%p 축소.<br>
                • 유통의 재고 밀어넣기(Push) 유인을 제거하고 재고 건전성 확보.
              </p>
            </div>

            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-emerald-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-2"></i>
                <span>Sell-Out 캐시백 및 소비자 직접 프로모션</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • 유통에 자금을 지원하는 대신 최종 소비자 대상 'LG OLED 스위스 캐시백 캠페인'(구매 영수증 등록 시 CHF 200~500 환급)으로 마케팅 예산 이관.<br>
                • 유통 중간 마진 잠식을 원천 차단하고 실판매를 직결 자극.
              </p>
            </div>

            <div class="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div class="font-bold text-emerald-400 flex items-center space-x-1.5 text-sm">
                <i class="fa-solid fa-3"></i>
                <span>Co-Op(공동 광고비) 감사 및 ROI 정밀 검증</span>
              </div>
              <p class="text-slate-300 leading-relaxed">
                • 유통 전단지/웹 배너 게재 비용 등 집행 내역의 실질 노출 여부를 전수 검증하고, ROI 기준 미달 유통에는 차기 분기 Co-Op 예산 자동 삭감 조치.
              </p>
            </div>
          </div>
        </div>

      </div>

      <!-- Execution Timeline & Milestone Road -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <h3 class="font-bold text-white text-base mb-4 flex items-center space-x-2">
          <i class="fa-solid fa-timeline text-brand-light"></i>
          <span>4P 혁신 과제 단계별 실행 로드맵 (Execution Milestones)</span>
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 relative">
            <span class="text-xs font-bold px-2 py-0.5 rounded bg-brand-red/20 text-brand-light">Phase 1: '26. 10월</span>
            <h4 class="font-bold text-white mt-2 text-sm">MSH/FUST 거래 조건 재협상</h4>
            <p class="text-slate-400 mt-1.5 leading-relaxed">
              • MSH/FUST 대상 S/D 상한선(28%) 통보 및 Black Friday 프로모션 가이드라인 합의.<br>
              • 최저 출하가 가이드라인 공표.
            </p>
          </div>
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 relative">
            <span class="text-xs font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300">Phase 2: '26. 11~12월</span>
            <h4 class="font-bold text-white mt-2 text-sm">성수기 Sell-Out 프로모션 전개</h4>
            <p class="text-slate-400 mt-1.5 leading-relaxed">
              • OLED 초대형 스위스 전국 소비자 캐시백 가동.<br>
              • Alltron/EP 프리미엄 독점 모델 집중 판촉 전개.<br>
              • 덤핑 거래선 출하량 즉시 제어.
            </p>
          </div>
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 relative">
            <span class="text-xs font-bold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300">Phase 3: '27. 1분기</span>
            <h4 class="font-bold text-white mt-2 text-sm">2027년 신모델 라인업/가격 재편</h4>
            <p class="text-slate-400 mt-1.5 leading-relaxed">
              • Y27 신모델 런칭 시 채널 전용 파생 모델 체계 안착.<br>
              • QNED 미니LED 라인업 비중 확대.<br>
              • MRGB 전문 전시 매장 120개점 확대.
            </p>
          </div>
          <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 relative">
            <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">Phase 4: '27. 상반기</span>
            <h4 class="font-bold text-white mt-2 text-sm">COI 15% 이상 상시 고수익 정착</h4>
            <p class="text-slate-400 mt-1.5 leading-relaxed">
              • 스위스 법인 연간 매출 $55M+, COI% 15.0% 이상 상시 달성.<br>
              • 자사몰 매출 비중 15% 돌파.<br>
              • 전 유통 거래선 흑자화 달성.
            </p>
          </div>
        </div>
      </div>

    </section>

    <!-- ========================================== -->
    <!-- TAB 4: Interactive Simulation & Detail Explorer -->
    <!-- ========================================== -->
    <section id="tab-simulator" class="tab-pane hidden space-y-6">

      <!-- Interactive Margin Simulator -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="font-bold text-white text-base flex items-center space-x-2">
              <i class="fa-solid fa-calculator text-emerald-400"></i>
              <span>유통 채널 매출차감률(S/D%) 개선 시뮬레이터</span>
            </h3>
            <p class="text-xs text-slate-400 mt-0.5">MSH 및 FUST의 S/D% 축소 조정 시 법인 전체 영업이익(COI) 개선 효과를 실시간 연산합니다.</p>
          </div>
          <button onclick="resetSimulator()" class="text-xs px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition border border-slate-700">
            기본값 초기화
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 p-4 bg-slate-950/60 rounded-xl border border-slate-800">
          <div class="space-y-4 text-xs">
            <!-- Slider 1: MSH S/D reduction -->
            <div>
              <div class="flex items-center justify-between font-bold text-slate-200 mb-1.5">
                <span>MSH (MediaMarkt) S/D% 감축 목표 (현재 38.0%)</span>
                <span id="label-msh-sd" class="text-rose-400 font-black text-sm">38.0% (-0.0%p)</span>
              </div>
              <input type="range" id="slider-msh-sd" min="20" max="38" step="0.5" value="38" oninput="updateSim()" class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-brand-red">
              <div class="flex justify-between text-[11px] text-slate-500 mt-1">
                <span>공격적 개선: 20%</span>
                <span>권고 상한: 28%</span>
                <span>현재 실적: 38%</span>
              </div>
            </div>

            <!-- Slider 2: FUST S/D reduction -->
            <div>
              <div class="flex items-center justify-between font-bold text-slate-200 mb-1.5">
                <span>FUST S/D% 감축 목표 (현재 38.3%)</span>
                <span id="label-fust-sd" class="text-rose-400 font-black text-sm">38.3% (-0.0%p)</span>
              </div>
              <input type="range" id="slider-fust-sd" min="20" max="38.3" step="0.5" value="38.3" oninput="updateSim()" class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-brand-red">
              <div class="flex justify-between text-[11px] text-slate-500 mt-1">
                <span>공격적 개선: 20%</span>
                <span>권고 상한: 28%</span>
                <span>현재 실적: 38.3%</span>
              </div>
            </div>

            <!-- Slider 3: QNED S/D reduction -->
            <div>
              <div class="flex items-center justify-between font-bold text-slate-200 mb-1.5">
                <span>QNED 세그먼트 S/D% 감축 목표 (현재 26.2%)</span>
                <span id="label-qned-sd" class="text-sky-400 font-black text-sm">26.2% (-0.0%p)</span>
              </div>
              <input type="range" id="slider-qned-sd" min="18" max="26.2" step="0.5" value="26.2" oninput="updateSim()" class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-sky-500">
              <div class="flex justify-between text-[11px] text-slate-500 mt-1">
                <span>'25년 수준: 20.5%</span>
                <span>현재 실적: 26.2%</span>
              </div>
            </div>
          </div>

          <!-- Simulation Output Results -->
          <div class="bg-slate-900 p-5 rounded-xl border border-slate-800 flex flex-col justify-between">
            <div>
              <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block">시뮬레이션 반영 후 예상 성과</span>
              <div class="mt-3 grid grid-cols-2 gap-3">
                <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                  <span class="text-[11px] text-slate-400 block">예상 추가 이익 창출</span>
                  <span id="sim-added-profit" class="text-xl font-black text-emerald-400">+$0K</span>
                </div>
                <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                  <span class="text-[11px] text-slate-400 block">수정 전사 영업이익</span>
                  <span id="sim-new-coi" class="text-xl font-black text-white">$4,972K</span>
                </div>
              </div>
              <div class="mt-3 bg-slate-950 p-3 rounded-lg border border-slate-800 flex items-baseline justify-between">
                <span class="text-xs text-slate-300">수정 영업이익률 (COI%)</span>
                <div class="flex items-baseline space-x-1.5">
                  <span class="text-slate-400 text-xs line-through">13.78%</span>
                  <span class="text-slate-400 text-xs">→</span>
                  <span id="sim-new-coi-rate" class="text-2xl font-black text-emerald-400">13.78%</span>
                </div>
              </div>
            </div>
            <div id="sim-feedback" class="text-xs text-slate-400 mt-3 border-t border-slate-800 pt-2.5">
              슬라이더를 조정하여 적자 유통의 할인율 정상화 시 이익 개선 효과를 확인하세요.
            </div>
          </div>
        </div>
      </div>

      <!-- Segment x Inch Cross Analysis Table -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <h3 class="font-bold text-white text-base mb-3 flex items-center space-x-2">
          <i class="fa-solid fa-up-right-and-down-left-from-center text-sky-400"></i>
          <span>인치대(Screen Size)별 3개년 수량 및 판가(ASP) 변화 추이</span>
        </h3>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-slate-800/80 text-slate-300 border-b border-slate-700 font-semibold">
                <th class="py-2.5 px-3">인치 구분</th>
                <th class="py-2.5 px-3 text-right">'24 판매 수량</th>
                <th class="py-2.5 px-3 text-right">'25 판매 수량</th>
                <th class="py-2.5 px-3 text-right">'26 판매 수량</th>
                <th class="py-2.5 px-3 text-right">'24 ASP</th>
                <th class="py-2.5 px-3 text-right">'25 ASP</th>
                <th class="py-2.5 px-3 text-right text-emerald-400 font-bold">'26 ASP</th>
                <th class="py-2.5 px-3 text-right font-bold">'26 COI%</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800 text-slate-200">
              <tr class="hover:bg-slate-800/40">
                <td class="py-2 px-3 font-semibold text-slate-300">&lt; 50형 (중소형)</td>
                <td class="py-2 px-3 text-right">11,881대</td>
                <td class="py-2 px-3 text-right">9,475대</td>
                <td class="py-2 px-3 text-right">9,958대</td>
                <td class="py-2 px-3 text-right">$498</td>
                <td class="py-2 px-3 text-right">$530</td>
                <td class="py-2 px-3 text-right text-slate-200 font-bold">$545</td>
                <td class="py-2 px-3 text-right text-slate-300">4.3%</td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="py-2 px-3 font-semibold text-slate-300">50 ~ 59형 (중형 메인)</td>
                <td class="py-2 px-3 text-right">13,074대</td>
                <td class="py-2 px-3 text-right">12,456대</td>
                <td class="py-2 px-3 text-right font-bold">13,240대</td>
                <td class="py-2 px-3 text-right">$614</td>
                <td class="py-2 px-3 text-right">$685</td>
                <td class="py-2 px-3 text-right text-rose-300 font-bold">$644</td>
                <td class="py-2 px-3 text-right text-slate-300">7.3%</td>
              </tr>
              <tr class="hover:bg-slate-800/40 bg-indigo-950/20 font-semibold">
                <td class="py-2 px-3 text-indigo-300">60 ~ 69형 (대형 OLED/QNED)</td>
                <td class="py-2 px-3 text-right">10,185대</td>
                <td class="py-2 px-3 text-right">10,109대</td>
                <td class="py-2 px-3 text-right font-bold text-white">11,579대</td>
                <td class="py-2 px-3 text-right">$822</td>
                <td class="py-2 px-3 text-right">$996</td>
                <td class="py-2 px-3 text-right text-white font-bold">$959</td>
                <td class="py-2 px-3 text-right text-emerald-400 font-black">11.6%</td>
              </tr>
              <tr class="hover:bg-slate-800/40 bg-indigo-950/20 font-semibold">
                <td class="py-2 px-3 text-indigo-300">70 ~ 79형 (프리미엄 대형)</td>
                <td class="py-2 px-3 text-right">4,278대</td>
                <td class="py-2 px-3 text-right">3,980대</td>
                <td class="py-2 px-3 text-right font-bold text-white">4,185대</td>
                <td class="py-2 px-3 text-right">$1,292</td>
                <td class="py-2 px-3 text-right text-emerald-400 font-bold">$1,441</td>
                <td class="py-2 px-3 text-right text-white font-bold">$1,396</td>
                <td class="py-2 px-3 text-right text-emerald-400 font-black">12.6%</td>
              </tr>
              <tr class="hover:bg-slate-800/40 bg-purple-950/30 font-bold">
                <td class="py-2 px-3 text-purple-300">80형 이상 (초대형 울트라)</td>
                <td class="py-2 px-3 text-right">2,092대</td>
                <td class="py-2 px-3 text-right">1,677대</td>
                <td class="py-2 px-3 text-right font-black text-emerald-300">2,277대</td>
                <td class="py-2 px-3 text-right">$1,371</td>
                <td class="py-2 px-3 text-right font-black text-emerald-400">$1,853</td>
                <td class="py-2 px-3 text-right font-black text-emerald-400">$1,824</td>
                <td class="py-2 px-3 text-right text-emerald-400 font-black">9.5%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </section>

  </main>

  <!-- Footer -->
  <footer class="mt-12 border-t border-slate-800 py-6 text-center text-xs text-slate-500">
    <p>LG Electronics European Operations • TV Sales Management Portal • Swiss Branch P&L & 4P Strategic Advisory Report</p>
    <p class="mt-1 text-[11px] text-slate-600">Generated on 2026-09-17 • Source Data: NERP Standard P&L Datamart (2024.01 ~ 2026.08)</p>
  </footer>

  <!-- Script Logic & Embedded Data -->
  <script>
    const PNL_DATA = {json.dumps(embedded_data, ensure_ascii=False)};

    // Tab Switcher
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.classList.remove('bg-brand-red', 'text-white', 'shadow-lg', 'shadow-brand-red/20');
        btn.classList.add('text-slate-400', 'font-medium');
      }});

      const targetPane = document.getElementById(tabId);
      if (targetPane) targetPane.classList.remove('hidden');

      const targetBtn = document.getElementById('btn-' + tabId);
      if (targetBtn) {{
        targetBtn.classList.add('bg-brand-red', 'text-white', 'shadow-lg', 'shadow-brand-red/20');
        targetBtn.classList.remove('text-slate-400', 'font-medium');
      }}

      // Trigger resize for charts if tab changed
      if (tabId === 'tab-overview') {{
        initOverviewCharts();
      }} else if (tabId === 'tab-4p-diagnostic') {{
        initDiagnosticCharts();
      }}
    }}

    // Charts Instances
    let chartWaterfallInst = null;
    let chartCostStackInst = null;
    let chartSegmentShareInst = null;

    function initOverviewCharts() {{
      // 1. Waterfall Chart
      const wfCtx = document.getElementById('chartWaterfall');
      if (wfCtx && !chartWaterfallInst) {{
        const wf = PNL_DATA.waterfall;
        const labels = ['2025 COI', '판매량 효과', '판가 효과', 'S/D 할인율', '재료/변동원가', '고정비/기타', '2026 COI'];
        
        // Waterfall logic
        const startVal = wf.last_coi / 1000;
        const vol = wf.volume / 1000;
        const prc = wf.price / 1000;
        const sd = wf.sd / 1000;
        const cogs = wf.var_cogs / 1000;
        const fixed = (wf.fixed_oh + wf.other_gap) / 1000;
        const endVal = wf.this_coi / 1000;

        const dataVals = [startVal, vol, prc, sd, cogs, fixed, endVal];
        const bgColors = [
          '#64748B',
          vol >= 0 ? '#10B981' : '#EF4444',
          prc >= 0 ? '#10B981' : '#EF4444',
          sd >= 0 ? '#10B981' : '#EF4444',
          cogs >= 0 ? '#10B981' : '#EF4444',
          fixed >= 0 ? '#10B981' : '#EF4444',
          '#A50034'
        ];

        chartWaterfallInst = new Chart(wfCtx, {{
          type: 'bar',
          data: {{
            labels: labels,
            datasets: [{{
              label: '영업이익 증감 (K$)',
              data: dataVals,
              backgroundColor: bgColors,
              borderRadius: 6
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ display: false }},
              tooltip: {{
                callbacks: {{
                  label: function(ctx) {{
                    const val = ctx.raw;
                    return (val >= 0 ? '+' : '') + val.toFixed(1) + ' K$';
                  }}
                }}
              }}
            }},
            scales: {{
              y: {{
                grid: {{ color: '#1F2937' }},
                ticks: {{ color: '#9CA3AF' }}
              }},
              x: {{
                grid: {{ display: false }},
                ticks: {{ color: '#9CA3AF', font: {{ size: 11 }} }}
              }}
            }}
          }}
        }});
      }}

      // 2. Cost Stack Chart
      const csCtx = document.getElementById('chartCostStack');
      if (csCtx && !chartCostStackInst) {{
        const labels = ['2024 YTD', '2025 YTD', '2026 YTD'];
        // Data from cost_stack
        // '24: mat 64.7%, cogs_other 6.0%, sga 27.1%, coi 2.3%
        chartCostStackInst = new Chart(csCtx, {{
          type: 'bar',
          data: {{
            labels: labels,
            datasets: [
              {{ label: '재료비율 (Material)', data: [64.67, 57.54, 56.46], backgroundColor: '#3B82F6', stack: 'stack1', borderRadius: 4 }},
              {{ label: '기타 제조원가/경비', data: [6.03, 5.46, 1.54], backgroundColor: '#6366F1', stack: 'stack1' }},
              {{ label: '판관비 (SG&A)', data: [27.03, 26.09, 28.22], backgroundColor: '#F59E0B', stack: 'stack1' }},
              {{ label: '영업이익률 (COI%)', data: [2.27, 10.91, 13.78], backgroundColor: '#10B981', stack: 'stack1', borderRadius: 4 }}
            ]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{
                position: 'bottom',
                labels: {{ color: '#9CA3AF', boxWidth: 12, font: {{ size: 11 }} }}
              }}
            }},
            scales: {{
              y: {{
                stacked: true,
                max: 100,
                grid: {{ color: '#1F2937' }},
                ticks: {{ color: '#9CA3AF', callback: v => v + '%' }}
              }},
              x: {{
                stacked: true,
                grid: {{ display: false }},
                ticks: {{ color: '#9CA3AF' }}
              }}
            }}
          }}
        }});
      }}
    }}

    function initDiagnosticCharts() {{
      const segCtx = document.getElementById('chartSegmentShare');
      if (segCtx && !chartSegmentShareInst) {{
        chartSegmentShareInst = new Chart(segCtx, {{
          type: 'doughnut',
          data: {{
            labels: ['OLED ($24.1M)', 'QNED ($5.6M)', 'UHD ($3.8M)', 'Others ($1.0M)', 'FHD ($1.0M)', 'MRGB ($0.6M)'],
            datasets: [{{
              data: [24.10, 5.63, 3.79, 1.02, 0.97, 0.58],
              backgroundColor: ['#A855F7', '#38BDF8', '#FBBF24', '#64748B', '#94A3B8', '#10B981'],
              borderWidth: 2,
              borderColor: '#0F172A'
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{
                position: 'right',
                labels: {{ color: '#E2E8F0', font: {{ size: 11 }}, boxWidth: 12 }}
              }}
            }}
          }}
        }});
      }}
    }}

    // Margin Simulator Logic
    function updateSim() {{
      const mshSlider = parseFloat(document.getElementById('slider-msh-sd').value);
      const fustSlider = parseFloat(document.getElementById('slider-fust-sd').value);
      const qnedSlider = parseFloat(document.getElementById('slider-qned-sd').value);

      const mshDeltaRate = (38.0 - mshSlider) / 100;
      const fustDeltaRate = (38.3 - fustSlider) / 100;
      const qnedDeltaRate = (26.2 - qnedSlider) / 100;

      document.getElementById('label-msh-sd').innerText = mshSlider.toFixed(1) + '% (-' + (38.0 - mshSlider).toFixed(1) + '%p)';
      document.getElementById('label-fust-sd').innerText = fustSlider.toFixed(1) + '% (-' + (38.3 - fustSlider).toFixed(1) + '%p)';
      document.getElementById('label-qned-sd').innerText = qnedSlider.toFixed(1) + '% (-' + (26.2 - qnedSlider).toFixed(1) + '%p)';

      // Gross Sales basis:
      // MSH Gross Sales approx $10,732K (since Net is $6,657K and SD% is 38.0%)
      const mshGross = 6656978 / (1 - 0.3797);
      const fustGross = 2342903 / (1 - 0.3827);
      const qnedGross = 5631499 / (1 - 0.262);

      const addedMshProfit = mshGross * mshDeltaRate;
      const addedFustProfit = fustGross * fustDeltaRate;
      const addedQnedProfit = qnedGross * qnedDeltaRate;

      const totalAdded = addedMshProfit + addedFustProfit + addedQnedProfit;
      const baseCoi = 4972182;
      const baseSales = 36076972;

      const newCoi = baseCoi + totalAdded;
      const newSales = baseSales + totalAdded;
      const newCoiRate = (newCoi / newSales) * 100;

      document.getElementById('sim-added-profit').innerText = '+ $' + Math.round(totalAdded / 1000).toLocaleString() + 'K';
      document.getElementById('sim-new-coi').innerText = '$' + Math.round(newCoi / 1000).toLocaleString() + 'K';
      document.getElementById('sim-new-coi-rate').innerText = newCoiRate.toFixed(2) + '%';

      const feedback = document.getElementById('sim-feedback');
      if (totalAdded > 0) {{
        feedback.innerHTML = '<span class="text-emerald-400 font-bold">시뮬레이션 분석:</span> MSH/FUST/QNED 할인율 정상화 시 영업이익이 현행 대비 <strong class="text-emerald-300">+$' + Math.round(totalAdded / 1000).toLocaleString() + 'K</strong> 증가하여 영업이익률이 <strong class="text-emerald-300">' + newCoiRate.toFixed(2) + '%</strong>에 도달합니다.';
      }} else {{
        feedback.innerText = '슬라이더를 조정하여 적자 유통의 할인율 정상화 시 이익 개선 효과를 확인하세요.';
      }}
    }}

    function resetSimulator() {{
      document.getElementById('slider-msh-sd').value = 38.0;
      document.getElementById('slider-fust-sd').value = 38.3;
      document.getElementById('slider-qned-sd').value = 26.2;
      updateSim();
    }}

    // Initial Load
    window.addEventListener('DOMContentLoaded', () => {{
      initOverviewCharts();
    }});
  </script>
</body>
</html>
"""

print(f"Writing report to {output_html_path}...")
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Report generated successfully! Size: {len(html_content):,} bytes")
