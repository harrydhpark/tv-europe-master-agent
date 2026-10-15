# Project Guidelines (GDMI Weekly Sellout Analysis)

> 글로벌 AGENTS.md에 정의된 규칙(셀 루프 금지, pandas overlay, GitLab 인증 우회)은 본 문서에서 반복하지 않습니다.
> 과거 버그 포스트모템은 `POSTMORTEM.md`에 보관되어 있습니다.

## 1. Excel COM 자동화 규칙

1. **계산 모드 제어**: 수식이 포함된 원천 워크북에서 값을 읽을 때 계산 모드를 `Manual`로 변경하지 마십시오. 반드시 `Automatic` 상태에서 수식 평가값을 메모리에 읽은 뒤, 쓰기 시점에서만 `Manual`로 전환하십시오.

2. **대용량 xlsb 저장 표준**: `save_and_close.vbs`를 통한 VBScript 분리 저장이 프로덕션 표준입니다 (18개국 매주 검증 완료). 비바이너리(`.xlsx`) 포맷에서는 `SaveCopyAs()` → Close → Replace 패턴도 대안으로 허용됩니다.

3. **FillDown 금지**: `FillDown()`을 지양하고 대상 열 범위에 직접 수식 문자열(Formula)을 할당하십시오.

4. **A~J열 값 복사 의무화**: `Revised_Final.xlsb`의 `GDMI System_Raw` 시트 A~J열은 static values로 관리됩니다. 원천(`Y26 Raw Data`)의 수식 평가 결과값을 값 붙여넣기(Paste Special as Values)로 주입해야 하며, `FillDown`/`AutoFill`은 절대 금지합니다.

5. **대용량 xlsx 동기화 시 COM 교착 방지**: `00. Raw Data` → `Y26 Raw Data` 복사 시 openpyxl 메모리 기반 고속 스크립트를 사용하십시오. `wb.Save()` 직접 호출은 STA 재계산 루프로 무한 hang을 유발합니다.

## 2. HTML 보고서 생성 표준

1. **스킬 및 레이아웃**: `gdmi-cpsi-html` 스킬을 사용하여 Stitch 프리미엄 5대 탭(Ⅰ. Executive Summary, Ⅱ. 주간, Ⅲ. 월간, Ⅳ. 유통별, Ⅴ. 재고 관리) 레이아웃을 100% 준수합니다.

2. **데이터 동적 연동**:
   - 수치 데이터의 TPL 내 하드코딩 절대 금지 — 동적 JSON 플레이스홀더로 연동합니다.
   - `Report Week` / `Reference Basis`: `Dashboard_Weekly!B3`에서 정규식 매칭 → `기준: W[주차] / [월]월 [일]일 (GDMi System 기준)` 형식 동적 생성.
   - `UPDATED DATE`: 빌더 실행 시점의 `datetime.date.today()` 사용.
   - 차트 라벨: `__LABELS_8W__`, `__LABELS_4W__` 플레이스홀더로 동적 교체.
   - 백업 파일(`_BACKUP_`, `_temp_`) 배제, `_Revised_Final.xlsb`만 빌드 대상.

3. **Chart.js 규칙**:
   - 캔버스 중복 점유 방지: `if (document.getElementById(...))` 가드 필수.
   - 실적/예측 경계점: FCST 첫 인덱스에 마지막 실적값 복사하여 선 연결.
   - BLU Mix 레이블: 실제 판매 수량(천 단위 콤마), 비중 1.5% 미만은 숨김.
   - BLU Mix 툴팁: 소수점 없는 반올림 정수 퍼센트 통일 (`Math.round(v) + '%'`).

4. **Weekly/Monthly 탭 보존**: `<section>` 전체를 generic table로 치환 금지. 주간 KPI는 `__WEEKLY_KPI_BODY__` 국소 플레이스홀더, 월간은 `DATA_MONTHLY_TREND` JSON으로 동적 렌더링.

