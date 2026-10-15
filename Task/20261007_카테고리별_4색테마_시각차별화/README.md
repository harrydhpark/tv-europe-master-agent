# [Task] 20261007_카테고리별_4색테마_시각차별화

## 1. 과제 개요 (Task Overview)
- **과제명**: TV 유럽영업 포털 4대 카테고리별 카드 테마 컬러(Full-Themed Card) 시각적 차별화 개편
- **실행 일자**: 2026년 10월 07일
- **수행 주체**: Master AI Agent (`99. Master Agent`), TV Europe Sales Management Portal
- **관련 파일**:
  - `00. TV Europe Sales Management Portal/styles.css`
  - `00. TV Europe Sales Management Portal/app.js`
  - `00. TV Europe Sales Management Portal/index.html`

---

## 2. 디자인 개편 상세 (4-Category Color System)

기존 단일 녹색(Teal)으로 일괄 적용되어 구분이 어려웠던 4대 카테고리 18개 대시보드 카드를 글로벌 BI 디자인 표준에 따라 **4대 독립 테마 컬러**로 완전 차별화하였습니다.

| 카테고리 | 키 (`categoryKey`) | 테마 컬러 | 상단 액센트 라인 | 태그 배지 (`category-tag`) | 액션 버튼 (`open-dashboard-btn`) | 상단 필터 칩 / 사이드바 아이콘 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **매출/손익 관리** | `sales` | **에메랄드 틸 (`#0D9488`)** | 3.5px solid `#0D9488` | 연한 틸 배경 (`#E6F7F5`) + `#0D9488` | `#0D9488` (Hover: `#0F766E`) | `#0D9488` (Teal) |
| **제품 정보** | `product` | **로열 인디고 (`#4F46E5`)** | 3.5px solid `#4F46E5` | 연한 인디고 (`#EEF2FF`) + `#4F46E5` | `#4F46E5` (Hover: `#4338CA`) | `#4F46E5` (Indigo) |
| **가격 관리** | `pricing` | **앰버 골드 (`#D97706`)** | 3.5px solid `#D97706` | 연한 앰버 (`#FEF3C7`) + `#B45309` | `#D97706` (Hover: `#B45309`) | `#D97706` (Amber) |
| **시장 정보** | `market` | **스카이 블루 (`#0284C7`)** | 3.5px solid `#0284C7` | 연한 스카이 (`#E0F2FE`) + `#0284C7` | `#0284C7` (Hover: `#0369A1`) | `#0284C7` (Sky Blue) |

---

## 3. 적용 UI 구성 요소
1. **Bento Card 상단 3.5px 컬러 액센트 라인** 및 **Hover 시 해당 컬러 섀도우 발광 효과**
2. **카테고리 태그 배지 (`.category-tag`)**: 카테고리별 파스텔 틴트 배경 및 고대비 텍스트
3. **카드 타이틀 아이콘 (`.card-title i.card-icon`)**: 카테고리별 전용 테마 색상 렌더링
4. **하단 액션 버튼 (`.open-dashboard-btn.linked`)**: 카테고리별 고유 색상 및 호버 시 섀도우 전환
5. **상단 필터 칩 (`.chip-btn[data-category="..."]`)**: 선택 시 카테고리 전용 컬러 활성화
6. **좌측 사이드바 카테고리 아코디언 아이콘 (`.cat-icon`) 및 수량 배지 (`.cat-count`)**: 카테고리별 전용 컬러 100% 동기화
7. **Firebase Hosting 실서버 배포 완료**:
   - `https://tv-sales-portal-2026.web.app`
