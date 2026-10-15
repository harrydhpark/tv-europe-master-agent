# 📑 AXIS 시스템 종합 가이드 챕터 번호 및 '3. 실무 활용 예시' 순서 재배치

## 1. 과제 개요
- **요청 일자**: 2026-10-07
- **요청자**: LGE Europe TV 해외영업 총괄 담당자
- **수행 에이전트**: Master AI Agent, Europe Sales Management Portal Orchestrator
- **배포 URL**: [AXIS 시스템 & TV Europe Sales Management Portal 종합 소개 보고서 | LGE Europe TV](https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html)

---

## 2. 사용자 요청 원문
> "'6. 실무 활용 예시'를 '3. 실무 활용 예시'로 변경해주고 나머지 항목의 번호는 하나씩 올려서 순서를 바꿔줘"

---

## 3. 핵심 변경 상세 및 아키텍처 개편

### 3.1 챕터 번호 및 순서 재배치 (Before vs After)

| 번호 | Before (기존 순서) | After (개편 순서) | 섹션 앵커 ID | 주요 내용 |
| :---: | :--- | :--- | :---: | :--- |
| **1** | 1. AXIS 소개 | **1. AXIS(Agentic eXecution & Integrated Sales System) 소개** | `#tab-overview` | 마스터 오케스트레이션 정의, 3계층 아키텍처 |
| **2** | 2. MASTER AI AGENT 구조 | **2. MASTER AI AGENT 구조** | `#tab-master` | 15대 전문 대시보드 및 도메인 에이전트 계통도 |
| **3** | 3. 세일즈 포탈 구성 | **3. 실무 활용 예시** *(기존 6번 전진 배치)* | `#tab-scenarios` | 4대 비즈니스 실무 활용 시나리오 (Before vs After, Prompt Chip) |
| **4** | 4. DB 구조 & 파이프라인 | **4. 세일즈 포탈 구성** *(기존 3번 +1 이동)* | `#tab-portal` | 15대 전문 AI 대시보드 카드, 데이터 파이프라인 |
| **5** | 5. 보안 구성 & 거버넌스 | **5. DB 구조 & 자동 동기화 파이프라인** *(기존 4번 +1)* | `#tab-db` | 시계열 Parquet DB, 원천 엑셀 Watcher |
| **6** | 6. 실무 활용 예시 | **6. 보안 구성 & 무마찰 거버넌스** *(기존 5번 +1)* | `#tab-security` | SHA-256 Auth Guard, No-Store, WAF 우회 |
| **7** | 7. FAQ & 로드맵 | **7. FAQ, 도입효과 & 로드맵** | `#tab-roadmap` | 정량/정성 ROI, 2026-2027 시스템 비전 |

### 3.2 구현 무결성 검증 (Zero Defect Engineering)
1. **사이드바 메뉴 및 탭 버튼 동기화**:
   - 좌측 메뉴바의 버튼 순서 및 라벨 번호를 1~6번까지 완벽 재배열.
   - `showTab(tabId, el)` 스크립트가 버튼 내 텍스트(`span`)를 동적으로 추출하여 상단 브레드크럼 타이틀(`breadcrumb-title`)에 즉시 반영하므로, 탭 전환 시 상단 경로명도 100% 자동 동기화.
2. **DOM 물리적 순서 정합 (Accessibility & Print Optimization)**:
   - 화면 탭 전환뿐 아니라 `@media print`(문서 인쇄/PDF 저장) 및 웹 접근성 시맨틱 구조를 보존하기 위해 HTML DOM 상의 `<section id="tab-scenarios">`를 `tab-master` 직후이자 `tab-portal` 직전 위치로 물리적 재배치 완료.
3. **URL 해시 라우팅 및 앵커 불변성 보존**:
   - 시나리오 뷰어(`scenario_01_result_viewer.html` ~ `scenario_04_result_viewer.html`) 등 외부 문서에서 참조하는 `#tab-scenarios`, `#tab-portal` 등 앵커 해시 ID를 100% 보존하여 모든 내·외부 링크 무결성 유지.

---

## 4. 라이브 배포 및 검증
- **호스팅 환경**: Google Firebase Hosting (`sales-portal`)
- **실서버 URL**: `https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html`
- **배포 상태**: 성공 (HTTP 200 OK, 캐시 우회 무중단 배포 완료)
