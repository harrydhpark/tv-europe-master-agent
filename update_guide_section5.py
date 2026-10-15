# -*- coding: utf-8 -*-
new_tab_security = '''<section id="tab-security" class="tab-content space-y-8">
                <!-- Section Header -->
                <div class="border-b border-slate-200 pb-5">
                    <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded bg-rose-50 text-rose-800 text-xs font-semibold mb-2 border border-rose-200">
                        <span class="material-symbols-outlined text-sm">verified_user</span>
                        <span>Enterprise Zero-Friction Security & Access Governance</span>
                    </div>
                    <h2 class="text-2xl font-bold text-primary tracking-tight font-headline">5. 보안 구성 & 무마찰 거버넌스</h2>
                    <p class="text-sm text-text-muted mt-1">
                        어려운 암호학 용어 없이 쉽게 이해하는 <strong>AXIS 사내 인가 보호, SHA-256 일방통행 암호화 & 무마찰 SSO 프리패스</strong>
                    </p>
                </div>

                <!-- 1. Easy Metaphor Intro: 스마트 사옥 출입 시스템 비유 -->
                <div class="bg-gradient-to-r from-slate-900 via-primary to-slate-800 rounded-2xl p-6 text-white shadow-md relative overflow-hidden">
                    <div class="relative z-10 space-y-4">
                        <div class="flex items-center gap-2.5 text-rose-300 font-semibold text-xs tracking-wider uppercase">
                            <span class="material-symbols-outlined text-base">shield_with_heart</span>
                            <span>스마트 사옥 출입 시스템으로 쉽게 이해하는 보안 원리</span>
                        </div>
                        <h3 class="text-xl font-bold font-headline leading-snug">
                            "메인 로비에서 출입증을 한 번 찍으면, 15개 전문 연구실을 비밀번호 없이 통과하고 자리를 비우면 스마트 센서가 자동으로 잠급니다."
                        </h3>
                        <p class="text-xs text-slate-300 leading-relaxed max-w-3xl">
                            기존 보안 방식은 페이지를 바꿀 때마다 비밀번호를 다시 묻거나, 반대로 보안이 허술해 주소창에 정보가 노출되는 문제가 있었습니다. AXIS는 담당자에게는 아무런 불편함이 없는 <strong>무마찰(Zero-Friction) 경험</strong>을 제공하면서도, 뒷단에서는 최고 등급의 일방통행 암호화와 자동 잠금 센서가 24시간 철통 방어막을 형성합니다.
                        </p>
                        
                        <!-- 4 Metaphor Grid -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-2">
                            <div class="bg-white/10 backdrop-blur-sm p-3.5 rounded-xl border border-white/10 space-y-1.5">
                                <div class="flex items-center gap-2 text-rose-300 font-bold text-xs">
                                    <span class="material-symbols-outlined text-lg">badge</span>
                                    <span>스마트 통합 출입증</span>
                                </div>
                                <div class="text-[11px] text-slate-200 font-medium">무마찰 SSO 프리패스</div>
                                <p class="text-[10.5px] text-slate-300 leading-normal">
                                    포털 1회 인증으로 산하 15개 전체 에이전트 대시보드를 추가 로그인 없이 자유롭게 이동
                                </p>
                            </div>

                            <div class="bg-white/10 backdrop-blur-sm p-3.5 rounded-xl border border-white/10 space-y-1.5">
                                <div class="flex items-center gap-2 text-amber-300 font-bold text-xs">
                                    <span class="material-symbols-outlined text-lg">fingerprint</span>
                                    <span>일방통행 지문 금고</span>
                                </div>
                                <div class="text-[11px] text-slate-200 font-medium">SHA-256 단방향 해시</div>
                                <p class="text-[10.5px] text-slate-300 leading-normal">
                                    비밀번호 글자를 절대 저장하지 않고 해커가 탈취해도 원문 복원이 불가능한 지문 형태로만 대조
                                </p>
                            </div>

                            <div class="bg-white/10 backdrop-blur-sm p-3.5 rounded-xl border border-white/10 space-y-1.5">
                                <div class="flex items-center gap-2 text-teal-300 font-bold text-xs">
                                    <span class="material-symbols-outlined text-lg">timer</span>
                                    <span>스마트 이석 센서</span>
                                </div>
                                <div class="text-[11px] text-slate-200 font-medium">30분 지능형 세션 가드</div>
                                <p class="text-[10.5px] text-slate-300 leading-normal">
                                    업무 중엔 끊김 없이 유지되되, 30분간 자리를 비우면 화면을 자동 잠가 비인가 노출 차단
                                </p>
                            </div>

                            <div class="bg-white/10 backdrop-blur-sm p-3.5 rounded-xl border border-white/10 space-y-1.5">
                                <div class="flex items-center gap-2 text-blue-300 font-bold text-xs">
                                    <span class="material-symbols-outlined text-lg">gmp_bad</span>
                                    <span>철통 보안 셔터</span>
                                </div>
                                <div class="text-[11px] text-slate-200 font-medium">Full-screen Auth Guard</div>
                                <p class="text-[10.5px] text-slate-300 leading-normal">
                                    외부인이 링크 복사나 비인가 경로로 침입 시 0.1초 만에 화면 전체를 셔터로 차단
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. 4단계 스마트 보안 라이프사이클 인터랙티브 인포그래픽 -->
                <div class="space-y-4">
                    <div class="flex items-center justify-between">
                        <h3 class="text-base font-bold text-primary flex items-center gap-2">
                            <span class="material-symbols-outlined text-secondary">security</span>
                            <span>AXIS 무마찰 보안 거버넌스의 4단계 라이프사이클</span>
                        </h3>
                        <span class="text-xs text-text-muted">보안성과 편의성의 완벽한 양립 (Zero-Friction & Zero-Trust)</span>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <!-- Step 1 -->
                        <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3 relative clean-card">
                            <div class="flex items-center justify-between">
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200">STEP 1. 지문 검증</span>
                                <span class="material-symbols-outlined text-amber-500 text-xl">fingerprint</span>
                            </div>
                            <h4 class="text-sm font-bold text-primary">SHA-256 단방향 암호화</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                사용자가 로그인 비밀번호를 입력하면 브라우저 내부에서 즉시 <strong>64자리 해시 지문</strong>으로 변환하여 대조합니다.
                            </p>
                            <div class="bg-amber-50/50 p-2.5 rounded-lg border border-amber-100 text-[11px] text-amber-900 space-y-1">
                                <div class="font-semibold flex items-center gap-1">
                                    <span class="material-symbols-outlined text-xs">no_encryption_gmailerrorred</span>
                                    <span>원문 보관 위험 0%</span>
                                </div>
                                <p class="text-[10.5px] text-slate-600">
                                    비밀번호 평문(Plaintext)은 서버나 PC 어디에도 일절 저장되지 않아 유출될 가능성이 전혀 없습니다.
                                </p>
                            </div>
                        </div>

                        <!-- Step 2 -->
                        <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3 relative clean-card">
                            <div class="flex items-center justify-between">
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200">STEP 2. 출입증 발급</span>
                                <span class="material-symbols-outlined text-secondary text-xl">passkey</span>
                            </div>
                            <h4 class="text-sm font-bold text-primary">무마찰 SSO 티켓 생성</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                포털 인증을 통과한 인가자에게 서브 대시보드로 안전하게 이동할 수 있는 <strong>암호화 세션 티켓</strong>을 자동 발행합니다.
                            </p>
                            <div class="bg-rose-50/50 p-2.5 rounded-lg border border-rose-100 text-[11px] text-rose-900 space-y-1">
                                <div class="font-semibold flex items-center gap-1">
                                    <span class="material-symbols-outlined text-xs">link</span>
                                    <span>Seamless Token 파라미터</span>
                                </div>
                                <p class="text-[10.5px] text-slate-600">
                                    HMAC 기반 <code>auth_token</code>과 타임스탬프가 연계되어 대시보드 클릭 시 즉각 백그라운드 전달됩니다.
                                </p>
                            </div>
                        </div>

                        <!-- Step 3 -->
                        <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3 relative clean-card">
                            <div class="flex items-center justify-between">
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-teal-50 text-teal-700 border border-teal-200">STEP 3. 흔적 소멸</span>
                                <span class="material-symbols-outlined text-teal-600 text-xl">cleaning_services</span>
                            </div>
                            <h4 class="text-sm font-bold text-primary">하이패스 & Clean URL 정제</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                서브 대시보드 진입 0.1초 만에 토큰 유효성을 승인한 뒤, 주소창에서 <strong>인증 파라미터를 즉시 자동 삭제</strong>합니다.
                            </p>
                            <div class="bg-teal-50/50 p-2.5 rounded-lg border border-teal-100 text-[11px] text-teal-900 space-y-1">
                                <div class="font-semibold flex items-center gap-1">
                                    <span class="material-symbols-outlined text-xs">history_edu</span>
                                    <span>history.replaceState</span>
                                </div>
                                <p class="text-[10.5px] text-slate-600">
                                    사용자가 URL을 복사하여 다른 사람에게 전달하거나 북마크해도 인증 토큰이 외부로 새어나가지 않습니다.
                                </p>
                            </div>
                        </div>

                        <!-- Step 4 -->
                        <div class="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3 relative clean-card">
                            <div class="flex items-center justify-between">
                                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200">STEP 4. 상시 보호</span>
                                <span class="material-symbols-outlined text-blue-600 text-xl">lock_clock</span>
                            </div>
                            <h4 class="text-sm font-bold text-primary">30분 이석 감지 & 자동 잠금</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                마우스와 키보드 움직임을 실시간 감지하여, <strong>30분 이상 자리 비움 시</strong> 화면을 자동으로 잠그고 세션을 파기합니다.
                            </p>
                            <div class="bg-blue-50/50 p-2.5 rounded-lg border border-blue-100 text-[11px] text-blue-900 space-y-1">
                                <div class="font-semibold flex items-center gap-1">
                                    <span class="material-symbols-outlined text-xs">vital_signs</span>
                                    <span>활동 하트비트 센서</span>
                                </div>
                                <p class="text-[10.5px] text-slate-600">
                                    업무를 계속 수행 중일 때는 매끄럽게 세션이 자동 연장되어 재로그인 스트레스가 전혀 없습니다.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 3. 혁신적 전/후 비교 카드 (Before vs After) -->
                <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-4">
                    <h3 class="text-base font-bold text-primary flex items-center gap-2">
                        <span class="material-symbols-outlined text-secondary">compare_arrows</span>
                        <span>도입 효과: 기존 파편화된 보안 방식 vs AXIS 스마트 통합 거버넌스</span>
                    </h3>
                    <p class="text-xs text-slate-600">
                        담당자의 업무 불편은 완전히 없애고(무마찰), 기업 중요 영업 데이터의 보안성은 극대화했습니다.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
                        <!-- Before Card -->
                        <div class="bg-rose-50/50 rounded-xl border border-rose-200 p-5 space-y-3">
                            <div class="flex items-center justify-between pb-2 border-b border-rose-200">
                                <div class="flex items-center gap-2 text-rose-800 font-bold text-sm">
                                    <span class="material-symbols-outlined text-lg">cancel</span>
                                    <span>기존 방식 (개별 로그인 & 취약한 보안)</span>
                                </div>
                                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-200 text-rose-900">BEFORE</span>
                            </div>
                            <ul class="text-xs text-slate-700 space-y-2.5 leading-relaxed">
                                <li class="flex items-start gap-2">
                                    <span class="text-rose-500 font-bold text-sm leading-none">•</span>
                                    <span><strong>반복 로그인의 피로:</strong> 15개 에이전트 대시보드를 옮겨 다닐 때마다 ID/PW를 매번 새로 입력해야 함</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-rose-500 font-bold text-sm leading-none">•</span>
                                    <span><strong>비밀번호 평문 노출 위험:</strong> 스크립트 코드나 브라우저 로컬 저장소에 암호가 그대로 노출되는 치명적 보안 취약점</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-rose-500 font-bold text-sm leading-none">•</span>
                                    <span><strong>URL 토큰 누출:</strong> 주소창에 인증 파라미터가 남아있어 메신저나 이메일로 링크 전달 시 권한이 비인가자에게 유출</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-rose-500 font-bold text-sm leading-none">•</span>
                                    <span><strong>화면 무단 노출:</strong> 담당자가 회의 참석이나 퇴근 시 브라우저를 켜두면 다른 사람에게 실적 데이터가 그대로 노출</span>
                                </li>
                            </ul>
                        </div>

                        <!-- After Card -->
                        <div class="bg-emerald-50/50 rounded-xl border border-emerald-200 p-5 space-y-3">
                            <div class="flex items-center justify-between pb-2 border-b border-emerald-200">
                                <div class="flex items-center gap-2 text-emerald-800 font-bold text-sm">
                                    <span class="material-symbols-outlined text-lg">check_circle</span>
                                    <span>AXIS 방식 (엔터프라이즈 스마트 보안 거버넌스)</span>
                                </div>
                                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-200 text-emerald-900">AFTER</span>
                            </div>
                            <ul class="text-xs text-slate-700 space-y-2.5 leading-relaxed">
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-600 font-bold text-sm leading-none">•</span>
                                    <span><strong>원클릭 Seamless SSO:</strong> 포털에서 딱 1번만 로그인하면 15개 산하 전체 대시보드에 즉시 자동 프리패스 접속</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-600 font-bold text-sm leading-none">•</span>
                                    <span><strong>SHA-256 일방통행 암호화:</strong> 비밀번호 글자를 남기지 않고 단방향 지문으로만 대조하여 탈취 시도 원천 차단</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-600 font-bold text-sm leading-none">•</span>
                                    <span><strong>주소창 0.1초 정제:</strong> 접속 즉시 주소창에서 토큰을 자동 파기하여 URL을 공유하거나 북마크해도 100% 안전</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-600 font-bold text-sm leading-none">•</span>
                                    <span><strong>지능형 30분 이석 가드:</strong> 키보드/마우스 감지로 일할 땐 편안히, 자리 비울 땐 자동으로 화면을 가려 전사 기밀 보호</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- 4. 엔지니어링 & 거버넌스 표준 원칙 (기술 상세 카드) -->
                <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-sm space-y-4">
                    <div class="flex items-center justify-between">
                        <h3 class="text-base font-bold text-primary flex items-center gap-2">
                            <span class="material-symbols-outlined text-slate-700">terminal</span>
                            <span>서브 대시보드 보안 표준 연동 규격 & 엔지니어링 표준 (`auth-guard.js`)</span>
                        </h3>
                        <span class="text-[11px] text-slate-500 bg-slate-100 px-2.5 py-1 rounded">개발자 & 인프라 관리자 연동 표준</span>
                    </div>
                    <p class="text-xs text-slate-600 leading-relaxed">
                        신규 서브 대시보드를 추가하거나 외주/사내 시스템을 연동할 때 복잡한 보안 설정 없이 아래 <strong>표준 스크립트 단 1줄</strong>을 HTML 최상단에 포함하기만 하면 전사 통일된 보안 정책이 100% 즉시 적용됩니다.
                    </p>

                    <!-- Code Snippet Box -->
                    <div class="bg-slate-900 text-slate-100 p-4 rounded-xl text-xs font-mono space-y-2">
                        <div class="text-slate-400">&lt;!-- 서브 대시보드 index.html &lt;head&gt; 최상단에 포함되는 표준 보안 임베드 규격 --&gt;</div>
                        <div class="text-emerald-400 font-bold">&lt;script src="auth-guard.js"&gt;&lt;/script&gt;</div>
                        <div class="text-slate-400 pt-2">// auth-guard.js 3대 무인 작동 로직:</div>
                        <div class="text-slate-300">1. URL에 Seamless auth_token 수신 시 → HMAC 검증 후 세션 수립 & 주소창 파라미터 즉각 파기</div>
                        <div class="text-slate-300">2. 비인가 URL 직접 접근 시 → 즉시 풀스크린 차단 모달을 띄우고 사내 인증 요구</div>
                        <div class="text-slate-300">3. 인증 통과 후 → 30분 활동 이벤트 리스너(mousemove/keydown) 가동 및 타임아웃 시 자동 세션 종료</div>
                    </div>

                    <!-- 3 Technical Rule Cards -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
                            <div class="flex items-center gap-2 text-primary font-bold text-xs">
                                <span class="material-symbols-outlined text-rose-600 text-base">vpn_key</span>
                                <span>1. Web Crypto API 가속</span>
                            </div>
                            <p class="text-[11px] text-slate-600 leading-relaxed">
                                외부 라이브러리 없이 브라우저 내장 네이티브 <code>crypto.subtle.digest('SHA-256')</code>를 호출하여 하드웨어 가속 기반의 초고속 암호화 연산을 수행합니다.
                            </p>
                        </div>

                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
                            <div class="flex items-center gap-2 text-primary font-bold text-xs">
                                <span class="material-symbols-outlined text-teal-600 text-base">enhanced_encryption</span>
                                <span>2. sessionStorage 세션 격리</span>
                            </div>
                            <p class="text-[11px] text-slate-600 leading-relaxed">
                                영구 저장되는 <code>localStorage</code>나 쿠키 대신 탭/브라우저가 닫히면 물리적으로 메모리에서 소멸되는 <code>sessionStorage</code>를 채택해 탈취 위험을 차단합니다.
                            </p>
                        </div>

                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
                            <div class="flex items-center gap-2 text-primary font-bold text-xs">
                                <span class="material-symbols-outlined text-blue-600 text-base">cloud_sync</span>
                                <span>3. 클라우드 보안 헤더 정책</span>
                            </div>
                            <p class="text-[11px] text-slate-600 leading-relaxed">
                                Firebase Hosting 배포 시 <code>X-Robots-Tag: noindex</code>(검색엔진 차단), <code>CSP frame-ancestors 'self'</code>, <code>Cache-Control: no-store</code>를 전역 강제합니다.
                            </p>
                        </div>
                    </div>
                </div>
            </section>'''

with open('d:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '<section id="tab-security"'
end_marker = '<!-- ========================================================================= -->\n            <!-- TAB 6: 실무 활용 방안'

start_pos = content.find(start_marker)
end_pos = content.find(end_marker)

if start_pos != -1 and end_pos != -1:
    updated_content = content[:start_pos] + new_tab_security + '\n\n            ' + content[end_pos:]
    with open('d:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Successfully updated section 5 in AXIS_System_Architecture_Guide.html!")
else:
    print(f"Markers not found: start_pos={start_pos}, end_pos={end_pos}")
