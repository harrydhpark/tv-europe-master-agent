# [Task] 20261007_스위스W41CPSI갱신

## 1. 질의 개요 (User Request)
- **실행 일시**: 2026-10-07
- **사용자 질의 원문**:
> "raw 데이터를 업데이트했어. 목표 주차를 41주로 스위스 대시보드 먼저 업데이트해줘"

- **연계 에이전트 (Dispatched Agents)**:
  - `01. GDMI_Weekly_Sellout_Analysis-main`

## 2. 생성 산출물 (Artifacts)
- 📄 **[Swiss_CPSI_Summary_Dashboard.html](./Swiss_CPSI_Summary_Dashboard.html)**
- 📄 **[metrics_Swiss.json](./metrics_Swiss.json)**

---

## 3. 핵심 요약 (Executive Summary)
스위스(Swiss) CPSI 워크북 및 대시보드 W41(실판매 보고 기준 W40 / 9월 28일) 주간 업데이트 완료. Raw Data 13,545행 추출/오버레이, 워크북 COM 갱신, Master_PD 실적 SUMIFS 변환, 분할 대시보드 4종 리빌드, Stitch 5-Tab HTML 빌드 완료.

---

## 4. 상세 분석 및 실행 답변 (Execution Output)

스위스 CPSI 대시보드 목표 주차 41(실판매 W40) 주간 업데이트 완료 보고\n\n- 기준 주차: W40 / 9월 28일 (GDMi System 기준)\n- 실판매(GDMi): 1,183대 (YoY -2.3%, 플랜 대비 달성률 211.2%)\n- 최근 4주 평균: 1,086대 (YoY -1.2%)\n- 연간 누적(YTD): 49,938대 (YoY +2.8%)\n- 채널 재고: 9,621대 (전년비 -457대)\n- 재고 주수(WOS): 8.9주 (적정 관리 구간 8.0~10.0주 Warning)\n- OLED 세그먼트: 609대 (비중 51.5%, YoY +10.3%, WOS 7.6주 Healthy)\n- QNED 세그먼트: 286대 (비중 24.2%, YoY -13.6%, WOS 11.9주)\n- 워크북 오류: 0건 (Dashboard 4종 전 시트 에러 0)\n- 단독 HTML 대시보드 빌드 및 Folder Keeper 3대 파일 정상 보존
