# [Task] 20261006_가이드UI_시나리오라벨개선

## 1. 질의 개요 (User Request)
- **실행 일시**: 2026-10-06
- **사용자 질의 원문**:
  1. "[AXIS 시스템 & TV Europe Sales Management Portal 종합 소개 보고서](https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html#tab-scenarios) 에서 첨부 이미지 화면의 내용중 (새창 열기), 실행완료 5초 표현은 삭제해줘"
  2. "'6. 실무 활용 방안 & 시나리오' 은 '6. 실무 활용 예시' 로 바꿔줘"
  3. "왼쪽 사이드 메뉴 중 '7. FAG, 도입효과 및 로드맵'은 삭제해줘"
  4. "'주간 권역/법인별 출하 진척률 및 유통 재고 주수(WOS) 점검' 을 '주간 지점/법인별 실판매 진척률 및 유통 재고(WOS) 점검'으로 변경해줘"
  5. "두번째 첨부 이미지는 '주간 실판매 점검' 으로 바꿔줘"
  6. "세번째 이미지의 상황 설명은 모든 예시에서 삭제해줘"
  7. "네번째 이미지는 삭제해줘"

- **연계 에이전트 (Dispatched Agents)**:
  - `Master AI Agent`
  - `TV Europe Sales Management Portal`

## 2. 생성 산출물 (Artifacts)
- 📄 **[AXIS_System_Architecture_Guide.html](./AXIS_System_Architecture_Guide.html)**: UI 텍스트 정제, 시나리오 명칭/태그 변경, 상황 설명 전수 삭제, 버튼 안내 삭제 반영 메인 가이드
- 📄 **[scenario_01_result_viewer.html](./scenario_01_result_viewer.html)**: 상단 헤더 및 브레드크럼(주간 지점/법인별 실판매 진척률 및 유통 재고(WOS) 점검) 동기화 전용 뷰어

---

## 3. 핵심 수정 사항 (Executive Summary)
1. **시나리오 01 메인 제목 변경**:
   - 기존: `주간 권역/법인별 출하 진척률 및 유통 재고 주수(WOS) 점검`
   - 변경: **`주간 지점/법인별 실판매 진척률 및 유통 재고(WOS) 점검`**
2. **시나리오 01 우측 상단 뱃지 태그 변경**:
   - 기존: `매주 월/화 주간회의`
   - 변경: **`주간 실판매 점검`**
3. **'상황 설명' 전수 삭제 (시나리오 1~4 전체)**:
   - 각 시나리오 카드 상단에 노출되던 `<p><strong>상황:</strong> ...</p>` 설명 단락 4개를 전수 삭제하여 카드가 한눈에 들어오도록 컴팩트화.
4. **네 번째 이미지(결과 버튼 옆 안내 텍스트) 삭제**:
   - `[마스터 에이전트 실전 답변 및 엑셀 결과 보기]` 버튼 우측의 `독립 전용 창에서 무편집 원문 답변 및 16개국 엑셀 매트릭스를 쾌적하게 확인·복귀` 안내 문구를 완전히 삭제하여 버튼만 깔끔하게 단독 배치.
5. **이전 요청 사항 완벽 유지**:
   - `(새 창 열기 ↗)` 및 `[실행 완료 5초]` 삭제 완료.
   - `6. 실무 활용 예시` 명칭 반영 완료.
   - 좌측 사이드바 `7. FAQ, 도입효과 & 로드맵` 제거 완료.
6. **Firebase Hosting 실서버 배포 완료**:
   - 배포 URL: [AXIS 시스템 종합 소개 가이드 (6. 실무 활용 예시 탭)](https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html#tab-scenarios)
   - HTTP 200 OK 라이브 검증 완료.