5. **유통 채널 규칙**:
   - `TOTAL_KEY`: 법인 고유 총합 키를 명시적 상수로 선언.
   - 채널 버튼: `flex flex-wrap` 다단 개행, 4W Avg=0인 채널은 필터링 제외, `__DEFAULT_CHANNEL__` 동적 주입.
   - 스위스 `CH_` 접두사: 엑셀 조회 시 `f"CH_{ch}"`, JSON 키는 접두사 제거.
   - 파싱 행수: 대형 법인(BN 등) `maxr ≥ 5000`, `try...except ValueError` 방어적 형변환.
   - 기준 주차 동적 추적: 하드코딩 열 인덱스 절대 금지, 헤더 정규식 매칭으로 동적 열 탐색.

## 3. 포털 iframe 연동 규칙

1. **SOP/CORS 우회**: iframe 내부 HTML에 `window.self !== window.top` 판별 스크립트 삽입 → 자체 사이드바 숨김 + `hashchange` 리스너로 외부 탭 전환 수신.

2. **해시 규격**: `#tab=weekly`, `#tab=monthly` 등 `tab=` 접두사 사용 (DOM ID와 1:1 매칭 방지). `handleHashTab`에서 4단계 `scrollTo(0,0)` (0/20/100/300ms).

3. **캐시 버스터**: 국가 변경 시에만 신규 `cb=Date.now()` 부여, 동일 국가 탭 전환 시 해시만 갱신.

4. **탭 전환**: 채널 선택 메뉴 숨김/노출 분기, 대시보드 타이틀·Indicator·Header 동적 바인딩 보장.

## 4. 포털 메인 (`index.html`) 규칙

1. **문구 표기**:
   - 웰컴 배너: `"유럽 전체 지점/법인의 주간 Sell-out..."` 형식 준수, `"16개 지역/법인"` 미사용.
   - 카드 영역 타이틀: `"지점/법인별 주간 실판매 실적 및 재고 요약"`.
   - YoY 양수 시 `+` 기호 1개만 사용 (중복 금지).

2. **컨테이너 구조**: `main` 태그의 직계 자식 = `header` + 3대 뷰 컨테이너(home, exec-summary, report)가 플랫 형제로 배치. 불필요한 래퍼 `<div>` 중첩 금지. 뷰 토글은 `style.display` 사용 (Tailwind `.hidden` 클래스 금지).

3. **갱신 스크립트 파싱**: 사이드바·메인 그리드에 동일 주석 패턴 사용 시 랜드마크 주석(`<!-- Sidebar Navigation -->`, `<!-- Main Content Area -->`)으로 영역 분할 후 파싱. 닫는 태그 유실 방지 필수.

4. **국가 목록**: UK는 Sweden 다음 순서. Ukraine(UR)은 완전 제외 — 18개 권역 체제.

5. **Executive Summary 뷰**: 사이드바 최상단에 Executive Summary 버튼 배치. 테이블: No, 법인명, 기준주차, 주간/4W 실판매(YoY), 채널재고, WOS, 건전성. 하단 3대 시사점 카드 상시 렌더링.

6. **재고 건전성 기준**: WOS ≤ 8.0 → ✓ Healthy(녹), 8.0 < WOS < 10.0 → ⚠ Warning(주황), WOS ≥ 10.0 → ⛔ Critical(적).

## 5. 주간 업데이트 SOP (6단계)

1. **원천 및 값 복사**: `00. Raw Data` → `Y26 Raw Data` → `Revised_Final.xlsb` GDMI System_Raw에 A:DQ 값 붙여넣기 + E1 주차 입력.
2. **정합성 검증 및 롤백**: Summary Y15:Y40(4W Avg > 0)인데 V15:V40(당주) = 0이면 E1을 1주차 롤백. 비대화형 환경에서는 자동 승인(y).
3. **Master_PD 실적 변환**: `run_apply_masterpd.py`로 시뮬레이션 → 실적 SUMIFS 변환.
4. **대시보드 4시트 리빌드**: `run_dashboard.py`로 Dashboard_Inventory 재생성.
5. **HTML 빌드 및 포털 연동**: `build_[법인]_cpsi_html.py` 실행 → 에이리어스 파일 복사 → `index.html` 링크 고정.
6. **뒷정리**: 백업(`*_BACKUP_*`, `*_temp_*`), 날짜 HTML 전수 삭제. Folder Keepers: `Revised_Final.xlsb`, `Y26 Raw Data`, 에이리어스 HTML 1개.

