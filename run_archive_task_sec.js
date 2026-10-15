const path = require('path');
const fs = require('fs');
const { archiveTask } = require('./scripts/archive_task.js');

const query = "AXIS 시스템 & TV Europe Sales Management Portal 종합 소개 보고서에서 '5. 보안 구성 & 거버넌스' 내용을 '4. DB 구조 & 파이프라인'과 동일한 방식으로 일반인도 이해하기 쉬운 비유와 다이어그램, 전후비교로 다시 구성";

const summary = `
- AXIS 시스템 아키텍처 가이드 5장(보안 구성 & 거버넌스)을 일반인/경영진 눈높이에 맞춘 '스마트 사옥 출입 시스템' 비유(통합 출입증, 일방통행 지문 금고, 스마트 이석 센서, 철통 보안 셔터)로 전면 개편
- 4단계 스마트 보안 라이프사이클: 1) SHA-256 일방통행 암호화(원문 보관 위험 0%), 2) 무마찰 SSO 티켓 생성, 3) 하이패스 & Clean URL(0.1초 만에 주소창 토큰 파기), 4) 30분 활동 감지 하트비트 & 자동 잠금
- 전/후 비교(Before vs After) 카드 및 하단 엔지니어링 표준(auth-guard.js 단 1줄 임베드 규격, Web Crypto API, sessionStorage, 클라우드 보안 헤더) 체계화
- 실제 웹 배포 사이트(https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html#tab-security) 즉각 반영 완료
`.trim();

const answerMarkdown = `
# AXIS 시스템 가이드 '5. 보안 구성 & 무마찰 거버넌스' 개편 보고서

## 1. 개요 및 목적
- **목적**: 전문 암호학 용어와 기술 스크립트 위주로 작성되어 있던 '5. 보안 구성 & 거버넌스' 섹션을, 일반 영업 담당자와 경영진도 "보안이 철통 같으면서도 사용하기는 왜 이렇게 편리한가(Zero-Friction)"를 직관적으로 이해할 수 있도록 일상 비유와 인포그래픽으로 재구성
- **반영 사이트**: [AXIS 시스템 & TV Europe Sales Management Portal 종합 소개 보고서](https://tv-sales-portal-2026.web.app/docs/AXIS_System_Architecture_Guide.html#tab-security)

---

## 2. 주요 개편 내용

### ① 스마트 사옥 출입 시스템 일상 비유 (Easy Metaphor)
- 💳 **스마트 통합 출입증 = 무마찰 SSO 프리패스**: 메인 로비에서 1회 인증으로 산하 15개 전문 연구실(대시보드)을 추가 암호 없이 자유롭게 통과
- 🔐 **일방통행 지문 금고 = SHA-256 단방향 해시**: 비밀번호 글자를 남기지 않고, 해커가 훔쳐가도 원문 복원이 불가능한 지문 형태로만 대조
- ⏱️ **스마트 이석 센서 = 30분 지능형 세션 가드**: 업무 중엔 끊김 없이 유지되되, 30분간 자리를 비우면 화면을 자동 잠가 비인가 노출 차단
- 🛡️ **철통 보안 셔터 = Full-screen Auth Guard**: 외부인이 URL 복사나 비인가 경로로 침입 시 0.1초 만에 셔터를 내리고 사내 인증 요구

### ② 4단계 스마트 보안 라이프사이클 인포그래픽
1. **STEP 1. [지문 검증] SHA-256 일방통행 암호화**: 비밀번호 입력 즉시 64자리 단방향 해시 지문으로 변환 대조 (원문 보관 위험 0%)
2. **STEP 2. [출입증 발급] 무마찰 SSO 티켓 생성**: 포털 인증 통과자에게 서브 대시보드 전용 HMAC auth_token 자동 발행
3. **STEP 3. [흔적 소멸] 하이패스 & Clean URL 정제**: 서브 대시보드 진입 0.1초 만에 주소창에서 토큰을 자동 삭제(history.replaceState)하여 URL 유출 차단
4. **STEP 4. [상시 보호] 30분 이석 감지 & 자동 잠금**: 마우스/키보드 움직임을 실시간 감지하여 이석 시 세션 파기 및 자동 화면 잠금

### ③ 혁신적 전/후 비교 (Before vs After)
| 구분 | 기존 방식 (개별 로그인 & 취약한 보안) | AXIS 엔터프라이즈 스마트 보안 거버넌스 |
| :--- | :--- | :--- |
| **로그인 경험** | 15개 대시보드 이동 시마다 ID/PW 재입력 반복 피로 | **원클릭 Seamless SSO**로 포털 1회 로그인 후 전사 프리패스 |
| **비밀번호 보관** | 코드나 브라우저에 비밀번호 평문(Plaintext) 노출 위험 | **SHA-256 일방통행 암호화**로 원문 노출 위험 0% |
| **URL 주소창** | 주소창에 인증 토큰이 남아 메신저 전달 시 권한 유출 | **0.1초 Clean URL 정제**로 주소창 흔적 즉각 소멸 |
| **이석 시 보안** | 로그인 상태 무한 유지로 타인에게 실적 화면 노출 | **지능형 30분 이석 감지 센서**로 자리 비움 시 자동 화면 잠금 |

### ④ 엔지니어링 & 거버넌스 표준 원칙 (기술 상세 보존)
1. **단 1줄 표준 임베드 규격**: \`<script src="auth-guard.js"></script>\` 단 한 줄로 전사 15개 대시보드 보안 100% 일괄 적용
2. **Web Crypto API 가속**: 브라우저 네이티브 하드웨어 가속 기반 SHA-256 연산
3. **sessionStorage 격리 & 클라우드 헤더**: 브라우저 종료 시 소멸되는 메모리 격리 및 Firebase X-Robots-Tag, CSP 전역 강제
`.trim();

const sourceGuide = 'd:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html';

const res = archiveTask({
  dateStr: '20261003',
  shortTitle: '아키텍처가이드보안개편',
  query: query,
  summary: summary,
  answerMarkdown: answerMarkdown,
  dispatchedAgents: ['Master Agent', '00. TV Europe Sales Management Portal'],
  artifacts: [sourceGuide]
});

console.log('Archive completed:', res);
