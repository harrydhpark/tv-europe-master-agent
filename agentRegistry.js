/**
 * TV Europe Sales Master AI Agent - Sub-Agent Registry
 * Maps all 15+ sub-agents, local data files, tool definitions, and live health status.
 */

const fs = require('fs');
const path = require('path');

const AGENTS = [
  // 1. 매출/손익 관리 (6 Agents)
  {
    id: "daily-sales-progress",
    name: "Daily Sales Progress",
    category: "sales",
    categoryName: "매출/손익 관리",
    period: "daily",
    mentionTag: "@DailySales",
    icon: "ri-pulse-line",
    desc: "유럽 권역 및 법인별 당월 일간 실시간 매출 진척률, 일일 출하 및 Run-rate 모니터링",
    agentUrl: "https://eucisdailysales.apps.hedej.lge.com/",
    dataPath: null, // HedEj 사내 시스템 API 연동
    sampleQueries: [
      "오늘 유럽 전체 일일 출하 및 당월 매출 진척률(Run Rate) 어때?",
      "독일과 영국의 이번 달 목표 대비 출하 진척률 비교해줘"
    ],
    toolDefinition: {
      name: "get_daily_sales_progress",
      description: "유럽 권역 및 18개 법인별 당월 매출 실시간 진척률과 일일 출하 Run-rate 데이터를 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          subsidiary: { type: "string", description: "법인 코드 (예: ALL, DG, UK, FS, ES, IT 등)" }
        }
      }
    }
  },
  {
    id: "kpi-sheet",
    name: "KPI Sheet",
    category: "sales",
    categoryName: "매출/손익 관리",
    period: "weekly",
    mentionTag: "@KPI",
    icon: "ri-file-list-3-line",
    desc: "21개 지사/지점별 매출 실적, Sell-in/out, 신모델 비중, 유통 재고, WOS(-4) 핵심 영업 KPI 종합 모니터링",
    agentUrl: "https://kpi-sheet-europe-2026.web.app",
    dataPath: "../06. KPI Sheet/executive_insights.json",
    metricsPath: "../06. KPI Sheet/build_metrics.json",
    rawExcelPath: "../06. KPI Sheet/26년_유럽+CIS_KPI_2026.xlsx",
    pipelineScript: {
      type: "node",
      script: "build_dashboard.js",
      cwd: "../06. KPI Sheet"
    },
    sampleQueries: [
      "유럽 전체 및 주요 법인의 재고 주수(WOS) 현황과 위험 법인 알려줘",
      "독일 법인(DG)의 신모델 Sell-in 비중과 Sell-out 수량 실적 요약해줘",
      "새로 입고된 KPI 시트로 데이터 파이프라인 갱신 실행해줘"
    ],
    toolDefinition: {
      name: "get_kpi_metrics",
      description: "KPI Sheet의 매출 실적, Sell-in, Sell-out, 신모델 비중, 유통재고 및 WOS(-4) 지표를 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          subsidiary: { type: "string", description: "법인/지사 코드 (예: TTL, DG, UK, FS, ES 등)" },
          metricType: { type: "string", enum: ["all", "psi", "pnl", "competitiveness"], description: "지표 구분" }
        }
      }
    }
  },
  {
    id: "pnl-analysis",
    name: "TV P&L Analysis",
    category: "sales",
    categoryName: "매출/손익 관리",
    period: "monthly",
    mentionTag: "@P&L",
    icon: "ri-funds-box-line",
    desc: "TV 사업부 Gross/Net 매출, 매출원가, 판촉비, 한계이익, 영업이익률 심층 손익 분석",
    agentUrl: "https://lge-tv-pnl-2026.web.app",
    dataPath: "../05. TV P&L Analysis",
    pipelineScript: {
      type: "python",
      script: "run_pnl_pipeline.py",
      cwd: "../05. TV P&L Analysis"
    },
    sampleQueries: [
      "유럽 권역의 OLED와 QNED 영업이익률 및 한계이익 트렌드 비교해줘",
      "프랑스 법인(FS) 판촉비(BTL) 집행률과 손익에 미친 영향 분석해줘"
    ],
    toolDefinition: {
      name: "get_pnl_analysis",
      description: "TV P&L Analysis 에이전트로부터 매출원가, 판촉비, 한계이익률, 영업이익률 데이터를 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          subsidiary: { type: "string", description: "법인 코드 (예: EU_TOTAL, DG, UK, FS 등)" },
          series: { type: "string", description: "OLED, QNED 또는 전체" }
        }
      }
    }
  },
  {
    id: "gdmi-weekly",
    name: "GDMI Weekly Sellout",
    category: "sales",
    categoryName: "매출/손익 관리",
    period: "weekly",
    mentionTag: "@GDMI",
    icon: "ri-calendar-check-line",
    desc: "주차별 유럽 15개국 법인/유통 주간 Sellout 실적 및 유통 재고 분석 리포트",
    agentUrl: "https://gdmi-weekly-dashboard.web.app",
    dataPath: "../01. GDMI_Weekly_Sellout_Analysis-main/_data",
    pipelineScript: {
      type: "python",
      script: "run_multi_agent_pipeline.py",
      cwd: "../01. GDMI_Weekly_Sellout_Analysis-main"
    },
    sampleQueries: [
      "이번 주 독일과 영국의 MediaMarkt 및 Currys Sellout 실적 어때?",
      "주요 15개국 최근 4주간 주차별 Sellout 추세 브리핑해줘"
    ],
    toolDefinition: {
      name: "get_gdmi_weekly_sellout",
      description: "GDMI 주간 Sellout 실적, 유통사별(MediaMarkt, Currys 등) 판매량 및 주차별 트렌드를 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          country: { type: "string", description: "국가 코드 (예: DE, UK, FR, IT, ES 등)" },
          retailer: { type: "string", description: "유통사명 (선택 사항)" }
        }
      }
    }
  },
  {
    id: "pre-profitability",
    name: "선행 수익성 분석",
    category: "sales",
    categoryName: "매출/손익 관리",
    period: "monthly",
    mentionTag: "@PreProfit",
    icon: "ri-calculator-line",
    desc: "신규 수주 및 출하 전 시나리오별 선행 이익률 예측 및 시뮬레이션 타당성 검증",
    agentUrl: "https://lge-advance-profitability-2026.web.app",
    dataPath: "../09. 선행수익성/advance_profitability_data.json",
    pipelineScript: {
      type: "node",
      script: "build_from_source_sheets.js",
      cwd: "../09. 선행수익성"
    },
    sampleQueries: [
      "선행수익성 데이터에서 한계이익률 미달 리스크 모델/수주 건 필터링해줘",
      "출하 예정인 2026 신규 수주 건들의 평균 예상 마진율 요약해줘"
    ],
    toolDefinition: {
      name: "get_advance_profitability",
      description: "신규 수주 건의 선행 수익성, 예상 마진율, 출하 전 타당성 및 리스크 모델을 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          subsidiary: { type: "string", description: "법인 코드" },
          riskOnly: { type: "boolean", description: "수익성 미달 리스크 항목만 필터링 여부" }
        }
      }
    }
  },
  {
    id: "profit-simulator",
    name: "수익성 Simulator",
    category: "sales",
    categoryName: "매출/손익 관리",
    period: "monthly",
    mentionTag: "@Simulator",
    icon: "ri-dashboard-2-line",
    desc: "환율(FX), 제조원가, 유통 장려금 변동 민감도 시뮬레이션 및 손익 시나리오 분석 도구",
    agentUrl: "https://lge-profitability-simulator-2026.web.app",
    dataPath: "../10. 수익성 Simulator/simulator_data.json",
    engineScript: "../10. 수익성 Simulator/simulator_engine.js",
    sampleQueries: [
      "환율 EUR/USD가 1.05로 3% 절하되고 판촉비가 1% 증가할 때 유럽 전체 영업이익 영향은?",
      "독일 법인의 유통 장려금 2%p 상향 시 한계이익률 민감도 시뮬레이션 돌려줘"
    ],
    toolDefinition: {
      name: "simulate_profitability",
      description: "환율(FX), 원가, 판촉비/장려금 변동 시나리오를 적용하여 유럽 전체 및 법인별 예상 손익을 시뮬레이션합니다.",
      parameters: {
        type: "object",
        properties: {
          fxRateChangePct: { type: "number", description: "환율 변동률 (%) (예: -3.0)" },
          rebateRateChangePct: { type: "number", description: "유통장려금 변동률 (%p) (예: 1.5)" },
          costChangePct: { type: "number", description: "제조원가 변동률 (%) (예: 2.0)" },
          subsidiary: { type: "string", description: "대상 법인 (기본값: ALL)" }
        }
      }
    }
  },

  // 2. 제품 정보 (5 Agents)
  {
    id: "prm-consulting-2025",
    name: "2025/26 거래선 PRM",
    category: "product",
    categoryName: "제품 정보",
    period: "monthly",
    mentionTag: "@PRM",
    icon: "ri-slideshow-line",
    desc: "유럽 거래선 상담 실적 리뷰(OLED M/S 51%), 2026 전략 로드맵(Wallpaper 9.9mm), 48장 HD 슬라이드 뷰어",
    agentUrl: "https://lge-product-showcase-2026.web.app/docs/2025-prm-consulting/",
    dataPath: "../07. 제품 소개 사이트 자동 제작 에이전트/published/2025-prm-consulting",
    sampleQueries: [
      "2026년 거래선 상담자료에서 Wallpaper OLED 9.9mm 디자인 전략 요약해줘",
      "유럽 거래선 PRM 자료에서 강조된 LG OLED 시장 점유율(51%) 성과 슬라이드 내용 알려줘"
    ],
    toolDefinition: {
      name: "get_prm_consulting_info",
      description: "거래선 PRM 상담 프레젠테이션 슬라이드 내용, 제품 전략 로드맵, 핵심 메시지를 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          topic: { type: "string", description: "주제 키워드 (예: wallpaper, oled ms, qned, ai processor)" }
        }
      }
    }
  },
  {
    id: "spec-sheet",
    name: "Spec Sheet Finder",
    category: "product",
    categoryName: "제품 정보",
    period: "monthly",
    mentionTag: "@Spec",
    icon: "ri-article-line",
    desc: "OLED/QNED/NanoCell 모델별 세부 하드웨어 사양 비교 매트릭스 (155개 모델 x 146개 스펙 항목)",
    agentUrl: "https://lge-product-showcase-2026.web.app",
    dataPath: "../07. 제품 소개 사이트 자동 제작 에이전트/published/2026-tv-spec-finder/specData.js",
    sampleQueries: [
      "65인치 OLED G6와 C6의 프로세서, HDMI 단자 수, 주사율 스펙 비교해줘",
      "2026년 QNED 신모델 중 144Hz를 지원하는 라인업 모델명 리스트 뽑아줘"
    ],
    toolDefinition: {
      name: "query_tv_specs",
      description: "TV 모델별 세부 기술 사양(패널, 주사율, HDMI 2.1 포트 수, 오디오 출력 등)을 검색 및 비교합니다.",
      parameters: {
        type: "object",
        properties: {
          modelA: { type: "string", description: "비교 모델 A (예: OLED65G6)" },
          modelB: { type: "string", description: "비교 모델 B (예: OLED65C6)" },
          feature: { type: "string", description: "특정 스펙 항목 (예: hdmi, hz, audio, processor)" }
        }
      }
    }
  },
  {
    id: "tv-profile",
    name: "TV Product Profile",
    category: "product",
    categoryName: "제품 정보",
    period: "monthly",
    mentionTag: "@Profile",
    icon: "ri-presentation-line",
    desc: "전략 모델 및 시리즈별 USP, 셀링 포인트, 주요 유통 타깃 사양 프로파일",
    agentUrl: "https://lge-product-showcase-2026.web.app",
    dataPath: "../07. 제품 소개 사이트 자동 제작 에이전트/published",
    sampleQueries: [
      "OLED evo G6의 핵심 USP 3가지와 주요 유통 셀링 포인트 정리해줘"
    ],
    toolDefinition: {
      name: "get_product_profile",
      description: "전략 TV 모델의 USP, 핵심 셀링 포인트, 유통사 상담용 세일즈 피치를 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          series: { type: "string", description: "시리즈명 (예: G6, C6, B6, QNED90)" }
        }
      }
    }
  },
  {
    id: "dealer-trip-calendar",
    name: "거래선 방한 상담 캘린더",
    category: "product",
    categoryName: "제품 정보",
    period: "monthly",
    mentionTag: "@Calendar",
    icon: "ri-calendar-event-line",
    desc: "유럽/CIS 주요 거래선 방한 일정, 본사 미팅 스케줄 및 상담 내역 통합 관리",
    agentUrl: "https://dealertrip.apps.hedej.lge.com/",
    dataPath: null,
    sampleQueries: [
      "다음 달 방한 예정인 유럽 주요 유통 거래선(B2B/리테일) 미팅 일정 알려줘"
    ],
    toolDefinition: {
      name: "get_dealer_visit_calendar",
      description: "유럽/CIS 주요 거래선의 본사 방한 상담 일정 및 미팅 스케줄을 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          month: { type: "string", description: "조회 월 (예: 2026-10)" }
        }
      }
    }
  },

  // 3. 가격 관리 (3 Agents)
  {
    id: "price-tracker",
    name: "Price Tracker",
    category: "pricing",
    categoryName: "가격 관리",
    period: "daily",
    mentionTag: "@PriceTracker",
    icon: "ri-price-tag-3-line",
    desc: "유럽 11개국 온/오프라인 유통 실시간 판매가(ASP) 스크래핑, 1:1 라인업 매칭, 최저가 및 Price Gap 추적",
    agentUrl: "https://eu-price-tracker-lge.web.app",
    dataPath: "../04. Price Tracker/data/executive_summary_data.json",
    anomalyPath: "../04. Price Tracker/data/anomaly_report_20260916.json",
    sampleQueries: [
      "독일 MediaMarkt에서 LG 65인치 C4와 삼성 S90D의 실시간 판매 가격 및 가격 갭 얼마야?",
      "오늘 유럽 11개국에서 발생한 비정상 가격 급락(Anomaly Alert) 모델 목록 보여줘",
      "영국 Currys에서 LG OLED 모델들의 현재 프로모션 할인 현황 알려줘"
    ],
    toolDefinition: {
      name: "get_tracked_prices",
      description: "유럽 11개국 유통사별(MediaMarkt, Currys, Fnac 등) LG 및 경쟁사(삼성) 실시간 판매 가격, 최저가, Price Gap을 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          country: { type: "string", description: "국가 코드 (예: DE, UK, FR, IT, ES, SE 등)" },
          modelOrInch: { type: "string", description: "모델명 또는 인치대 (예: 65C4, 55B4, 65인치)" },
          retailer: { type: "string", description: "유통사명 (예: MediaMarkt, Currys)" }
        }
      }
    }
  },
  {
    id: "ata-guide",
    name: "ATA Guide",
    category: "pricing",
    categoryName: "가격 관리",
    period: "monthly",
    mentionTag: "@ATA",
    icon: "ri-shield-check-line",
    desc: "Authorization To Act / 권역별 최저 승인 판매 가격 가이드라인 및 승인 현황",
    agentUrl: "https://lge-product-showcase-2026.web.app/docs/ata-guide/",
    dataPath: "../07. 제품 소개 사이트 자동 제작 에이전트/published/ata-guide",
    sampleQueries: [
      "유럽 본사 승인 최저가(ATA Floor Price) 기준 65인치 C4의 국가별 가이드라인 얼마야?",
      "현재 ATA 승인 대기 중인 프로모션 특가 건 확인해줘"
    ],
    toolDefinition: {
      name: "get_ata_guideline",
      description: "권역별 최저 승인 판매 가격(ATA Floor Price) 가이드라인 및 승인 정책을 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          model: { type: "string", description: "모델명 (예: 65C4, 55B4)" },
          country: { type: "string", description: "국가 코드" }
        }
      }
    }
  },
  {
    id: "price-elasticity",
    name: "가격 탄력성 시뮬레이터",
    category: "pricing",
    categoryName: "가격 관리",
    period: "monthly",
    mentionTag: "@Elasticity",
    icon: "ri-line-chart-line",
    desc: "18개월 유럽 20개국 패널 회귀분석 기반 가격 변동에 따른 판매량 변화 및 4대 경쟁 대응 시뮬레이션",
    agentUrl: "https://lge-price-elasticity-2026.web.app",
    dataPath: "../12. 가격 탄력성 회귀분석",
    sampleQueries: [
      "2027 Q1에 유럽 OLED 가격을 3% 인상할 경우 예상되는 판매량 감소율과 매출 변화는?",
      "경쟁사 삼성이 가격을 5% 인하할 때 우리의 가격 대응 시나리오 4가지 시뮬레이션 결과 보여줘"
    ],
    toolDefinition: {
      name: "simulate_price_elasticity",
      description: "가격 탄력성 패널 회귀분석 모델을 기반으로 가격 인상/인하 시 판매량 및 경쟁사 대응 시나리오를 예측합니다.",
      parameters: {
        type: "object",
        properties: {
          priceChangePct: { type: "number", description: "LG 가격 변동률 (%) (예: 3.0)" },
          competitorScenario: { type: "string", enum: ["as_is", "follow_price", "aggressive_cut", "premium_defense"], description: "경쟁사 대응 시나리오" }
        }
      }
    }
  },

  // 4. 시장 정보 (4 Agents)
  {
    id: "gfk-monthly",
    name: "GfK Monthly Report",
    category: "market",
    categoryName: "시장 정보",
    period: "monthly",
    mentionTag: "@GfK",
    icon: "ri-pie-chart-2-line",
    desc: "유럽 15개국 GfK 월간 시장 실판매(Sellout), 시장 규모, 브랜드별/인치별 점유율 리포트",
    agentUrl: "https://gfk-report-monthly-lge.web.app",
    dataPath: "../02. GFK_Report_Monthly-main/00. GFK Report",
    sampleQueries: [
      "최신 8월 유럽 15개국 전체 TV 시장 규모(M/Size)와 성장률 트렌드 알려줘",
      "독일, 영국, 프랑스 3개국에서 LG의 OLED 및 전체 TV 점유율(M/S) 비교해줘"
    ],
    toolDefinition: {
      name: "get_gfk_market_report",
      description: "GfK 공인 월간 시장 규모, 판매량, 브랜드 점유율 및 세그먼트 실적을 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          country: { type: "string", description: "국가명 (예: Germany, UK, France, Italy, Spain 등)" },
          segment: { type: "string", enum: ["ALL", "OLED", "QNED", "UHD"], description: "제품 세그먼트" }
        }
      }
    }
  },
  {
    id: "ms-trend",
    name: "M/S Trend",
    category: "market",
    categoryName: "시장 정보",
    period: "weekly",
    mentionTag: "@MSTrend",
    icon: "ri-bar-chart-grouped-line",
    desc: "경쟁사(삼성, 소니, 하이센스) 대비 브랜드별/인치별 Market Share 트렌드",
    agentUrl: "https://tv-ms-trend-dashboard.web.app",
    dataPath: "../08. MS Trend/ms_trend_insights.json",
    diffDataPath: "../08. MS Trend/ms_trend_diff.json",
    pipelineScript: {
      type: "python",
      script: "run_pipeline.py",
      cwd: "../08. MS Trend"
    },
    sampleQueries: [
      "유럽 전체 OLED 시장에서 삼성과의 점유율 격차(Gap) 추이와 변화 요인 분석해줘",
      "초대형(75인치 이상) 세그먼트에서 하이센스와 TCL 점유율 급상승 국가 어디야?"
    ],
    toolDefinition: {
      name: "get_ms_trend",
      description: "경쟁사(Samsung, Sony, Hisense, TCL) 대비 LG TV의 주간/월간 점유율(Market Share) 트렌드를 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          segment: { type: "string", description: "세그먼트 (예: OLED, 75inch_plus, TTL)" },
          competitor: { type: "string", description: "비교 대상 경쟁사 (예: Samsung, TCL, Hisense)" }
        }
      }
    }
  },
  {
    id: "fx-monitor",
    name: "FX-Monitor",
    category: "market",
    categoryName: "시장 정보",
    period: "daily",
    mentionTag: "@FX",
    icon: "ri-money-dollar-circle-line",
    desc: "글로벌 주요 통화(EUR, USD, GBP, PLN 등) 실시간 환율 변동 추이 및 실적 리스크 분석",
    agentUrl: "https://fx-tracker-4f44c.web.app",
    dataPath: "../03. FX-Monitor-main/data/real_rates.json",
    commentaryPath: "../03. FX-Monitor-main/data/commentaries.json",
    sampleQueries: [
      "현재 EUR/USD, GBP/USD, EUR/PLN 실시간 환율과 연초 계획 대비 변동폭 알려줘",
      "최근 유로화 약세가 유럽 TV 사업부 손익에 미치는 리스크 브리핑해줘"
    ],
    toolDefinition: {
      name: "get_fx_rates",
      description: "주요 통화(EUR, USD, GBP, PLN)의 실시간 환율, 연초 계획 대비 격차 및 환리스크 분석 코멘터리를 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          currencyPair: { type: "string", description: "통화쌍 (예: EURUSD, GBPUSD, EURPLN)" }
        }
      }
    }
  },
  {
    id: "weekly-ms-analysis",
    name: "Weekly MS Analysis",
    category: "market",
    categoryName: "시장 정보",
    period: "weekly",
    mentionTag: "@WeeklyMS",
    icon: "ri-line-chart-fill",
    desc: "유럽 GfK 주간 실판매 요약 및 3대 핵심국가(FR, GB, IT) 주차별 MS 트렌드",
    agentUrl: null,
    dataPath: "../13. weekly MS Analysis",
    sampleQueries: [
      "최근 W35 주차 프랑스, 영국, 이탈리아 주간 판매량 및 MS 트렌드 요약해줘"
    ],
    toolDefinition: {
      name: "get_weekly_ms_analysis",
      description: "W35 등 주간 GfK 실판매 집계와 주요국(FR, GB, IT) 주차별 점유율을 조회합니다.",
      parameters: {
        type: "object",
        properties: {
          week: { type: "string", description: "주차 (예: W35, W34)" },
          country: { type: "string", description: "국가 (예: FR, GB, IT)" }
        }
      }
    }
  }
];

