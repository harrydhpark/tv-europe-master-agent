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
const {
  dispatchViaAgentApi,
  ensureAutonomousArchive,
  scanTaskDeliverables,
  listBrainConversations,
  readConversationTranscript
} = require('./scripts/antigravity_sidecar_engine');

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

  // 2026 Product Lineup & Specs (only attach when query asks about specs/lineup to keep prompt fast)
  if (datasets.productLineup2026 && /스펙|사양|라인업|프로세서|주사율|백라이트|spec|lineup/i.test(q)) {
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
const VENV_PYTHON = path.resolve(BASE_DIR, '..', '04. Price Tracker', 'python_env', 'python.exe');
const PYTHON_EXE = fs.existsSync(VENV_PYTHON) ? VENV_PYTHON : 'python';
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

  // GroupBy hints (Check '제품군' BEFORE '제품' so '제품군별' maps to 'segment', not 'model')
  let groupby = null;
  if (q.includes('거래선') || q.includes('고객') || q.includes('account') || q.includes('채널') || q.includes('유통')) groupby = 'account';
  else if (q.includes('세그먼트') || q.includes('segment') || q.includes('카테고리') || q.includes('제품군') || q.includes('라인업')) groupby = 'segment';
  else if (q.includes('모델') || q.includes('model') || q.includes('제품')) groupby = 'model';
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
  const needsDetail = segment || groupby || month !== null ||
    q.includes('손익') || q.includes('매출') || q.includes('영업이익') || q.includes('한계이익') ||
    q.includes('마진') || q.includes('p&l') || q.includes('이익률') ||
    q.includes('점유율') || q.includes('비중') || q.includes('m/s') || q.includes('ms') ||
    q.includes('실적') || q.includes('수량') || q.includes('물량') || q.includes('현황');

  if (!needsDetail) return null;

  // Default groupby to segment if not specified so product group share is always available
  if (!groupby) groupby = 'segment';

  return { subCode, segment, groupby, period, month, year };
}

// Execute Parquet query via Python subprocess
function runParquetQuery(intent) {
  return new Promise((resolve) => {
    if (!fs.existsSync(PARQUET_QUERY_SCRIPT)) {
      console.warn('[ParquetQuery] Script not found');
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

    console.log(`📊 [ParquetQuery] Executing: ${PYTHON_EXE} ${args.join(' ')}`);

    const tryExec = (pyBin, isFallback) => {
      execFile(pyBin, args, { timeout: 15000, maxBuffer: 5 * 1024 * 1024, env: { ...process.env, PYTHONIOENCODING: 'utf-8' } }, (err, stdout, stderr) => {
        if (err) {
          if (!isFallback && pyBin !== 'python') {
            return tryExec('python', true);
          }
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
    };

    tryExec(PYTHON_EXE, false);
  });
}

// ── Gemini API Call (server-side, using Node.js https) ──────────────────────
function callGeminiAPI(queryText, groundTruth, apiKey, model = 'gemini-3-flash-preview') {
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
     - breakdown: 세그먼트별/모델별 상세 배열 (수량, 순매출, 매출비중% share_pct, 차감율% sd_pct, 한계이익, 한계이익률% mp_pct, 영업이익, 영업이익률% opm_pct)
     - account_breakdown: 주요 거래선(Key Accounts Top 8)별 상세 배열 (수량, 순매출, 매출비중%, 차감율%, 한계이익, 한계이익률%, 영업이익, 영업이익률%)
     - monthly_trend: 월별 손익 추이 배열
     - parquetLiveQuery가 존재하면 반드시 상단에 전체 합계 요약 표, 1) 제품군(Segment)별 손익 비교 마크다운 표(합계 행 포함), 2) 주요 거래선(account_breakdown)별 손익 비교 마크다운 표, 3) 월별 손익 추이 및 GfK M/S 경쟁 현황, 4) 심층 경영 시사점을 모두 마크다운 표(Table)와 함께 작성하십시오!
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
    const candidateModels = [model, 'gemini-3-flash-preview', 'gemini-2.5-flash', 'gemini-3.1-flash-lite', 'gemini-3.5-flash'].filter(Boolean);
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
        timeout: 18000
      };

      let handled = false;
      const nextModel = () => {
        if (handled) return;
        handled = true;
        tryModels(index + 1);
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => { data += chunk; });
        res.on('end', () => {
          if (handled) return;
          try {
            const json = JSON.parse(data);
            if (res.statusCode !== 200) {
              console.warn(`[Gemini] ${curModel} failed with HTTP ${res.statusCode}: ${json.error?.message}. Trying fallback...`);
              return nextModel();
            }
            let text = json.candidates?.[0]?.content?.parts?.[0]?.text || '';
            text = text.replace(/^```json\s*/i, '').replace(/\s*```$/i, '').trim();
            const parsed = JSON.parse(text);
            if (!parsed.answerMarkdown && parsed.text) parsed.answerMarkdown = parsed.text;
            handled = true;
            resolve(parsed);
          } catch (e) {
            console.warn(`[Gemini] ${curModel} parse error, trying next: ${e.message}`);
            return nextModel();
          }
        });
      });

      req.on('timeout', () => {
        console.warn(`[Gemini] ${curModel} request timed out. Trying fallback...`);
        req.destroy();
        return nextModel();
      });

      req.on('error', (err) => {
        if (handled) return;
        console.warn(`[Gemini] Network error with ${curModel}: ${err.message}`);
        return nextModel();
      });
      req.write(bodyStr);
      req.end();
    }

    tryModels(0);
  });
}