> **Summary C6 연결 필수 검증**: E1 입력 시 `Summary!C6 = ='GDMI System_Raw'!E1` 수식 연결 확인 및 복원. C6 하드코딩 시 피벗이 이전 주차에 고정되어 누락이 은폐됩니다.

> **업데이트 전 주차 확인 의무**: 에이전트가 임의로 기본값 주차를 사용하여 즉시 기동하는 것은 금지. 반드시 사용자에게 기준 주차를 확인받아야 합니다.

## 6. 특수/무판매 법인 규칙

- `ZERO_SALES_CORPS`: 러시아(RA), 카자흐스탄(AK).
- **과반수 합의 주차(majority_week) 산출 및 동률 우선순위**:
  - 활성 16개 법인 처리 후 확정된 주차 빈도 집계 시 동률(예: W39 8개 vs W38 8개)이 발생할 경우, 임의로 하위 주차를 선택하지 않고 **사용자 지정 목표 주차(`target_week`) 또는 최신 주차(`max`)를 최우선으로 채택**합니다.
- **이중 롤백(Double Rollback) 원천 차단 (`--force` 강제 동기화)**:
  - `majority_week`는 이미 유럽 활성 법인들의 주차 검증과 롤백이 반영된 '최종 합의 주차'입니다.
  - 따라서 Phase 2에서 `ZERO_SALES_CORPS`를 업데이트할 때는 반드시 **`--force` 옵션을 인수로 전달**하여, 카자흐스탄(AK)의 인접 CIS 수출 유통(KG, MNG, TJ, TM, UZ 등)의 주간 실적 미입력으로 인한 **2차 추가 롤백(Double Rollback, 예: W39→W38→W37, 보고주차 W36 왜곡)을 영구적으로 방지**해야 합니다.
  - 카자흐스탄(AK)은 1회 롤백 시 반드시 **E1 = 38 (보고 주차 W37)**로 유지 관리되어야 합니다.

## 7. 법인별 스크립트 복제 규칙

- 타 법인 스크립트 복제 시 타이틀·헤더·포털명에서 이전 법인 명칭 완전 교체 (대소문자·공백 조합 전수 조사).
- `valid_channels = []` 루프 전 명시적 초기화 (중복 버튼 방지).
- `TOTAL_KEY` 매핑 불일치 방어: `if blu in ("Austria TTL", "Italy TTL"): blu = TOTAL_KEY`.
- TPL `<section>` 중복 복사 및 탭 버튼 스코프 누출 금지 — 구조적 무결성 전수 검사.

## 8. 멀티 에이전트 시스템 (MAS) 운영 규칙

본 프로젝트는 데이터 관리(ETL/COM)와 결과 분석(인사이트)의 완전 분리를 위해 **4-티어 멀티 에이전트 시스템**으로 운영됩니다:

1. **에이전트 역할 분담**:
   - **Orchestrator Agent**: 파이프라인 총괄, 주차 확인, 실시간 마일스톤 상태 보드 렌더링 (`run_multi_agent_pipeline.py`).
   - **Data Management Agent**: Raw Sync, Excel COM, 롤백 검증, 무정지 분리 저장 및 정규화 데이터 계약(`export_normalized_metrics.py`) 추출.
   - **Insight Analytics Agent**: COM-Free 고속 환경에서 18개 법인 카드별 심층 진단문 및 유럽 3대 전략 시사점 카드 도출 (`generate_macro_insights.py`).
   - **Web UI & Presentation Agent**: Stitch 5-Tab HTML 대시보드 컴파일, `index.html` 갱신 및 파일/링크 무결성 자체 검증 (`update_index_portal.py`).

2. **정규화 데이터 계약(Normalized Data Contract) 준수**:
   - 데이터 에이전트와 분석/UI 에이전트 간의 데이터 핸드오프는 `_data/metrics_[CORP].json` 및 `_data/europe_summary.json` 표준 JSON 인터페이스를 필수 매개로 합니다.
   - 분석 및 UI 렌더링 단계에서는 Excel COM을 절대 호출하지 않고 경량 JSON 데이터셋만을 소비하여 고속 무결점 실행을 보장합니다.

