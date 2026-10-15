# [Task] 20261007_스위스대시보드엑셀다운로드구현

## 1. 질의 개요 (User Request)
- **실행 일시**: 2026-10-07
- **사용자 질의 원문**:
> "각 법인별 페이지에서 EXECUTIVE SUMMARY 장에서 C-PSI TV Sell-out 주간 요약 제목 옆에 엑셀파일을 다운받을수 있도록 해줘. 먼저 스위스의 경우 Swiss_CPSI_Revised_Final 엑셀파일 다운로드가 될 수 있도록 만들어줘"

- **연계 에이전트 (Dispatched Agents)**:
  - `01. GDMI Weekly Sellout Analysis`
  - `Web UI & Presentation Agent`

## 2. 생성 산출물 (Artifacts)
- 📄 **[Swiss_CPSI_Summary_Dashboard.html](./Swiss_CPSI_Summary_Dashboard.html)**
- 📄 **[firebase.json](./firebase.json)**

---

## 3. 핵심 요약 (Executive Summary)
스위스 C-PSI 대시보드 헤더의 C-PSI TV Sell-out 주간 요약 제목 우측에 Swiss_CPSI_Revised_Final.xlsb 원본 엑셀 다운로드 버튼을 신설하고, Firebase 호스팅 ignore 및 Content-Type 헤더 최적화를 통해 실서버 라이브 다운로드를 완벽 구현함. 또한 공통 빌드 엔진(build_cpsi_html_engine.py)에도 __XLSB_FILENAME__ 자동 바인딩 로직을 선제 반영함.

---

## 4. 상세 분석 및 실행 답변 (Execution Output)

### 스위스 C-PSI 엑셀 원본 다운로드 기능 구현 결과

- **버튼 UI 디자인**: 에메랄드 그린 테마, 스프레드시트 아이콘, Excel 다운로드 (.xlsb) 라벨
- **대상 파일**: Swiss_CPSI_Revised_Final.xlsb
- **Firebase 연동**: firebase.json ignore 목록 조정 및 application/vnd.ms-excel.sheet.binary.macroEnabled.12 헤더 설정
- **실서버 라이브 검증**: HTTP 200 OK 다운로드 확인 완료
