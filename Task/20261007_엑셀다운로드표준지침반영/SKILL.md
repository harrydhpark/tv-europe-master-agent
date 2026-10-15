---
name: gdmi-cpsi-html
description: Swiss 및 타 법인 CPSI 워크북의 시트 데이터를 Stitch 프리미엄 디자인(5대 탭 - 요약, 주간, 월간, 유통별, 인벤토리) 기반의 단일 HTML 대시보드로 변환하는 시각화 스킬. "요약/Dashboard HTML로", "CPSI 대시보드 만들어", "시트를 HTML로", "주간 리포트 HTML" 요청에 사용.
---

# CPSI 요약·Dashboard → HTML 대시보드 (Stitch Premium 5대 탭)

업데이트된 Swiss CPSI 워크북(.xlsb)의 **1번째 시트(요약)** 와 **2번째 시트(Dashboard)** 를
**탭 전환형 단일 HTML**로 변환한다. 요약은 보고서풍 카드로, Dashboard는 모든 표를 그대로 + 차트.

## 입력
작업 폴더에서 최신 Swiss CPSI 워크북을 찾는다(없으면 사용자에게 요청):
- 파일명에 `CPSI` 포함, `.xlsb`. 여러 개면 최신 수정본을 쓰고 무엇을 골랐는지 보고.

## 실행
**통합 공통 엔진(`build_cpsi_html_engine.py`)**을 실행하는 것이 권장 표준입니다 (18개 유럽/CIS 법인 공통 지원, `regions_config.json` 기반 자동 바인딩).

```bash
# 1. 특정 법인 지정 실행 (스위스, 베네룩스 등)
python3 .agents/skills/gdmi-cpsi-html/scripts/build_cpsi_html_engine.py \
  --region Swiss \
  --folder "05. Swiss" \
  --date 2026_0615

# 2. 베네룩스 (대형 법인, 25개 유통 채널)
python3 .agents/skills/gdmi-cpsi-html/scripts/build_cpsi_html_engine.py \
  --region BN \
  --folder "02. BN"

# 3. 임의 법인 자동 해석 (폴더 경로만 지정해도 법인 자동 판별)
python3 .agents/skills/gdmi-cpsi-html/scripts/build_cpsi_html_engine.py \
  --folder "01. AG"
```

> **참고**: 기존의 `build_[법인]_cpsi_html.py` 개별 번들 스크립트도 하위 호환성을 위해 유지되지만, 신규 기능 및 버그픽스는 공통 엔진 `build_cpsi_html_engine.py`에 일원화 적용됩니다.

스크립트가 생성하는 것:
- **Ⅰ. 요약 리포트**: 제목·기준주차 배너 → ■ 섹션별 포인트(번호 + 굵은 제목 + 설명 단락). 리스크/부진 항목은 빨강 강조.
- **Ⅱ. 주간 판매 현황**: GDMi 실적, 예측(FCST), 전년(PY), 계획(Plan) 4대 라인 트렌드 그래프 및 5대 BLU(OLED, QNED, NANO, UHD, FHD/STV) 믹스 바 차트가 7대 채널 누적 합산 기반으로 실시간 동적 렌더링됩니다.
- **Ⅲ. 월간 시뮬레이션**: 월별 GDMi 실적/예측 및 PY 바 차트와 시뮬레이션 표 데이터를 표출합니다.
- **Ⅳ. 유통별 실적**: 7대 유통 거래선(Alltron, Conforama, FNAC, FUST, Interdiscount, MSH, Online) 버튼을 클릭하여 주간 판매 추이, BLU 믹스, 월간 판매량, KPI 테이블이 100% 동적 상호 작용하며 갱신됩니다.
- **Ⅴ. 재고 분석**: 6대 BLU(OLED, QNED, NANO, UHD, FHD/STV) 전체 재고 요약 카드, 재고 관리 대상 모델 LIST 테이블(WOS 8주 초과 붉은색 강조 서식 적용), Critical 모델 핵심 채널 프로그레스 바 영역이 인벤토리 실데이터와 동적 바인딩되어 실시간 노출됩니다.
- 숫자 서식: WOS→`N.N주` (8.0주 초과 붉은색 강조), vs/비율→`%`, 그 외 정수→천단위 구분. 한국어·LG 비즈니스 톤·반응형.
- Chart.js 및 Datalabels 플러그인은 CDN에서 로드하며 데이터는 HTML 내부 인라인 JSON(`DATA_WEEKLY_TREND` 등)으로 오프라인에서도 작동합니다.

