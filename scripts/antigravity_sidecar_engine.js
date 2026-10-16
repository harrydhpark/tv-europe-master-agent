const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFile, spawn } = require('child_process');
const { archiveTask, TASK_BASE_DIR } = require('./archive_task');

const ROOT_DIR = path.resolve(__dirname, '..');
const BRAIN_DIR = process.env.ANTIGRAVITY_BRAIN_DIR || path.join(process.env.USERPROFILE || 'C:\\Users\\harry.park', '.gemini', 'antigravity', 'brain');
const PYTHON_EXE = path.resolve(ROOT_DIR, '..', '04. Price Tracker', 'python_env', 'python.exe');

/**
 * Wraps a raw user prompt from the Sales Portal into an AXIS Master Agent
 * autonomous orchestration prompt that produces the exact same output quality
 * as prompting directly inside Antigravity IDE.
 */
function buildAxisMasterPrompt(rawQuery, options = {}) {
  const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  return `[Sales Portal -> Antigravity AXIS Master Agent Direct Dispatch]
작업 공간(Workspace): d:\\TV 유럽영업\\15. AX Task\\2026 AX 실행과제\\99. Master Agent
실행 모드: 전 과정 100% 완전 무인 자율 실행 (Autonomous Execution Mode)

[사용자 지시사항 (User Prompt)]
${rawQuery}

[필수 수행 프로토콜 (AXIS Master Agent Execution Protocol)]
1. 산하 15대 전문 에이전트 디렉토리(01~15) 및 글로벌 스킬(tv-business-plan-2027, tv-price-tracker, kpi-sheet-update, tv-ms-trend-dashboard, profitability-simulator, advance-profitability-dashboard, excel-large-dataset-ops 등)의 원천 데이터(Parquet, DuckDB, Excel, JSON)를 직접 조회하여 정확한 팩트 수치를 기반으로 작업을 수행하십시오.
2. 중간 확인 질문 없이 데이터 추출, 산출물 파일(.xlsx, .docx, .html) 생성, 대시보드 빌드 및 검증까지 전 과정을 무인으로 완결하십시오.
3. 작업 완료 직전 반드시 Global Rule(Master Agent Task Auto-Archiving Rule)에 따라 'd:\\TV 유럽영업\\15. AX Task\\2026 AX 실행과제\\99. Master Agent\\Task\\${today}_작업제목' 폴더를 생성하고 README.md 및 생성된 모든 산출물 파일을 복사 보관한 뒤 Task/README.md 레지스트리를 갱신하십시오.`;
}

/**
 * Lists recent Antigravity conversations from the brain directory
 */
function listBrainConversations(limit = 15) {
  if (!fs.existsSync(BRAIN_DIR)) return [];
  try {
    const entries = fs.readdirSync(BRAIN_DIR, { withFileTypes: true })
      .filter(d => d.isDirectory() && !d.name.startsWith('.'));

    const candidates = [];
    for (const entry of entries) {
      const convId = entry.name;
      const transcriptPath = path.join(BRAIN_DIR, convId, '.system_generated', 'logs', 'transcript.jsonl');
      if (!fs.existsSync(transcriptPath)) continue;
      try {
        const stat = fs.statSync(transcriptPath);
        candidates.push({ convId, transcriptPath, stat });
      } catch (e) {}
    }

    candidates.sort((a, b) => b.stat.mtimeMs - a.stat.mtimeMs);
    const topCandidates = candidates.slice(0, limit);

    const convs = [];
    for (const { convId, transcriptPath, stat } of topCandidates) {
      try {
        const content = fs.readFileSync(transcriptPath, 'utf8');
        const lines = content.split('\n').filter(l => l.trim().length > 0);
        let firstPrompt = '';
        let lastPrompt = '';
        let lastStatus = 'IDLE';
        let lastStepType = '';

        for (const line of lines) {
          try {
            const step = JSON.parse(line);
            if (step.type === 'USER_INPUT' && step.content) {
              const cleaned = step.content
                .replace(/<USER_REQUEST>/g, '')
                .replace(/<\/USER_REQUEST>/g, '')
                .trim();
              if (!firstPrompt) firstPrompt = cleaned;
              lastPrompt = cleaned;
            }
            if (step.status) lastStatus = step.status;
            if (step.type) lastStepType = step.type;
          } catch (e) {}
        }

        convs.push({
          conversationId: convId,
          updatedAt: stat.mtime.toISOString(),
          mtimeMs: stat.mtimeMs,
          stepCount: lines.length,
          firstPrompt: (firstPrompt || '세션 시작').slice(0, 120),
          lastPrompt: (lastPrompt || firstPrompt || '세션 진행 중').slice(0, 120),
          lastStatus,
          lastStepType
        });
      } catch (e) {}
    }

    return convs;
  } catch (err) {
    console.warn('[SidecarEngine] Error listing brain conversations:', err.message);
    return [];
  }
}

