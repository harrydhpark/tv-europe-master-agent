# [Task] 20261006_스위스유통가격전수조사

## 1. 질의 개요 (User Request)
- **실행 일시**: 2026-10-06
- **사용자 질의 원문**:
> 1. "스위스 유통 가격 오늘자로 조사해서 업데이트해줘"
> 2. "/grill-me https://www.mediamarkt.ch/de/search.html?query=samsung%20oled%20s95h&searchFeatures%5B0%5D%5Bname%5D=suggest&searchFeatures%5B0%5D%5Bvalue%5D=1 에 대시보드 포함안된 모델이 있어. 추가해줘"

- **연계 에이전트 (Dispatched Agents)**:
  - `04. Price Tracker`
  - `swiss_tv_tracker`

## 2. 생성 산출물 (Artifacts)
- 📄 **[price tracker_swiss_2026 1006_v1.xlsx](./price%20tracker_swiss_2026%201006_v1.xlsx)**
- 📄 **[Swiss_ATA_Comparison_2026_1006.xlsx](./Swiss_ATA_Comparison_2026_1006.xlsx)**
- 📄 **[swiss_price_dashboard.html](./swiss_price_dashboard.html)**
- 📄 **[patch_swiss_s95h.py](./patch_swiss_s95h.py)**

---

## 3. 핵심 요약 (Executive Summary)
스위스 3대 유통사(MediaMarkt, Interdiscount, Digitec) 2026년 10월 6일(W41) 전수 가격 조사, MediaMarkt CH 마켓플레이스 파트너(Buchmann) 판매 Samsung OLED S95H 전 라인업(77", 65", 55", 48") 정밀 수집 및 Digitec 48S95H 1:1 매칭 신설, 엑셀/대시보드 반영, 27회차 시계열 DB 적재 및 Firebase 호스팅 배포 완료

---

## 4. 상세 분석 및 실행 답변 (Execution Output)

# 스위스 3대 유통사 TV 가격 조사 및 S95H 라인업 확장 보고서 (2026.10.06 / W41)

## 1. 개요 및 요약
- **조사 일자**: 2026년 10월 6일 (W41)
- **조사 대상 유통 채널**: MediaMarkt CH, Interdiscount CH, Digitec CH
- **조사 대상 모델**: 2025년 및 2026년형 LG vs Samsung TV 라인업
- **총 유효 수집 표본수**: 총 449개 모델 (MediaMarkt 182개, Interdiscount 107개, Digitec 160개)
- **데이터 품질 게이트(Quality Gates)**: R1~R4 이상치 검증 완료 (CRITICAL 0건, WARN 0건 - 100% 정상 통과)
- **S95H 플래그십 전수 보강**:
  - MediaMarkt CH 공식 파트너 판매자(Buchmann)를 통해 판매 중인 Samsung 2026년형 최고급 OLED **S95H 4개 전 라인업(77", 65", 55", 48")** 정밀 추가 및 실판매가 최신화
  - `Swiss_ATA_Comparison_2026_1006.xlsx`의 `Swiss_2026` 시트에 **`48S95H` 행을 신설(Row 31)**하고, Digitec에 등록된 `QE48S95HAEXZU`(1,916 CHF)와 MediaMarkt `QE48S95H`(1,985.25 CHF)를 1:1 완벽 페어링 매칭