## 검증 (필수)
- 5대 탭이 정상적으로 다 로드되고 탭 클릭 시마다 상단 대시보드 타이틀 및 유통 선택 버튼 숨김/노출 분기가 완벽히 작동하는지 확인.
- 브라우저 개발자 도구 콘솔에 `window.onerror` 전역 에러 배너나 JS Runtime Exception이 0건인지 체크.
- `<canvas>` 차트 6개가 이중 바인딩 충돌 없이 정상적으로 다 그려지는지 확인.

## 출력
마지막 줄에 `DASHBOARD_FILE: <html 경로>`를 출력한다.

## 주의
- 시트는 **위치 기준**(1번째=요약, 2번째=Dashboard)으로 읽되, 이름이 다르면 위치를 우선한다.
- Dashboard 시트 값은 캐시값을 읽으므로, 2단계(Swiss CPSI 업데이트 + cpsi 스킬)가 끝나 Excel에서
  저장된 최신 .xlsb를 입력으로 사용해야 최신 주차가 반영된다.
- **Report Week, Reference Basis 및 UPDATED DATE 동적 연동**:
  * 대시보드 상단의 리포트 주차/날짜(Report Week)와 상세 대시보드 내 `Reference Basis` (`__SUBTITLE__`)는 절대 `요약` 시트의 stale한 subtitle 문자열을 그대로 사용하거나 하드코딩해서는 안 됩니다. 반드시 `Dashboard_Weekly` 시트의 B3 셀에서 `Reference: [월/일]W` 정규식 매칭을 통해 실제 데이터 기준 날짜(dt)를 구하고, 이를 기반으로 주차 정보(`W{dt.isocalendar()[1]}`)와 포맷팅된 날짜 표기를 조합하여 **`기준: W[주차] / [월]월 [일]일 (GDMi System 기준)`** 형식으로 동적으로 생성 및 치환하십시오.
  * `UPDATED DATE` (`__DATEKR__`)는 엑셀 데이터의 기준일이 아닌, 빌더 스크립트가 실행되어 배포본이 작성되는 **실제 오늘 일자(배포 시간)**를 `%Y년 %m월 %d일` 형식(`datetime.date.today().strftime(...)`)으로 생성하여 렌더링해야 합니다.
  * 차트 라벨(`labels:`) 또한 하드코딩된 주차를 제거하고 플레이스홀더(`__LABELS_8W__`, `__LABELS_4W__`)를 사용해 엑셀에서 로드된 실제 데이터 라벨 리스트를 기반으로 동적 교체해야 합니다.
- **대시보드 일괄 재생성 시 백업 파일 배제**:
  * `regenerate_all.py` 등 대시보드 재생성 스크립트 작성 시, 폴더 내 `.xlsb` 파일 목록 중 `_BACKUP_` 또는 `_temp_` 패턴이 파일명에 포함된 백업본을 무시하고, 실제 최신화된 활성 원본 워크북(`_Revised_Final.xlsb`)만 찾아 빌드하도록 필터링을 반드시 적용하십시오. 백업본은 업데이트 파이프라인 기동 전 생성되어 과거(stale) 주차 데이터를 품고 있으므로, 이를 오독할 시 주간 데이터 정합성이 붕괴됩니다.