/**
 * Reads structured steps from a specific conversation's transcript.jsonl
 */
function readConversationTranscript(conversationId, maxSteps = 60) {
  if (!conversationId) return null;
  const transcriptPath = path.join(BRAIN_DIR, conversationId, '.system_generated', 'logs', 'transcript.jsonl');
  if (!fs.existsSync(transcriptPath)) return null;

  try {
    const raw = fs.readFileSync(transcriptPath, 'utf8');
    const lines = raw.split('\n').filter(l => l.trim().length > 0);
    const parsedSteps = [];
    let latestAnswerMarkdown = '';
    let latestThinking = '';
    const activeToolCalls = [];

    for (const line of lines.slice(-maxSteps)) {
      try {
        const step = JSON.parse(line);
        const toolCalls = Array.isArray(step.tool_calls)
          ? step.tool_calls.map(tc => ({
              name: tc.name,
              toolSummary: tc.args?.toolSummary || tc.args?.Description || tc.name,
              toolAction: tc.args?.toolAction || tc.name,
              targetFile: tc.args?.TargetFile || tc.args?.AbsolutePath || ''
            }))
          : [];

        if (step.thinking) {
          latestThinking = step.thinking;
        }
        if (toolCalls.length > 0) {
          toolCalls.forEach(tc => activeToolCalls.push({
            stepIndex: step.step_index,
            ...tc,
            createdAt: step.created_at
          }));
        }
        if (step.type === 'PLANNER_RESPONSE' && step.content && toolCalls.length === 0) {
          latestAnswerMarkdown = step.content;
        }

        parsedSteps.push({
          stepIndex: step.step_index,
          source: step.source,
          type: step.type,
          status: step.status,
          createdAt: step.created_at,
          thinking: step.thinking ? step.thinking.slice(0, 500) : '',
          toolCalls,
          content: step.type === 'USER_INPUT'
            ? (step.content || '').replace(/<\/?USER_REQUEST>/g, '').trim()
            : (step.type === 'PLANNER_RESPONSE' ? (step.content || '') : '')
        });
      } catch (e) {}
    }

    return {
      conversationId,
      totalLines: lines.length,
      steps: parsedSteps,
      latestThinking: latestThinking ? latestThinking.slice(0, 600) : '',
      recentToolCalls: activeToolCalls.slice(-12),
      latestAnswerMarkdown
    };
  } catch (err) {
    return null;
  }
}

/**
 * Scans 99. Master Agent/Task for recent archived task folders and deliverables
 */
