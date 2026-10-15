import os
import re

html_path = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\00. TV Europe Sales Management Portal\docs\AXIS_System_Architecture_Guide.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the heavy drawer in Scenario 01 with the clean external viewer button
clean_button_html = '''<!-- Open Dedicated Standalone Result Viewer -->
                        <div class="mt-3.5 pt-3.5 border-t border-slate-200/80 flex flex-wrap items-center justify-between gap-3">
                            <a href="scenario_01_result_viewer.html" 
                               target="_blank" 
                               rel="noopener noreferrer"
                               class="py-2.5 px-4 rounded-lg bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold flex items-center gap-2 shadow-sm transition-all hover:scale-105 active:scale-95 group">
                                <span class="material-symbols-outlined text-sm group-hover:rotate-12 transition-transform">open_in_new</span>
                                <span class="font-headline text-sm font-bold">마스터 에이전트 실전 답변 및 엑셀 결과 보기 (새 창 열기 ↗)</span>
                                <span class="px-2 py-0.5 rounded-full bg-teal-800 text-teal-200 text-[10px] font-semibold tracking-wide">실행 완료 5초</span>
                            </a>
                            <span class="text-[11px] text-slate-500 flex items-center gap-1">
                                <span class="material-symbols-outlined text-xs text-teal-600">verified</span>
                                <span>독립 전용 창에서 무편집 원문 답변 및 16개국 엑셀 매트릭스를 쾌적하게 확인·복귀</span>
                            </span>
                        </div>'''

# Replace from Real Agent Execution Result Section to Scenario 2
pattern = r'<!-- Real Agent Execution Result Section \(Interactive Drawer\) -->[\s\S]*?<!-- Scenario 2:'
html = re.sub(pattern, clean_button_html + "\n                    </div>\n\n                    <!-- Scenario 2:", html, count=1)

# Also remove the heavy unused JS block from the main guide to keep it lightweight
pattern_js = r'// Scenario 01 Live Execution Result Helpers[\s\S]*?function downloadScenario01Excel\(\) \{[\s\S]*?\}\s*\}'
html = re.sub(pattern_js, '// Scenario 01 result viewer decoupled to standalone scenario_01_result_viewer.html', html)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Cleaned up AXIS_System_Architecture_Guide.html successfully!")
