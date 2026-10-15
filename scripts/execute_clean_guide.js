const fs = require('fs');
const path = 'd:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html';
let html = fs.readFileSync(path, 'utf8');

// The replacement button markup
const cleanButtonHtml = `<!-- Open Dedicated Standalone Result Viewer -->
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
                        </div>`;

const startPattern = '<!-- Real Agent Execution Result Section (Interactive Drawer) -->';
const endPattern = '<!-- Scenario 2:';

const startIdx = html.indexOf(startPattern);
const endIdx = html.indexOf(endPattern);

console.log('startIdx:', startIdx, 'endIdx:', endIdx);

if (startIdx !== -1 && endIdx !== -1 && startIdx < endIdx) {
    const before = html.substring(0, startIdx);
    const after = html.substring(endIdx);
    
    // Check closing div before Scenario 2
    // Scenario 1 card needs to close properly
    html = before + cleanButtonHtml + '\n                    </div>\n\n                    ' + after;
    console.log('Replaced drawer section successfully.');
} else {
    console.log('Warning: Drawer pattern not found directly. Let us search alternatives.');
}

// Clean up heavy JS from the end of file
const jsStartPattern = '// Scenario 01 Live Execution Result Helpers';
const jsIdx = html.indexOf(jsStartPattern);
if (jsIdx !== -1) {
    // Find where the helper ends (before closing </script>)
    const endScriptIdx = html.indexOf('</script>', jsIdx);
    if (endScriptIdx !== -1) {
        html = html.substring(0, jsIdx) + '// Scenario 01 result viewer decoupled to standalone scenario_01_result_viewer.html\n    ' + html.substring(endScriptIdx);
        console.log('Removed heavy JS helpers successfully.');
    }
}

fs.writeFileSync(path, html, 'utf8');
console.log('AXIS_System_Architecture_Guide.html successfully updated and lightweight!');