function scanTaskDeliverables(limit = 15, sinceTimeMs = 0) {
  if (!fs.existsSync(TASK_BASE_DIR)) return [];
  try {
    const dirs = fs.readdirSync(TASK_BASE_DIR, { withFileTypes: true })
      .filter(d => d.isDirectory() && /^\d{8}_/.test(d.name));

    const results = [];
    for (const dir of dirs) {
      const folderPath = path.join(TASK_BASE_DIR, dir.name);
      const stat = fs.statSync(folderPath);
      const files = fs.readdirSync(folderPath, { withFileTypes: true })
        .filter(f => f.isFile())
        .map(f => {
          const fStat = fs.statSync(path.join(folderPath, f.name));
          const ext = path.extname(f.name).toLowerCase();
          let type = 'file';
          if (ext === '.xlsx' || ext === '.xlsb' || ext === '.csv') type = 'excel';
          else if (ext === '.docx' || ext === '.pdf') type = 'document';
          else if (ext === '.html') type = 'web';
          else if (f.name.toLowerCase() === 'readme.md' || ext === '.md') type = 'markdown';
          else if (ext === '.py' || ext === '.js') type = 'script';

          const webUrl = `/tasks-archive/${encodeURIComponent(dir.name)}/${encodeURIComponent(f.name)}`;
          return {
            name: f.name,
            type,
            ext,
            size: fStat.size,
            sizeBytes: fStat.size,
            updatedAt: fStat.mtime.toISOString(),
            mtimeMs: fStat.mtimeMs,
            url: webUrl,
            webUrl
          };
        });

      const maxFileMtime = files.reduce((max, f) => Math.max(max, f.mtimeMs), stat.mtimeMs);
      if (sinceTimeMs > 0 && maxFileMtime < sinceTimeMs) continue;

      let summary = '';
      const readmePath = path.join(folderPath, 'README.md');
      if (fs.existsSync(readmePath)) {
        try {
          const md = fs.readFileSync(readmePath, 'utf8');
          const match = md.match(/> "([^"]+)"/);
          if (match) summary = match[1].slice(0, 140);
        } catch (e) {}
      }

      results.push({
        folderName: dir.name,
        dateStr: dir.name.slice(0, 8),
        title: dir.name.slice(9),
        summary,
        updatedAt: new Date(maxFileMtime).toISOString(),
        mtimeMs: maxFileMtime,
        readmeUrl: `/tasks-archive/${encodeURIComponent(dir.name)}/README.md`,
        files,
        deliverables: files
      });
    }

    return results
      .sort((a, b) => b.mtimeMs - a.mtimeMs)
      .slice(0, limit);
  } catch (err) {
    console.warn('[SidecarEngine] Error scanning Task deliverables:', err.message);
    return [];
  }
}

/**
 * Checks if `agentapi` CLI is available in the current Sidecar PATH
 */
function checkAgentApiAvailable() {
  return new Promise((resolve) => {
    execFile('where.exe', ['agentapi'], { timeout: 3000 }, (err, stdout) => {
      if (!err && stdout && stdout.trim().length > 0) {
        resolve(stdout.trim().split(/\r?\n/)[0]);
      } else {
        resolve(null);
      }
    });
  });
}

/**
 * Dispatches a prompt directly to Antigravity via `agentapi` (when running inside Antigravity Sidecar)
 * and tails `transcript.jsonl` until completion.
 */