- **주간/월간 탭 디자인 보존 및 수치 정합성**:
  * **Weekly/Monthly 탭 레이아웃 보존**: 미려한 2단 병합 헤더와 차트 좌우 그리드, 카테고리 슬라이서 등 Stitch 프리미엄 레이아웃을 100% 보존하기 위해 `<section>` 전체를 generic table로 치환하지 않습니다. 주간 KPI 테이블은 `<tbody>` 영역에만 `__WEEKLY_KPI_BODY__` 플레이스홀더를 두고 행(`<tr>`/`<td>`) 단위로 포맷팅하여 주입해야 하며, 월간 탭의 모든 테이블과 차트는 자바스크립트가 인라인 JSON(`DATA_MONTHLY_TREND`)을 참조해 클라이언트 단에서 동적 렌더링하도록 템플릿 내부 HTML 구조를 100% 정적으로 완전히 유지해야 합니다.
  * **실적선과 예측선 경계점 연동**: 주간 판매 추이 차트에서 실적(Actuals) 실선과 예측(Forecast) 점선이 만나는 경계 주차에서 선이 끊어지지 않도록, 예측 데이터셋(`FCST`)의 첫 예측 주차 직전 인덱스(실적 데이터의 마지막 값 위치)에 마지막 실적값을 복사하여 연결이 자연스럽게 이어지도록 처리합니다.
  * **BLU Mix 차트의 수량 레이블 표기**: 주간 BLU Mix Trend 차트는 비율 누적 막대 그래프이지만, 막대 안의 레이블은 실제 판매 수량(Units, 대)을 표시해야 합니다. 단순 백분율(예: `63.814`)을 표출하지 말고, 해당 주차의 실제 판매 수량(`DATA_WEEKLY_TREND.GDMi`와 곱하여 역산한 실제 수량)으로 변환한 뒤 천 단위 콤마 포맷(예: `3,617`)으로 렌더링해야 합니다. 비중이 1.5% 미만인 미세 구간은 레이블 겹침 방지를 위해 텍스트를 숨깁니다.
  * **BLU Mix 차트 툴팁 비중 표기 통일**: 주간 판매 현황(`bluMixChart`) 및 유통별 판매 현황(`channelBluMixChart`)의 BLU Sell-out Trend 누적 막대 차트에서 마우스를 막대에 갖다 댔을 때 표시되는 툴팁(Tooltip)의 값은 반드시 소수점 없는 반올림 정수 퍼센트(예: `OLED: 45%`)로 통일하여 표기해야 합니다. 주간 차트는 백분율 데이터를 반올림(`Math.round(v) + '%'`)하고, 유통별 차트는 판매수량 데이터를 기준으로 해당 주차의 전체 BLU 수량의 합산값 대비 비중을 계산(`Math.round((val / sum) * 100) + '%'`)하여 렌더링하도록 템플릿(TPL)을 구성합니다.
  * **글로벌 국가별 총합 키 (`TOTAL_KEY`) 관리**: 각 법인별 대시보드 스크립트 작성 시, 법인 고유의 총합 키(`TOTAL_KEY` - 예: `Benelux TTL`, `Austria TTL`, `Swiss TTL`, `RO TTL`)를 명시적 상수로 선언하여 엑셀 시트 파싱 키 매핑(`cat_map`) 및 자바스크립트 슬라이서 기본값과 연동되도록 해야 합니다.
- **유통 채널 다단 개행 (flex-wrap) 및 비활성 채널 필터링**:
  * 유통 선택 메뉴바 컨테이너에는 `flex flex-wrap items-center gap-2 py-1` 등을 지정하여 화면 폭을 넘을 경우 여러 줄로 개행되도록 해야 하며, 4주 평균 판매 실적(`4W Avg`)이 `0`인 유통 채널은 동적으로 필터링하여 제외해야 합니다.
  * 제외된 유통 채널이 초기 로드 함수(`updateChannelView`)에서 호출되어 JS 에러가 나지 않도록, 필터링 후 생존한 첫 번째 유효 채널을 `__DEFAULT_CHANNEL__` 플레이스홀더를 사용해 자바스크립트에 동적으로 주입해야 합니다.
- **대용량 시트 파싱 탐색 행수 확장 및 방어적 형변환**:
  * 카테고리와 거래선이 많은 베네룩스 등 대형 법인의 경우 `Master_PD+KAM` 시트가 3,000행을 초과하므로, `build_channel` 내 `grid` 파싱 범위(`maxr`)를 최소 `5000` 이상으로 확장하여 데이터 누락을 원천 차단하십시오.
  * 데이터 파싱 시 헤더 텍스트(예: `Ch.Inv (개)`) 등이 숫자로 강제 형변환될 때 발생하는 `ValueError`로 인한 빌드 크래시를 방지하기 위해 `try...except ValueError` 구문으로 감싸 방어적으로 처리해야 합니다.
