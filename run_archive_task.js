const path = require('path');
const fs = require('fs');
const { archiveTask } = require('./scripts/archive_task.js');

const query = "AXIS 시스템 & TV Europe Sales Management Portal 종합 소개 보고서에서 '4. DB 구조 & 파이프라인' 내용을 주간 엑셀 원천 데이터의 중앙 DuckDB 자동 동기화 아키텍처 구현 내용과 작업 결과를 토대로 일반인도 이해하기 쉽게 다이어그램과 텍스트로 다시 구성";

const summary = `
- AXIS 시스템 아키텍처 가이드 4장(DB 구조 & 파이프라인)의 기술적 내용을 일반인/경영진 눈높이에 맞춘 4단계 라이프사이클 인포그래픽 및 직관적 비유(업무 장부, 24시간 감시 센서, 중앙 디지털 금고, 실시간 브로드캐스트)로 전면 개편
- 4단계 자동 파이프라인: 1) 엑셀 저장 감지(3초 디바운스 파일락 방지), 2) DuckDB 중앙 코어 정산(주차별 멱등성 Upsert로 과거 보존), 3) 초경량 웹 마스터 번들(1.1MB, 0.1초 로딩), 4) 실시간 알림(SSE) 및 1-Click Firebase 배포
- 전/후 비교(Before vs After) 카드 및 하단 엔지니어링 무결성 원칙(Pandas Overlay, SaveCopyAs, Star Schema) 체계화
- 실제 웹 배포 사이트(https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html#tab-db) 즉각 반영 완료
`.trim();

const answerMarkdown = `
# AXIS 시스템 가이드 '4. DB 구조 & 자동 동기화 파이프라인' 개편 보고서

## 1. 개요 및 목적
- **목적**: 기존의 복잡한 엑셀 COM 규칙과 데이터베이스 전문 용어로 서술되어 있던 '4. DB 구조 & 파이프라인' 섹션을, 일반 영업 담당자 및 경영진도 한눈에 시스템의 작동 원리와 혁신성을 이해할 수 있도록 재구성
- **반영 사이트**: [AXIS 시스템 & TV Europe Sales Management Portal 종합 소개 보고서](https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html#tab-db)

---

## 2. 주요 개편 내용

### ① 누구나 이해하는 직관적 일상 비유 (Easy Metaphor)
- 📁 **원천 엑셀 파일들 = 주간 업무 장부**: 영업 실적, P&L, 시장점유율, 가격 등 각 팀 서랍에 저장되던 주간 엑셀
- 👁️ **File Watcher 엔진 = 24시간 감시 센서**: 새 엑셀이 저장되는 순간 3초 만에 안전하게 감지하여 작업 큐에 등록
- 🏦 **중앙 DuckDB 코어 = 초고속 디지털 금고**: 수백만 건의 데이터를 1초 만에 과거 데이터 손실 없이 완벽히 정산·보관
- 📢 **웹 번들 & SSE = 실시간 브로드캐스트**: 정산 완료 즉시 화면에 팝업이 뜨고 버튼 하나로 전사 클라우드 즉시 배포

### ② 4단계 자동 파이프라인 비주얼 인포그래픽
1. **STEP 1. [감지] 엑셀 파일 저장 감지**: 담당자가 폴더에 저장 시 3초 안정화 디바운스 대기 후 파일 락 해제 시점 안전 감지
2. **STEP 2. [정산] DuckDB 중앙 코어 정산**: 주차별 안전 멱등성(Upsert)으로 W1~W38 데이터 손실 없이 W39 주차 데이터만 안전 교체
3. **STEP 3. [압축] 웹 최적화 마스터 번들**: 수십만 행의 데이터를 1.1MB 경량 JSON으로 압축하여 0.1초 만에 로딩
4. **STEP 4. [전파] 실시간 알림 & 1-Click 배포**: 서버-화면 실시간 스트림(SSE) 토스트 알림 및 원클릭 클라우드 배포

### ③ 혁신적 전/후 비교 (Before vs After)
| 구분 | 기존 수동 취합 방식 (Before) | AXIS 중앙 자동 동기화 (After) |
| :--- | :--- | :--- |
| **작업 방식** | 담당자가 엑셀을 열고 복사/수식 재연결 (30분~1시간) | 폴더에 엑셀 저장 즉시 **100% 전자동 무인 처리** |
| **안정성** | 20~50MB 엑셀 로딩 시 프로그램 정체(Hang) 및 충돌 | 3초 안정화 디바운스 및 초고속 컬럼 엔진으로 무정체 처리 |
| **데이터 무결성** | 수작업 복사 실수 및 과거 주차 덮어쓰기 위험 | **주차별 멱등성 업서트**로 과거 데이터 100% 영구 보존 |
| **보고 및 배포** | 엑셀 파일 전달 지연, 모바일/웹 열람 불가 | **0.1초 웹 로딩**, 실시간 토스트 알림 및 원클릭 클라우드 배포 |

### ④ 엔지니어링 무결성 원칙 (기술 상세 보존)
1. **Pandas Overlay 벌크 주입**: 셀 단위 루프 금지, 메모리 블록 단위 주입
2. **SaveCopyAs 원자적 대체**: Calculation = Manual 상태에서 임시 파일 복제 저장 및 원자적 교체
3. **Star Schema 10대 핵심 테이블**: 5대 Fact + 3대 Dim 정규화 구조 유지
`.trim();

const sourceGuide = 'd:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html';

const res = archiveTask({
  dateStr: '20261003',
  shortTitle: '아키텍처가이드DB개편',
  query: query,
  summary: summary,
  answerMarkdown: answerMarkdown,
  dispatchedAgents: ['Master Agent', '00. TV Europe Sales Management Portal'],
  artifacts: [sourceGuide]
});

console.log('Archive completed:', res);
