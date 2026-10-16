# [Task] 20261016_포털마스터에이전트연동

## 1. 질의 개요 (User Request)
- **실행 일시**: 2026-10-16
- **사용자 질의 원문**:
> "/grill-me sales portal에서 프롬프트로 작업을 지시할 경우 안티그래비티의 AXIS master agent에 연결하여 작업을 수행하는 업무 플로우를 구현할 수 있나요? 에이전트에 직접 프롬프트로 작업을 지시하는것과 동일한 수준의 output을 얻을 수 있는 방법을 알려줘"

- **연계 에이전트 (Dispatched Agents)**:
  - `00. Sales Management Portal`
  - `99. Master AI Agent`
  - `Antigravity Sidecar (axis-portal-bridge)`

## 2. 생성 산출물 (Artifacts)
- 📄 **[AXIS_Portal_MasterAgent_Workflow_Report.html](./AXIS_Portal_MasterAgent_Workflow_Report.html)**
- 📄 **[start_sidecar_bridge.js](./start_sidecar_bridge.js)**
- 📄 **[antigravity_sidecar_engine.js](./antigravity_sidecar_engine.js)**
- 📄 **[axis_portal_bridge.js](./axis_portal_bridge.js)**
- 📄 **[axis_portal_bridge.css](./axis_portal_bridge.css)**
- 📄 **[START_AXIS_PORTAL_BRIDGE.bat](./START_AXIS_PORTAL_BRIDGE.bat)**
- 📄 **[sidecar.json](./sidecar.json)**

---

## 3. 핵심 요약 (Executive Summary)
00. TV Europe Sales Management Portal 상단 통합 AI 커맨드 바 + 우측 3-Tab 슬라이드 드로어 구축 및 Antigravity Sidecar(agentapi) + 실시간 transcript.jsonl 미러링 + 100% 무인 Task/ 아카이빙 파이프라인 전체 구현 완료

---

## 4. 상세 분석 및 실행 답변 (Execution Output)

## 1. 개요 및 설계 확정 사항 (`/grill-me` 4대 의사결정 반영)

1. **[포털 진입 UX] 상단 통합 AI 커맨드 바 + 우측 슬라이드 드로어(Drawer)**
   - `00. TV Europe Sales Management Portal/index.html` 상단 검색창(`#searchInput`)을 **실시간 대시보드 검색 + AXIS Master Agent 프롬프트 지시 겸용 통합 AI 커맨드 바**(`Ctrl+K`, `Enter`, `AXIS AI 실행` 버튼)로 업그레이드하였습니다.
   - 프롬프트 실행 시 현재 보던 대시보드 화면을 잃지 않고 우측에서 **슬라이드 드로어(`#axisAgentDrawer`)**가 열리며, 필요 시 **`3단 전체화면`** 버튼으로 `99. Master Agent` 전체 워크스페이스로 즉시 확장(`?q=` 자동 전달)됩니다.

2. **[엔진 연결 아키텍처] Antigravity Sidecar (`agentapi`) + 실시간 `transcript.jsonl` 미러링 + 자율 코프로세서**
   - `~/.gemini/config/sidecars/axis-portal-bridge/sidecar.json` 및 `start_sidecar_bridge.js`를 구성하여 Antigravity IDE 기동 시 브릿지 서버(`Port 5050`)와 워커(`watch_bridge.js`)가 자동 구동됩니다.
   - 포털에서 입력한 프롬프트는 `buildAxisMasterPrompt()`를 통해 15대 전문 서브에이전트·글로벌 스킬·무인 아카이빙 프로토콜이 주입되어 `agentapi` 및 자율 코프로세서(Parquet Live Query + 15-Agent Ground Truth + Gemini AI)로 실행됩니다.
   - `~/.gemini/antigravity/brain/<conversation-id>/.system_generated/logs/transcript.jsonl`을 실시간 파싱하여 에이전트의 내부 추론(`thinking`), 도구 호출(`tool_calls`), 응답(`PLANNER_RESPONSE`)을 포털 드로어에서 그대로 미러링합니다.

3. **[산출물 전달 및 자율 실행 범위] 전 과정 100% 완전 무인 실행**
   - 데이터 조회(Parquet/DuckDB/Excel)부터 분석 리포트(`.html`), 정밀 추출 데이터(`.csv`), 그리고 `99. Master Agent/Task/YYYYMMDD_작업제목/` 폴더 자동 생성 및 `Task/README.md` 레지스트리 갱신까지 중간 확인 없이 100% 무인으로 완결됩니다.
   - 완료 즉시 포털 우측 드로어 하단 및 `Task/ 산출물 폴더` 탭에 다운로드/열기 카드가 자동 렌더링됩니다.

## 2. 구현 및 배포 파일 일람
- `C:\Users\harry.park\.gemini\config\sidecars\axis-portal-bridge\sidecar.json`
- `d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\start_sidecar_bridge.js`
- `d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\START_AXIS_PORTAL_BRIDGE.bat`
- `d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\scripts\antigravity_sidecar_engine.js`
- `d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\watch_bridge.js`
- `d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\server.js`
- `d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\public\axis_portal_bridge.css`
- `d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\public\axis_portal_bridge.js`
- `d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\00. TV Europe Sales Management Portal\index.html` (동기화 완료)