- **법인별 스크립트 복제 시 라벨 및 변수 초기화 일관성**:
  * 타 법인의 빌더 스크립트를 복제하여 신규 법인 스크립트를 작성할 때, HTML 내부의 타이틀 및 포털 라벨 명칭에 이전 법인의 흔적(예: `LGE FS`, `FS C-PSI` 등 공백이나 대소문자가 섞인 문자열)이 남지 않도록 파일 전체의 문자열을 전수 검사하여 정교하게 치환 및 최적화하십시오.
  * 중복 유통망 버튼 렌더링 버그를 원천 차단하기 위해, 복제 스크립트 작성 시 채널 누적 변수인 `valid_channels`가 전체 목록으로 기선언된 채 루프를 도는 일이 없도록 루프 진입 전 반드시 빈 리스트(`valid_channels = []`)로 명시적 초기화하여 적용해야 합니다.
  * 엑셀 잔존 텍스트(예: `Italy TTL`, `Austria TTL`)에 의한 차트 데이터 맵핑 예외를 막기 위해, `rows[r].get(1)` 파싱부에서 `if blu in ("Austria TTL", "Italy TTL"): blu = TOTAL_KEY` 등 방어적 맵핑 코드를 삽입하십시오.
  * **HTML 템플릿 중복 및 태그 스코프 누출 방지**: 법인별 대시보드 빌더 스크립트의 `TPL` 문자열을 수정하거나 복제할 때, 특정 탭 섹션(예: `<section id="tab_channel">`)이 실수로 두 번 복사되거나 탭 버튼 등의 요소가 개별 탭 섹션 바깥에 누출되지 않도록 구조적 무결성을 전수 검사해야 합니다. 탭 영역 외부로 노출된 정적 요소는 모든 탭 화면에서 중복 노출되는 중대한 레이아웃 버그를 유발합니다.
