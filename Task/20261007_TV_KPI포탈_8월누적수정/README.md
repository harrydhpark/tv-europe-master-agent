# [Task] 20261007_TV_KPI포탈_8월누적수정

## 1. 질의 개요 (User Request)
- **실행 일시**: 2026-10-07
- **사용자 질의 원문**:
> "첨부 이미지처럼 YTD(7월 누적)으로 되어 있는데 YTD(8월 누적)으로 바꿔줘"

- **연계 에이전트 (Dispatched Agents)**:
  - `06. KPI Sheet`
  - `Web UI & Presentation Agent`

## 2. 생성 산출물 (Artifacts)
- 📄 **[index.html](./index.html)**
- 📄 **[build_dashboard.js](./build_dashboard.js)**

---

## 3. 핵심 요약 (Executive Summary)
TV KPI 포탈(06. KPI Sheet)의 2026년 상단 KPI 요약 카드 뱃지 및 집계 범위를 기존 7월 누적(7월 말)에서 8월 누적(8월 말)으로 전면 교체(Net Sales, 영업이익, Sell-in, Sell-out 1~8월 합산 및 유통재고 8월말 기준 집계)하고 Firebase Hosting 라이브 배포 완료.

---

## 4. 상세 분석 및 실행 답변 (Execution Output)

### TV KPI 포탈 YTD 집계 기준 8월 누적/8월 말 수정 결과

- **라벨 변경**: YTD (7월 누적) ➔ YTD (8월 누적), YTD (7월 말) ➔ YTD (8월 말)
- **연산 범위 조정**:
  - Flow 지표 (Net Sales, 영업이익, Sell-in, Sell-out): H1(1~6월) + 7월 + 8월 누적 합산
  - 영업이익률 (%): 1~8월 누적 영업이익 / 1~8월 누적 Net Sales
  - Stock 지표 (유통재고): 8월 말 기준 잔여 재고
- **반영 파일**: index.html 및 build_dashboard.js 동기화 완료
- **배포 및 검증**: Firebase Hosting 라이브 배포 완료 (https://kpi-sheet-europe-2026.web.app)
