/**
 * TV Europe Sales Master AI Agent - Data Bundle Compiler
 * Bundles latest normalized datasets from sibling folders into a static JSON for Firebase Hosting.
 */

const fs = require('fs');
const path = require('path');
const { AGENTS, getAgentStatusSummary } = require('./agentRegistry');

const PUBLIC_DIR = path.resolve(__dirname, 'public');
const OUTPUT_BUNDLE_PATH = path.join(PUBLIC_DIR, 'master_data_bundle.json');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function safeReadJson(relPath, defaultValue = null) {
  try {
    const fullPath = path.resolve(__dirname, relPath);
    if (fs.existsSync(fullPath)) {
      const content = fs.readFileSync(fullPath, 'utf8');
      return JSON.parse(content);
    }
  } catch (e) {
    console.warn(`[build_bundle] Warning reading ${relPath}: ${e.message}`);
  }
  return defaultValue;
}

function buildBundle() {
  console.log('🚀 [Master Agent] Compiling multi-agent static bundle...');
  ensureDir(PUBLIC_DIR);

  const bundle = {
    compiledAt: new Date().toISOString(),
    version: "1.0.0",
    agentsStatus: getAgentStatusSummary(__dirname),
    datasets: {}
  };

  // 1. KPI Sheet
  console.log('  - Ingesting KPI Sheet metrics & insights...');
  bundle.datasets.kpi = {
    executiveInsights: safeReadJson('../06. KPI Sheet/executive_insights.json', {}),
    buildMetrics: safeReadJson('../06. KPI Sheet/build_metrics.json', {}),
    pipelineStatus: safeReadJson('../06. KPI Sheet/pipeline_status.json', {})
  };

  // 2. Price Tracker
  console.log('  - Ingesting Price Tracker summary & anomalies...');
  const anomalyFiles = [];
  const priceDataDir = path.resolve(__dirname, '../04. Price Tracker/data');
  if (fs.existsSync(priceDataDir)) {
    const files = fs.readdirSync(priceDataDir);
    const anomalies = files.filter(f => f.startsWith('anomaly_report_')).sort().reverse();
    if (anomalies.length > 0) {
      bundle.datasets.priceTracker = {
        summary: safeReadJson(`../04. Price Tracker/data/${anomalies[0]}`, {}),
        latestAnomalyFile: anomalies[0]
      };
    }
  }
  if (!bundle.datasets.priceTracker) {
    bundle.datasets.priceTracker = {
      summary: safeReadJson('../04. Price Tracker/data/executive_summary_data.json', {})
    };
  }

  // 3. FX-Monitor
  console.log('  - Ingesting FX-Monitor real rates & commentary...');
  bundle.datasets.fx = {
    rates: safeReadJson('../03. FX-Monitor-main/data/real_rates.json', {}),
    commentaries: safeReadJson('../03. FX-Monitor-main/data/commentaries.json', {})
  };

  // 4. MS Trend
  console.log('  - Ingesting MS Trend insights, diff & time-series...');
  const msRaw = safeReadJson('../08. MS Trend/ms_trend_data.json', {});
  const msTimeSeries = {};
  if (msRaw.regions) {
    const regionsToExtract = [
      { key: '유럽', code: 'EU' },
      { key: 'Switzerland', code: 'SWISS' },
      { key: 'AG', code: 'AG' },
      { key: 'DG', code: 'DG' },
      { key: 'UK (2)', code: 'UK' },
      { key: 'FS', code: 'FS' },
      { key: 'IS', code: 'IS' },
      { key: 'ES', code: 'ES' },
      { key: 'PL', code: 'PL' },
      { key: 'BN', code: 'BN' },
      { key: 'Netherlands', code: 'NL' },
      { key: 'Belgium', code: 'BE' },
      { key: 'CZ', code: 'CZ' },
      { key: 'HS', code: 'HS' },
      { key: 'RO', code: 'RO' },
      { key: 'PT', code: 'PT' },
      { key: 'SW (2)', code: 'SW' }
    ];

    regionsToExtract.forEach(({ key, code }) => {
      const reg = msRaw.regions[key];
      if (!reg || !reg.data) return;
      msTimeSeries[code] = {
        regionKey: key,
        nameEn: reg.region_name_en,
        nameKr: reg.region_name_kr,
        metrics: {}
      };

      reg.data.forEach(r => {
        const lbls = (r.labels || []).filter(Boolean).join(' ');
        let mKey = null;
        if (r.index === 38) mKey = 'lg_oled_ms';
        else if (r.index === 68) mKey = 'samsung_oled_ms';
        else if (r.index === 83 || r.index === 96) { if (!msTimeSeries[code].metrics['sony_oled_ms']) mKey = 'sony_oled_ms'; }
        else if (r.index === 109) mKey = 'philips_oled_ms';
        else if (r.index === 122) mKey = 'panasonic_oled_ms';
        else if (r.index === 13) mKey = 'market_oled_weight';
        else if (r.index === 34) mKey = 'lg_oled_sales';
        else if (r.index === 64) mKey = 'samsung_oled_sales';
        else if (r.index === 27) mKey = 'lg_total_ms';
        else if (r.index === 60) mKey = 'samsung_total_ms';

        if (mKey) {
          msTimeSeries[code].metrics[mKey] = {
            index: r.index,
            label: lbls,
            y24: r.y24,
            y25: r.y25,
            y26: r.y26
          };
        }
      });
    });
  }

  bundle.datasets.msTrend = {
    insights: safeReadJson('../08. MS Trend/ms_trend_insights.json', {}),
    diff: safeReadJson('../08. MS Trend/ms_trend_diff.json', {}),
    timeSeries: msTimeSeries
  };

  // 5. Advance Profitability (Sample / Summary to keep bundle lean)
  console.log('  - Ingesting Advance Profitability data...');
  const advProfit = safeReadJson('../09. 선행수익성/advance_profitability_data.json', null);
  if (advProfit) {
    bundle.datasets.advanceProfitability = {
      summary: advProfit.summary || { count: Array.isArray(advProfit) ? advProfit.length : 0 },
      sample: Array.isArray(advProfit) ? advProfit.slice(0, 50) : advProfit
    };
  }

  // 6. Real TV P&L Subsidiary Reports (All available European entities)
  console.log('  - Ingesting TV P&L subsidiary real reports (15 European countries)...');
  const { RealDataEngine } = require('./realDataEngine');
  const realEngine = new RealDataEngine(__dirname);
  bundle.datasets.pnlSubsidiaries = {};

  const pnlFolders = [
    { code: 'AG', folder: '01. AG' },
    { code: 'BN', folder: '02. BN' },
    { code: 'CK', folder: '03. CK' },
    { code: 'SWISS', folder: '05. Swiss' },
    { code: 'ES', folder: '06. ES' },
    { code: 'FS', folder: '07. FS' },
    { code: 'HS', folder: '08. HS' },
    { code: 'IS', folder: '09. IS' },
    { code: 'LA', folder: '10. LA' },
    { code: 'MK', folder: '11. MK' },
    { code: 'PL', folder: '12. PL' },
    { code: 'PT', folder: '13. PT' },
    { code: 'RO', folder: '14. RO' },
    { code: 'SW', folder: '15. SW' },
    { code: 'UK', folder: '16. UK' }
  ];

  pnlFolders.forEach(({ code, folder }) => {
    const pnl = realEngine.getRealPnlData(folder);
    if (pnl && pnl.DATA && pnl.DATA.standard) {
      bundle.datasets.pnlSubsidiaries[code] = {
        latestYear: pnl.LATEST_YEAR,
        latestMonth: pnl.LATEST_MONTH,
        monthlyTrend: (pnl.DATA.standard.monthly_trend || []).slice(-6),
        kpi: pnl.DATA.standard.kpi
      };
    }
  });

  // Write bundle to public
  const jsonStr = JSON.stringify(bundle, null, 2);
  fs.writeFileSync(OUTPUT_BUNDLE_PATH, jsonStr, 'utf8');

  const sizeKb = (Buffer.byteLength(jsonStr, 'utf8') / 1024).toFixed(1);
  console.log(`✅ [Master Agent] Bundle successfully created: ${OUTPUT_BUNDLE_PATH} (${sizeKb} KB)`);
}

if (require.main === module) {
  buildBundle();
}

module.exports = { buildBundle };
