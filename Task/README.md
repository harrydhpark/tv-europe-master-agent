# 🗂️ Master Agent Task Execution Registry

이 디렉토리는 **TV Europe Sales Master AI Agent**를 통해 질의받고 수행된 모든 전략 분석 과제와 결과물을 날짜별(`YYYYMMDD_질문내용`)로 영구 보관하는 아카이브 저장소입니다.

---

## 📌 실행 과제 아카이브 목록 (Task Registry)

| 실행 일자 | Task 폴더 | 핵심 질문 요약 | 연계 에이전트 | 산출물 |
| :---: | :--- | :--- | :--- | :---: |
| **2026-10-16** | [20261016_9월_스위스_수익성_분석](./20261016_9월_스위스_수익성_분석) | 9월 스위스 수익성 분석 보고서 만들어줘 | Master AI Agent, P&L Analysis, KPI Sheet, MS Trend, FX-Monitor | 📄 보고서 |
| **2026-10-16** | [20261016_AXIS작업지시Pilot이관](./20261016_AXIS작업지시Pilot이관) | /grill-me 기존의 프롬프트 창을 세일즈 포탈 대 | Master Agent, Global Sales Portal, P&L Analysis | 🌐 Web 리포트 |
| **2026-10-16** | [20261016_워드보고서로_만들어줘](./20261016_워드보고서로_만들어줘) | 워드보고서로 만들어줘 | Master AI Agent, kpi-sheet, fx-monitor, price-tracker | 📄 보고서 |
| **2026-10-16** | [20261016_9월_영국_수익성_분석](./20261016_9월_영국_수익성_분석) | 9월 영국 수익성 분석 보고서 만들어줘 | Master AI Agent, pnl-analysis, P&L Analysis, 수익성 Simulator, MS Trend, KPI Sheet | 📄 보고서 |
| **2026-10-16** | [20261016_스위스_7월_제품군별_점유](./20261016_스위스_7월_제품군별_점유) | 스위스 7월 제품군별 점유율 확인해줘 | Master AI Agent, ms-trend | 📄 보고서 |
| **2026-10-16** | [20261016_스위스_8월_제품군별_점유](./20261016_스위스_8월_제품군별_점유) | 스위스 8월 제품군별 점유율 확인해줘 | Master AI Agent, ms-trend, kpi-sheet | 📄 보고서 |
| **2026-10-16** | [20261016_포털마스터에이전트연동](./20261016_포털마스터에이전트연동) | /grill-me sales portal에서 프롬프트로 | Sales Management Portal, Master AI Agent, Antigravity Sidecar (axis-portal-bridge) | 🌐 Web 리포트 |
| **2026-10-15** | [20261015_27년BP_2차_QNED3만대감축정합](./20261015_27년BP_2차_QNED3만대감축정합) | 27년 사업계획 2차 회신 RAW 파일('③모델별RAW') QNED 30,001대 감축(1,877,751대→1,847,750대), 98"↑(53,521대) 완전 보존, 27년 신모델(M05~M12) 90" 미만 모델 최대잔여법 비례 차감 및 16개국 법인별 가이드 100% 정합(0오차, 음수 방지) 전수 감사 합격 | Master AI Agent, 사업계획_27년 Data Engineer, Lineup & P&L Engine | 📊 Excel, 📄 보고서 |
| **2026-10-15** | [20261015_MSTrend8월업데이트](./20261015_MSTrend8월업데이트) | 2026년 8월 M/S Databook DB 업데이트 및 8월 vs 7월 Diff 대시보드 리포트 배포 (스위스 포함 14개 법인) | 08. MS Trend, Master Agent | 🌐 Web 배포(Firebase), 📄 보고서, 📊 JSON |
| **2026-10-14** | [20261014_손익대시보드배포및다운로드검증](./20261014_손익대시보드배포및다운로드검증) | 유럽 15개국 TV 손익 대시보드 Firebase 라이브 배포 완료 및 스위스 대시보드 최신 9월 원본 엑셀(.xlsb, 112.7MB) 다운로드 링크 자동 연동·수신 100% 무결성 검증 | 05. TV P&L Analysis, Dashboard Publisher | 🌐 Web 배포(Firebase), 📊 Excel, 📄 보고서 |
| **2026-10-14** | [20261014_유럽15개국9월손익업데이트](./20261014_유럽15개국9월손익업데이트) | 유럽 15개국(AG, BN, CK, Swiss, ES, FS, HS, IS, LA, MK, PL, PT, RO, SW, UK) TV 2026년 9월 NERP 실적 분석 및 개별 대시보드·포털(index.html) 전사 일괄 업데이트 완료 (RA/AK/UR 제외) | 05. TV P&L Analysis, Financial Analyst, Dashboard Publisher | 🌐 Web 대시보드 15개, 📄 포털 리포트 |
| **2026-10-14** | [20261014_스위스9월손익업데이트](./20261014_스위스9월손익업데이트) | 스위스(Swiss) TV 2026년 9월 NERP 실적 분석, Swiss_TV_Profitability_Report.html 대시보드 9월 업데이트 및 메인 포털(index.html) 스위스 실적 카드 동기화 완료 | 05. TV P&L Analysis, Financial Analyst, Dashboard Publisher | 🌐 Web 리포트, 📄 보고서 |
| **2026-10-12** | [20261012_법인별_Raw_수식_표준화](./20261012_법인별_Raw_수식_표준화) | 스위스(Swiss) Raw 시트 A:U 수식 21개 표준 기준 유럽 16개 법인 P&L Analysis NERP Raw 시트 동기화 및 무결성 검증 완료 (DG 파일은 94만 행 한계로 방안 C 원본 보존) | 05. TV P&L Analysis, Master Agent | 📊 Excel, 📄 검증 리포트 |
| **2026-10-08** | [20261008_TV가격조사무결성혁신및유럽확장](./20261008_TV가격조사무결성혁신및유럽확장) | TV 가격 조사 무결성 혁신 및 유럽 실시간 전수 조사 확장 (DE, AT, UK, ES, IT, NL, FR, CH 전수 실시간 수집 및 7대 품질게이트 100% 합격) | 04. Price Tracker | 📊 Excel, 🌐 Web 대시보드, 🛡️ 품질게이트 v2 |
| **2026-10-08** | [20261008_가격조사엔진무결성및자기개선구축](./20261008_가격조사엔진무결성및자기개선구축) | Price Tracker 실시간 가격 조사 무결성 복원(오추출·과거가격 재사용·모델 누락 방지) 및 4단계 엔진 사다리, 7대 품질 게이트(Hard Halt), 독립 검증기, 상시 카나리, 주간 자율 개선 제안 루프(Self-Improvement) 구축 | 04. Price Tracker, Master Agent | 📊 파이프라인 엔진, 🛡️ 품질게이트 v2, 📄 진단/개선 보고서 |
| **2026-10-07** | [20261007_33번슬라이드_사운드나레이션분할연계](./20261007_33번슬라이드_사운드나레이션분할연계) | 33번 슬라이드 AI Voice Remastering & Karaoke Mode 사운드-나레이션 3단계 분할 연계 엔진 구축 (도입부 나레이션 1문장 발화 및 자막 표출 → 약 18.6초 기능 사운드 비디오 시연 및 자막 자동 은닉 → 시연 종료 후 2문장 후속 나레이션 및 자막 재개, 우측 설명창 [기능 사운드 시연] 뱃지 적용) | 제품 소개 사이트 자동 제작 에이전트 | 🌐 Web 대시보드, 📄 보고서 |
| **2026-10-07** | [20261007_스위스65S85H가격조사](./20261007_스위스65S85H가격조사) | 스위스 유통에서의 현재 65S85H의 가격 조사 | 04. Price Tracker, swiss_tv_tracker | 📊 Excel, 📄 보고서 |
| **2026-10-07** | [20261007_AXIS_가이드_실무활용예시3번재배치](./20261007_AXIS_가이드_실무활용예시3번재배치) | AXIS 시스템 소개 가이드 내 '6. 실무 활용 예시'를 3번으로 전진 배치하고 4~6번 항목 순서/번호 일괄 재배치(3.실무예시, 4.포탈구성, 5.DB구조, 6.보안구성), DOM 물리적 재배치 및 Firebase 라이브 배포 완료 | Master AI Agent, Europe Sales Management Portal | 🌐 Web 가이드, 📄 보고서 |
| **2026-10-07** | [20261007_가이드_AXIS정의및소개문구수정](./20261007_가이드_AXIS정의및소개문구수정) | AXIS 가이드 1장 타이틀 '1. AXIS(Agentic eXecution & Integrated Sales System) 소개' 변경 및 마스터 에이전트 핵심 소개 문구 정제 일괄 반영, Firebase 라이브 배포 완료 | Master AI Agent, Europe Sales Management Portal | 🌐 Web 가이드, 📄 보고서 |
| **2026-10-07** | [20261007_카테고리컬러_제품_매출손익_맞교환](./20261007_카테고리컬러_제품_매출손익_맞교환) | 포털 '제품 정보'와 '매출/손익 관리' 카테고리 테마 컬러 상호 맞교환(제품 정보: LG Red, 매출/손익 관리: Emerald Teal) 및 Firebase 라이브 배포 완료 | Master AI Agent, Europe Sales Management Portal | 🌐 Web 포털, 📄 보고서 |
| **2026-10-07** | [20261007_가이드포탈복귀_무반응해결및사이드버튼제거](./20261007_가이드포탈복귀_무반응해결및사이드버튼제거) | AXIS 가이드 내 사이드바 중복 복귀 버튼(`세일즈 포탈로 이동`) 삭제 및 좌측 상단 [포탈로 돌아가기] 클릭 시 Chromium 브라우저 `window.close()` 무음 차단 버그로 인한 무반응 결함 규명/직접 전환(Fallback Direct Navigation) 해결 완료 | Master AI Agent, Europe Sales Management Portal | 🌐 Web 가이드, 📄 보고서 |
| **2026-10-07** | [20261007_사이드바_AXIS위치및컬러개편](./20261007_사이드바_AXIS위치및컬러개편) | 포털 사이드바 'AXIS 시스템 소개' 최상단(홈 위) 배치 및 화이트 볼드체 변경, 카테고리 컬러 리밸런싱(매출/손익: LG Red, 제품 정보: Emerald Teal) 및 Firebase 라이브 배포 완료 | Master AI Agent, Europe Sales Management Portal | 🌐 Web 포털, 📄 보고서 |
| **2026-10-07** | [20261007_카테고리별_4색테마_시각차별화](./20261007_카테고리별_4색테마_시각차별화) | TV 유럽영업 포털 4대 카테고리별 카드(Full-Themed Card: 상단 액센트라인·태그배지·타이틀아이콘·액션버튼) 및 상단 필터 칩·사이드바 아이콘을 4대 독립 테마 컬러(틸/인디고/앰버/스카이블루)로 시각적 차별화 개편 및 Firebase 라이브 배포 완료 | Master AI Agent, Europe Sales Management Portal | 🌐 Web 포털, 📄 보고서 |
| **2026-10-07** | [20261007_제품정보_PRM순서및2026명칭개선](./20261007_제품정보_PRM순서및2026명칭개선) | TV 유럽영업 포털 제품 정보 대시보드 내 '2025년 거래선 PRM 상담자료' 맨 뒤 배치 및 '2026 TV PRM', '2026 Spec Sheet', '2026 TV Product profile' 2026 연도 명칭 통일 적용 완료 | Master AI Agent, Europe Sales Management Portal | 🌐 Web 포털, 📄 보고서 |
| **2026-10-07** | [20261007_가이드포탈복귀_세션유지개선](./20261007_가이드포탈복귀_세션유지개선) | AXIS 시스템 아키텍처 가이드에서 [포탈로 돌아가기] 클릭 시 로그인 화면 노출 결함 원인 규명, localStorage 기반 다중 탭 세션 동기화(Dual-Sync) 및 rel="opener" 링크 보강, 무인증 방지 라이브 배포 완료 | Master AI Agent, Europe Sales Management Portal | 🌐 Web 포털, 📄 보고서 |
| **2026-10-07** | [20261007_법인별_OLED_시리즈별_수익성분석](./20261007_법인별_OLED_시리즈별_수익성분석) | 2026년 1~8월 누적 실적 NERP P&L Analysis 원천 기준 유럽 법인별 OLED TV 내 W / G / C / B 시리즈 매출 비중, 영업이익율(COI%), 한계이익율(MP%) 종합 분석 및 전략 진단 | Master Agent, TV P&L Analysis Agent, Financial Analyst | 📊 Excel, 📄 보고서 |
| **2026-10-07** | [20261007_시나리오02_전략회의개편](./20261007_시나리오02_전략회의개편) | AXIS 시스템 가이드 6장에서 6. 실무활용예시 두번 | Master Agent, Europe Sales Management Portal, Europe Strategic Insight | 📄 보고서 |
| **2026-10-07** | [20261007_2026전략회의_PD회의_추진과제정리](./20261007_2026전략회의_PD회의_추진과제정리) | 2026년 전략회의(2/5/9월) 및 PD회의(4/8월) 시계열 논의 사안·추진과제 총괄 정리 (유럽 공통과제 vs 16개 법인/지점별 실행과제) | Master Agent, Europe Strategic Insight, Planning Group | 📄 Word 보고서 |
| **2026-10-06** | [20261006_유럽가격지연원인및실시간개편](./20261006_유럽가격지연원인및실시간개편) | 아래 사례처럼 실시간 라이브 쿼리를 건너뛰고 기존 로컬 | Price Tracker, Master Agent | 📊 Excel, 📊 Excel, 🌐 Web 리포트 |
| **2026-10-06** | [20261006_스위스미디어마트가격불일치규명](./20261006_스위스미디어마트가격불일치규명) | 스위스 MediaMarkt LG OLED 65C67 가격 불일치(대시보드 1,999 CHF vs 실제 1,599 CHF) 원인 규명(Aus unserer Werbung 프로모션 인하 및 무인 스케줄러 STEALTH_FAST 캐시 폴백), 원천 DB/엑셀 1,599 CHF 동기화 및 라이브 배포 완료 | 04. Price Tracker, swiss_tv_tracker, Master AI Agent | 📊 Excel, 🌐 Web 대시보드, 📄 보고서 |
| **2026-10-06** | [20261006_가이드UI_시나리오라벨개선](./20261006_가이드UI_시나리오라벨개선) | AXIS 아키텍처 가이드 시나리오 버튼 문구 정제((새 창 열기), 실행완료 5초 삭제), '6. 실무 활용 예시' 명칭 변경, 사이드바 7번 메뉴 삭제 및 Firebase 배포 | Master AI Agent, Europe Sales Management Portal | 🌐 Web 가이드, 📄 보고서 |
| **2026-10-06** | [20261006_스위스유통가격전수조사](./20261006_스위스유통가격전수조사) | 스위스 3대 유통사(MediaMarkt, Interdiscount, Digitec) 2026년 10월 6일(W41) 전수 가격 조사, Samsung OLED S95H 전 라인업(77/65/55/48") 및 48S95H 신규 행 매칭 반영, W41 주간 변동 분석, 품질 게이트 통과, 시계열 DB 적재 및 Firebase 호스팅 배포 | 04. Price Tracker, swiss_tv_tracker, Master AI Agent | 📊 Excel, 🌐 Web 리포트, 📄 보고서 |
| **2026-10-03** | [20261003_스페인_OLED최저가_ATA비교](./20261003_스페인_OLED최저가_ATA비교) | 스페인 MediaMarkt 55/65인치 OLED 최저가 변동 현황과 삼성 동급 모델과의 Price Gap, 그리고 ATA Guide 상 최저 승인 가능선 비교 분석 | Master AI Agent, Price Tracker, ATA Guide, Profitability Simulator | 📊 Excel, 📄 보고서 |
| **2026-10-03** | [20261003_시나리오01_결과및엑셀뷰어](./20261003_시나리오01_결과및엑셀뷰어) | /grill-me 실무 시나리오 01 실전 답변 및 엑셀 결과 독립 뷰어 분리([← 가이드로 돌아가기] 연동), 표 헤더 블랙 버그 수정, 16개국 A~P 법인 가명화 및 Firebase 실배포 | Master AI Agent, Europe Sales Management Portal, KPI Sheet Orchestrator | 🌐 Web 리포트, 📊 Excel |
| **2026-10-03** | [20261003_유통재고WOS_OLED비중](./20261003_유통재고WOS_OLED비중) | 유럽 전 법인 중 유통재고 주수(WOS)가 6주를 초과 | Master AI Agent, KPI Sheet Orchestrator, GDMI Weekly Sellout Analysis | 📊 Excel |
| **2026-10-03** | [20261003_아키텍처가이드보안개편](./20261003_아키텍처가이드보안개편) | AXIS 시스템 & TV Europe Sales Man | Master Agent, Europe Sales Management Portal | 📄 보고서 |
| **2026-10-03** | [20261003_아키텍처가이드DB개편](./20261003_아키텍처가이드DB개편) | AXIS 시스템 & TV Europe Sales Man | Master Agent, Europe Sales Management Portal | 📄 보고서 |
| **2026-10-03** | [20261003_세일즈포탈_15대에이전트개편](./20261003_세일즈포탈_15대에이전트개편) | /grill-me '3. 세일즈 포탈 허브'를 '3. 세일즈 포탈 구성'으로 변경 및 15대 전문 AI 대시보드 카드 통합, 추천 프롬프트 삭제 후 3대 핵심 블록(원천 데이터, 연계 DB/파이프라인, 핵심 지표 & 실무 활용 목적) 보강, 7대 챕터 정규화 및 라이브 배포 | Master AI Agent, TV Europe Sales Management Portal | 🌐 Web 가이드, 📄 보고서 |
| **2026-10-03** | [20261003_포탈복귀탑바개선](./20261003_포탈복귀탑바개선) | /grill-me AXIS 시스템 소개 보고서에서 세일즈 포탈로 돌아갈 때 첨부 이미지처럼 다크 네이비 스마트 탑바([← 포탈로 돌아가기] [시스템 가이드] AXIS 시스템 종합 소개, 인쇄/PDF 저장 단축 버튼 및 배포 상태 칩) 구축, 공용 portal-topbar.js 표준화 및 Firebase 배포 | Master AI Agent, TV Europe Sales Management Portal | 🌐 Web 리포트, 📄 보고서 |
| **2026-10-02** | [20261002_해외영업전달용_오프라인패키지](./20261002_해외영업전달용_오프라인패키지) | /grill-me 이 컨텐츠를 파일로 전달하여 해외영업인원이 실행해서 볼 수 있도록 해줘 (사내 보안 정책 100% 통과 원클릭 실행형 오프라인 압축 패키지 ZIP 구축, 72개 슬라이드·54개 모션비디오·하이브리드 음성/자막 엔진·초경량 로컬서버 런처 동봉, 오프라인 및 인터넷 없는 출장지 무설치 자립 구동 완결) | 제품 소개 사이트 자동 제작 에이전트, prm-presenter-guide-engine Skill | 📦 ZIP 패키지 (178.89MB), 📄 보고서 |
| **2026-10-02** | [20261002_슬라이드10_자막숨김제어](./20261002_슬라이드10_자막숨김제어) | /grill-me 슬라이드 10에 대해서만 자막을 슬라이드쇼 모드에서 보여주지 말아줘. 컨텐츠의 내용과 중복되어 가시성이 떨어져 (대화형 슬라이드 10 음성 나레이션 5턴 정상 유지, 슬라이드쇼 모드 하단 투명 자막 바 및 오버레이 말풍선 선별 숨김, 타 슬라이드 자막 자동 복원 및 라이브 배포) | 제품 소개 사이트 자동 제작 에이전트, prm-presenter-guide-engine Skill | 🌐 Web 대시보드, 📄 보고서 |
| **2026-10-02** | [20261002_슬라이드쇼자막싱크수정](./20261002_슬라이드쇼자막싱크수정) | /grill-me 슬라이드쇼 모드에서 영문 나레이션과 자막의 싱크가 맞지 않고 특히 두번째 자막 변경시 부터 나레이션보다 한참 늦게 자막이 바뀌어 (클라우드 고음질 음성의 onboundary 미발행 결함 규명, 155 WPM 모델 기반 밀리초 정밀 캘리브레이션, 2.5초 지연 락 제거 및 50ms 고속 인터벌 무지연 Fallback, 고립 단어 방지 시네마틱 청킹, 브라우저 캐시 무력화 배포로 100% 무오차 실시간 동기화 완결) | 제품 소개 사이트 자동 제작 에이전트, prm-presenter-guide-engine Skill | 🌐 Web 대시보드, 📄 보고서 |
| **2026-10-02** | [20261002_슬라이드영상나레이션싱크수정](./20261002_슬라이드영상나레이션싱크수정) | /grill-me 슬라이드의 동영상(애니메이션 효과)과 영문 script 간에 불일치가 일어나는 슬라이드가 많아... 영문 스크립트에 맞게 동영상의 애니메이션 효과가 싱크가 맞도록 점검해서 수정해줘 (슬라이드 4 프롬프트창 타이핑 지연 1.2s→7.0s 조정, 질문1·질문2·결론박스 1:1 완벽 동기화, 19초 고화질 MP4 재렌더링 및 라이브 배포) | 제품 소개 사이트 자동 제작 에이전트, prm-presenter-guide-engine Skill | 🎬 MP4 모션 비디오, 🌐 Web 대시보드, 📄 보고서 |
| **2026-10-02** | [20261002_포탈사이드바개편](./20261002_포탈사이드바개편) | /grill-me 첨부 포탈 이미지에서 Master AI Agent 는 삭제해줘, Axis 시스템 소개는 녹색 글씨로 변경해서 Monthly 대시보드와 한줄 띄워서 보여줘 (사이드바 Master AI Agent 메뉴 제거, 16px 은은한 구분선 추가, AXIS 시스템 소개 포털 시그니처 틸 그린 테마 전환 및 라이브 배포) | TV Europe Sales Management Portal, global-sales-portal Skill | 🌐 Web 포털, 📄 보고서 |
| **2026-10-01** | [20261001_2027파트너성장전략대시보드](./20261001_2027파트너성장전략대시보드) | /grill-me 2027 LG TV & Partner Growth Strategy 대시보드 구축 및 고도화 (슬라이드쇼 음성-자막 실시간 듀얼 드라이브(Dual-Drive Clock & Boundary) 싱크 엔진 탑재(Chromium onboundary 미발행 브라우저 버그 근본 해결, 72개 슬라이드 361개 135자 이내 2줄 청크 80ms 클럭 추적 및 경계 이벤트 수신 시 실시간 리캘리브레이션 무오차 동기화, 첫 문장 멈춤 결함 100% 영구 해결), 컨테이너 100% 투명화 및 화이트 고대비 아웃라인 가독성 극대화, 상단 헤더 '📑 목차' 원클릭 토글 버튼(단축키 T/M) 신설 및 슬라이드 단일 카드 격리(Single Slide Focus View), Slide 24~72 전수 49개 슬라이드 국·영문 대본 100% 무손실 완전 일치화, 슬라이드 전환 시 음성 듣기 자동 실행, Slide 11·12 영상-나레이션 순차 재생(Video-First) 엔진, Slide 10 5턴 대화형 통합 및 72p 재색인, 52개 모션 비디오 인라인 전환 및 세일즈 포털 연동) | 제품 소개 사이트 자동 제작 에이전트, prm-presenter-guide-engine Skill, TV Europe Sales Management Portal | 🌐 Web 대시보드, 🎬 MP4 모션 비디오, 📄 보고서 |
| **2026-10-01** | [20261001_AXIS시스템구성_가이드개편](./20261001_AXIS시스템구성_가이드개편) | /grill-me AXIS 통합 네이밍 확정, 1.3 시스템 구성 개편 및 좌측 메뉴 2번 'MASTER AI AGENT 구조' 3계층(마스터-15대 도메인-3대 기술 서브) SVG 계통 다이어그램 & 실무 시나리오 역할 전면 재구축 | Master AI Agent, TV Europe Sales Management Portal | 🌐 Web 리포트, 📄 PRD, 📑 Task 기록 |
| **2026-10-01** | [20261001_AXIS시스템소개보고서](./20261001_AXIS시스템소개보고서) | /grill-me AXIS 시스템 & TV Europe Sales Management Portal 종합 소개 HTML 보고서 제작 (8대 챕터 정밀 분할, 15대 에이전트 전수 수록, DB/보안 아키텍처, 포털 연동 및 PRD 완결) | Master AI Agent, TV Europe Sales Management Portal | 📄 PRD, 🌐 Web 리포트 |
| **2026-10-01** | [20261001_PD회의_MRGB논의정리](./20261001_PD회의_MRGB논의정리) | 지난 PD회의에서 MRGB와 관련하여 논의된 내용 정리 (GfK 카테고리 매핑, QNED 대체 금지, 성수기 판촉가 및 15개국 손익 현황) | Master AI Agent, Strategic Reports Knowledge Base | 📄 보고서 |
| **2026-10-01** | [20261001_영업보고서학습설계](./20261001_영업보고서학습설계) | /grill-me 마스터 에이전트 사내 주요 영업 보고서 학습 및 전략 자문/의사결정 지원 체계 구현 설계 | Master Agent, Strategic Knowledge RAG, DuckDB Core | 📄 보고서/설계서 |
| **2026-09-30** | [20260930_스위스25년4Q손익](./20260930_스위스25년4Q손익) | 스위스 작년 4분기 펀더멘털 손익 기준으로 영업이익율과 | P&L Analysis | 📄 보고서 |
| **2026-09-30** | [20260930_스위스_선행물동_판가조정](./20260930_스위스_선행물동_판가조정) | /grill-me 스위스 선행 물동 '판가' 시트 29개 모델 신규 가격을 '판가조정' 시트 K:P열(10월~3월)에 일괄 반영 및 대상 모델 R:W열 차감율 3%p(0.03) 일괄 감액 (0% 예외 보존) | Master AI Agent, TV P&L Analysis Agent | 📊 Excel, 📄 보고서 |
| **2026-09-30** | [20260930_스위스_제품군별_분기별_한계이익](./20260930_스위스_제품군별_분기별_한계이익) | /grill-me 스위스 지점 제품군별(OLED, MRGB, QNED, NUHD, Total) 분기별('25.1Q~'26.3Q) 한계이익률(MP%) 정리 및 원가/판촉 드라이버 분석, 엑셀 생성 | Master AI Agent, TV P&L Analysis Agent | 📊 Excel, 📄 보고서 |
| **2026-09-30** | [20260930_GSCP_W39vsW40_물동비교](./20260930_GSCP_W39vsW40_물동비교) | /grill-me GSCP W39 vs W40 4분기 물동 비교 분석 (FCST -5,334대 하향 및 SA -2,368대 조정, 공급 충족률 88.9%→97.6% 개선, 세그먼트/인치/Top모델 다차원 진단 및 비교 엑셀 생성) | Master AI Agent, GSCP 물동 분석 파이프라인 | 📊 Excel, 📄 보고서 |
| **2026-09-30** | [20260930_GDMI대시보드재배포](./20260930_GDMI대시보드재배포) | 수정사항이 있으니 재배포해줘 (AG/UK CPSI 정합성 보정 데이터 반영, 18개국 지표/인사이트/대시보드 리빌드 및 Firebase 무중단 재배포) | GDMI_Weekly_Sellout_Analysis-main | 🌐 Web 대시보드, 📑 JSON, 📄 보고서 |
| **2026-09-30** | [20260930_CPSI정합성점검](./20260930_CPSI정합성점검) | CPSI Master(0929) vs 에이전트 정합성 대조, 오스트리아(AG) 채널 추가 및 영국(UK) 본토 필터링 조치 완료 (13개국 100% 완전 정합 달성) | GDMI_Weekly_Sellout_Analysis, Master Agent | 📊 Excel, 📄 보고서 |
| **2026-09-30** | [20260930_거래선상담자료영문설명창](./20260930_거래선상담자료영문설명창) | 2026 유럽 거래선 상담 자료_v9 PPT 영문 스크 | 제품 소개 사이트 자동 제작 에이전트 | 🌐 Web 리포트 |
| **2026-09-30** | [20260930_유럽18개국CPSI갱신](./20260930_유럽18개국CPSI갱신) | 나머지 국가들도 대시보드 업데이트해줘 | GDMI_Weekly_Sellout_Analysis-main | 🌐 Web 리포트 |
| **2026-09-30** | [20260930_전체에이전트DuckDB동기화](./20260930_전체에이전트DuckDB동기화) | 새로운 파일들이 많은데 지금 중앙 DuckDB와 웹 번 | Master Agent, Price Tracker, GDMI Weekly, P&L, MS Trend, KPI Sheet, FX-Monitor | 📄 보고서 |
| **2026-09-30** | [20260930_주간엑셀DuckDB자동동기화](./20260930_주간엑셀DuckDB자동동기화) | 에이전트의 데이터 소스들이 주로 엑셀로 이루어져 있고  | Master Agent, File Watcher, DuckDB Core, DataOps | 📄 보고서 |
| **2026-09-30** | [20260930_스위스CPSI갱신](./20260930_스위스CPSI갱신) | 목표 주차를 40으로 스위스 대시보드 업데이트해줘 | GDMI_Weekly_Sellout_Analysis-main | 🌐 Web 리포트 |
| **2026-09-29** | [20260929_27년BP_1분기OLED_극초대형수량정합](./20260929_27년BP_1분기OLED_극초대형수량정합) | /grill-me 1분기 OLED 국가별 수량 100% 정합(EU 336,896대, 16개국 0오차), UHD 극초대형(98"↑) 결손(-1,286대) 원인(26년 98" 소형이관 증발 및 MRGB 100" 역류) 규명 및 해결(98"/115" 캐리오버 지정), 8대 전략세그먼트(128개 세부목표 100% 일치)·연간순매출($2,545.2M)·SD 28.00%·클린컷 100% 완전 보존 전수 감사 합격 | Master AI Agent, 사업계획_27년 Data Engineer, Lineup Clean-Cut & P&L Engine | 📊 Excel, 📄 보고서 |
| **2026-09-29** | [20260929_유럽호주가격전수조사무결성감사](./20260929_유럽호주가격전수조사무결성감사) | 유럽 11개국 및 호주 TV 가격 전수 조사 및 모델 무결성 감사 | Price Tracker | 📄 Word/MD 리포트, 🌐 Web 대시보드, 📊 Excel |
| **2026-09-29** | [20260929_27년BP_77인치이상OLED수량정합](./20260929_27년BP_77인치이상OLED수량정합) | /grill-me 77인치 이상 OLED 수량 2개 법인(LGELA +1,948대, LGEPL +1,674대) 목표 초과 원인 규명(Clean-Cut 광역 매칭 시 26년 48인치 부재로 77인치로 이관된 결함) 및 해결(동일 48인치 27년 모델 5~12월 분산 배부 환원), 16개국 77인치↑ 100% 일치(LA 5,728대, PL 10,197대), 단가/SD 재보정을 통한 순매출(,545.2M)·SD 28.00%·Q1 순매출(.8M) 100% 보존 전수 감사 합격 | Master AI Agent, 사업계획_27년 Data Engineer, Lineup Clean-Cut & P&L Engine | 📊 Excel, 📄 보고서 |
| **2026-09-28** | [20260928_27년BP_차감율28프로조정](./20260928_27년BP_차감율28프로조정) | /grill-me 유럽 연간 전체 차감율(SD Rate) 28.07%→28.00% 정합 및 16개국 법인별 목표 차감율 동기화, GP 단가 원자적 연동(G* (1-SD) = Net 불변)을 통한 연간 순매출($2,545.2M) 및 16개국 순매출 $0.00M 오차 보존, Q1 순매출($616.8M)·총수량(526.5만대)·클린컷 100% 보존 전수 감사 합격 | Master AI Agent, 사업계획_27년 Data Engineer, P&L SD & Pricing Pipeline | 📊 Excel, 📄 보고서 |
| **2026-09-28** | [20260928_27년BP_신구모델전환및판가누락해결](./20260928_27년BP_신구모델전환및판가누락해결) | /grill-me 27년 신모델 1~4월 배부 제거(0대), 26년 구모델 5~12월 배부 제거(FHD 제외 0대) 클린컷 확립, 스페인(ES) 85/75 QNED 전월 판가 누락(유형 1) 포르투갈 판가 100% 매핑, 26년 FHD 하반기 판가 연장으로 유럽 전체 판가 미싱 0건(Zero Defect) 달성, 연간 순매출($2,545.2M) 및 총수량(526.5만대) 100% 보존 전수 감사 합격 | Master AI Agent, 사업계획_27년 Data Engineer, Lineup Clean-Cut Pipeline | 📊 Excel, 📄 보고서 |
| **2026-09-28** | [20260928_27년BP_상하반기매출비중조정](./20260928_27년BP_상하반기매출비중조정) | /grill-me 상반기 매출 비중 55% 초과 국가(BN) 5%p 축소(57.69%→52.69%), 50~54% 국가 7개국(AG, Swiss, ES, LA, MK, PT, SW) 49.00% 달성, 5~6월 신모델 수량 하반기(7~12월) 계절성 비례 이전(60,894대), 연간 순매출(,545.2M) 및 16개국 연간 총수량(526.5만대)·8대 전략세그먼트·특화타깃 100% 완전 보존 전수 감사 완료 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Seasonality Rebalance Pipeline | 📊 Excel, 📄 보고서 |
| **2026-09-28** | [20260928_27년BP_1분기순매출및4월단가조정](./20260928_27년BP_1분기순매출및4월단가조정) | /grill-me 1분기 순매출 국가별 목표(EU TTL $616.7M) 가격만 조정하여 100% 일치, 4월 가격에 동일 배율 적용, 1~4월 변동분 하반기(7~12월) 단가 가중 비례 반영으로 연간 순매출($2,545.2M) 및 총매출 100% 보존, 전 모델 수량(526.5만대) 완전 불변 전수 감사 완료 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Pricing Pipeline | 📊 Excel, 📄 보고서 |
| **2026-09-28** | [20260928_27년BP_분기이동_B시리즈91캡](./20260928_27년BP_분기이동_B시리즈91캡) | /grill-me 1분기 3%·2분기 4% 감축 및 4분기 증량 배부(+89,046대, 총수량 100% 보존), OLED B시리즈 91% 캡(전년비 -4%p 추가 축소) 및 동일 인치대 C시리즈 이전(3,648대), 5개국 유통별 비중 동기화, 매출 $3,533.9M/순매출 $2,545.2M/차감율 28.0% 100% 보존 전수 감사 완료 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Scenario Engine | 📊 Excel, 📄 보고서 |
| **2026-09-28** | [20260928_27년BP_5개법인_유통별BLU비중배부](./20260928_27년BP_5개법인_유통별BLU비중배부) | /grill-me DG, ES, FS, IS, UK 5개 법인의 유통(유통1~4, OTHERS) 수량을 26년 실적 비중(ES/FS/IS/UK는 P&L Sell-in 매출 비중, DG는 GDMI Sell-out 수량 비중)대로 BLU별(OLED, MRGB, QNED, UHD, FHD) 재배부, '①유통업데이트' W7:AA11 및 '②모델별RAW' U열 유통사명 기입, 유럽 526.5만대/8대 세그먼트/재무($3,533.9M/순$2,545M/차감28%) 100% 보존 전수 감사 완료 | Master AI Agent, TV P&L Analysis, GDMI Weekly Sellout Analysis, 사업계획_27년 Data Engineer | 📊 Excel, 📄 보고서 |
| **2026-09-28** | [20260928_27년BP_TD수량및매출반영](./20260928_27년BP_TD수량및매출반영) | /grill-me 27년 BP TD 목표 수량(526.5만대) 및 매출($3,533.9M/순매출$2,545M/차감28%) 반영, 1~4월 26년 모델/5~12월 27년 모델 clean-cut 전환, OLED B시리즈 26년 초과 9개국 95% 캡 및 C시리즈 수량 이전(26,775대) & C시리즈 단가 조정 매출 보존, 폴란드 FHD(439대) 신규 등록·배부, 영국 QNED(402,921대) 정합, OLED 97"(2,501대)/77"↑(22.3만대)/UHD 극초대형(2.35만대) 16개 법인별 100% 전수 정합 완료 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Top-Down Engine | 📊 Excel, 📄 보고서 |
| **2026-09-28** | [20260928_사이드바_기준시점표시](./20260928_사이드바_기준시점표시) | 첨부 이미지는 kpi SHEET의 대시보드 데이터의 기 | KPI Sheet | 📄 보고서 |
| **2026-09-28** | [20260928_OLED_QNED_전년수치보](./20260928_OLED_QNED_전년수치보) | OLED, QNED 전년 수치가 맞지 않아. 원인을 파 | DataOps Agent, DevOps Agent, BI Analyst Agent | 📄 보고서 |
| **2026-09-28** | [20260928_CPSI2025수치보정](./20260928_CPSI2025수치보정) | 2025년 수치도 26년_유럽+CIS_KPI_2026와 | DataOps Agent, DevOps Agent, KPI Sheet Orchestrator | 📄 보고서 |
| **2026-09-28** | [20260928_대시보드배포](./20260928_대시보드배포) | 대시보드 업데이트하고 배포해줘 | DevOps Agent, KPI Sheet Orchestrator | 📄 보고서 |
| **2026-09-28** | [20260928_CPSI스킬영구저장](./20260928_CPSI스킬영구저장) | 다음에 ★ (Final) Y26 Consolidated | KPI Sheet Orchestrator, DataOps Agent, kpi-sheet-update Skill | 📄 보고서 |
| **2026-09-28** | [20260928_CPSI컬럼오류수정](./20260928_CPSI컬럼오류수정) | 첫번째 첨부 이미지는 CPSI 파일에서 EU TTL로  | KPI Sheet Orchestrator, DataOps Agent, DevOps Agent, BI Analyst Agent | 📄 보고서 |
| **2026-09-28** | [20260928_CPSI업데이트](./20260928_CPSI업데이트) | D:\\TV 유럽영업\\15. AX Task\\2026 | KPI Sheet (DataOps, DevOps, BI Analyst) | 📄 보고서 |
| **2026-09-28** | [20260928_매출장업데이트](./20260928_매출장업데이트) | D:\\TV 유럽영업\\15. AX Task\\2026 | KPI Sheet (DataOps, DevOps, BI Analyst) | 📄 보고서 |
| **2026-09-28** | [20260928_KPISheet정리](./20260928_KPISheet정리) | D:\\TV 유럽영업\\15. AX Task\\2026 | KPI Sheet (DataOps, DevOps) | 📄 보고서 |
| **2026-09-28** | [20260928_27년BP_신구모델매칭_물동비교](./20260928_27년BP_신구모델매칭_물동비교) | /grill-me 27년 사업계획에서 26년 모델과 27년 모델의 국가별 매칭 형태(1:1, N:1, 1:N, 단종/신규) 및 연간 물동 비교 분석 | Master AI Agent, 사업계획_27년 Data Engineer, Lineup Matching Engine | 📊 Excel, 🌐 Web 리포트 |
| **2026-09-24** | [20260924_2026모델전면재조사및W시리즈제외](./20260924_2026모델전면재조사및W시리즈제외) | 2026년형 모델 전 유럽 유통사 전면 재조사 및 대시보드 W 시리즈/32" UHD 표출 제외 | Price Tracker, Master Orchestrator, Data Intelligence Agent | 📊 Excel, 🌐 Web 대시보드 |
| **2026-09-24** | [20260924_이탈리아미디어월드OLED재조사](./20260924_이탈리아미디어월드OLED재조사) | MediaWorld IT 삼성 OLED 2026년 모델 전면 재조사 및 대시보드 복구 | Price Tracker, Master Orchestrator | 📊 Excel, 🌐 Web 리포트 |
| **2026-09-24** | [20260924_GDMI주간W39업데이트](./20260924_GDMI주간W39업데이트) | D:\TV 유럽영업\15. AX Task\2026 AX | GDMI Weekly Sellout Agent, Master AI Orchestrator, Data Management Agent, Insight Analytics Agent, Web UI Agent | 🌐 Web 리포트, 🌐 Web 리포트 |
| **2026-09-24** | [20260924_가격조사지연해결및배포](./20260924_가격조사지연해결및배포) | 모든 유통들의 가격을 조사해서 대시보드를 업데이트해줘  | Price Tracker, Master Agent | 📊 Excel, 📊 Excel, 📊 Excel, 📊 Excel, 🌐 Web 리포트, 🌐 Web 리포트, 🌐 Web 리포트 |
| **2026-09-22** | [20260922_27년BP_3대시나리오_갭극복모델](./20260922_27년BP_3대시나리오_갭극복모델) | /grill-me 27년 BP 3대 시나리오 갭 극복 배부 모델(0% Floor, QNED/MRGB Cap) 구축, 가격 탄력성 기반 2,545M$ 연동, 3대 원천 XLSB 파일 일괄 갱신 및 GDMI 스타일 웹 수립보고서 전면 개편 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Elasticity Revenue Engine | 📊 Excel (4종), 🌐 Web 리포트 |
| **2026-09-22** | [20260922_전략회의D2슬라이드30영문화](./20260922_전략회의D2슬라이드30영문화) | 26.9월 전략회의 D2 Slide 30 가격탄력성 회귀분석 영문 슬라이드 제작 및 검수 | Master AI Agent, 12. 가격 탄력성 회귀분석 | 📑 PPTX, 🖼️ PNG |
| **2026-09-22** | [20260922_27년BP시장경쟁지표수립](./20260922_27년BP시장경쟁지표수립) | 27년 BP 시장경쟁지표 완결: TTL, 3.1 OLED, 3.2 UHD, 3.3 Premium LCD(93만행 GfK Raw 연동) 시트 구축 및 19/24M 가중평균 격차 산출 | Master AI Agent, 08. MS Trend, 06. KPI Sheet Agent | 📊 Excel |
| **2026-09-21** | [20260921_27년BP전략목표수량정밀재배부](./20260921_27년BP전략목표수량정밀재배부) | /grill-me 옵션 B 실행: 세부 전략 품목(W/G/CB, MRGB, QNED, 일반UHD, FHD) 100% 정밀 재배부 및 Net 2,545M$, 차감율 28.0% 재정합 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Revenue/SD Optimizer | 📊 Excel (3종) |
| **2026-09-21** | [20260921_27년시나리오별전략목표수량교차검증](./20260921_27년시나리오별전략목표수량교차검증) | /grill-me 시나리오별로 법인별 전략목표 수량(TV Total 및 세부 품목 W/G/QNED/MRGB) 실측 및 교차 검증 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Strategic Target Validator | 📄 보고서 |
| **2026-09-21** | [20260921_27년시나리오별GP가격정율조정](./20260921_27년시나리오별GP가격정율조정) | /grill-me 시나리오별 유럽/국가별 Net 매출(2,545M$, OLED 1,388M, UHD 1,062M, FHD 95M) 및 차감율 28.0% GP 판가 정율 보정 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Revenue/SD Optimizer | 📊 Excel (3종) |
| **2026-09-21** | [20260921_27년시나리오별차감율현황](./20260921_27년시나리오별차감율현황) | 시나리오별로 전체 및 법인별 차감율(SD Rate) 및 매출 현황 집계/정리 | Master AI Agent, 사업계획_27년 Data Engineer, P&L SD Analyst | 📄 보고서 |
| **2026-09-21** | [20260921_27년BP수량배부정합성검증수정](./20260921_27년BP수량배부정합성검증수정) | /grill-me 3대 시나리오 BLU별 연간 수량 합 목표 가이드(526.5만 대) 정합성 검증 및 100% 일치 재배부 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Scenario Engine | 📊 Excel (3종) |
| **2026-09-21** | [20260921_27년시나리오별매출비교표](./20260921_27년시나리오별매출비교표) | /grill-me '법인별 수량_시나리오별' 시트에 27년 사업계획 TV Total 시나리오별 매출 비교표(백만불, %) 생성 및 배부 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Revenue Allocator | 📊 Excel |
| **2026-09-21** | [20260921_27년BP법인별작성양식수식연동](./20260921_27년BP법인별작성양식수식연동) | /grill-me 3대 시나리오 '●법인별작성양식' 분기 Net 매출 수식(AU:BH) 일괄 주입 및 자동계산 연동 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Form Bridge | 📊 Excel (3종) |
| **2026-09-21** | [20260921_27년BP3대시나리오수량배부](./20260921_27년BP3대시나리오수량배부) | /grill-me '법인별 수량_시나리오별' 기반 AO:AZ 모델 수량 배분 및 3대 시나리오 파일 분할 생성 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Scenario Engine | 📊 Excel (3종) |
| **2026-09-21** | [20260921_27년BP모델별차감율28프로반영](./20260921_27년BP모델별차감율28프로반영) | /grill-me 26년 BP 차감율 기반 연간 28.0% 보정 및 BR:CC 일괄 반영 | Master AI Agent, 사업계획_27년 Data Engineer, P&L SD Optimizer | 📊 Excel |
| **2026-09-21** | [20260921_엑셀SaveHang방지스킬화](./20260921_엑셀SaveHang방지스킬화) | 엑셀 저장 문제 원인 분석/해결 바탕 스킬 제정 및 전역 규칙 동기화 | Master AI Agent, Data Engineer, Excel Large Dataset Ops | 📄 스킬 명세 |
| **2026-09-21** | [20260921_27년BP모델별유럽판가반영](./20260921_27년BP모델별유럽판가반영) | /grill-me '②모델별RAW' 유럽(02.유럽) BF:BQ 판가 반영 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Pricing Pipeline | 📊 Excel |
| **2026-09-21** | [20260921_27년시나리오별목표배부](./20260921_27년시나리오별목표배부) | /grill-me '법인별 수량' sheet를 복사해서 | Master AI Agent, 사업계획_27년 Data Engineer, P&L Scenario Simulator | 📊 Excel |
| **2026-09-21** | [20260921_사업계획법인별수량산출](./20260921_사업계획법인별수량산출) | /grill-me '실적+전략회의 취합본'의 데이터를  | Master AI Agent, 사업계획_27년 Data Engineer, P&L Analysis Engine | 📊 Excel |
| **2026-09-21** | [20260921_27년사업계획엑셀구조](./20260921_27년사업계획엑셀구조) | 향후 작업을 위해 세개 엑셀파일의 구조를 기억할 수 있 | Master AI Agent, 사업계획_27년 Data Engineer | 📄 보고서 |
| **2026-09-21** | [20260921_전법인Parquet일괄빌드](./20260921_전법인Parquet일괄빌드) | 모든 지점과 법인에 대해서도 원천 Excel(.xlsb | P&L Analysis, P&L Data Engineer (core/data_engineer.py), Master AI Orchestrator, Parquet Live Query Bridge | 📄 보고서 |
| **2026-09-21** | [20260921_대시보드품질동기화](./20260921_대시보드품질동기화) | 대시보드에 문의하는 모든 질문에 대해 안티그래비티에서  | P&L Analysis, Master AI Orchestrator, Parquet Live Query Engine | 📄 보고서 |
| **2026-09-21** | [20260921_스위스2026MRGB손익](./20260921_스위스2026MRGB손익) | 스위스 2026년 누적 MRGB 매출·영업이익·한계이익 분석 | P&L Analysis (Swiss) | 📊 Excel, 📄 보고서 |
| **2026-09-21** | [20260921_2026_MRGB라인업스펙연](./20260921_2026_MRGB라인업스펙연) | 2026년 mrgb 제품 라인업 소개해줘 | Spec Sheet Finder, 2025/26 거래선 PRM, Master AI Orchestrator, Gemini 3.8 Flash | 📄 보고서 |
| **2026-09-18** | [20260918_전대시보드영문화연동](./20260918_전대시보드영문화연동) | 세일즈 포탈 내 각각의 대시보드들도 모두 영문화 작업을 | GDMI Weekly, P&L, KPI Sheet, MS Trend, Simulator, Price Elasticity | 📄 보고서 |
| **2026-09-18** | [20260918_MSTrend영문화](./20260918_MSTrend영문화) | /grill-me 대시보드에서 영어버젼을 만들어줘 | MS Trend Dashboard Agent | 🌐 Web 리포트 |
| **2026-09-17** | [20260917_스위스손익및4P개선](./20260917_스위스손익및4P개선) | 스위스 2024~2026.08 손익 분석 및 4P 혁신 과제 | P&L Analysis, Master Agent | 📄 Word 보고서, 🌐 Web 리포트 |
| **2026-09-17** | [20260917_스위스7월경영실적](./20260917_스위스7월경영실적) | 스위스 지점 2026년 7월 경영 성과 및 손익 분석 | P&L, KPI, Price, MS Trend | 📄 Word 보고서 |
| **2026-09-17** | [20260917_그리스8월경영실적](./20260917_그리스8월경영실적) | 그리스 법인 2026년 8월 실적 및 전략 진단 | P&L, KPI, Price, MS Trend | 📄 Word 보고서 |
| **2026-09-17** | [20260917_체코판매모델진단](./20260917_체코판매모델진단) | 체코 2026년 판매 모델 경쟁력·수익성 진단 | Price, KPI, P&L, Simulator | 📄 Word 보고서 |

---

## 📂 폴더 구조 표준 (Task Archive Convention)
```
Task/
  ├── README.md                                 # 전체 태스크 인덱스 및 목록
  └── YYYYMMDD_질문내용(10자내외)/
        ├── README.md                           # 질문 원문, 분석 보고서, 타임라인, 실행 답변
        └── [산출물 파일들]                      # 워드 보고서(.docx), 엑셀(.xlsx), 이미지 등
```

## 🛠️ 신규 Task 아카이빙 유틸리티 사용법
```bash
node -e "
const { archiveTask } = require('./scripts/archive_task');
archiveTask({
  dateStr: '20260917',
  shortTitle: '작업제목10자내외',
  query: '사용자 질문 원문',
  summary: '핵심 요약 불릿 포인트',
  dispatchedAgents: ['05. TV P&L Analysis', '06. KPI Sheet'],
  answerMarkdown: '최종 생성된 마크다운 보고서 본문',
  artifactPaths: ['생성된_워드보고서.docx'],
  moveArtifacts: true
});
"
```| [20260922_27년BP_3대시나리오_갭극복모델](./20260922_27년BP_3대시나리오_갭극복모델) | 2026-09-22 | 2027년 BP 3대 시나리오 구축 (0% Floor 보장, 중도/공격형 갭극복 멱함수 배분 모델, C1 동적 전환) | `사업계획 수립_20260922.xlsx` |
