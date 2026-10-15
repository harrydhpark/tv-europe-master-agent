# [Task] 20261007_가이드포탈복귀_세션유지개선

## 1. 과제 개요 (Task Overview)
- **과제명**: AXIS 시스템 소개 보고서에서 [포탈로 돌아가기] 클릭 시 로그인 화면 노출 결함 원인 규명 및 세션 영속화 개선
- **실행 일자**: 2026년 10월 07일
- **수행 주체**: Master AI Agent (`99. Master Agent`), TV Europe Sales Management Portal
- **관련 파일**:
  - `00. TV Europe Sales Management Portal/app.js`
  - `00. TV Europe Sales Management Portal/index.html`
  - `00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html`

---

## 2. 결함 원인 심층 분석 (Root Cause Analysis)

1. **`sessionStorage`의 탭(Tab) 격리 한계**:
   - 포털의 기존 인증 로직(`app.js`)은 로그인 성공 시 `sessionStorage`에만 사용자 ID와 활동 타임스탬프를 보관함.
   - `sessionStorage`는 단일 브라우저 탭 컨텍스트 내에서만 유효하며, 같은 도메인(`tv-sales-portal-2026.web.app`)이더라도 새 탭/새 창/외부 링크 유입 탭에는 세션 데이터가 공유되지 않음.
2. **`target="_blank"` 및 브라우저 프로세스 격리**:
   - 포털 사이드바에서 "AXIS 시스템 소개" 클릭 시 `target="_blank"` 속성에 의해 새 탭으로 가이드가 열림.
   - 최신 모던 브라우저(Chrome, Edge 등)는 `target="_blank"`에 기본적으로 `rel="noopener"`를 적용하여 새 탭의 프로세스를 격리하므로, `window.opener`가 `null`이 됨.
3. **복귀 Fallback 실행 시 무인증 상태 인식**:
   - 가이드의 [포탈로 돌아가기] 함수(`returnToPortal`)는 `window.opener` 닫기 또는 `history.back()` 실패 시 `window.location.href = portalUrl`로 포털 메인으로 직접 이동함.
   - 이때 해당 탭의 `sessionStorage`에는 로그인 정보가 없으므로 `index.html` 로드 즉시 `checkAuthStatus()`가 무인증으로 판단하여 `loginOverlay`(로그인 화면)를 노출함.

---

## 3. 해결 조치 사항 (Implementation Details)

1. **`localStorage` 기반 다중 탭 세션 동기화 (Dual-Sync)**:
   - `app.js` 내 인증 검증 및 갱신 로직을 `localStorage` 우선 및 `sessionStorage` 동시 저장 방식으로 전환.
   - 30분 비활동 자동 로그아웃(`AUTH_CONFIG.TIMEOUT_MS: 30분`) 타이머는 동일하게 엄격 유지하여 보안성 100% 보존.
   - 이제 사용자가 포털에서 로그인하면 동일 브라우저의 모든 탭(가이드, 대시보드 뷰어 등)에서 로그인 세션이 공유되어 복귀 시 로그인 화면 없이 메인 화면이 즉시 로드됨.
2. **`rel="opener"` 링크 속성 보강**:
   - `index.html` 내 가이드 링크에 `rel="opener"`를 명시하여 포털에서 가이드로 새 탭을 열었을 때 `window.opener` 참조를 보존.
   - [포탈로 돌아가기] 클릭 시 기존 포털 탭으로 매끄럽게 포커스가 이동하고 새 탭이 자동 닫히도록 최적화.
3. **스크립트 캐시버스터 갱신**:
   - `index.html` 내 `app.js?v=20261007_auth`로 캐시를 무력화하여 최신 인증 패치가 즉시 반영되도록 조치.
4. **Firebase Hosting 실서버 배포 완료**:
   - `https://tv-sales-portal-2026.web.app`
   - `https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html`
