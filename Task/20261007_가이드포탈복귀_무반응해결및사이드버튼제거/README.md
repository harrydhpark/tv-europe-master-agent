# [Task] 20261007_가이드포탈복귀_무반응해결및사이드버튼제거

## 1. 과제 개요 (Task Overview)
- **과제명**: AXIS 시스템 소개 가이드 내 사이드바 중복 복귀 버튼(`세일즈 포탈로 이동`) 삭제 및 좌측 상단 [포탈로 돌아가기] 무반응 결함 원인 규명/수정
- **실행 일자**: 2026년 10월 07일
- **수행 주체**: Master AI Agent (`99. Master Agent`), TV Europe Sales Management Portal
- **관련 파일**:
  - `00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html`

---

## 2. 결함 원인 분석 및 해결 방안

### 1) 좌측 상단 [포탈로 돌아가기] 무반응 결함 원인 (Root Cause)
- **증상**: 상단 고정 탑바 좌측의 [← 포탈로 돌아가기] 버튼을 클릭해도 아무런 동작이 일어나지 않고 현재 페이지에 그대로 머무름.
- **원인**:
  - 기존 `returnToPortal(e)` 함수 내에서 새 탭(`target="_blank" rel="opener"`)으로 열린 경우 `window.opener.focus()` 및 `window.close()`를 실행한 뒤 곧바로 `return;`으로 함수를 종료하도록 작성되어 있었습니다.
  - 최신 크롬/엣지(Chromium) 브라우저는 보안 정책상 일반 하이퍼링크로 열린 탭에 대해 **`window.close()` 호출을 조용히 무시(Silent Block)**하며 에러(`throw`)도 발생시키지 않습니다. 또한 백그라운드 탭으로의 포커스 전환(`window.opener.focus()`) 역시 사용자 인터랙션 보호 정책으로 차단됩니다.
  - 그 결과 탭이 닫히지도 않고, 부모 창으로 포커스가 넘어가지도 않은 상태에서 `return;`으로 함수가 끝나버려 **사용자 화면에서는 클릭해도 아무런 반응이 없는 것처럼 보이는 결함**이 발생했습니다.
- **해결 조치**:
  - `window.opener.focus()`와 `window.close()`를 시도하되 조용히 차단되는 경우를 대비하여 `return;` 조기 종료를 제거.
  - 브라우저가 창 닫기를 차단하더라도 곧바로 `window.location.href = portalUrl;` (`https://tv-sales-portal-2026.web.app/index.html`)로 현재 창을 세일즈 포탈 홈으로 즉시 전환하도록 **Fallback Direct Navigation** 메커니즘을 적용했습니다.

### 2) 첨부 이미지 요소 삭제
- **사용자 요청**: `media_1791337745100.png`에 첨부된 좌측 사이드메뉴 하단의 `[← 세일즈 포탈로 이동 PORTAL]` 중복 버튼 삭제.
- **해결 조치**:
  - `AXIS_System_Architecture_Guide.html` 사이드바 내의 `<div class="pt-5 px-3">...</div>` 요소를 완전히 삭제하여 상단 글로벌 탑바의 `[← 포탈로 돌아가기]` 단일 표준 버튼으로 일원화하였습니다.

---

## 3. 실서버 라이브 배포 정보
- **배포 플랫폼**: Firebase Hosting
- **배포 URL**: `https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html`
- **배포 상태**: 성공 (Deploy complete)
