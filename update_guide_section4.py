# -*- coding: utf-8 -*-
new_tab_db = '''<section id="tab-db" class="tab-content space-y-8">
                <!-- Section Header -->
                <div class="border-b border-slate-200 pb-5">
                    <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded bg-teal-50 text-teal-800 text-xs font-semibold mb-2 border border-teal-200">
                        <span class="material-symbols-outlined text-sm">database</span>
                        <span>Enterprise High-Speed Analytical Pipeline & Core Database</span>
                    </div>
                    <h2 class="text-2xl font-bold text-primary tracking-tight font-headline">4. DB 구조 & 자동 동기화 파이프라인</h2>
                    <p class="text-sm text-text-muted mt-1">
                        어려운 데이터베이스 용어 없이 누구나 쉽게 이해하는 <strong>AXIS 주간 엑셀 자동 동기화 & 초고속 데이터 라이프사이클</strong>
                    </p>
                </div>

                <!-- 1. Easy Metaphor Intro: 누구나 이해하는 일상 속 비유 -->
                <div class="bg-gradient-to-r from-slate-900 via-primary to-slate-800 rounded-2xl p-6 text-white shadow-md relative overflow-hidden">
                    <div class="relative z-10 space-y-4">
                        <div class="flex items-center gap-2.5 text-teal-300 font-semibold text-xs tracking-wider uppercase">
                            <span class="material-symbols-outlined text-base">lightbulb</span>
                            <span>쉬운 비유로 한눈에 이해하는 시스템 원리</span>
                        </div>
                        <h3 class="text-xl font-bold font-headline leading-snug">
                            "각 팀의 엑셀 장부를 폴더에 넣기만 하면, 24시간 센서가 감지해 1초 만에 중앙 디지털 금고에 정산합니다."
                        </h3>
                        <p class="text-xs text-slate-300 leading-relaxed max-w-3xl">
                            기존에는 수십 MB 크기의 엑셀 파일을 일일이 열고, 복사하고, 취합하느라 컴퓨터가 멈추고 많은 시간이 걸렸습니다. AXIS는 담당자가 평소처럼 엑셀 파일을 저장하는 즉시, 보이지 않는 무인 파이프라인이 즉각 작동하여 데이터를 안전하게 정산하고 웹 화면에 0.1초 만에 띄워줍니다.
                        </p>
                        
                        <!-- 4 Metaphor Grid -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-2">
                            <div class="bg-white/10 backdrop-blur-sm p-3.5 rounded-xl border border-white/10 space-y-1.5">
                                <div class="flex items-center gap-2 text-teal-300 font-bold text-xs">
                                    <span class="material-symbols-outlined text-lg">folder_open</span>
                                    <span>주간 업무 장부</span>
                                </div>
                                <div class="text-[11px] text-slate-200 font-medium">원천 엑셀 파일들</div>
                                <p class="text-[10.5px] text-slate-300 leading-normal">
                                    영업 실적, P&L, 시장점유율, 가격 등 각 팀 서랍에 저장되던 주간 엑셀
                                </p>
                            </div>

                            <div class="bg-white/10 backdrop-blur-sm p-3.5 rounded-xl border border-white/10 space-y-1.5">
                                <div class="flex items-center gap-2 text-amber-300 font-bold text-xs">
                                    <span class="material-symbols-outlined text-lg">sensors</span>
                                    <span>24시간 감시 센서</span>
                                </div>
                                <div class="text-[11px] text-slate-200 font-medium">File Watcher 엔진</div>
                                <p class="text-[10.5px] text-slate-300 leading-normal">
                                    새 엑셀이 저장되는 순간 3초 만에 안전하게 감지하여 작업 큐에 등록
                                </p>
                            </div>

                            <div class="bg-white/10 backdrop-blur-sm p-3.5 rounded-xl border border-white/10 space-y-1.5">
                                <div class="flex items-center gap-2 text-blue-300 font-bold text-xs">
                                    <span class="material-symbols-outlined text-lg">account_balance</span>
                                    <span>초고속 디지털 금고</span>
                                </div>
                                <div class="text-[11px] text-slate-200 font-medium">중앙 DuckDB 코어</div>
                                <p class="text-[10.5px] text-slate-300 leading-normal">
                                    수백만 건의 데이터를 1초 만에 과거 데이터 손실 없이 완벽히 정산·보관
                                </p>
                            </div>

                            <div class="bg-white/10 backdrop-blur-sm p-3.5 rounded-xl border border-white/10 space-y-1.5">
                                <div class="flex items-center gap-2 text-rose-300 font-bold text-xs">
                                    <span class="material-symbols-outlined text-lg">cell_tower</span>
                                    <span>실시간 브로드캐스트</span>
                                </div>
                                <div class="text-[11px] text-slate-200 font-medium">화면 알림 & 배포</div>
                                <p class="text-[10.5px] text-slate-300 leading-normal">
                                    정산 완료 즉시 화면에 팝업이 뜨고 버튼 하나로 전사 클라우드 즉시 배포
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. 4단계 자동 파이프라인 인터랙티브 인포그래픽 -->
                <div class="space-y-4">
                    <div class="flex items-center justify-between">
                        <h3 class="text-base font-bold text-primary flex items-center gap-2">
                            <span class="material-symbols-outlined text-accent-teal">account_tree</span>
                            <span>주간 엑셀 데이터의 4단계 자동 동기화 라이프사이클</span>
                        </h3>
                        <span class="text-xs text-text-muted">100% 무인 자동화 (Zero Manual Touch)</span>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <!-- Step 1 -->
                        <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3 relative clean-card">
                            <div class="flex items-center justify-between">
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200">STEP 1. 감지</span>
                                <span class="material-symbols-outlined text-amber-500 text-xl">file_open</span>
                            </div>
                            <h4 class="text-sm font-bold text-primary">엑셀 파일 저장 감지</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                담당자가 분석 폴더에 주간 엑셀(KPI, P&L, GDMI, 크롤링 DB 등)을 저장하면 <strong>File Watcher</strong>가 실시간으로 포착합니다.
                            </p>
                            <div class="bg-amber-50/50 p-2.5 rounded-lg border border-amber-100 text-[11px] text-amber-900 space-y-1">
                                <div class="font-semibold flex items-center gap-1">
                                    <span class="material-symbols-outlined text-xs">timer</span>
                                    <span>3초 안정화 디바운스</span>
                                </div>
                                <p class="text-[10.5px] text-slate-600">
                                    엑셀 저장이 완료되어 파일 락(Lock)이 완전히 풀릴 때까지 3초 대기하여 파일 깨짐을 원천 방지합니다.
                                </p>
                            </div>
                        </div>

                        <!-- Step 2 -->
                        <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3 relative clean-card">
                            <div class="flex items-center justify-between">
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-teal-50 text-teal-700 border border-teal-200">STEP 2. 정산</span>
                                <span class="material-symbols-outlined text-teal-600 text-xl">database</span>
                            </div>
                            <h4 class="text-sm font-bold text-primary">DuckDB 중앙 코어 정산</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                파이썬 오케스트레이터가 가동되어 수십만 행을 1초 만에 정규화하고 <strong>중앙 DuckDB</strong>에 고속 주입합니다.
                            </p>
                            <div class="bg-teal-50/50 p-2.5 rounded-lg border border-teal-100 text-[11px] text-teal-900 space-y-1">
                                <div class="font-semibold flex items-center gap-1">
                                    <span class="material-symbols-outlined text-xs">sync_saved_locally</span>
                                    <span>주차별 안전 멱등성 (Upsert)</span>
                                </div>
                                <p class="text-[10.5px] text-slate-600">
                                    과거 1~38주 차 장부는 안전하게 보존하고, 새로 들어온 39주 차 데이터만 깨끗하게 교체합니다.
                                </p>
                            </div>
                        </div>

                        <!-- Step 3 -->
                        <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3 relative clean-card">
                            <div class="flex items-center justify-between">
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200">STEP 3. 압축</span>
                                <span class="material-symbols-outlined text-blue-600 text-xl">folder_zip</span>
                            </div>
                            <h4 class="text-sm font-bold text-primary">웹 최적화 마스터 번들</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                정산된 대용량 DB를 웹 브라우저가 즉각 띄울 수 있도록 <strong>초경량 JSON 번들(1.1MB)</strong>로 즉시 재컴파일합니다.
                            </p>
                            <div class="bg-blue-50/50 p-2.5 rounded-lg border border-blue-100 text-[11px] text-blue-900 space-y-1">
                                <div class="font-semibold flex items-center gap-1">
                                    <span class="material-symbols-outlined text-xs">speed</span>
                                    <span>초고속 0.1초 로딩</span>
                                </div>
                                <p class="text-[10.5px] text-slate-600">
                                    무거운 DB 연산을 브라우저 밖에서 미리 끝내두어 일반 PC/모바일에서도 지연 없이 열립니다.
                                </p>
                            </div>
                        </div>

                        <!-- Step 4 -->
                        <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3 relative clean-card">
                            <div class="flex items-center justify-between">
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200">STEP 4. 전파</span>
                                <span class="material-symbols-outlined text-purple-600 text-xl">notifications_active</span>
                            </div>
                            <h4 class="text-sm font-bold text-primary">실시간 알림 & 1-Click 배포</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                포털 관리자 화면에 즉시 <strong>토스트 팝업</strong>이 발생하며, 클릭 한 번으로 Firebase 클라우드에 전사 배포됩니다.
                            </p>
                            <div class="bg-purple-50/50 p-2.5 rounded-lg border border-purple-100 text-[11px] text-purple-900 space-y-1">
                                <div class="font-semibold flex items-center gap-1">
                                    <span class="material-symbols-outlined text-xs">cloud_done</span>
                                    <span>SSE 이벤트 스트림</span>
                                </div>
                                <p class="text-[10.5px] text-slate-600">
                                    화면 새로고침 없이도 "✨ W39 데이터 동기화 완료" 알림이 실시간으로 안내됩니다.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 3. 혁신적 전/후 비교 카드 (Before vs After) -->
                <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-4">
                    <h3 class="text-base font-bold text-primary flex items-center gap-2">
                        <span class="material-symbols-outlined text-secondary">compare_arrows</span>
                        <span>도입 효과: 기존 수동 취합 방식 vs AXIS 자동 파이프라인</span>
                    </h3>
                    <p class="text-xs text-slate-600">
                        매주 반복되던 번거로운 수작업 취합과 컴퓨터 멈춤 문제를 근본적으로 해소했습니다.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
                        <!-- Before Card -->
                        <div class="bg-rose-50/50 rounded-xl border border-rose-200 p-5 space-y-3">
                            <div class="flex items-center justify-between pb-2 border-b border-rose-200">
                                <div class="flex items-center gap-2 text-rose-800 font-bold text-sm">
                                    <span class="material-symbols-outlined text-lg">cancel</span>
                                    <span>기존 방식 (수동 취합 & 개별 엑셀)</span>
                                </div>
                                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-200 text-rose-900">BEFORE</span>
                            </div>
                            <ul class="text-xs text-slate-700 space-y-2.5 leading-relaxed">
                                <li class="flex items-start gap-2">
                                    <span class="text-rose-500 font-bold text-sm leading-none">•</span>
                                    <span><strong>컴퓨터 멈춤 현상:</strong> 20~50MB가 넘는 대형 엑셀을 열 때마다 엑셀 프로그램이 멈추거나 파일 락 충돌 발생</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-rose-500 font-bold text-sm leading-none">•</span>
                                    <span><strong>막대한 시간 소요:</strong> 담당자가 매주 엑셀을 열고, 시트를 복사하고, 수식을 다시 거는 데 30분~1시간 소요</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-rose-500 font-bold text-sm leading-none">•</span>
                                    <span><strong>인적 실수 및 데이터 유실:</strong> 실수로 지난주 데이터를 덮어쓰거나 수식이 깨지는 휴먼 에러 상존</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-rose-500 font-bold text-sm leading-none">•</span>
                                    <span><strong>웹 연동 불가:</strong> 엑셀로만 남아있어 경영진 보고나 해외 법인 실시간 공유가 어렵고 느림</span>
                                </li>
                            </ul>
                        </div>

                        <!-- After Card -->
                        <div class="bg-emerald-50/50 rounded-xl border border-emerald-200 p-5 space-y-3">
                            <div class="flex items-center justify-between pb-2 border-b border-emerald-200">
                                <div class="flex items-center gap-2 text-emerald-800 font-bold text-sm">
                                    <span class="material-symbols-outlined text-lg">check_circle</span>
                                    <span>AXIS 방식 (DuckDB 중앙 자동 동기화)</span>
                                </div>
                                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-200 text-emerald-900">AFTER</span>
                            </div>
                            <ul class="text-xs text-slate-700 space-y-2.5 leading-relaxed">
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-600 font-bold text-sm leading-none">•</span>
                                    <span><strong>100% 무인 자동 감지:</strong> 담당자는 평소대로 엑셀을 저장만 하면 3초 내에 센서가 알아서 감지·가동</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-600 font-bold text-sm leading-none">•</span>
                                    <span><strong>1초 내 초고속 정산:</strong> 수십만 건의 대용량 데이터도 DuckDB 컬럼 엔진으로 1초 이내 정산 완료 (50배 가속)</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-600 font-bold text-sm leading-none">•</span>
                                    <span><strong>주차별 안전 멱등성:</strong> 기존 1~38주 차 기록은 완벽 보존하고 이번 주차만 깔끔하게 교체하여 무결성 100% 보장</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-600 font-bold text-sm leading-none">•</span>
                                    <span><strong>실시간 웹 대시보드 로딩:</strong> 1.1MB 경량 번들로 압축되어 모바일과 웹 어디서든 0.1초 만에 즉시 열람</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- 4. 엔지니어링 무결성 원칙 (접이식 아코디언 / 기술 디테일) -->
                <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-4">
                    <div class="flex items-center justify-between">
                        <h3 class="text-base font-bold text-primary flex items-center gap-2">
                            <span class="material-symbols-outlined text-slate-700">verified_user</span>
                            <span>엔지니어링 무결성 원칙 & 표준 아키텍처 (기술 상세)</span>
                        </h3>
                        <span class="text-[11px] text-slate-500 bg-slate-100 px-2.5 py-1 rounded">개발자 & 데이터 엔지니어 참조 표준</span>
                    </div>
                    <p class="text-xs text-slate-600 leading-relaxed">
                        AXIS 시스템은 대용량 파일 다중 접속 시 발생할 수 있는 <strong>엑셀 충돌(Crash), 프로세스 무한 정체(Hang), 동시성 락(Lock)</strong>을 방지하기 위해 엄격한 사내 엔지니어링 규칙을 100% 준수합니다.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                        <!-- Rule 1 -->
                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
                            <div class="flex items-center gap-2 text-primary font-bold text-xs">
                                <span class="material-symbols-outlined text-accent-teal text-base">layers</span>
                                <span>1. Pandas Overlay 벌크 주입</span>
                            </div>
                            <p class="text-[11px] text-slate-600 leading-relaxed">
                                엑셀 셀 하나씩 반복문으로 접근하는 방식을 엄격히 금지합니다. Python Pandas 메모리 상에서 벌크 로드 후 <code>mode='a'</code>, <code>if_sheet_exists='overlay'</code>를 통해 기존 서식과 수식을 완벽히 유지하며 블록 단위로 일괄 주입합니다.
                            </p>
                        </div>

                        <!-- Rule 2 -->
                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
                            <div class="flex items-center gap-2 text-primary font-bold text-xs">
                                <span class="material-symbols-outlined text-secondary text-base">security_update_good</span>
                                <span>2. SaveCopyAs 원자적 대체 패턴</span>
                            </div>
                            <p class="text-[11px] text-slate-600 leading-relaxed">
                                대용량 바이너리(XLSB/XLSX) 작업 시 <code>wb.Save()</code> 직접 호출을 금지합니다. <code>Calculation = Manual</code> 상태에서 <code>SaveCopyAs</code>로 임시 파일에 충돌 없이 복제 저장한 뒤 원자적 파일 교체(Atomic Move)를 수행하여 RPC 프로세스 락을 원천 차단합니다.
                            </p>
                        </div>

                        <!-- Rule 3 -->
                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
                            <div class="flex items-center gap-2 text-primary font-bold text-xs">
                                <span class="material-symbols-outlined text-accent-blue text-base">hub</span>
                                <span>3. Star Schema 10대 핵심 테이블</span>
                            </div>
                            <p class="text-[11px] text-slate-600 leading-relaxed">
                                중앙 DuckDB 코어는 5대 Fact(Sellout, P&L, Price, MS, Advance Profit)와 3대 Dim(법인, 모델라인업, 환율) 및 운영 테이블(동기화 로그, 이상치 감지)로 정규화되어 데이터 정합성과 확장성을 보장합니다.
                            </p>
                        </div>
                    </div>
                </div>
            </section>'''

with open('d:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '<section id="tab-db"'
end_marker = '<!-- ========================================================================= -->\n            <!-- TAB 5: 보안 구성 & 거버넌스'

start_pos = content.find(start_marker)
end_pos = content.find(end_marker)

if start_pos != -1 and end_pos != -1:
    updated_content = content[:start_pos] + new_tab_db + '\n\n            ' + content[end_pos:]
    with open('d:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Successfully updated section 4 in AXIS_System_Architecture_Guide.html!")
else:
    print(f"Markers not found: start_pos={start_pos}, end_pos={end_pos}")