## 9. 웹 배포 및 HTTP 검증 안전 수칙 (PowerShell Anti-Hang)

1. **PowerShell `curl` 앨리어스 사용 절대 금지**:
   - Windows PowerShell 환경에서 `curl`은 기본적으로 `Invoke-WebRequest` cmdlet으로 앨리어싱되어 있습니다.
   - `curl -s -I <url>` 등 네이티브 curl 플래그 호출 시 PowerShell 매개변수 바인딩 에러(`ParameterBindingException: MissingArgument`)가 발생합니다.
   - 반드시 명시적 확장자를 포함한 **`curl.exe`**를 호출하십시오:
     ```powershell
     curl.exe -s -I "https://gdmi-weekly-dashboard.web.app"
     ```

2. **`Invoke-WebRequest` IE MSHTML 엔진 교착 방지**:
   - PowerShell 5.1에서 `Invoke-WebRequest`를 옵션 없이 실행하면 백그라운드에서 Internet Explorer MSHTML 엔진을 초기화하려고 시도하며 프로세스가 무한 정체(Hang)됩니다.
   - PowerShell cmdlet을 사용할 때는 반드시 **`-UseBasicParsing`**과 **`-TimeoutSec`**을 명시하십시오:
     ```powershell
     (Invoke-WebRequest -Uri "https://gdmi-weekly-dashboard.web.app" -UseBasicParsing -TimeoutSec 10).StatusCode
     ```

3. **배포 후 라이브 검증 원칙**:
   - Firebase Hosting 배포(`firebase deploy --only hosting`) 완료 로그(`Deploy complete!`) 확인 즉시 배포 성공으로 판정하며, 불필요한 장기 백그라운드 HTTP 폴링 검증을 지양합니다.

## 10. 대시보드 원본 엑셀(.xlsb) 다운로드 및 Firebase 호스팅 표준

1. **상단 헤더 상시 고정 다운로드 버튼**:
   - Stitch 5-Tab HTML 대시보드의 `Page Header` 영역(`__TITLE__` 우측)에 에메랄드 그린(`bg-emerald-600 hover:bg-emerald-700 text-white`) 테마의 `Excel 다운로드 (.xlsb)` 버튼을 배치합니다.
   - `Executive Summary`뿐 아니라 주간/월간/유통별/재고 관리 등 **어떤 탭에서도 상시 노출**되도록 상단 공통 헤더에 유지하며, 반응형(`flex-col md:flex-row md:items-center justify-between`)으로 구현합니다.
   - 통합 빌더 엔진(`build_cpsi_html_engine.py`)에서 `os.path.basename(target_xlsb)`를 추출하여 `__XLSB_FILENAME__` 플레이스홀더를 통해 `href` 및 `download` 속성에 18개 권역 고유의 `*_CPSI_Revised_Final.xlsb` 파일명을 1:1 자동 바인딩합니다.

2. **Firebase Hosting 바이너리(.xlsb) 배포 및 Anti-404 규칙**:
   - **Negative Glob 미지원 주의**: Firebase CLI의 `firebase.json` `ignore` 파서는 negate(`!important.txt`) 패턴을 공식 지원하지 않습니다. `**/*.xlsb` 전체를 ignore 목록에 넣으면 negate 예외를 추가하더라도 파일이 누락되어 웹 다운로드 시 `404 Not Found`가 발생합니다.
   - **올바른 Ignore 패턴**: `**/*.xlsb` 전체를 ignore하지 말고, 임시/백업 패턴(`**/*_BACKUP_*`, `**/*_temp_*`, `**/~$*`)만 명시적으로 ignore하여 원본 배포 대상인 `*_CPSI_Revised_Final.xlsb`가 정상 업로드되도록 관리하십시오.
   - **MIME Content-Type 헤더 매핑**: 브라우저에서 바이너리 매크로 엑셀 파일이 즉시 다운로드 파일로 인식되도록 `firebase.json` headers에 `**/*.xlsb` 대상 `Content-Type: application/vnd.ms-excel.sheet.binary.macroEnabled.12`를 필수 등록하십시오.