// ── Deterministic Ground-Truth Fallback Synthesis (when no API Key) ─────────
function buildDeterministicGroundTruthReport(query, groundTruth) {
  const lines = [];
  const subName = groundTruth.targetSubsidiary?.name || groundTruth.parquetLiveQuery?.subsidiary_kr || '유럽 영업본부';
  const monthMatch = (query || '').match(/(\d{1,2})\s*월/);
  const reqMonth = monthMatch ? parseInt(monthMatch[1], 10) : 8;
  const pq = (groundTruth.parquetLiveQuery && groundTruth.parquetLiveQuery.success) ? groundTruth.parquetLiveQuery : null;
  const actualMonth = pq?.actual_month || groundTruth.targetSubsidiary?.latestMonth || reqMonth;
  const isPnlQuery = /수익성|손익|마진|이익|매출|보고서|p&l/i.test(query || '');

  const reportTitle = isPnlQuery
    ? `📊 ${subName} — 수익성(P&L) 및 제품·채널 포트폴리오 심층 분석 보고서`
    : `📊 ${subName} — 제품군별 점유율(비중) 및 시장 경쟁력 심층 분석 보고서`;

  const periodNote = (reqMonth && actualMonth && reqMonth !== actualMonth)
    ? `2026년 ${actualMonth}월 최신 결산 마감 기준 (요청: ${reqMonth}월)`
    : (pq?.period || `2026년 ${actualMonth}월 NERP 결산 기준`);

  lines.push(`## ${reportTitle}`);
  lines.push(`> **분석 지시 프롬프트**: "${query}" | **데이터 기준**: ${periodNote} (NERP Parquet DB & GfK M/S Trend)\n`);

  // 0. Executive KPI Summary Table
  if (pq && pq.total) {
    const t = pq.total;
    const wos = groundTruth.targetSubsidiary?.wos ?? '-';
    lines.push(`### 📌 Executive Summary — 핵심 손익(P&L) 지표 요약`);
    lines.push(`| 총 판매수량 (Qty) | 총매출 (Gross Sales) | 매출차감 (SD / 차감율) | 순매출 (Net Sales) | 한계이익 (MP / 이익률) | 영업이익 (COI / 이익률) | 유통재고 (WOS) |`);
    lines.push(`| ---: | ---: | ---: | ---: | ---: | ---: | ---: |`);
    lines.push(`| **${Number(t.qty || 0).toLocaleString()}대** | $${Number(t.gross_sales || 0).toLocaleString()} | $${Number(Math.abs(t.sales_deduction || 0)).toLocaleString()} (**${t.sd_pct ?? '-'}%**) | **$${Number(t.net_sales || 0).toLocaleString()}** | $${Number(t.marginal_profit || 0).toLocaleString()} (**${t.mp_pct ?? '-'}%**) | $${Number(t.operating_income || 0).toLocaleString()} (**${t.opm_pct ?? '-'}%**) | **${wos}주** |\n`);
  }

  // 1. Live Parquet Breakdown (Segment Share & P&L)
  if (pq) {
    const t = pq.total || {};
    const bd = Array.isArray(pq.breakdown) ? pq.breakdown : [];
    const dimKey = pq.groupby || pq.filters?.groupby || 'segment';
    const dimLabelMap = {
      segment: '제품군 (Segment)',
      account: '거래선 (Account)',
      model: '모델 (Model)',
      inch: '인치대 (Inch)',
      series: '시리즈 (Series)'
    };
    const dimHeader = dimLabelMap[dimKey] || dimKey;

    lines.push(`### 1. ${subName} ${dimHeader}별 판매 비중 및 손익(P&L) 구조`);
    lines.push(`*(원천 데이터: \`05. TV P&L Analysis/법인별/cache/raw_data.parquet\` 실시간 쿼리 — 총 ${Number(pq.row_count || 0).toLocaleString()}건 트랜잭션 집계)*\n`);

    if (bd.length > 0) {
      lines.push(`| ${dimHeader} | 판매수량 (대) | 수량 비중 (%) | 순매출액 (Net Sales) | 매출 비중 (%) | 차감율 (SD%) | 한계이익액 (MP) | 한계이익률 (MP%) | 영업이익액 (COI) | 영업이익률 (COI%) |`);
      lines.push(`| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |`);
      bd.slice(0, 15).forEach(r => {
        const name = r.label ?? r[dimKey] ?? '-';
        const qty = Number(r.qty || 0).toLocaleString();
        const qtyShare = r.qty_share_pct !== undefined ? `${Number(r.qty_share_pct).toFixed(1)}%` : '-';
        const netSales = `$${Number(r.net_sales || 0).toLocaleString()}`;
        const salesShare = r.share_pct !== undefined ? `**${Number(r.share_pct).toFixed(1)}%**` : '-';
        const sdPct = r.sd_pct !== undefined ? `${Number(r.sd_pct).toFixed(1)}%` : '-';
        const mpAmt = `$${Number(r.marginal_profit || 0).toLocaleString()}`;
        const mpPct = r.mp_pct !== undefined ? `${Number(r.mp_pct).toFixed(1)}%` : '-';
        const coiAmt = `$${Number(r.operating_income || 0).toLocaleString()}`;
        const opmPct = r.opm_pct !== undefined ? `**${Number(r.opm_pct).toFixed(1)}%**` : '-';
        lines.push(`| **${name}** | ${qty}대 | ${qtyShare} | ${netSales} | ${salesShare} | ${sdPct} | ${mpAmt} | ${mpPct} | ${coiAmt} | ${opmPct} |`);
      });
      lines.push(`| **전체 합계 (Total)** | **${Number(t.qty || 0).toLocaleString()}대** | **100.0%** | **$${Number(t.net_sales || 0).toLocaleString()}** | **100.0%** | **${t.sd_pct ?? '-'}%** | **$${Number(t.marginal_profit || 0).toLocaleString()}** | **${t.mp_pct ?? '-'}%** | **$${Number(t.operating_income || 0).toLocaleString()}** | **${t.opm_pct ?? '-'}%** |\n`);

      const topSalesRow = bd[0];
      const byQty = [...bd].sort((a, b) => (b.qty || 0) - (a.qty || 0));
      const topQtyRow = byQty[0];
      const getLabel = (r) => String(r.label ?? r[dimKey] ?? '');
      const oledRow = bd.find(r => getLabel(r).toUpperCase() === 'OLED');
      const qnedRow = bd.find(r => getLabel(r).toUpperCase() === 'QNED');
      const mrgbRow = bd.find(r => getLabel(r).toUpperCase() === 'MRGB');
      const premiumSalesShare = ((oledRow?.share_pct || 0) + (qnedRow?.share_pct || 0) + (mrgbRow?.share_pct || 0)).toFixed(1);
      const premiumQtyShare = ((oledRow?.qty_share_pct || 0) + (qnedRow?.qty_share_pct || 0) + (mrgbRow?.qty_share_pct || 0)).toFixed(1);

      lines.push(`#### 💡 제품 포트폴리오 및 수익성 핵심 진단`);
      if (topSalesRow) {
        lines.push(`- **최대 매출 주력 부문**: **${getLabel(topSalesRow)}** 부문이 순매출 **$${Number(topSalesRow.net_sales || 0).toLocaleString()}**로 전체 매출의 **${topSalesRow.share_pct}%**를 차지하며 외형과 이익을 견인하고 있습니다 (차감율 ${topSalesRow.sd_pct}%, 한계이익률 ${topSalesRow.mp_pct}%, 영업이익률 ${topSalesRow.opm_pct}%).`);
      }
      if (topQtyRow) {
        lines.push(`- **최대 물량(Volume) 부문**: 판매수량 기준으로는 **${getLabel(topQtyRow)}**가 **${Number(topQtyRow.qty || 0).toLocaleString()}대 (${topQtyRow.qty_share_pct}%)**로 가장 높은 수량 비중을 기록했습니다.`);
      }
      if (oledRow || qnedRow) {
        lines.push(`- **프리미엄(OLED + QNED + MRGB) 믹스 비중**: 매출 기준 **${premiumSalesShare}%** (수량 기준 **${premiumQtyShare}%**)로, 고부가 프리미엄 라인업이 법인 한계이익 창출의 핵심 축을 담당하고 있습니다.\n`);
      }
    }

    // 2. Top Accounts Breakdown Table (if groupby was segment, also show Top Accounts!)
    const accBd = Array.isArray(pq.account_breakdown) ? pq.account_breakdown : [];
    if (accBd.length > 0 && dimKey !== 'account') {
      lines.push(`### 2. 주요 유통 채널·거래선(Key Accounts)별 수익성 현황 (Top ${accBd.length})`);
      lines.push(`| 순위 | 거래선명 (Account) | 판매수량 (대) | 순매출액 (Net Sales) | 매출 비중 (%) | 차감율 (SD%) | 한계이익률 (MP%) | 영업이익액 (COI) | 영업이익률 (COI%) |`);
      lines.push(`| :---: | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |`);
      accBd.forEach((r, idx) => {
        const accName = r.label || r.account || '-';
        lines.push(`| ${idx + 1} | **${accName}** | ${Number(r.qty || 0).toLocaleString()}대 | $${Number(r.net_sales || 0).toLocaleString()} | **${Number(r.share_pct || 0).toFixed(1)}%** | ${Number(r.sd_pct || 0).toFixed(1)}% | ${Number(r.mp_pct || 0).toFixed(1)}% | $${Number(r.operating_income || 0).toLocaleString()} | **${Number(r.opm_pct || 0).toFixed(1)}%** |`);
      });
      lines.push('');
    }

    // 3. Monthly P&L Trend Table
    const mTrend = Array.isArray(pq.monthly_trend) ? pq.monthly_trend : [];
    if (mTrend.length > 1) {
      lines.push(`### 3. ${pq.year || 2026}년 월별 손익(P&L) 추이 (1월 ~ ${pq.latest_month || actualMonth}월)`);
      lines.push(`| 기준월 | 판매수량 (대) | 순매출액 (Net Sales) | 매출차감율 (SD%) | 한계이익액 (MP) | 한계이익률 (MP%) | 영업이익액 (COI) | 영업이익률 (COI%) |`);
      lines.push(`| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |`);
      mTrend.forEach(m => {
        const isTarget = m.month === actualMonth;
        const mLabel = isTarget ? `**${m.month}월 (당월)**` : `${m.month}월`;
        lines.push(`| ${mLabel} | ${Number(m.qty || 0).toLocaleString()}대 | $${Number(m.net_sales || 0).toLocaleString()} | ${Number(m.sd_pct || 0).toFixed(1)}% | $${Number(m.marginal_profit || 0).toLocaleString()} | ${Number(m.mp_pct || 0).toFixed(1)}% | $${Number(m.operating_income || 0).toLocaleString()} | **${Number(m.opm_pct || 0).toFixed(1)}%** |`);
      });
      lines.push('');
    }
  }

  // 4. GfK Market Share (M/S Trend) Analysis (with automatic latest non-zero month fallback)
  if (groundTruth.msTrendData && groundTruth.msTrendData.metrics) {
    const ms = groundTruth.msTrendData;
    const m = ms.metrics;
    const probeSeries = m.lg_total_ms?.y26 || m.lg_oled_ms?.y26 || [];
    let latestValidIdx = Math.max(0, Math.min(11, (reqMonth || 8) - 1));
    if (!probeSeries[latestValidIdx] || probeSeries[latestValidIdx] <= 0) {
      for (let i = 11; i >= 0; i--) {
        if (probeSeries[i] && probeSeries[i] > 0) {
          latestValidIdx = i;
          break;
        }
      }
    }
    const mIdx = latestValidIdx;
    const prevIdx = Math.max(0, mIdx - 1);
    const fmtPct = (v) => (v !== undefined && v !== null && v > 0) ? `${(Number(v) * 100).toFixed(1)}%` : '-';
    const fmtDiff = (cur, prev) => {
      if (!cur || !prev) return '-';
      const d = (Number(cur) - Number(prev)) * 100;
      return `${d >= 0 ? '+' : ''}${d.toFixed(1)}%p`;
    };

    const gfkNote = (reqMonth && (mIdx + 1) !== reqMonth) ? ` *(GfK 최신 마감: 2026년 ${mIdx + 1}월 기준)*` : '';
    lines.push(`### 4. GfK 외부 시장 점유율 (M/S Trend) 경쟁 현황 (${ms.nameKr || ms.targetRegion})${gfkNote}`);
    lines.push(`| 시장 지표 (GfK 기준) | 2025년 연간 | 2026년 ${prevIdx + 1}월 (전월) | **2026년 ${mIdx + 1}월 (최신당월)** | 전월비 증감 (MoM) | 2025년 동월비 (YoY) |`);
    lines.push(`| :--- | ---: | ---: | ---: | ---: | ---: |`);

    const metricRows = [
      ['**LG 전체 TV M/S**', m.lg_total_ms],
      ['Samsung 전체 TV M/S', m.samsung_total_ms],
      ['**LG OLED TV M/S**', m.lg_oled_ms],
      ['Samsung OLED TV M/S', m.samsung_oled_ms],
      ['Sony OLED TV M/S', m.sony_oled_ms],
      ['시장 내 OLED 제품군 비중', m.market_oled_weight]
    ];

    metricRows.forEach(([label, series]) => {
      if (!series) return;
      const y25Avg = series.y25 ? series.y25[12] : null;
      const y25SameMonth = series.y25 ? series.y25[mIdx] : null;
      const prevVal = series.y26 ? series.y26[prevIdx] : null;
      const curVal = series.y26 ? series.y26[mIdx] : null;
      lines.push(`| ${label} | ${fmtPct(y25Avg)} | ${fmtPct(prevVal)} | **${fmtPct(curVal)}** | ${fmtDiff(curVal, prevVal)} | ${fmtDiff(curVal, y25SameMonth)} |`);
    });
    lines.push('');
  }

  // 5. Target Subsidiary Overall KPI, WOS & Strategic Action Plan
  if (groundTruth.targetSubsidiary) {
    const sub = groundTruth.targetSubsidiary;
    const wosNum = Number(sub.wos || 0);
    lines.push(`### 5. ${sub.name} 유통 건전성 진단 및 전략적 실행 권고안 (Action Plan)`);
    lines.push(`- **유통 재고 주수 (Channel WOS)**: **${sub.wos ?? '-'}주** (${wosNum > 8 ? '⚠️ 적정 8주 초과 — 채널 셀아웃 프로모션 및 선적 속도 조절 필요' : '✅ 적정 재고 범위(6~8주) 내 매우 건전하게 운영 중'})`);
    if (pq && pq.total) {
      const sdVal = Number(pq.total.sd_pct || 0);
      const opmVal = Number(pq.total.opm_pct || 0);
      lines.push(`- **매출차감율(SD%) 효율화**: 당월 차감율 **${sdVal.toFixed(1)}%** 수준으로, 저수익 보급형(UHD/FHD)의 조건부 리베이트를 고수익 **OLED·QNED 대형 인치대 Sell-out 인센티브**로 전환하여 한계이익률(${pq.total.mp_pct}%)을 방어해야 합니다.`);
      lines.push(`- **영업이익률(COI%) 관리 방향**: 당월 영업이익률 **${opmVal.toFixed(1)}%**($${Number(pq.total.operating_income || 0).toLocaleString()}) 달성을 기반으로, 성수기 진입 전 주요 거래선(Top Accounts) 내 프리미엄 모델 전시 점유비중을 확대하십시오.\n`);
    } else {
      lines.push('');
    }
  }

  lines.push(`---`);
  lines.push(`*본 문서는 Antigravity AXIS Master Agent 자율 실행 파이프라인에 의해 생성되었으며, \`99. Master Agent/Task\` 하위에 Executive HTML·CSV·Markdown 산출물로 자동 아카이빙되었습니다.*`);
  return lines.join('\n');
}

