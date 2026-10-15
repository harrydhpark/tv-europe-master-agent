# [Task] 20261007_TV_KPI포탈엑셀다운로드구

## 1. 질의 개요 (User Request)
- **실행 일시**: 2026-10-07
- **사용자 질의 원문**:
> "동일한 방식으로 TV KPI 포탈에 06. KPI Sheet의 26년_유럽+CIS_KPI_2026 파일을 다운받을 수 있도록 해줘"

- **연계 에이전트 (Dispatched Agents)**:
  - `06. KPI Sheet`
  - `DevOps Agent`
  - `Web UI & Presentation Agent`

## 2. 생성 산출물 (Artifacts)
- 📄 **[index.html](./index.html)**
- 📄 **[firebase.json](./firebase.json)**
- 📄 **[build_dashboard.js](./build_dashboard.js)**
- 📄 **[AGENTS.md](./AGENTS.md)**

---

## 3. 핵심 요약 (Executive Summary)
TV KPI 포탈(06. KPI Sheet) 상단 Top Bar Header에 에메랄드 그린 테마의 원본 엑셀(26년_유럽+CIS_KPI_2026.xlsx) 다운로드 버튼을 신설하고, build_dashboard.js 템플릿 영구 반영 및 firebase.json ignore/headers 설정을 통해 실서버 라이브 다운로드(HTTP 200 OK)를 완벽히 구현함. 아울러 kpi-sheet-update SKILL.md 및 프로젝트 AGENTS.md에 표준으로 등록함.

---

## 4. 상세 분석 및 실행 답변 (Execution Output)

### TV KPI 포탈 엑셀 원본 다운로드 기능 구현 결과

- **대상 사이트**: TV KPI Portal (https://kpi-sheet-europe-2026.web.app)
- **버튼 UI**: 에메랄드 그린 테마, 스프레드시트 아이콘, Excel 다운로드 (.xlsx) 라벨
- **다운로드 대상 파일**: 26년_유럽+CIS_KPI_2026.xlsx (23.5MB)
- **호스팅 설정**: firebase.json ignore 조정 및 application/vnd.openxmlformats-officedocument.spreadsheetml.sheet 헤더 매핑
- **라이브 검증**: 실서버 HTTP 200 OK 다운로드 응답 확인 완료
- **지침 반영**: kpi-sheet-update SKILL.md 및 06. KPI Sheet/.agents/AGENTS.md 표준 등록 완료