async function dispatchViaAgentApi(rawQuery, options = {}, onProgress = () => {}) {
  const agentApiBin = await checkAgentApiAvailable();
  if (!agentApiBin) {
    return { executed: false, reason: 'agentapi_not_in_path' };
  }

  const startTimeMs = Date.now();
  const wrappedPrompt = buildAxisMasterPrompt(rawQuery, options);
  const targetConvId = options.conversationId || null;

  onProgress({
    step: 1,
    totalSteps: 4,
    currentAgent: 'Antigravity Sidecar (agentapi)',
    desc: targetConvId
      ? `기존 Antigravity 세션(${targetConvId.slice(0, 8)})에 프롬프트를 전송하고 있습니다...`
      : 'Antigravity AXIS Master Agent 신규 세션을 생성하고 프롬프트를 전달하고 있습니다...'
  });

  const args = targetConvId
    ? ['send-message', targetConvId, wrappedPrompt]
    : ['new-conversation', wrappedPrompt];

  return new Promise((resolve) => {
    execFile(agentApiBin, args, { timeout: 15000, cwd: ROOT_DIR }, (err, stdout, stderr) => {
      if (err) {
        console.warn(`[SidecarEngine] agentapi invocation error: ${err.message}`);
        return resolve({ executed: false, reason: err.message });
      }

      // Identify the active conversation ID from stdout or newest brain directory
      let convId = targetConvId;
      const uuidMatch = (stdout || '').match(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i);
      if (uuidMatch) convId = uuidMatch[0];

      // Poll transcript.jsonl for up to 180 seconds
      let pollCount = 0;
      const maxPolls = 180;
      const pollTimer = setInterval(() => {
        pollCount++;
        if (!convId) {
          const recent = listBrainConversations(1);
          if (recent.length > 0 && recent[0].mtimeMs >= startTimeMs - 5000) {
            convId = recent[0].conversationId;
          }
        }

        if (convId) {
          const transcript = readConversationTranscript(convId, 40);
          if (transcript && transcript.steps.length > 0) {
            const lastStep = transcript.steps[transcript.steps.length - 1];
            const recentTool = transcript.recentToolCalls[transcript.recentToolCalls.length - 1];

            onProgress({
              step: Math.min(3, 1 + Math.floor(transcript.recentToolCalls.length / 2)),
              totalSteps: 4,
              currentAgent: recentTool ? `Tool: ${recentTool.name}` : 'AXIS Master Agent',
              desc: recentTool
                ? `${recentTool.toolAction || recentTool.toolSummary || recentTool.name}`
                : (transcript.latestThinking ? transcript.latestThinking.slice(0, 120) + '...' : '마스터 에이전트가 추론 및 분석을 수행 중입니다...'),
              conversationId: convId,
              thinking: transcript.latestThinking,
              toolCalls: transcript.recentToolCalls
            });

            // Check if final planner response is complete
            if (
              lastStep.type === 'PLANNER_RESPONSE' &&
              lastStep.status === 'DONE' &&
              (!lastStep.toolCalls || lastStep.toolCalls.length === 0) &&
              lastStep.content &&
              pollCount > 2
            ) {
              clearInterval(pollTimer);
              const newTasks = scanTaskDeliverables(3, startTimeMs - 10000);
              return resolve({
                executed: true,
                engine: 'antigravity-sidecar-agentapi',
                conversationId: convId,
                answerMarkdown: lastStep.content,
                thinking: transcript.latestThinking,
                toolCalls: transcript.recentToolCalls,
                taskArchive: newTasks[0] || null
              });
            }
          }
        }

        if (pollCount >= maxPolls) {
          clearInterval(pollTimer);
          return resolve({ executed: false, reason: 'agentapi_timeout', conversationId: convId });
        }
      }, 1000);
    });
  });
}

/**
 * Generates an Excel (.xlsx) and standalone HTML report deliverable inside a Task folder
 * when autonomous execution runs via the local co-processor engine.
 */
