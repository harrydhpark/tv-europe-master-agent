const fs = require('fs');
const path = require('path');
const { archiveTask } = require('./archive_task');

const dateStr = '20261003';
const shortTitle = '시나리오01_결과및엑셀뷰어';
const query = '/grill-me 첨부에서 처럼 \'6. 실무 활용 방안 & 시나리오\' 에서 실제 질문을 한 결과가 위에 나와 있어. 이를 \'답변 결과\' 로 표현해서 클릭하면 위의 에이전트가 실행한 결과를 보여주고 파일 결과문인 엑셀파일의 내용도 보여줘. 이를 통해 실제 에이전트가 수행한 결과가 어떻게 수행됐는지 검색자가 알수 있도록 가시성있게 보여줘';
const summary = 'AXIS 아키텍처 가이드 6장 시나리오 01(주간 WOS 점검) 실전 질의 프롬프트 하단에 [마스터 에이전트 실전 답변 및 엑셀 결과 보기] 인라인 확장 아코디언 드로어 구축: 2단 탭(AI 분석 보고서 / 16개국 엑셀 매트릭스 시트 뷰어) 분리, [전체/과다재고/정상] 인터랙티브 필터 칩, Base64 인라인 내장형 원클릭 실제 .xlsx 엑셀 다운로드 엔진 구현 및 Firebase Hosting(tv-sales-portal-2026.web.app) 라이브 배포 완료';

const answerMarkdown = `
# AXIS 시스템 가이드 '시나리오 01 마스터 에이전트 실전 답변 & 엑셀 뷰어' 구축 보고서

## 1. 개요 및 목적
- **목적**: '6. 실무 활용 방안 & 시나리오'의 시나리오 01(주간 권역/법인별 출하 진척률 및 유통 재고 주수 점검)에서 마스터 에이전트에게 실제 질의한 분석 결과와 산출 엑셀 파일의 내용을 보고서 내에서 즉시 확인하고 다운로드할 수 있도록 대화형 인터랙티브 뷰어 컴포넌트를 구축
- **배포 URL**: [AXIS 시스템 & TV Europe Sales Management Portal 소개 가이드 (시나리오 탭)](https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html#tab-scenarios)

---

## 2. 주요 구현 사항

### ① 인라인 확장 아코디언 드로어 (Inline Expandable Drawer)
- 프롬프트 복사 칩 바로 아래에 **\`[✨ 마스터 에이전트 실전 답변 및 엑셀 결과 보기 (Live Execution Output) | 실행 완료 5초]\`** 토글 버튼 배치
- 클릭 시 부드러운 전환 효과와 함께 시나리오 카드 내부에서 리치 결과 컨테이너가 확장

### ② 2단 탭 네비게이션 & 다운로드 툴바
- **상단 다크 네이비 헤더 바**:
  - \`[💬 AI 분석 보고서 (총평 & 리스크 진단)]\` 탭
  - \`[📊 엑셀 데이터 시트 뷰어 (16개 법인 매트릭스)]\` 탭
  - 우측: **\`[📥 엑셀 원본 다운로드 (.xlsx)]\`** 원클릭 다운로드 버튼

### ③ 탭 1: AI 분석 보고서 (Executive Diagnostic Report)
- **에이전트 브리핑 헤더**: 소요 시간(4.8초), 참조 DB(06. KPI Sheet 9/21W 주차 실적 기반), 질의 일시, Task 아카이브 태그 명시
- **4대 핵심 KPI 카드 그리드**:
  - 유럽 본부(EU TTL) 평균 WOS: **7.31주**
  - 과다재고 리스크 (>6주): **13개 법인**
  - 재고부족 리스크 (<3주): **0개 법인**
  - 정상 범위 (3~6주): **3개 법인** (오스트리아, 포르투갈, 베네룩스)
- **3대 리스크 클러스터 심층 진단 카드**:
  - 🚨 **유형 A: 신모델 과잉 선적형 (루마니아 24.7주, 폴란드 18.5주, 프랑스 15.1주)**
  - 💎 **유형 B: 프리미엄 OLED 주도형 (독일 29.4%, 스위스 18.9%, 베네룩스 24.7%)**
  - ⚠️ **유형 C: 구모델 정체 + 저가형 편중형 (스페인 7.7주/구모델 7.6주, 이탈리아 36.3%)**
- **OLED 신모델 3대 지표 정의 가이드**: 세대교체율, 프리미엄 믹스율, 볼륨 기여율 명확화

### ④ 탭 2: 인터랙티브 엑셀 데이터 시트 뷰어 & 원클릭 다운로드
- **원클릭 필터 칩**: \`[전체 (17)]\`, \`[과다재고 리스크 (13)]\`, \`[정상 (3)]\` 즉시 필터링
- **스타일링된 엑셀 매트릭스 표**:
  - 네이비 헤더(#1B365D), 지브라 행(#F9FAFB), 리스크 적색/정상 녹색 뱃지
  - 16개국 법인 + 본부(TTL) 전수 14개 핵심 컬럼 수록
  - 숫자 포맷팅(천단위 콤마, % 소수점 1자리, 주수 표시)
- **Base64 인라인 엑셀 다운로드 엔진**:
  - 외부 파일 경로 의존성 없이 브라우저 메모리상에서 순수 Base64 디코딩 후 실제 생성된 \`유럽_법인별_유통재고WOS_OLED신모델비중_요약.xlsx\` 파일을 즉시 다운로드

### ⑤ Firebase Hosting 실서버 배포 완료
- 사이트: \`https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html\`
- HTTP 상태: **200 OK** 검증 완료
`;

const srcHtml = path.resolve('d:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html');
const srcXlsx = path.resolve('d:/TV 유럽영업/15. AX Task/2026 AX 실행과제/99. Master Agent/유럽_법인별_유통재고WOS_OLED신모델비중_요약.xlsx');

const res = archiveTask({
  dateStr,
  shortTitle,
  query,
  answerMarkdown,
  summary,
  dispatchedAgents: ['Master AI Agent', 'TV Europe Sales Management Portal', 'KPI Sheet Orchestrator'],
  artifactPaths: [srcHtml, srcXlsx]
});

console.log('Archive completed:', res);
