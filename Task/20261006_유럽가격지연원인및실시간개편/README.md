# [Task] 20261006_유럽가격지연원인및실시간개편

## 1. 질의 개요 (User Request)
- **실행 일시**: 2026-10-06
- **사용자 질의 원문**:
> "아래 사례처럼 실시간 라이브 쿼리를 건너뛰고 기존 로컬 캐시(data/raw_mediamarkt_lg.json)에 저장되어 있던 9월 기준 가격(1,999 CHF)을 그대로 읽어오는 것을 엄격하게 금지했는데 왜 다시 반복된 건지 원인을 찾아서 반드시 실시간 커리가 될 수 있도록 해줘. 유럽 유통 가격 조사에서는 이러한 원칙을 적용시켰는데 제대로 실행되고 있는지도 파악해줘 / 지연되는 원인을 파악해줘"

- **연계 에이전트 (Dispatched Agents)**:
  - `04. Price Tracker`
  - `99. Master Agent`

## 2. 생성 산출물 (Artifacts)
- 📄 **[price tracker_swiss_2026 1006_v1.xlsx](./price%20tracker_swiss_2026%201006_v1.xlsx)**
- 📄 **[Swiss_ATA_Comparison_2026_1006.xlsx](./Swiss_ATA_Comparison_2026_1006.xlsx)**
- 📄 **[swiss_price_dashboard.html](./swiss_price_dashboard.html)**
- 📄 **[scrape_mediamarkt.py](./scrape_mediamarkt.py)**
- 📄 **[scrape_interdiscount.py](./scrape_interdiscount.py)**
- 📄 **[scrape_digitec.py](./scrape_digitec.py)**
- 📄 **[scrape_and_sync_hungary.py](./scrape_and_sync_hungary.py)**
- 📄 **[run_full_survey_pipeline.py](./run_full_survey_pipeline.py)**

---

## 3. 핵심 요약 (Executive Summary)
스위스 및 헝가리 가격 수집 지연(14분 정체)의 원인은 scrape_mediamarkt.py 내 import time 누락으로 Firecrawl 루프에서 예외가 발생해 로컬 Scrapling 브라우저가 60~80개 페이지를 순차 렌더링했기 때문임. 과거 캐시(1999 CHF)가 재탕된 원인은 auto_survey_scheduler.bat의 STEALTH_FAST=1 플래그 시 스크립트들이 실시간 수집을 건너뛰고 로컬 JSON을 읽도록 하드코딩되어 있었기 때문임. 유럽 11개국 전수 감사를 완료하고 스위스 3사(MediaMarkt, Interdiscount, Digitec) 및 헝가리 MediaMarkt에 Firecrawl Stealth API 라이브 수집 엔진을 전면 적용, 과거 캐시 로드 코드를 영구 삭제하였으며, 파이프라인에 당일 생성 여부를 검증하는 Pre-flight Assertion Gate를 신설하여 65C67 가격을 실시간 1599 CHF로 완벽 동기화함.

---

## 4. 상세 분석 및 실행 답변 (Execution Output)

### 1. 지연되는 근본 원인 규명
- **원인 1 (import time 누락에 따른 Firecrawl 예외)**: scrape_mediamarkt.py 상단에 import time이 누락되어 time.sleep(0.5)에서 NameError 발생.
- **원인 2 (로컬 브라우저 세션의 60~80페이지 순차 렌더링)**: 예외 발생으로 인해 2단계 Fallover인 로컬 StealthySession이 가동되어 23개 카테고리 60~80개 페이지를 페이지당 8~12초씩 순차 렌더링 및 Cloudflare 대기하면서 14분 이상 지연 정체 발생.
- **조치**: import time 추가 및 Firecrawl 실시간 엔진 최적화로 수십 초 내에 100% 라이브 추출 완료.

### 2. 과거 캐시(1,999 CHF) 재탕 원인 규명
- **원인**: auto_survey_scheduler.bat에 set STEALTH_FAST=1이 설정되어 있었으나, scrape_mediamarkt.py, scrape_interdiscount.py, scrape_digitec.py, scrape_and_sync_hungary.py 내부에서 is_fast 시 실시간 수집을 전면 스킵하고 raw_*.json 로컬 캐시를 그대로 로드하도록 코딩되어 있었음.

### 3. 유럽 11개국 실시간 수집 현황 전수 감사
- **서유럽 5개국(DE, ES, IT, NL, FR)**: Firecrawl Stealth API로 117개 쿼리 100% 실시간 정상 작동 확인.
- **영국(UK), 체코(CZ), 그리스(GR), 호주(AU)**: 실시간 수집 정상 작동 확인.
- **스위스(CH) 및 헝가리(HU)**: 금번 Firecrawl Stealth 엔진 전면 장착 및 캐시 로드 코드 영구 삭제 완료.

### 4. 영구 재발 방지 시스템 개편
- **스위스 3사 & 헝가리 Firecrawl 라이브 수집 표준화**: MediaMarkt CH (65C67: 1599 CHF), Interdiscount CH (65C68: 1699.95 CHF), Digitec CH (110 Samsung / 133 LG), MediaMarkt HU (100개 모델) 전원 실시간 라이브 수집 완료.
- **과거 캐시 재사용 로직 영구 삭제**: 0건 수집 시 과거 캐시를 로드하지 않고 즉시 RuntimeError로 빌드를 중단.
- **Pre-flight Assertion Gate 탑재**: Phase 1 종료 후 24개 데이터셋의 당일 생성 및 최소 수량을 검증하여 위반 시 Hard Halt.
- **스위스 엑셀 및 대시보드 반영**: price tracker_swiss_2026 1006_v1.xlsx 및 public/index.html에 1599 CHF 반영 완료.