- **5대 탭 서브 네비게이션 및 iframe 2중 사이드바 차단 (SOP/CORS 우회)**:
  * 대시보드 포털(`index.html`)의 왼쪽 사이드바 국가명 아래에는 2대 탭 대신 5대 세부 탭 메뉴(`Executive Summary`, `주간 판매 현황`, `월간 판매 현황`, `유통별 판매 현황`, `재고 관리 대상 모델`)가 전부 띄워져야 하며, 클릭 시 오른쪽 공간에 해당 내용이 바로 연계 표출되어야 합니다.
  * 부모 포털과 iframe 내부 리포트의 사이드 메뉴 중복 노출을 차단하기 위해, iframe 내부의 사이드바(`aside`)는 반드시 숨겨지고 `main` 영역 마진이 `0`으로 확장되어야 합니다.
  * 로컬 `file://` 프로토콜 실행 환경에서 브라우저의 동일출처정책(SOP/CORS) 제약으로 인해 부모 JS가 iframe DOM에 직접 접근하는 행위가 제한되는 현상을 원천 방지하기 위해, iframe 내부 HTML 템플릿 코드에 자체적인 iframe 여부 판별 스크립트(`window.self !== window.top`)를 삽입하여 자신의 사이드바를 DOM 레벨에서 직접 숨기도록 처리하고, `hashchange` 이벤트 리스너 및 로드 타임 hash 처리를 구현하여 URL hash(예: `#tab_weekly`)를 통해 외부에서 탭 전환 명령을 안전하게 수신하도록 구성합니다.
  * **해시 이동 시 브라우저 자동 스크롤 방지 및 상단 리셋**: iframe URL의 해시값 변경(예: `#tab_weekly`)에 의한 브라우저의 기본 자동 스크롤(Auto-scroll to ID) 현상으로 인해 타이틀 배너와 기준 주차 등의 상단 정보가 뷰포트 위쪽으로 가려져 중간부터 보이는 버그를 막아야 합니다. 이를 위해 iframe 내부의 해시 전환 수신 스크립트(`handleHashTab`) 내에 `window.scrollTo(0, 0)` 호출을 삽입하고, 비동기 스크롤 타이밍 보정을 위해 즉각적인 스크롤 리셋과 `setTimeout` 기반의 다단계(20ms, 100ms) 추가 스크롤 최상단 리셋 처리를 강제 연동해야 합니다.
  * 포털 홈 카드 클릭 시, 요약 리포트는 `Ⅰ. Executive Summary` 탭으로, 상세 Dashboard는 `Ⅱ. 주간 판매 현황` 탭으로 100% 대응하여 이동 및 활성화되어야 합니다.
  * **포털 내 캐시 버스터 최적화 (동일 국가 탭 전환 시 새로고침 방지)**: 포털 메인(`index.html`)에서 최신 배포 리포트를 강제 수신하기 위해 도입하는 캐시 버스터(예: `cb=Date.now()`)는 오직 국가가 변경되는 시점(최초 로드 시, `currentPath !== path`)에만 신규 타임스탬프를 부여해야 합니다. 동일 국가 내에서 상세 탭을 이동할 때는 기존 URL 매개변수를 완전히 보존한 채 해시값(`#tab_weekly` 등)만 갱신하여, 아이프레임이 전체 재로딩(Reload)되는 병목과 탭 상태 초기화 오동작을 완벽히 차단해야 합니다.
  * **스위스 법인 유통 채널 접두사 (`CH_`) 매핑 규칙**: 스위스 법인 대시보드 빌더(`build_swiss_cpsi_html.py`) 작성/수정 시, `Master_PD+KAM` 시트의 유통 채널명은 반드시 `CH_` 접두사가 포함된 형태(예: `CH_Alltron`, `CH_FNAC` 등)로 엑셀에 기록되어 있습니다. 따라서 파이썬 빌더 스크립트에서 엑셀 키 매핑을 시도할 때 `ch_key_prefix` 변수를 반드시 `f"CH_{ch}"` 형태로 바인딩하여 데이터 조회를 수행해야 하며, 최종 생성되는 인라인 JSON(`DATA_CHANNEL`) 키값은 접두사를 제외한 원래 채널명(`ch` - 예: `Alltron`)으로 저장하여 프론트엔드 버튼 클릭 연동 시 에러(Cannot read properties of undefined (reading 'weekly'))를 방지해야 합니다.
      * **포털 메인 홈 (`index.html`) 문구 및 표기 규칙 (Portal Home Text & Labeling Rules)**:
        - 포털 메인 홈(`index.html`)의 웰컴 배너 소개 문구는 반드시 `"본 포털은 유럽 전체 지점/법인의 주간 Sell-out 실적 흐름 및 채널 재고/WOS 현황을 일원화하여 모니터링하기 위한 시스템입니다. 아래 대시보드 목록에서 국가를 선택하시면 상세 분석 데이터와 탭 전환형 인터랙티브 차트를 확인하실 수 있습니다"` 형식을 준수해야 하며, `"16개 지역/법인"` 명칭을 사용하지 마십시오.
        - 지점 요약 카드 영역의 메인 타이틀은 `"지점/법인별 주간 실판매 실적 및 재고 요약"`으로 명시하며, `"16대 지역별"` 명칭을 지양하십시오.
        - 각 요약 카드의 전년비 성장률 수치(YoY)가 양수일 때는 플러스 기호가 중복되지 않도록 반드시 `"YoY +00.0%"` 형태로 기호 `+`를 1개만 사용하여 렌더링되도록 확인 및 보정하십시오 (`YoY ++` 중복 표기 금지).
  * **유통 채널 분석의 기준 주차 동적 추적 (Dynamic Week Reference Alignment)**: 유통 채널 분석 탭(`tab_channel`)의 주차별 데이터(`weekly_indices`)를 읽어올 때 하드코딩된 열 인덱스(예: `range(32, 40)`)를 절대 사용하지 마십시오. 반드시 `Dashboard_Weekly` 시트의 헤더 영역에서 `Reference: [날짜/주차]` 정규식 매칭을 통해 현재 리포트의 기준 날짜 문자열을 실시간 파싱하고, `Master_PD+KAM` 시트의 헤더 행(6행)에서 해당 날짜와 매칭되는 열 인덱스를 동적으로 찾아 주차 범위를 구성해야 합니다. 이는 주간 탭(`tab_weekly`)과 유통별 탭(`tab_channel`) 간의 수치 불일치 및 주차 밀림 버그를 차단하는 필수 규칙입니다.
  * **포털 메인 홈(`index.html`) 업데이트 안전성 및 레이아웃 무결성 규칙 (Portal Update Safety & Layout Integrity)**:
    - **사이드바-그리드 카드 주석 검색 충돌 방지**: 포털 메인 갱신 스크립트 작성 시, 사이드바 메뉴 영역과 메인 그리드 카드 영역에 중복 사용되는 동일 주석 패턴(`<!-- [국가명] -->`)으로 단순 `find` 및 치환을 수행해서는 안 됩니다. 반드시 `<!-- Sidebar Navigation -->`과 `<!-- Main Content Area -->` 같은 랜드마크 주석을 우선 검색하여 탐색 영역을 분할한 후 파싱을 진행하십시오.
    - **치환 탐색 범위 닫는 태그 유실 방지**: 국가 카드를 치환할 때, 시작 및 끝 탐색 인덱스를 잘못 설정하여 카드 외부의 그리드 컨테이너(`</div>`) 및 홈 뷰 컨테이너(`</div>`) 닫는 태그가 삭제되지 않도록 해야 합니다. 닫는 태그 유실 시 `report-view-container`가 자식 노드로 중첩되어 iframe 로드 시 우측 공간이 백화(0x0 픽셀)되는 치명적인 UI 레이아웃 붕괴가 발생합니다.
    - **Tailwind `.hidden` 클래스 간섭 배제**: Iframe을 로드하는 컨테이너(`report-view-container`)의 초기 상태 설정 시, Tailwind CSS의 `.hidden` 클래스를 직접 부여하지 마십시오. Tailwind의 `.hidden`은 `display: none !important;`를 내장하고 있으므로 자바스크립트의 `style.display = 'block'` 인라인 스타일 지정을 덮어쓰고 무효화합니다. 대신 HTML 인라인 스타일인 `style="display: none;"`을 지정하여 뷰 토글이 정상적으로 동작하도록 구성하십시오.
  * **주간 업데이트 완료 후 백업 파일 및 과거 대시보드 정리 규칙**:
    - HTML 대시보드 생성 후, 해당 법인 폴더 내 신규 생성된 대시보드 HTML 파일(`*_CPSI_Summary_Dashboard_[YYYY_MMDD].html`)을 제외한 모든 과거 HTML 파일(예: `*_2026_0722.html`) 및 엑셀 백업 파일(`*_BACKUP_*.xlsb`)을 일괄 정리/삭제하십시오.
    - 메인 포털 `index.html` 내 해당 법인의 5개 탭 링크 URL이 기본 에이리어스 HTML 경로(`./[폴더]/[법인]_CPSI_Summary_Dashboard.html`)로 올바르게 업데이트되었는지 검증하십시오.
  * **포털 메인(`index.html`) Executive Summary 뷰 및 재고 건전성 기준 표준**:
    - **사이드바 메뉴 순서**: `대시보드 포털 홈` ➡️ 최상단 `Executive Summary` 버튼(오스트리아 바로 위) ➡️ 18대 Regional Dashboards (01. Austria ~ 15. Sweden ➡️ **16. United Kingdom (스웨덴 바로 다음)** ➡️ 17. Russia ➡️ 18. AK). **우크라이나(UR)는 완전 제외**.
    - **Executive Summary 종합 뷰**:
      * 상단 테이블: `No`, `지점/법인명`, `기준 주차/일자`, `주간 실판매(YoY)`, `4주 평균 실판매(YoY)`, `채널 재고(전년비 증감 k대)`, `재고 주수(WOS)`, `재고 건전성`.
      * 하단 카드: **'주요 시사점 및 현황 분석'** 3대 핵심 카드(`01. 실판매 성장세`, `02. 재고 증감 흐름`, `03. 건전성 & 관리`) 필수 렌더링.
    - **재고 건전성 (Health Criteria) 평가 기준**:
      * **✓ Healthy**: 재고 주수 **8.0주 이하** (`WOS ≤ 8.0주`, 녹색 뱃지)
      * **⚠ Warning**: 재고 주수 **8.0주 초과 ~ 10.0주 미만** (`8.0주 < WOS < 10.0주`, 주황 뱃지)
      * **⛔ Critical**: 재고 주수 **10.0주 이상** (`WOS ≥ 10.0주`, 적색 뱃지)
  * **포털 메인(`index.html`) 뷰 컨테이너 구조 및 Flex 높이 분배 무결성 규칙 (Container Layout Integrity)**:
    - `index.html`의 메인 컨텐츠 영역(`main`)은 `ml-72 flex-1 flex flex-col h-screen overflow-hidden`으로 뷰포트에 완벽히 고정되어야 합니다.
    - `main` 태그의 직계 자식으로는 상단 헤더(`header`)와 3대 메인 뷰 컨테이너(`home-view-container`, `exec-summary-container`, `report-view-container`)가 **단일 레벨의 형제(Flat Siblings)**로 직접 배치되어야 합니다.
    - 중간에 `main-view-container`와 같은 불필요한 `flex-1` 래퍼 `<div>`가 잘못 닫혀 형제 요소로 남아있을 경우, 리포트 뷰 상태에서도 빈 공간(376.5px)을 상단에서 차지하여 **상단 거대 공백 및 iframe 아래 밀림/내용 잘림(Top: 456px) 버그**를 유발하므로, 절대 불필요한 래퍼 태그를 중복 삽입하거나 태그 스코프를 잘못 닫지 않도록 구조적 무결성을 유지하십시오.
    - 뷰 토글 시에는 비활성 컨테이너에 `style.display = 'none'`을, 활성 컨테이너에 `style.display = 'block'`(또는 `flex`)을 부여하고 부모 스크롤을 항상 `scrollTop = 0`으로 즉시 리셋해야 합니다.
  * **URL 해시 앵커 자동 스크롤 차단 및 `#tab=...` 안전 규격 준수 (Hash Anchor Protection)**:
    - 메인 포털에서 iframe으로 특정 탭을 지정하여 로드할 때, `#tab_weekly`와 같이 DOM 요소 ID와 1:1 일치하는 해시를 부여하면 브라우저 내장 렌더러가 `<section id="tab_weekly">` 위치로 강제 스크롤 점프를 수행하여 상단 타이틀 및 기준일 헤더(~250px)가 뷰포트 위로 밀려 사라집니다.
    - 따라서 URL 해시 파라미터는 반드시 **`#tab=weekly`**, **`#tab=monthly`**, **`#tab=channel`**, **`#tab=inventory`**, **`#tab=summary`** 규격을 준수해야 합니다.
    - 각 법인별 대시보드 HTML 및 빌더 템플릿(TPL)의 `handleHashTab` 함수는 `tabId.startsWith('tab=')` 분기를 통해 `tab_` 접두사로 안전하게 변환한 후 `switchTab()`을 구동하고, 4단계 지연 `window.scrollTo(0, 0)`(0ms, 20ms, 100ms, 300ms)을 호출하여 항상 최상단 타이틀 뷰를 100% 보장해야 합니다.
  * **웹 배포 및 라이브 검증 안전 수칙 (Windows PowerShell Anti-Hang)**:
    - 대시보드 빌드 및 Firebase 배포 후 HTTP 상태 검증 시 Windows PowerShell 환경의 `curl` 앨리어스 사용을 금지합니다 (`MissingArgument` 오류 유발).
    - 반드시 명시적 확장자를 부여한 **`curl.exe -s -I <url>`**를 호출하거나, `Invoke-WebRequest` 사용 시 **`-UseBasicParsing -TimeoutSec 10`**을 필수로 지정하여 레거시 IE DOM 엔진 초기화로 인한 프로세스 무한 정체(Hang)를 원천 차단하십시오.
  * **대시보드 원본 엑셀(.xlsb) 다운로드 버튼 및 Firebase 호스팅 표준**:
    - **상단 헤더 고정 버튼**: Stitch 5-Tab 대시보드 상단 Page Header 영역(`__TITLE__` 우측)에 에메랄드 그린(`bg-emerald-600 hover:bg-emerald-700 text-white`) 테마의 `Excel 다운로드 (.xlsb)` 버튼을 배치합니다. `Executive Summary`뿐 아니라 주간/월간/유통별/재고 등 전 탭에서 상시 노출되도록 상단 공통 헤더에 반응형(`flex-col md:flex-row md:items-center justify-between`)으로 고정합니다.
    - **통합 빌더 엔진(`build_cpsi_html_engine.py`) 자동 바인딩**: 스크립트 실행 시 대상 워크북의 파일명(`os.path.basename(target_xlsb)`)을 추출하여 `__XLSB_FILENAME__` 플레이스홀더를 통해 `href` 및 `download` 속성에 18개 권역 고유의 `*_CPSI_Revised_Final.xlsb` 파일명이 1:1 자동 바인딩되도록 템플릿(TPL)을 유지합니다.
    - **Firebase Hosting 바이너리(.xlsb) 배포 및 Anti-404**:
      - Firebase CLI `firebase.json` ignore 파서는 negate(`!important.txt`) 패턴을 미지원하므로 `**/*.xlsb` 전체를 ignore에 넣으면 다운로드 링크가 404로 깨집니다.
      - 반드시 `**/*_BACKUP_*`, `**/*_temp_*`, `**/~$*`만 명시적으로 ignore하여 `*_CPSI_Revised_Final.xlsb` 배포를 허용하십시오.
      - `firebase.json` headers에 `**/*.xlsb`에 대한 `Content-Type: application/vnd.ms-excel.sheet.binary.macroEnabled.12`를 필수로 등록하여 브라우저 다운로드 연동을 보장하십시오.