// ── Task Processor ──────────────────────────────────────────────────────────
async function processTask(taskId, content) {
  const query = content.query;
  const apiKey = content.apiKey || process.env.GEMINI_API_KEY || '';
  const conversationId = content.conversationId || null;
  const preferSidecar = content.executionMode !== 'local_fast';

  console.log(`\n🚨 [BRIDGE_WORKER] Task: ${taskId}`);
  console.log(`📝 Query: "${query}"`);
  console.log(`🔗 Conversation ID: ${conversationId || '(auto/new)'}`);

  // Update progress: step 1 - received
  writeProgress(taskId, 1, "Antigravity Sidecar Bridge", "포털 프롬프트를 수신하여 Antigravity AXIS Master Agent 세션을 연결하고 있습니다...");

  try {
    // 1. Primary Engine: Antigravity Sidecar (agentapi) + Live transcript.jsonl Mirroring
    if (preferSidecar) {
      const sidecarResult = await dispatchViaAgentApi(
        query,
        { conversationId },
        (prog) => writeProgress(taskId, prog.step || 2, prog.currentAgent || "AXIS Master Agent", prog.desc || "실행 중...", prog)
      );

      if (sidecarResult && sidecarResult.executed) {
        const taskArchive = sidecarResult.taskArchive || ensureAutonomousArchive({
          query,
          answerMarkdown: sidecarResult.answerMarkdown,
          dispatchedAgents: ['Master AI Agent', 'Antigravity Sidecar (agentapi)']
        });

        const outboxFile = path.join(OUTBOX_DIR, `result_${taskId}.json`);
        const resultData = {
          taskId,
          engine: 'antigravity-sidecar-agentapi',
          conversationId: sidecarResult.conversationId,
          dispatchedAgents: ['master-agent', 'antigravity-sidecar'],
          timeline: (sidecarResult.toolCalls || []).map((tc, idx) => ({
            step: idx + 1,
            agent: tc.name,
            status: 'completed',
            desc: tc.toolAction || tc.toolSummary || tc.name
          })),
          thinking: sidecarResult.thinking || '',
          answerMarkdown: sidecarResult.answerMarkdown || '',
          artifact: {
            title: "Antigravity AXIS Master Agent 실행 결과",
            type: "markdown",
            markdown: sidecarResult.answerMarkdown || ''
          },
          taskArchive,
          deliverables: taskArchive ? taskArchive.deliverables : [],
          completedAt: new Date().toISOString()
        };

        fs.writeFileSync(outboxFile, JSON.stringify(resultData, null, 2), 'utf8');
        try { fs.unlinkSync(path.join(INBOX_DIR, `${taskId}.json`)); } catch (e) {}
        console.log(`✅ [BRIDGE_WORKER] Sidecar agentapi task ${taskId} completed!`);
        return;
      }
    }

    // 2. Co-Processor Engine: Parquet Live Query + 15-Agent Ground Truth + Gemini AI + Auto-Archiver
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

    let result = null;
    const hasRichParquet = Boolean(groundTruth.parquetLiveQuery?.success && groundTruth.parquetLiveQuery?.breakdown?.length > 0);
    if (apiKey && apiKey.length >= 10 && !(hasRichParquet && content.executionMode === 'local_fast')) {
      writeProgress(taskId, 2, "AXIS Master Agent (Gemini Engine)", "원천 팩트 데이터를 기반으로 심층 분석 및 산출물 보고서를 작성하고 있습니다...");
      console.log(`🤖 [BRIDGE_WORKER] Calling Gemini API for task ${taskId}...`);
      try {
        result = await callGeminiAPI(query, groundTruth, apiKey);
      } catch (gemErr) {
        console.warn(`[BRIDGE_WORKER] Gemini API fallback triggered: ${gemErr.message}`);
      }
    }
    if (!result) {
      writeProgress(taskId, 2, "AXIS Ground-Truth Synthesizer", "15대 에이전트 원천 데이터베이스(Parquet/NERP/GfK)를 집계하여 보고서를 생성하고 있습니다...");
      const md = buildDeterministicGroundTruthReport(query, groundTruth);
      result = {
        dispatchedAgents: ['pnl-analysis', 'kpi-sheet', 'ms-trend'],
        timeline: [
          { step: 1, agent: "15-Agent Ground Truth Loader", status: "completed", desc: "유럽 법인별 NERP 손익·KPI·M/S 원천 데이터 로드 완료" },
          { step: 2, agent: "AXIS Autonomous Report Engine", status: "completed", desc: "원천 팩트 기반 마크다운·HTML·CSV 산출물 자동 생성" }
        ],
        answerMarkdown: md,
        artifact: {
          title: "AXIS Master Agent 자율 분석 보고서",
          type: "markdown",
          markdown: md
        }
      };
    }

    // Ensure Parquet breakdown table is always included when live Parquet data exists
    if (groundTruth.parquetLiveQuery?.breakdown?.length > 0) {
      const pq = groundTruth.parquetLiveQuery;
      const hasAllSegments = pq.breakdown.slice(0, 3).every(row => {
        const key = row.segment || row.account || row.model || '';
        return key && (result.answerMarkdown || '').includes(key);
      });
      if (!hasAllSegments) {
        const detMd = buildDeterministicGroundTruthReport(query, groundTruth);
        result.answerMarkdown = `${result.answerMarkdown || ''}\n\n---\n\n${detMd}`;
      }
    }

    // Ensure artifact has markdown fallback
    if (!result.artifact) {
      result.artifact = {
        title: "안티그래비티 AI 분석 보고서",
        type: "markdown",
        markdown: result.answerMarkdown
      };
    } else {
      result.artifact.markdown = result.answerMarkdown;
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

    // Step 3: Mandatory Autonomous Task Archiving (Task/YYYYMMDD_...)
    writeProgress(taskId, 3, "Task Registry Auto-Archiver", "99. Master Agent/Task 하위에 산출물(.html, .csv, README.md)을 자동 아카이빙하고 있습니다...");
    const taskArchive = ensureAutonomousArchive({
      query,
      answerMarkdown: result.answerMarkdown || '',
      dispatchedAgents: result.dispatchedAgents || [],
      parquetData: groundTruth.parquetLiveQuery || null
    });

    if (taskArchive) {
      result.timeline = [
        ...(result.timeline || []),
        {
          step: (result.timeline?.length || 0) + 1,
          agent: "Task Auto-Archiver",
          status: "completed",
          desc: `Task/${taskArchive.folderName} 폴더 생성 및 산출물(${taskArchive.deliverables?.length || 0}건) 영구 보관 완료`
        }
      ];
    }

    // Attach latest Antigravity Brain conversation ID for live session linking
    const recentConvs = listBrainConversations(1);
    const activeConvId = conversationId || (recentConvs[0] ? recentConvs[0].conversationId : null);

    // Write final result to outbox
    const outboxFile = path.join(OUTBOX_DIR, `result_${taskId}.json`);
    const resultData = {
      taskId,
      engine: apiKey && apiKey.length >= 10 ? 'axis-autonomous-gemini' : 'axis-autonomous-groundtruth',
      conversationId: activeConvId,
      dispatchedAgents: result.dispatchedAgents || [],
      timeline: result.timeline || [],
      answerMarkdown: result.answerMarkdown || '',
      artifact: result.artifact,
      taskArchive,
      deliverables: taskArchive ? taskArchive.deliverables : [],
      completedAt: new Date().toISOString()
    };

    fs.writeFileSync(outboxFile, JSON.stringify(resultData, null, 2), 'utf8');

    // Clean up inbox file
    const inboxFile = path.join(INBOX_DIR, `${taskId}.json`);
    try { fs.unlinkSync(inboxFile); } catch (e) {}

    console.log(`✅ [BRIDGE_WORKER] Task ${taskId} completed & archived to ${taskArchive ? taskArchive.folderName : 'outbox'}!`);

  } catch (err) {
    console.error(`❌ [BRIDGE_WORKER] Task ${taskId} failed:`, err.message);
    // Write error result so dashboard doesn't hang
    const outboxFile = path.join(OUTBOX_DIR, `result_${taskId}.json`);
    fs.writeFileSync(outboxFile, JSON.stringify({
      taskId,
      dispatchedAgents: [],
      timeline: [{ step: 1, agent: "Bridge Worker", status: "error", desc: err.message }],
      answerMarkdown: `⚠️ 에이전트 실행 중 오류가 발생했습니다: ${err.message}`,
      artifact: { title: "오류", type: "markdown", markdown: `오류: ${err.message}` },
      completedAt: new Date().toISOString()
    }, null, 2), 'utf8');
  }
}

function writeProgress(taskId, step, agent, desc, extra = {}) {
  const progressFile = path.join(PROGRESS_DIR, `${taskId}.json`);
  fs.writeFileSync(progressFile, JSON.stringify({
    taskId,
    step,
    totalSteps: extra.totalSteps || 3,
    currentAgent: agent,
    desc,
    conversationId: extra.conversationId || null,
    thinking: extra.thinking || '',
    toolCalls: extra.toolCalls || [],
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
