# [Task] 20261007_제품정보_PRM순서및2026명칭개선

## 1. 과제 개요 (Task Overview)
- **과제명**: TV 유럽영업 포털 제품 정보 카테고리 내 대시보드 배치 순서 재조정 및 연도(2026) 명칭 통일화
- **실행 일자**: 2026년 10월 07일
- **수행 주체**: Master AI Agent (`99. Master Agent`), TV Europe Sales Management Portal
- **관련 파일**:
  - `00. TV Europe Sales Management Portal/app.js`
  - `00. TV Europe Sales Management Portal/index.html`

---

## 2. 주요 변경 사항 (Changes Implemented)

1. **'2025년 거래선 PRM 상담자료' 대시보드 맨 뒤 배치**:
   - `DASHBOARDS` 배열 및 `index.html` 좌측 사이드바 아코디언 메뉴에서 `prm-consulting-2025` 카드를 제품 정보 카테고리의 맨 마지막(6번째)으로 이동.
2. **2026 연도 명칭 통일 적용**:
   - `tv-prm`: `TV PRM` ➡️ **`2026 TV PRM`**
   - `spec-sheet`: `Spec Sheet` ➡️ **`2026 Spec Sheet`**
   - `tv-profile`: `TV Product profile` ➡️ **`2026 TV Product profile`**
   - 포털 메인 카드, 좌측 사이드바 서브 내비게이션, 다국어 사전(`DASHBOARD_I18N`) 전수 일관 반영 완료.
3. **제품 정보 카테고리 최종 6대 대시보드 라인업 순서**:
   1. `2027 파트너 성장 전략 (PRM)`
   2. `2026 TV PRM`
   3. `2026 Spec Sheet`
   4. `2026 TV Product profile`
   5. `거래선 방한 상담 일정 캘린더`
   6. `2025년 거래선 PRM 상담자료`
4. **Firebase Hosting 실서버 배포 완료**:
   - `https://tv-sales-portal-2026.web.app`
