# [Task] 20261007_엑셀다운로드표준지침반영

## 1. 질의 개요 (User Request)
- **실행 일시**: 2026-10-07
- **사용자 질의 원문**:
> "지침과 스킬에 저장해줘"

- **연계 에이전트 (Dispatched Agents)**:
  - `01. GDMI Weekly Sellout Analysis`
  - `Web UI & Presentation Agent`

## 2. 생성 산출물 (Artifacts)
- 📄 **[AGENTS.md](./AGENTS.md)**
- 📄 **[SKILL.md](./SKILL.md)**

---

## 3. 핵심 요약 (Executive Summary)
대시보드 상단 헤더 원본 엑셀(.xlsb) 다운로드 버튼 신설 표준, 통합 빌더 엔진(build_cpsi_html_engine.py)의 __XLSB_FILENAME__ 동적 바인딩 로직, Firebase Hosting 배포 시 negative glob 미지원에 따른 ignore 설정 및 바이너리 MIME Content-Type 헤더 연동 규칙을 AGENTS.md 및 gdmi-cpsi-html SKILL.md에 영구 저장함.

---

## 4. 상세 분석 및 실행 답변 (Execution Output)

### 대시보드 엑셀 다운로드 표준 및 Firebase 배포 수칙 반영 완료

- **프로젝트 가이드라인**: AGENTS.md에 섹션 10(대시보드 원본 엑셀 다운로드 및 Firebase 호스팅 표준) 신설
- **스킬 지침**: gdmi-cpsi-html SKILL.md에 상단 헤더 고정 버튼 표준, __XLSB_FILENAME__ 자동 바인딩 로직 및 Firebase Anti-404 ignore/MIME 규칙 상세화
- **영구 보존**: 향후 주간 업데이트 및 유지보수 시 자동 표준 준수 보장
