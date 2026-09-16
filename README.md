# TV Europe Sales Master AI Agent (tv-europe-master-agent)

**TV Europe Sales Management Portal 산하 17개 전문 서브 에이전트를 총괄 지휘하는 AI 오케스트레이터 및 안티그래비티 에이전틱 브릿지 시스템**

---

## 1. 개요 (Overview)

본 프로젝트는 TV Europe Sales Management Portal 산하의 각 전문 서브 에이전트(KPI Sheet, TV P&L, Price Tracker, 수익성 Simulator, GDMI Weekly Sellout, GfK Monthly, FX-Monitor 등)를 하나의 통합 인터페이스로 연결하여, 자연어 대화를 통해 복합적인 영업 분석, 시뮬레이션, 데이터 파이프라인 제어를 수행하는 올인원 전략 영업 참모 시스템입니다.

### 핵심 기능 (Key Features)
1. **Multi-Agent Orchestration**: 17개 전문 서브 에이전트 도구 매핑 및 자동 디스패치 (`agentRegistry.js`)
2. **Antigravity Agentic Bridge**: 웹 챗봇 질의를 실제 원천 데이터셋과 스크립트로 전달하여 분석 후 실시간 브리핑하는 파일 시스템 기반 비동기 브릿지 (`antigravity_worker.py`)
3. **Interactive Live Canvas**: 
   - 4대 핵심 메트릭 카드 및 정밀 데이터 매트릭스 표
   - Chart.js 4.4 기반 다각도 시각화
   - 실시간 환율/장려금 변동 민감도 슬라이더
   - [MD 복사], [인쇄/PDF], [CSV 다운로드], [전체화면 확대]
4. **Pipeline Safety Confirmation Modal**: 대용량 데이터 갱신 시 대상 스크립트 및 영향 범위를 사전 고지하고 사용자 명시적 승인 후 실행 (`FR-2.3`)
5. **LGE SHA-256 Auth Guard**: 사내 포털 표준 보안 인증 연동 (`LGE135` / `LGE246`)

---

## 2. 시스템 아키텍처 (Architecture)

```
[Web Browser UI (index.html / app.js)]
       │
       ▼ (HTTP POST /api/bridge/task)
[Express Server (server.js:5050)]
       │
       ▼ (Task JSON write)
[Bridge Filesystem: agent_bridge/inbox]
       │
       ▼ (Polling 0.5s)
[Antigravity Worker (antigravity_worker.py)]
       ├── Parsing 15+ European Subsidiaries P&L (HTML/JSON)
       ├── Cross-Domain Price Gap Scraping DB (MediaMarkt, Saturn, Amazon)
       ├── Executive Insights & Inventory WOS (KPI Sheet)
       └── Real-time FX & Rebate Simulation Engine
       │
       ▼ (Result JSON write)
[Bridge Filesystem: agent_bridge/outbox]
       │
       ▼ (Polling 0.4s & Response)
[Live Artifact Canvas & Chat Stream]
```

---

## 3. 설치 및 실행 가이드 (Getting Started)

### 3.1 의존성 설치
```powershell
npm install
```

### 3.2 서비스 구동
```powershell
# 1. 안티그래비티 자율 에이전트 워커 실행 (백그라운드)
python -u antigravity_worker.py

# 2. Express 웹 서버 실행 (Port 5050)
node server.js
```

- 웹 브라우저 접속: `http://localhost:5050`
- 인증 암호: `LGE135` 또는 `LGE246`

---

## 4. 디렉터리 구조 (Directory Structure)

```
99. Master Agent/
├── agent_bridge/             # 비동기 통신 브릿지 (inbox, progress, outbox)
├── public/                   # 웹 프론트엔드 정적 파일
│   ├── app.js                # 클라이언트 애플리케이션 로직 및 UI 제어
│   ├── auth-guard.js         # LGE SHA-256 인증 가드
│   ├── index.html            # 3단 스플릿 메인 UI
│   ├── master_data_bundle.json # 사전 빌드 정규화 데이터 번들
│   └── styles.css            # Stitch Strategic Insight 디자인 시스템 스타일
├── agentRegistry.js          # 17개 서브 에이전트 메타데이터 및 도구 명세
├── antigravity_worker.py     # 원천 DB 직접 파싱 및 브릿지 태스크 프로세서
├── build_bundle.js           # 정적 호스팅용 종합 데이터 번들 빌더
├── firebase.json             # Firebase Hosting 배포 설정
├── localRuleEngine.js        # 오프라인 로컬 규칙 및 시나리오 처리 엔진
├── package.json              # 프로젝트 메타데이터 및 스크립트 정의
├── PRD_Master_Agent.md       # 마스터 에이전트 요구사항 정의서 (PRD)
├── realDataEngine.js         # 실시간 형제 데이터 디렉터리 인덱서
└── server.js                 # Express API 백엔드 서버 (Port 5050)
```

---

## 5. 라이선스 및 개발팀
- 개발: TV Europe Sales AX Task Team (2026 AX 실행과제)
- 라이선스: ISC
