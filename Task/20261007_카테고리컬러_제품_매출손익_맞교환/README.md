# [Task] 20261007_카테고리컬러_제품_매출손익_맞교환

## 1. 과제 개요 (Task Overview)
- **과제명**: TV 유럽영업 포털 '제품 정보'와 '매출/손익 관리' 카테고리 테마 컬러 상호 맞교환 (제품 정보: LG Red, 매출/손익 관리: Emerald Teal)
- **실행 일자**: 2026년 10월 07일
- **수행 주체**: Master AI Agent (`99. Master Agent`), TV Europe Sales Management Portal
- **관련 파일**:
  - `00. TV Europe Sales Management Portal/styles.css`
  - `00. TV Europe Sales Management Portal/index.html`

---

## 2. 변경 상세 내역 (Color Swap Matrix)

사용자 요청에 따라 두 핵심 카테고리의 시각적 테마 컬러를 상호 맞교환하였습니다.

| 카테고리 | 키 (`categoryKey`) | 테마 컬러 | 상단 액센트 라인 | 태그 배지 (`category-tag`) | 액션 버튼 (`open-dashboard-btn`) | 상단 필터 칩 / 사이드바 아이콘 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **제품 정보** | `product` | **LG Red (`#C40046`)** | 3.5px solid `#C40046` | 연한 로즈 배경 (`#FFF1F2`) + `#C40046` | `#C40046` (Hover: `#A50034`) | `#C40046` (LG Red) |
| **매출/손익 관리** | `sales` | **에메랄드 틸 (`#0D9488`)** | 3.5px solid `#0D9488` | 연한 틸 배경 (`#E6F7F5`) + `#0D9488` | `#0D9488` (Hover: `#0F766E`) | `#0D9488` (Teal) |
| **가격 관리** | `pricing` | **앰버 골드 (`#D97706`)** | 3.5px solid `#D97706` | 연한 앰버 (`#FEF3C7`) + `#B45309` | `#D97706` (Hover: `#B45309`) | `#D97706` (Amber) |
| **시장 정보** | `market` | **스카이 블루 (`#0284C7`)** | 3.5px solid `#0284C7` | 연한 스카이 (`#E0F2FE`) + `#0284C7` | `#0284C7` (Hover: `#0369A1`) | `#0284C7` (Sky Blue) |

---

## 3. 세부 반영 구성 요소
1. **Bento Card 상단 3.5px 액센트 라인 & Hover 글로우 섀도우**:
   - `cat-product`: 3.5px solid `#C40046` (LG Red)
   - `cat-sales`: 3.5px solid `#0D9488` (Emerald Teal)
2. **카테고리 태그 배지 (`.category-tag`)**:
   - `.product`: `#FFF1F2` 배경 + `#C40046` 텍스트
   - `.sales`: `#E6F7F5` 배경 + `#0D9488` 텍스트
3. **카드 타이틀 아이콘 (`.card-icon`)**:
   - 제품 정보: `#C40046`
   - 매출/손익 관리: `#0D9488`
4. **대시보드 열기 액션 버튼 (`.open-dashboard-btn.linked`)**:
   - 제품 정보: `#C40046` (Hover: `#A50034`)
   - 매출/손익 관리: `#0D9488` (Hover: `#0F766E`)
5. **상단 필터 칩 (`.chip-btn[data-category="..."]`)**:
   - 제품 정보 Active/Hover: `#C40046`
   - 매출/손익 관리 Active/Hover: `#0D9488`
6. **좌측 사이드바 카테고리 아코디언 (`#accordion-...`)**:
   - `#accordion-product`: 아이콘 `#C40046`, 카운트 배지 `#FFA2B2`
   - `#accordion-sales`: 아이콘 `#0D9488`, 카운트 배지 `#2DD4BF`

---

## 4. 라이브 배포 정보
- **배포 플랫폼**: Firebase Hosting
- **배포 URL**: `https://tv-sales-portal-2026.web.app`
- **캐시버스터 버전**: `v=20261007_colors_swap`