- **시계열 히스토리 연계**: 총 27회차 누적 조사 데이터(07/04 ~ 10/06) 연계 및 주간 변동 분석(W31~W41) 최신화 완료
- **웹 대시보드 라이브 배포**: Firebase Hosting (https://swiss-price-tracker-lge.web.app) 배포 및 HTTP 200 OK 검증 완료

## 2. 채널별 수집 및 엑셀 적재 현황
| 유통사 | 브랜드 | 2025/2026 수집 모델 수 | 비고 |
| :--- | :--- | :---: | :--- |
| **MediaMarkt CH** | Samsung | 108개 | 직판 및 검증 파트너(Buchmann) 전수 수집 (S95H 전 인치, S90H, S85H, QN80H 등) |
| **MediaMarkt CH** | LG | 74개 | 직판 정품 전수 수집 (G6, C6, B68, MRGB87, QNED86B 등) |
| **Interdiscount CH** | Samsung | 70개 | 카테고리 기반 직판 필터링 및 노이즈 제거 |
| **Interdiscount CH** | LG | 37개 | 직판 정품 모델 매핑 완료 |
| **Digitec CH** | Samsung | 64개 (원천 113개) | 직판 최저가 기준 단일화 (48S95H 포함) |
| **Digitec CH** | LG | 96개 (원천 110개) | 직판 최저가 기준 단일화 |
| **합계** | **LG / Samsung** | **449개** | **무결성 100% 달성** |

## 3. Samsung OLED S95H vs LG OLED G6 비교 현황 (2026.10.06 최신화)
| 화면 크기 | LG 모델 (G6) | LG 실판매가 (CHF) | Samsung 모델 (S95H) | MediaMarkt CH (CHF) | Interdiscount CH (CHF) | Digitec CH (CHF) | 비고 |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| **83인치** | OLED83G67LW | 5,999 CHF | 83S95H | - | - | - | 미출시 / 품절 |
| **77인치** | OLED77G67LW | 4,999 CHF | **QE77S95H** | **4,553.70 CHF** | - | **4,328.00 CHF** | **신규 추가 (MSH)** |
| **65인치** | OLED65G67LW | 3,499 CHF | **QE65S95H** | **3,500.00 CHF** | 3,399.95 CHF | 3,329.00 CHF | **가격 갱신 (-170.55 CHF 인하)** |
| **55인치** | OLED55G67LW | 2,499 CHF | **QE55S95H** | **2,522.10 CHF** | - | - | 기 반영 |
| **48인치** | *(G6 미출시)* | - | **QE48S95H** | **1,985.25 CHF** | - | **1,916.00 CHF** | **신규 행 추가 (48S95H)** |

## 4. Pan-European Master URL Registry 영구 등록 내역
- `CH_MEDIAMARKT_SAMSUNG_QE77S95H`: `https://www.mediamarkt.ch/de/product/_samsung-qe77s95h-fernseher-77-1956-cm-uhd-4k-184263169.html`
- `CH_MEDIAMARKT_SAMSUNG_QE65S95H`: `https://www.mediamarkt.ch/de/product/_samsung-qe65s95h-oled-tv-65-1651-cm-uhd-4k-180857100.html`
- `CH_MEDIAMARKT_SAMSUNG_QE55S95H`: `https://www.mediamarkt.ch/de/product/_samsung-qe55s95h-oled-tv-55-1397-cm-uhd-4k-180857119.html`
- `CH_MEDIAMARKT_SAMSUNG_QE48S95H`: `https://www.mediamarkt.ch/de/product/_samsung-qe48s95haexzu-oled-tv-48-1219-cm-uhd-4k-180857089.html`
- 정기 수집 스크립트(`scripts/scrape_mediamarkt.py`)에 타깃 쿼리 `https://www.mediamarkt.ch/de/search.html?query=samsung%20oled%20s95h` 영구 등록 완료

## 5. W41(10.06) 주간 변동 주요 내용 (전주 09.29 대비)
- 총 변동 모델: 44개 (가격 인하 5건, 프로모션 1건, 신규 2건)
- **주요 가격 인하 (Price Drops)**:
  1. MediaMarkt Samsung 65" QE65S95H: 3,670.55 CHF -> 3,500.00 CHF (-170.55 CHF, -4.6%)
  2. MediaMarkt Samsung 100" QE100QN80H: 3,300 CHF -> 3,099 CHF (-201 CHF, -6.1%)
  3. MediaMarkt LG 65" 65MRGB87B9B: 1,299 CHF -> 1,199 CHF (-100 CHF, -7.7%)
  4. MediaMarkt LG 65" 65QNED71B6B: 699 CHF -> 599 CHF (-100 CHF, -14.3%)
  5. MediaMarkt LG 50" 50MRGB87B9B: 769 CHF -> 739 CHF (-30 CHF, -3.9%)
- 가격 인상(Hikes): 0건 (안정세 유지)
