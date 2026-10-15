/**
 * Antigravity Session Bridge Watcher + Gemini AI Auto-Worker
 * 
 * 1. Monitors agent_bridge/inbox for tasks from the Web Dashboard.
 * 2. Loads master_data_bundle.json as Ground Truth context.
 * 3. Calls Google Gemini API server-side to reason over the data.
 * 4. Writes structured results to agent_bridge/outbox for the dashboard to render.
 * 
 * No hardcoded analysis engines — Gemini is the sole reasoning brain.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const { execFile } = require('child_process');

const BASE_DIR = __dirname;
const INBOX_DIR = path.join(BASE_DIR, 'agent_bridge', 'inbox');
const PROGRESS_DIR = path.join(BASE_DIR, 'agent_bridge', 'progress');
const OUTBOX_DIR = path.join(BASE_DIR, 'agent_bridge', 'outbox');

// Ensure directories exist
[INBOX_DIR, PROGRESS_DIR, OUTBOX_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

// ── Load Master Data Bundle (Ground Truth) ──────────────────────────────────
let bundleData = {};
try {
  const bundlePath = path.join(BASE_DIR, 'public', 'master_data_bundle.json');
  bundleData = JSON.parse(fs.readFileSync(bundlePath, 'utf8'));
  console.log(`📦 Master Data Bundle loaded (${(fs.statSync(bundlePath).size / 1024).toFixed(0)} KB)`);
} catch (e) {
  console.error('[Watcher] Failed to load master_data_bundle.json:', e.message);
}

// ── Load Strategic Reports Catalog (Knowledge Base) ────────────────────────
let strategicCatalog = { reports: [], slides: [] };
try {
  const catalogPath = path.join(BASE_DIR, 'data', 'strategic_reports_catalog.json');
  if (fs.existsSync(catalogPath)) {
    strategicCatalog = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
    console.log(`📚 Strategic Reports Knowledge Base loaded (${strategicCatalog.totalReports} reports, ${strategicCatalog.totalSlides} slides)`);
  }
} catch (e) {
  console.error('[Watcher] Failed to load strategic_reports_catalog.json:', e.message);
}

// ── Subsidiary Mapping (Prioritized Full Names + Standalone Code Matching) ──
const FULL_COUNTRY_MAP = [
  // Full names (Korean) - highest priority
  ['스위스', 'SWISS'], ['오스트리아', 'AG'], ['독일', 'DG'], ['영국', 'UK'],
  ['프랑스', 'FS'], ['이탈리아', 'IS'], ['스페인', 'ES'], ['폴란드', 'PL'],
  ['네덜란드', 'BN'], ['베네룩스', 'BN'], ['체코', 'CK'], ['슬로바키아', 'CK'],
  ['헝가리', 'MK'], ['그리스', 'HS'], ['포르투갈', 'PT'], ['루마니아', 'RO'],
  ['스웨덴', 'SW'], ['노르딕', 'SW'], ['북유럽', 'SW'], ['발틱', 'LA'],
  ['라트비아', 'LA'], ['러시아', 'RA'],
  // Full names (English)
  ['switzerland', 'SWISS'], ['swiss', 'SWISS'], ['austria', 'AG'],
  ['germany', 'DG'], ['france', 'FS'], ['italy', 'IS'], ['spain', 'ES'],
  ['poland', 'PL'], ['netherlands', 'BN'], ['benelux', 'BN'],
  ['czech', 'CK'], ['slovakia', 'CK'], ['hungary', 'MK'], ['greece', 'HS'],
  ['portugal', 'PT'], ['romania', 'RO'], ['sweden', 'SW'], ['nordic', 'SW'],
  ['baltic', 'LA'], ['latvia', 'LA'], ['russia', 'RA']
];

const CODE_MATCH_LIST = [
  'SWISS', 'LGEAG', 'LGEDG', 'LGEUK', 'LGEFS', 'LGEIS', 'LGEES', 'LGEPL',
  'LGEBN', 'LGECK', 'LGEMK', 'LGEHS', 'LGEPT', 'LGERO', 'LGESW', 'LGELA', 'LGERA',
  'AG', 'DG', 'UK', 'FS', 'IS', 'ES', 'PL', 'BN', 'CK', 'MK', 'HS', 'PT', 'RO', 'SW', 'LA', 'RA'
];

const SUBS_NAMES = {
  'AG': '오스트리아 법인 (LGEAG)', 'SWISS': '스위스 지점 (Swiss)',
  'DG': '독일 법인 (LGEDG)', 'UK': '영국 법인 (LGEUK)',
  'FS': '프랑스 법인 (LGEFS)', 'IS': '이탈리아 법인 (LGEIS)',
  'ES': '스페인 법인 (LGEES)', 'PL': '폴란드 법인 (LGEPL)',
  'BN': '베네룩스 법인 (LGEBN)', 'CK': '체코/슬로바키아 법인 (LGECK)',
  'MK': '헝가리 법인 (LGEMK)', 'HS': '그리스 법인 (LGEHS)',
  'PT': '포르투갈 법인 (LGEPT)', 'RO': '루마니아 법인 (LGERO)',
  'SW': '스웨덴/노르딕 법인 (LGESW)', 'LA': '발틱 법인 (LGELA)',
  'RA': '러시아 법인 (LGERA)'
};

function detectSubsidiary(queryText) {
  const q = (queryText || '').toLowerCase();

  // 1. Priority 1: Full country names (substring)
  for (const [name, code] of FULL_COUNTRY_MAP) {
    if (q.includes(name.toLowerCase())) {
      return code;
    }
  }

  // 2. Priority 2: Standalone corporate codes with word boundary (\b)
  for (const code of CODE_MATCH_LIST) {
    const regex = new RegExp(`\\b${code}\\b`, 'i');
    if (regex.test(queryText)) {
      return code.replace(/^LGE/, '');
    }
  }

  return null;
}

// ── Build Ground Truth Context for Gemini ───────────────────────────────────
function buildGroundTruth(queryText) {
  const q = (queryText || '').toLowerCase();
  const datasets = bundleData.datasets || {};

  // Detect target subsidiary using robust prioritized detector
  const targetSubCode = detectSubsidiary(queryText);
  const targetSubName = targetSubCode ? (SUBS_NAMES[targetSubCode] || targetSubCode) : '';

  const context = {
    asOf: "2026.08 NERP 결산 실적",
    overallKpi: datasets.kpi?.executiveInsights?.summary || {},
    regionalAlerts: datasets.kpi?.executiveInsights?.regional_rankings || {},
    fxRates: datasets.fx?.rates || {},
    priceSummary: datasets.priceTracker?.summary || {}
  };

  // P&L subsidiary data
  if (targetSubCode && datasets.pnlSubsidiaries?.[targetSubCode]) {
    const subPnl = datasets.pnlSubsidiaries[targetSubCode];
    let wosVal = 7.5;
    try {
      const riskList = datasets.kpi?.executiveInsights?.regional_rankings?.risk_wos || [];
      const rItem = riskList.find(r =>
        (targetSubCode === 'SWISS' && r.entity?.toLowerCase().includes('swiss')) ||
        r.entity?.toUpperCase().includes(targetSubCode)
      );
      if (rItem?.wos) wosVal = rItem.wos;
    } catch (e) {}

    context.targetSubsidiary = {
      code: targetSubCode,
      name: targetSubName,
      wos: wosVal,
      latestYear: subPnl.latestYear,
      latestMonth: subPnl.latestMonth,
      monthlyTrend: subPnl.monthlyTrend,
      kpi: subPnl.kpi
    };
  }

  // MS Trend Time-Series (2024~2026, 31 months)
  const msSeriesMap = datasets.msTrend?.timeSeries || {};
  const msTarget = targetSubCode || 'EU_TTL';
  if (msSeriesMap[msTarget]) {
    context.msTrendData = {
      targetRegion: msTarget,
      nameKr: msSeriesMap[msTarget].nameKr,
      metrics: msSeriesMap[msTarget].metrics
    };
  }

  // 2026 Product Lineup & Specs (MRGB, OLED, QNED, etc.)
  if (datasets.productLineup2026) {
    context.productLineup2026 = datasets.productLineup2026;
  }

  // Strategic Meeting Reports Knowledge Context (2025~2026 전략회의/PD회의)
  if (strategicCatalog && strategicCatalog.slides && strategicCatalog.slides.length > 0) {
    const matched = strategicCatalog.slides.filter(s => {
      const textMatch = targetSubCode && (s.subsidiary_tags || '').includes(targetSubCode);
      const oledMatch = q.includes('oled') && (s.product_tags || '').includes('OLED');
      const qnedMatch = q.includes('qned') && (s.product_tags || '').includes('QNED');
      return textMatch || oledMatch || qnedMatch;
    }).slice(0, 3);

    if (matched.length > 0) {
      context.strategicMeetingDecisions = matched.map(s => ({
        report: s.report_name,
        date: s.report_date,
        meetingType: s.meeting_type,
        slideNo: s.slide_no,
        title: s.slide_title,
        keyPoints: (s.content_text || '').split('\n').filter(l => l.trim()).slice(0, 3)
      }));
    }
  }

  return context;
}

// ── Parquet Live Query Engine (Python Subprocess) ───────────────────────────
const PYTHON_EXE = path.resolve(BASE_DIR, '..', '04. Price Tracker', 'python_env', 'python.exe');
const PARQUET_QUERY_SCRIPT = path.join(BASE_DIR, 'scripts', 'parquet_query.py');

// Detect if query requires detailed P&L analysis (segment/account/model level)
function parseDetailedIntent(queryText) {
  const q = (queryText || '').toLowerCase();

  // Subsidiary detection using robust detector
  const subCode = detectSubsidiary(queryText);
  if (!subCode) return null; // No specific subsidiary → skip parquet query

  // Segment keywords
  let segment = null;
  if (q.includes('mrgb') || q.includes('미니') || q.includes('마이크로')) segment = 'MRGB';
  else if (q.includes('oled') || q.includes('올레드')) segment = 'OLED';
  else if (q.includes('qned') || q.includes('큐넨')) segment = 'QNED';
  else if (q.includes('uhd')) segment = 'UHD';
  else if (q.includes('fhd')) segment = 'FHD';

  // GroupBy hints
  let groupby = null;
  if (q.includes('거래선') || q.includes('고객') || q.includes('account') || q.includes('채널') || q.includes('유통')) groupby = 'account';
  else if (q.includes('모델') || q.includes('model') || q.includes('제품')) groupby = 'model';
  else if (q.includes('세그먼트') || q.includes('segment') || q.includes('카테고리') || q.includes('제품군')) groupby = 'segment';
  else if (q.includes('인치') || q.includes('사이즈') || q.includes('inch')) groupby = 'inch';
  else if (q.includes('시리즈') || q.includes('series')) groupby = 'series';

  // If segment is specified but no groupby, default to account breakdown
  if (segment && !groupby) groupby = 'account';

  // Period
  let period = 'YTD';
  let month = null;
  const monthMatch = queryText.match(/(\d{1,2})\s*월/);
  if (monthMatch) { month = parseInt(monthMatch[1], 10); period = null; }
  else if (q.includes('l3m') || q.includes('3개월') || q.includes('최근 3') || q.includes('최근3')) period = 'L3M';
  else if (q.includes('당월') || q.includes('mtd')) period = 'MTD';
  else if (q.includes('6개월') || q.includes('l6m')) period = 'L6M';

  // Year
  let year = null;
  const yearMatch = queryText.match(/(20\d{2})/);
  if (yearMatch) year = parseInt(yearMatch[1], 10);

  // Determine if this needs detailed analysis (not just general overview)
  const needsDetail = segment || groupby ||
    q.includes('손익') || q.includes('매출') || q.includes('영업이익') || q.includes('한계이익') ||
    q.includes('마진') || q.includes('p&l') || q.includes('이익률');

  if (!needsDetail) return null;

  return { subCode, segment, groupby, period, month, year };
}

// Execute Parquet query via Python subprocess
function runParquetQuery(intent) {
  return new Promise((resolve) => {
    if (!fs.existsSync(PYTHON_EXE) || !fs.existsSync(PARQUET_QUERY_SCRIPT)) {
      console.warn('[ParquetQuery] Python env or script not found');
      resolve(null);
      return;
    }

    const args = [PARQUET_QUERY_SCRIPT, '--sub', intent.subCode];
    if (intent.year) args.push('--year', String(intent.year));
    if (intent.month) args.push('--month', String(intent.month));
    if (intent.period) args.push('--period', intent.period);
    if (intent.segment) args.push('--segment', intent.segment);
    if (intent.groupby) args.push('--groupby', intent.groupby);
    if (intent.groupby === 'model') args.push('--top', '10');

    console.log(`📊 [ParquetQuery] Executing: python ${args.join(' ')}`);

    execFile(PYTHON_EXE, args, { timeout: 15000, maxBuffer: 5 * 1024 * 1024 }, (err, stdout, stderr) => {
      if (err) {
        console.warn(`[ParquetQuery] Error: ${err.message}`);
        resolve(null);
        return;
      }
      try {
        const result = JSON.parse(stdout);
        if (result.success) {
          console.log(`📊 [ParquetQuery] Success: ${result.row_count} rows, total net_sales=$${result.total?.net_sales}`);
        }
        resolve(result);
      } catch (e) {
        console.warn(`[ParquetQuery] JSON parse error: ${e.message}`);
        resolve(null);
      }
    });
  });
}

// ── Gemini API Call (server-side, using Node.js https) ──────────────────────
function callGeminiAPI(queryText, groundTruth, apiKey, model = 'gemini-3.8-flash') {
  return new Promise((resolve, reject) => {
    const systemInstruction = `당신은 LG전자(LGE) TV 유럽영업본부의 수석 전략 참모 AI 에이전트(Master Orchestrator)입니다.
포털 산하 15개 전문 에이전트(05. TV P&L Analysis, 06. KPI Sheet, 04. Price Tracker, 08. MS Trend, 03. FX-Monitor, 10. 수익성 Simulator)의 실제 데이터베이스와 직결되어 있습니다.

[데이터 준수 원칙]
1. 반드시 아래 제공된 원천 팩트 데이터(Ground Truth Dataset)의 수치만을 신뢰하여 분석해야 합니다. 절대 허구의 실적 수치를 지어내거나 할루시네이션하지 마십시오.
   - P&L 지표: sales(Net Sales 매출액, 달러), mp(한계이익률 비율, 예: 0.285 = 28.5%), coi(영업이익률 비율, 예: 0.0586 = 5.86%, COI 금액 = sales * coi), sd(차감율)
   - KPI 지표: WOS(유통 재고 주수, 6~8주 적정, 8주 초과 시 위험 감지)
   - MS Trend 지표: y24(2024년 1~12월+연평균, 총 13개 값), y25(2025년 13개 값), y26(2026년 13개 값, 0인 항목은 미래 미확정 월)
     - lg_oled_ms: LG OLED 점유율, samsung_oled_ms: 삼성 OLED 점유율, sony_oled_ms: 소니 OLED 점유율
     - lg_total_ms: LG 전체 TV 점유율, samsung_total_ms: 삼성 전체 TV 점유율
     - market_oled_weight: 시장 내 OLED 비중
   - 비율 수치는 소수 (예: 0.379 = 37.9%)이며, 보고서에서는 반드시 %로 환산하여 표기하십시오.
   - 제품 라인업/스펙 지표: productLineup2026(MRGB, OLED, QNED, NanoCell의 세그먼트, 모델명, 인치대, 프로세서, 주사율, 백라이트 기술 등 원천 팩트 데이터)
   - Parquet 라이브 쿼리 데이터 (parquetLiveQuery): 원천 결산 데이터베이스(raw_data.parquet)로부터 직접 실시간 집계된 최우선(Highest Priority) 정밀 팩트 데이터입니다.
     - total: 전체 합계 객체 (qty 수량, gross_sales 총매출, sales_deduction 차감액, sd_pct 차감율%, net_sales 순매출, marginal_profit 한계이익, mp_pct 한계이익률%, operating_income 영업이익, opm_pct 영업이익률%)
     - breakdown: 거래선별/세그먼트별/모델별 상세 배열 (각 거래선/모델별 수량, 순매출, 한계이익, 한계이익률%, 영업이익, 영업이익률%, 매출비중% share_pct)
     - monthly_trend: 월별 추이 배열
     - parquetLiveQuery가 존재하면 반드시 이를 100% 최우선 활용하여, 상단에 전체 합계 요약, 중단에 거래선별/세그먼트별 정밀 비교 표(전체 합계 행 필수 포함), 월별 추이, 그리고 심층 경영 시사점을 포함한 최고급 비즈니스 보고서로 작성하십시오!
2. 보고서 문체: LG전자 임원 및 유럽영업본부장 보고에 적합하도록 정중하고 권위 있는 최고 수준의 비즈니스 한국어 마크다운으로 작성하십시오.
3. 사용자 질문에 정확히 부합하는 내용만 답변하십시오. 
   - 제품 라인업/스펙(MRGB, OLED, QNED 등)을 물으면 라인업과 스펙 특징을 상세한 표와 함께 분석 보고서로 답하십시오.
   - 점유율(M/S)을 물으면 점유율을, 손익(P&L)을 물으면 손익을 답하십시오. 절대 질문과 무관한 다른 영역의 데이터를 답변하지 마십시오.
4. 응답 형식: 반드시 아래 JSON 스키마 규격에 맞춰 JSON 형태로만 출력해야 합니다.
{
  "dispatchedAgents": ["ms-trend", "kpi-sheet"],
  "timeline": [
    { "step": 1, "agent": "에이전트명", "status": "completed", "desc": "작업 설명" }
  ],
  "answerMarkdown": "마크다운 문자열 (테이블, 불릿 등 자유 사용)",
  "artifact": {
    "title": "보고서 제목",
    "type": "markdown",
    "markdown": "answerMarkdown과 동일"
  }
}`;

    const requestBody = {
      contents: [{
        role: "user",
        parts: [{
          text: `[사용자 질의]: "${queryText}"\n\n[제공된 원천 팩트 데이터 (Ground Truth Dataset)]:\n${JSON.stringify(groundTruth, null, 2)}`
        }]
      }],
      systemInstruction: { parts: [{ text: systemInstruction }] },
      generationConfig: {
        temperature: 0.2,
        responseMimeType: "application/json"
      }
    };

    const bodyStr = JSON.stringify(requestBody);
    const candidateModels = [model, 'gemini-3.5-flash', 'gemini-3.8-flash', 'gemini-3-flash-preview', 'gemini-3.1-flash-lite'].filter(Boolean);
    const uniqueModels = [...new Set(candidateModels)];

    function tryModels(index = 0) {
      if (index >= uniqueModels.length) {
        return reject(new Error('All candidate Gemini models failed'));
      }
      const curModel = uniqueModels[index];
      console.log(`🤖 [Gemini] Requesting model [${index + 1}/${uniqueModels.length}]: ${curModel}...`);
      const urlPath = `/v1beta/models/${curModel}:generateContent?key=${apiKey}`;

      const options = {
        hostname: 'generativelanguage.googleapis.com',
        port: 443,
        path: urlPath,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(bodyStr)
        },
        timeout: 30000
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => { data += chunk; });
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            if (res.statusCode !== 200) {
              console.warn(`[Gemini] ${curModel} failed with HTTP ${res.statusCode}: ${json.error?.message}. Trying fallback...`);
              return tryModels(index + 1);
            }
            let text = json.candidates?.[0]?.content?.parts?.[0]?.text || '';
            text = text.replace(/^```json\s*/i, '').replace(/\s*```$/i, '').trim();
            const parsed = JSON.parse(text);
            if (!parsed.answerMarkdown && parsed.text) parsed.answerMarkdown = parsed.text;
            resolve(parsed);
          } catch (e) {
            console.warn(`[Gemini] ${curModel} parse error, trying next: ${e.message}`);
            return tryModels(index + 1);
          }
        });
      });

      req.on('timeout', () => {
        console.warn(`[Gemini] ${curModel} request timed out. Trying fallback...`);
        req.destroy();
        return tryModels(index + 1);
      });

      req.on('error', (err) => {
        console.warn(`[Gemini] Network error with ${curModel}: ${err.message}`);
        return tryModels(index + 1);
      });
      req.write(bodyStr);
      req.end();
    }

    tryModels(0);
  });
}

// ── Task Processor ──────────────────────────────────────────────────────────
async function processTask(taskId, content) {
  const query = content.query;
  const apiKey = content.apiKey || process.env.GEMINI_API_KEY || '';

  console.log(`\n🚨 [BRIDGE_WORKER] Task: ${taskId}`);
  console.log(`📝 Query: "${query}"`);
  console.log(`🔑 API Key: ${apiKey ? `${apiKey.substring(0, 8)}...` : '(없음)'}`);

  // Update progress: step 1 - received
  writeProgress(taskId, 1, "Antigravity Bridge", "질의를 수신하여 원천 데이터 컨텍스트를 구축하고 있습니다...");

  if (!apiKey || apiKey.length < 10) {
    console.log(`⚠️ [BRIDGE_WORKER] No API key for task ${taskId}. Leaving for frontend fallback.`);
    return; // No API key → frontend will use its own fallback
  }

  try {
    // Build ground truth context from data bundle
    const groundTruth = buildGroundTruth(query);

    // Check if detailed P&L query (segment/account/model) is requested
    const detailedIntent = parseDetailedIntent(query);
    if (detailedIntent) {
      writeProgress(taskId, 1, "Parquet Live Query", `${detailedIntent.subCode} 원천 Parquet 데이터베이스를 실시간 쿼리하고 있습니다...`);
      const liveData = await runParquetQuery(detailedIntent);
      if (liveData && liveData.success) {
        groundTruth.parquetLiveQuery = liveData;
        console.log(`📊 [BRIDGE_WORKER] Injected live Parquet data into Ground Truth (${liveData.row_count} rows, ${liveData.breakdown?.length || 0} breakdown rows)`);
      }
    }

    // Update progress: step 2 - calling Gemini
    writeProgress(taskId, 2, "Gemini 3.8 Flash", "Google Gemini AI가 원천 팩트 데이터를 분석하고 보고서를 작성하고 있습니다...");

    console.log(`🤖 [BRIDGE_WORKER] Calling Gemini API for task ${taskId}...`);
    const result = await callGeminiAPI(query, groundTruth, apiKey);

    // Ensure artifact has markdown fallback
    if (!result.artifact) {
      result.artifact = {
        title: "안티그래비티 AI 분석 보고서",
        type: "markdown",
        markdown: result.answerMarkdown
      };
    }

    // Prepend Parquet Live Query to timeline if executed
    if (groundTruth.parquetLiveQuery) {
      if (!result.dispatchedAgents?.includes('pnl-analysis')) {
        result.dispatchedAgents = ['pnl-analysis', ...(result.dispatchedAgents || [])];
      }
      result.timeline = [
        { step: 1, agent: "Parquet Live Query", status: "completed", desc: `${detailedIntent.subCode} 원천 Parquet(${groundTruth.parquetLiveQuery.row_count}행) 실시간 다차원 쿼리 완료` },
        ...(result.timeline || []).map((t, idx) => ({ ...t, step: idx + 2 }))
      ];
    }

    // Write final result to outbox
    const outboxFile = path.join(OUTBOX_DIR, `result_${taskId}.json`);
    const resultData = {
      taskId,
      dispatchedAgents: result.dispatchedAgents || [],
      timeline: result.timeline || [],
      answerMarkdown: result.answerMarkdown || '',
      artifact: result.artifact,
      completedAt: new Date().toISOString()
    };

    fs.writeFileSync(outboxFile, JSON.stringify(resultData, null, 2), 'utf8');

    // Clean up inbox file
    const inboxFile = path.join(INBOX_DIR, `${taskId}.json`);
    try { fs.unlinkSync(inboxFile); } catch (e) {}

    console.log(`✅ [BRIDGE_WORKER] Task ${taskId} completed! Result saved to outbox.`);

  } catch (err) {
    console.error(`❌ [BRIDGE_WORKER] Task ${taskId} failed:`, err.message);
    // Write error result so dashboard doesn't hang
    const outboxFile = path.join(OUTBOX_DIR, `result_${taskId}.json`);
    fs.writeFileSync(outboxFile, JSON.stringify({
      taskId,
      dispatchedAgents: [],
      timeline: [{ step: 1, agent: "Bridge Worker", status: "error", desc: err.message }],
      answerMarkdown: `⚠️ Gemini API 호출 중 오류가 발생했습니다: ${err.message}\n\n설정 패널에서 유효한 Google Gemini API Key를 입력해 주세요.`,
      artifact: { title: "오류", type: "markdown", markdown: `오류: ${err.message}` },
      completedAt: new Date().toISOString()
    }, null, 2), 'utf8');
  }
}

function writeProgress(taskId, step, agent, desc) {
  const progressFile = path.join(PROGRESS_DIR, `${taskId}.json`);
  fs.writeFileSync(progressFile, JSON.stringify({
    taskId, step, totalSteps: 3,
    currentAgent: agent, desc,
    timestamp: new Date().toISOString()
  }, null, 2), 'utf8');
}

// ── Inbox Polling Loop ──────────────────────────────────────────────────────
const processedTasks = new Set();

function checkInbox() {
  try {
    const files = fs.readdirSync(INBOX_DIR).filter(f => f.endsWith('.json'));
    for (const file of files) {
      const taskId = file.replace('.json', '');
      if (processedTasks.has(taskId)) continue;

      const filePath = path.join(INBOX_DIR, file);
      try {
        const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        processedTasks.add(taskId);

        // Process asynchronously (don't block polling)
        processTask(taskId, content).catch(err => {
          console.error(`[Watcher] Unhandled error processing ${taskId}:`, err);
        });

      } catch (err) {
        console.error(`[Watcher] Error reading ${file}:`, err);
      }
    }
  } catch (err) {
    console.error('[Watcher] Poll error:', err);
  }
}

// ── Startup ─────────────────────────────────────────────────────────────────
console.log('====================================================');
console.log('🤖 Antigravity Bridge Watcher + Gemini AI Worker');
console.log(`📂 Monitoring Inbox: ${INBOX_DIR}`);
console.log(`📦 Data Bundle: ${Object.keys(bundleData.datasets || {}).length} datasets loaded`);
console.log('====================================================');

setInterval(checkInbox, 400);
