# [Task] 20261007_스위스65S85H가격조사

## 1. 질의 개요 (User Request)
- **실행 일시**: 2026-10-07
- **사용자 질의 원문**:
> "스위스 유통에서의 현재 65S85H의 가격 조사해줘"

- **연계 에이전트 (Dispatched Agents)**:
  - `04. Price Tracker`
  - `swiss_tv_tracker`

## 2. 생성 산출물 (Artifacts)
- 📄 **[Swiss_ATA_Comparison_2026_1006.xlsx](./Swiss_ATA_Comparison_2026_1006.xlsx)**
- 📄 **[raw_mediamarkt_samsung.json](./raw_mediamarkt_samsung.json)**
- 📄 **[raw_interdiscount_samsung.json](./raw_interdiscount_samsung.json)**
- 📄 **[raw_digitec_samsung.json](./raw_digitec_samsung.json)**

---

## 3. 핵심 요약 (Executive Summary)
스위스 3대 가전 유통사(Digitec, Interdiscount, MediaMarkt)의 Samsung 2026년형 65인치 OLED TV(65S85H) 현재 실판매가 전수 조사 및 시계열 변동 추이, LG 65B6 대비 가격 경쟁력 및 상위 모델(65S90H)과의 가격 역전 현상 분석 완료

---

## 4. 상세 분석 및 실행 답변 (Execution Output)

# 스위스 유통에서의 Samsung 65S85H 현재 가격 조사 보고서

## 1. 개요
- **대상 모델**: Samsung 65" OLED TV S85H (2026년형 4K OLED)
- **세부 모델 코드**: QE65S85H / QE65S85HAEXZU
- **조사 기준일**: 2026년 10월 7일 (최신 수집 회차: 2026.10.06 W41 마감 데이터 및 실시간 검증)
- **조사 유통 채널**: 스위스 3대 주요 가전 유통사 (Digitec, Interdiscount, MediaMarkt CH)

---

## 2. 유통사별 현재 판매 가격 및 프로모션 현황

| 유통사 | 판매 모델 코드 | 판매 가격 (CHF) | 캐시백 / 혜택 | 실질 체감가 (Net) | 배송 | 가격 포지션 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Digitec (Galaxus)** | QE65S85HAEXZU | **1,568.00 CHF** | 없음 (0 CHF) | **1,568.00 CHF** | 무료 | 🥇 **스위스 유통 최저가** |
| **Interdiscount** | QE65S85H | **1,699.95 CHF** | 없음 (0 CHF) | **1,699.95 CHF** | 무료 | 🥈 Digitec 대비 +131.95 CHF |
| **MediaMarkt CH** | QE65S85H | **1,816.95 CHF** | 없음 (0 CHF) | **1,816.95 CHF** | 무료 | 🥉 최고가 (Digitec 대비 +248.95 CHF) |

- **스위스 시장 최저가**: **Digitec의 1,568.00 CHF**
- **유통 채널별 가격 격차**: 최대 **248.95 CHF** (MediaMarkt 1,816.95 CHF vs Digitec 1,568.00 CHF)

---

## 3. 시계열 가격 변동 추이 (Price History Trend)

스위스 3대 유통사의 최근 10회차(7월 말 ~ 10월 초) 시계열 가격 데이터 분석 결과:

1. **Digitec (지속적 계단식 인하)**:
   - 07/28: 2,219.00 CHF
   - 09/01: 1,784.00 CHF (재입고)
   - 09/07: 1,699.00 CHF (-85 CHF)
   - 09/12: 1,666.00 CHF (-33 CHF)
   - 09/24: 1,633.00 CHF (-33 CHF)
   - 10/06 ~ 현재: **1,568.00 CHF** (-65 CHF, 최저가 경신)

2. **Interdiscount (대폭 인하 후 가격 고정)**:
   - 07/28: 2,499.95 CHF
   - 08/06: 2,299.95 CHF (-200 CHF)
   - 08/26: 1,999.95 CHF (-300 CHF)
   - 09/03 ~ 현재: **1,699.95 CHF** (-300 CHF, 누적 총 -800 CHF 인하 후 1개월 이상 동결)

3. **MediaMarkt CH (후발 등록 및 고가 유지)**:
   - 09/24: 1,832.65 CHF (온라인 최초 등록)
   - 09/29 ~ 현재: **1,816.95 CHF** (-15.70 CHF 소폭 조정 후 유지)

---

## 4. 경쟁사(LG) 및 라인업 비교 비즈니스 시사점

1. **LG 1:1 비교 모델(OLED65B68LA)과의 가격 비교**:
   - **Digitec**: LG 65B6 (1,799 CHF) vs 삼성 65S85H (1,568 CHF) ➔ **삼성 231 CHF 저렴** (ATA: 114.7)
   - **MediaMarkt**: LG 65B6 (1,899 CHF) vs 삼성 65S85H (1,816.95 CHF) ➔ **삼성 82.05 CHF 저렴** (ATA: 104.5)
   - **Interdiscount**: LG 65B6 미취급 (삼성 65S85H 단독 판매 중)
   - **시사점**: 스위스 엔트리 65인치 OLED 시장에서 삼성이 LG B6 대비 82~231 CHF 가량 낮은 가격으로 진입하여 가격 경쟁 우위를 적극 활용하고 있음.

2. **삼성 상위 라인업(65S90H)과의 가격 역전 현상**:
   - **MediaMarkt**: 상위 모델인 **65S90H**가 프로모션 특가 **1,699.00 CHF**로 판매되고 있어, 하위 모델인 **65S85H(1,816.95 CHF)**가 상위 모델보다 오히려 **117.95 CHF 비싼 가격 역전** 발생.
   - **Digitec**: 상위 65S90H(1,699 CHF) vs 하위 65S85H(1,568 CHF)로 131 CHF의 정상적인 티어별 가격 차이 유지 중.