// Helper functions
function getAllAgents() {
  return AGENTS;
}

function getAgentById(id) {
  return AGENTS.find(a => a.id === id);
}

function findAgentByMention(text) {
  if (!text) return null;
  const lower = text.toLowerCase();
  return AGENTS.find(a => lower.includes(a.mentionTag.toLowerCase()));
}

function getAgentStatusSummary(baseDir = __dirname) {
  return AGENTS.map(agent => {
    let hasData = false;
    let lastModified = null;
    let fileSizeBytes = 0;

    if (agent.dataPath) {
      const fullPath = path.resolve(baseDir, agent.dataPath);
      try {
        if (fs.existsSync(fullPath)) {
          const stat = fs.statSync(fullPath);
          hasData = true;
          lastModified = stat.mtime.toISOString();
          fileSizeBytes = stat.size;
        }
      } catch (e) {
        // pass
      }
    }

    return {
      id: agent.id,
      name: agent.name,
      category: agent.category,
      categoryName: agent.categoryName,
      period: agent.period,
      mentionTag: agent.mentionTag,
      icon: agent.icon,
      desc: agent.desc,
      agentUrl: agent.agentUrl,
      dataPath: agent.dataPath,
      pipelineScript: agent.pipelineScript || null,
      hasLocalData: hasData,
      lastModified: lastModified || (agent.period === "daily" ? "Today (Live)" : "Latest Active"),
      fileSizeBytes: fileSizeBytes,
      status: hasData || agent.agentUrl ? "online" : "standby"
    };
  });
}

function getToolDeclarations() {
  return AGENTS.map(a => a.toolDefinition).filter(Boolean);
}

module.exports = {
  AGENTS,
  getAllAgents,
  getAgentById,
  findAgentByMention,
  getAgentStatusSummary,
  getToolDeclarations
};