function generateDeliverableFiles({ taskDir, folderName, query, answerMarkdown, parquetData }) {
  const generatedPaths = [];

  // 1. Always generate a standalone Executive HTML Report in the Task folder
  try {
    const htmlFileName = `${folderName}_Executive_Report.html`;
    const htmlPath = path.join(taskDir, htmlFileName);
    const createdStr = new Date().toISOString().slice(0, 19).replace('T', ' ');
    const safeQuery = String(query || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const htmlContent = `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[AXIS Executive Report] ${folderName}</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root { --slate-950: #020617; --slate-900: #0F172A; --slate-800: #1E293B; --teal-600: #0D9488; --blue-600: #2563EB; --bg: #F1F5F9; --border: #CBD5E1; }
    * { box-sizing: border-box; }
    body { font-family: 'Inter', 'Malgun Gothic', -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--slate-900); margin: 0; padding: 28px 20px 60px; line-height: 1.68; }
    .toolbar-wrap { max-width: 1040px; margin: 0 auto 14px; display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap; }
    .toolbar-left { font-size: 0.8rem; font-weight: 600; color: #475569; display: flex; align-items: center; gap: 8px; }
    .toolbar-actions { display: flex; gap: 8px; flex-wrap: wrap; }
    .btn-action { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; border-radius: 8px; font-size: 0.8rem; font-weight: 700; cursor: pointer; border: 1px solid #CBD5E1; background: #FFFFFF; color: #0F172A; transition: all 0.15s ease; box-shadow: 0 1px 2px rgba(15,23,42,0.05); }
    .btn-action:hover { background: #F8FAFC; border-color: #94A3B8; transform: translateY(-1px); }
    .btn-action.primary { background: #0F172A; color: #FFFFFF; border-color: #0F172A; }
    .btn-action.primary:hover { background: #1E293B; }
    .btn-action.teal { background: #0D9488; color: #FFFFFF; border-color: #0D9488; }
    .btn-action.teal:hover { background: #0F766E; }
    .container { max-width: 1040px; margin: 0 auto; background: #FFFFFF; border: 1px solid var(--border); border-radius: 14px; box-shadow: 0 12px 32px rgba(15,23,42,0.08); overflow: hidden; }
    .header { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: #FFFFFF; padding: 26px 36px; display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; border-bottom: 3px solid #0D9488; }
    .header-eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #5EEAD4; margin-bottom: 6px; font-weight: 600; }
    .header h1 { margin: 0; font-family: 'IBM Plex Sans', sans-serif; font-size: 1.35rem; font-weight: 700; letter-spacing: -0.01em; color: #FFFFFF; }
    .badge { background: rgba(13,148,136,0.22); border: 1px solid #14B8A6; color: #5EEAD4; font-size: 0.74rem; padding: 5px 12px; border-radius: 999px; font-weight: 700; white-space: nowrap; }
    .meta { padding: 14px 36px; background: #F8FAFC; border-bottom: 1px solid #E2E8F0; font-size: 0.82rem; color: #334155; display: flex; flex-wrap: wrap; gap: 20px; align-items: center; }
    .meta-item strong { color: #0F172A; font-weight: 700; }
    .content { padding: 32px 36px 40px; }
    .content h2 { font-family: 'IBM Plex Sans', sans-serif; font-size: 1.22rem; font-weight: 700; color: #0F172A; background: #F8FAFC; border-left: 5px solid #0F172A; padding: 10px 14px; margin: 22px 0 14px; border-radius: 0 8px 8px 0; }
    .content h2:first-child { margin-top: 0; }
    .content h3 { font-family: 'IBM Plex Sans', sans-serif; font-size: 1.03rem; font-weight: 700; color: #0F172A; border-left: 4px solid #0D9488; padding-left: 10px; margin: 26px 0 12px; }
    .content h4 { font-size: 0.94rem; font-weight: 700; color: #1E293B; margin: 18px 0 8px; }
    .content blockquote { margin: 12px 0 20px; padding: 12px 16px; background: #F0FDFA; border-left: 4px solid #0D9488; border-radius: 0 8px 8px 0; color: #134E4A; font-size: 0.86rem; }
    .content blockquote p { margin: 0; }
    .content table { width: 100%; border-collapse: collapse; margin: 14px 0 22px; font-size: 0.84rem; border: 1px solid #CBD5E1; }
    .content th { background: #0F172A; color: #FFFFFF; padding: 10px 12px; text-align: left; font-weight: 700; border: 1px solid #1E293B; white-space: nowrap; }
    .content td { padding: 9px 12px; border: 1px solid #E2E8F0; color: #1E293B; }
    .content tr:nth-child(even) td { background: #F8FAFC; }
    .content tr:last-child td { border-bottom: 2px solid #0F172A; }
    .content ul { padding-left: 20px; margin: 10px 0 18px; }
    .content li { margin-bottom: 6px; font-size: 0.9rem; color: #1E293B; }
    .content code { font-family: 'JetBrains Mono', monospace; background: #F1F5F9; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; color: #0F766E; }
    .content hr { border: 0; border-top: 1px solid #E2E8F0; margin: 28px 0 16px; }
    .toast { position: fixed; bottom: 24px; right: 24px; background: #0F172A; color: #5EEAD4; border: 1px solid #0D9488; padding: 12px 18px; border-radius: 10px; font-size: 0.84rem; font-weight: 700; box-shadow: 0 10px 25px rgba(2,6,23,0.35); opacity: 0; pointer-events: none; transition: opacity 0.2s ease; z-index: 9999; }
    .toast.show { opacity: 1; }
    @media print {
      body { background: #FFFFFF; padding: 0; }
      .toolbar-wrap { display: none !important; }
      .container { box-shadow: none; border: none; max-width: 100%; }
    }
  </style>
</head>
<body>
  <div class="toolbar-wrap">
    <div class="toolbar-left">
      <span>📄 LGE Europe TV Executive HTML Document</span>
      <span>•</span>
      <span>Task ID: <code>${folderName}</code></span>
    </div>
    <div class="toolbar-actions">
      <button class="btn-action teal" onclick="copyRichHtml()">📋 서식 유지 복사 (이메일/워드 붙여넣기용)</button>
      <button class="btn-action" onclick="copyPlainText()">📝 순수 텍스트 복사</button>
      <button class="btn-action primary" onclick="window.print()">🖨️ 인쇄 / PDF 저장</button>
    </div>
  </div>
  <div class="container" id="executiveDocContainer">
    <div class="header">
      <div>
        <div class="header-eyebrow">LGE EUROPE TV SALES STRATEGY • AXIS MASTER AI AGENT</div>
        <h1>🤖 AXIS 전략 분석 리포트 — ${folderName}</h1>
      </div>
      <span class="badge">EXECUTIVE HTML REPORT</span>
    </div>
    <div class="meta">
      <div class="meta-item"><strong>지시 프롬프트:</strong> ${safeQuery}</div>
      <div class="meta-item"><strong>작성 일시:</strong> ${createdStr}</div>
      <div class="meta-item"><strong>데이터 원천:</strong> NERP P&amp;L Parquet DB &amp; GfK M/S Trend</div>
    </div>
    <div class="content" id="reportBody"></div>
  </div>
  <div class="toast" id="copyToast">클립보드에 복사되었습니다.</div>
  <script id="rawMd" type="text/plain">${String(answerMarkdown || '').replace(/<\/script>/gi, '<\\/script>')}</script>
  <script>
    function showToast(msg) {
      const t = document.getElementById('copyToast');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2600);
    }

    function applyInlineStylesForCopy(rootEl) {
      rootEl.querySelectorAll('h2').forEach(el => {
        el.setAttribute('style', 'font-family: Malgun Gothic, Arial, sans-serif; font-size: 15pt; font-weight: bold; color: #0F172A; background-color: #F8FAFC; border-left: 5px solid #0F172A; padding: 8px 12px; margin: 18px 0 10px 0;');
      });
      rootEl.querySelectorAll('h3').forEach(el => {
        el.setAttribute('style', 'font-family: Malgun Gothic, Arial, sans-serif; font-size: 12pt; font-weight: bold; color: #0F172A; border-left: 4px solid #0D9488; padding-left: 8px; margin: 16px 0 8px 0;');
      });
      rootEl.querySelectorAll('h4').forEach(el => {
        el.setAttribute('style', 'font-family: Malgun Gothic, Arial, sans-serif; font-size: 10.5pt; font-weight: bold; color: #1E293B; margin: 12px 0 6px 0;');
      });
      rootEl.querySelectorAll('blockquote').forEach(el => {
        el.setAttribute('style', 'font-family: Malgun Gothic, Arial, sans-serif; font-size: 9.5pt; background-color: #F0FDFA; border-left: 4px solid #0D9488; padding: 10px 14px; margin: 10px 0 14px 0; color: #134E4A;');
      });
      rootEl.querySelectorAll('table').forEach(tbl => {
        tbl.setAttribute('style', 'width: 100%; border-collapse: collapse; margin: 12px 0 18px 0; font-family: Malgun Gothic, Arial, sans-serif; font-size: 9.5pt; border: 1px solid #CBD5E1;');
        const rows = tbl.querySelectorAll('tr');
        rows.forEach((tr, rIdx) => {
          const isTotalRow = /합계|Total/i.test(tr.innerText || '');
          tr.querySelectorAll('th').forEach(th => {
            th.setAttribute('style', 'background-color: #0F172A; color: #FFFFFF; padding: 8px 10px; border: 1px solid #1E293B; font-weight: bold; text-align: left;');
          });
          tr.querySelectorAll('td').forEach((td, cIdx) => {
            const txt = (td.innerText || '').trim();
            const isNum = cIdx > 0 && (/^[\\$\\+\\-]?[0-9,]+(\\.[0-9]+)?(%|%p|대|주|건)?$/.test(txt) || txt === '-');
            const bg = isTotalRow ? '#F1F5F9' : (rIdx % 2 === 0 ? '#F8FAFC' : '#FFFFFF');
            const fw = isTotalRow ? 'bold' : 'normal';
            const align = isNum ? 'right' : 'left';
            td.setAttribute('style', 'background-color: ' + bg + '; color: #0F172A; padding: 7px 10px; border: 1px solid #CBD5E1; text-align: ' + align + '; font-weight: ' + fw + ';');
          });
        });
      });
    }

    const raw = document.getElementById('rawMd').textContent;
    const bodyEl = document.getElementById('reportBody');
    bodyEl.innerHTML = marked.parse(raw);
    applyInlineStylesForCopy(bodyEl);

    async function copyRichHtml() {
      try {
        const clone = document.getElementById('executiveDocContainer').cloneNode(true);
        applyInlineStylesForCopy(clone);
        const htmlStr = clone.outerHTML;
        const plainStr = document.getElementById('executiveDocContainer').innerText;
        if (navigator.clipboard && window.ClipboardItem) {
          const item = new ClipboardItem({
            'text/html': new Blob([htmlStr], { type: 'text/html' }),
            'text/plain': new Blob([plainStr], { type: 'text/plain' })
          });
          await navigator.clipboard.write([item]);
          showToast('✅ 서식 유지 HTML이 복사되었습니다! (아웃룩/워드/노션에 바로 Ctrl+V 붙여넣기 가능)');
          return;
        }
        await navigator.clipboard.writeText(plainStr);
        showToast('✅ 클립보드에 텍스트가 복사되었습니다.');
      } catch (e) {
        const sel = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(document.getElementById('executiveDocContainer'));
        sel.removeAllRanges();
        sel.addRange(range);
        document.execCommand('copy');
        sel.removeAllRanges();
        showToast('✅ 서식 유지 문서가 복사되었습니다!');
      }
    }

    async function copyPlainText() {
      const text = document.getElementById('reportBody').innerText;
      try {
        await navigator.clipboard.writeText(text);
        showToast('✅ 순수 텍스트가 클립보드에 복사되었습니다!');
      } catch (e) {
        showToast('⚠️ 복사에 실패했습니다.');
      }
    }
  </script>
</body>
</html>`;
    fs.writeFileSync(htmlPath, htmlContent, 'utf8');
    generatedPaths.push(htmlPath);
  } catch (e) {
    console.warn('[SidecarEngine] Could not create HTML deliverable:', e.message);
  }

  // 2. If parquetData breakdown exists, also write a UTF-8 BOM CSV/Excel-ready table
  if (parquetData && Array.isArray(parquetData.breakdown) && parquetData.breakdown.length > 0) {
    try {
      const csvFileName = `${folderName}_Data_Extract.csv`;
      const csvPath = path.join(taskDir, csvFileName);
      const cols = Object.keys(parquetData.breakdown[0]);
      const lines = [cols.join(',')];
      for (const row of parquetData.breakdown) {
        lines.push(cols.map(c => {
          const val = row[c] === null || row[c] === undefined ? '' : String(row[c]);
          return val.includes(',') || val.includes('"') ? `"${val.replace(/"/g, '""')}"` : val;
        }).join(','));
      }
      fs.writeFileSync(csvPath, '\uFEFF' + lines.join('\r\n'), 'utf8');
      generatedPaths.push(csvPath);
    } catch (e) {
      console.warn('[SidecarEngine] Could not create CSV deliverable:', e.message);
    }
  }

  return generatedPaths;
}

/**
 * Ensures every Sales Portal prompt execution is archived into 99. Master Agent/Task/YYYYMMDD_...
 * following the Mandatory Auto-Archiving Rule.
 */
function ensureAutonomousArchive({ query, answerMarkdown, dispatchedAgents = [], parquetData = null }) {
  try {
    const todayStr = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const shortTitle = (query || '포털AI분석')
      .replace(/^\/grill-me\s*/i, '')
      .replace(/[^가-힣a-zA-Z0-9\s]/g, '')
      .trim()
      .split(/\s+/)
      .slice(0, 4)
      .join('_')
      .slice(0, 14) || '포털자율분석';

    const firstArchive = archiveTask({
      dateStr: todayStr,
      shortTitle,
      query,
      answerMarkdown,
      summary: (answerMarkdown || '').split('\n').slice(0, 6).join('\n'),
      dispatchedAgents: ['Master AI Agent', ...dispatchedAgents],
      artifactPaths: []
    });

    const extraFiles = generateDeliverableFiles({
      taskDir: firstArchive.taskDir,
      folderName: firstArchive.folderName,
      query,
      answerMarkdown,
      parquetData
    });

    if (extraFiles.length > 0) {
      archiveTask({
        dateStr: todayStr,
        shortTitle,
        query,
        answerMarkdown,
        summary: (answerMarkdown || '').split('\n').slice(0, 6).join('\n'),
        dispatchedAgents: ['Master AI Agent', ...dispatchedAgents],
        artifactPaths: extraFiles
      });
    }

    const scanned = scanTaskDeliverables(5);
    return scanned.find(t => t.folderName === firstArchive.folderName) || scanned[0] || null;
  } catch (err) {
    console.warn('[SidecarEngine] Auto-archive warning:', err.message);
    return null;
  }
}

/**
 * Ensures 00. TV Europe Sales Management Portal/index.html remains a clean dashboard search bar
 * (since the AXIS Prompt Pilot has been moved to AXIS_System_Architecture_Guide.html Tab 7),
 * and ensures sidecars.enabled = true in ~/.gemini/config/config.json.
 */
function syncPortalBridgeFiles() {
  const results = { portalSynced: false, configSynced: false };
  try {
    const portalDir = path.resolve(ROOT_DIR, '..', '00. TV Europe Sales Management Portal');
    if (fs.existsSync(portalDir)) {
      const targets = [portalDir];
      const portalPublicDir = path.join(portalDir, 'public');
      if (fs.existsSync(portalPublicDir)) targets.push(portalPublicDir);

      for (const dir of targets) {
        const idxPath = path.join(dir, 'index.html');
        if (fs.existsSync(idxPath)) {
          let html = fs.readFileSync(idxPath, 'utf8');
          if (html.includes('axis_portal_bridge.js') || html.includes('axis_portal_bridge.css')) {
            html = html
              .replace(/\s*<!-- AXIS Master Agent Unified AI Command Bar & Slide-over Drawer Bridge -->/g, '')
              .replace(/\s*<link[^>]*axis_portal_bridge\.css[^>]*>/g, '')
              .replace(/\s*<script[^>]*axis_portal_bridge\.js[^>]*><\/script>/g, '');
            fs.writeFileSync(idxPath, html, 'utf8');
          }
        }
      }
      results.portalSynced = true;
    }
  } catch (e) {
    console.warn('[SidecarEngine] Portal bridge sync notice:', e.message);
  }

  try {
    const configPath = path.join(os.homedir(), '.gemini', 'config', 'config.json');
    if (fs.existsSync(configPath)) {
      const raw = fs.readFileSync(configPath, 'utf8');
      const parsed = JSON.parse(raw);
      if (!parsed.sidecars || parsed.sidecars.enabled !== true) {
        parsed.sidecars = Object.assign({}, parsed.sidecars || {}, { enabled: true });
        fs.writeFileSync(configPath, JSON.stringify(parsed, null, 2), 'utf8');
      }
      results.configSynced = true;
    }
  } catch (e) {
    console.warn('[SidecarEngine] Config sidecars sync notice:', e.message);
  }

  return results;
}

module.exports = {
  BRAIN_DIR,
  buildAxisMasterPrompt,
  listBrainConversations,
  readConversationTranscript,
  scanTaskDeliverables,
  checkAgentApiAvailable,
  dispatchViaAgentApi,
  ensureAutonomousArchive,
  syncPortalBridgeFiles
};

