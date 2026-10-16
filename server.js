/**
 * TV Europe Sales Master AI Agent - Express API Server & Pipeline Runner
 * Serves web interface, handles multi-agent orchestration, and triggers CLI pipelines safely.
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const { AGENTS, getAgentStatusSummary, getAgentById } = require('./agentRegistry');
const { LocalRuleEngine } = require('./localRuleEngine');
const {
  listBrainConversations,
  readConversationTranscript,
  scanTaskDeliverables,
  syncPortalBridgeFiles
} = require('./scripts/antigravity_sidecar_engine');

// Auto-sync Sales Portal Bridge UI assets & Sidecar config on load
syncPortalBridgeFiles();

const app = express();
const PORT = process.env.PORT || 5050;

app.use(cors());
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Private-Network', 'true');
  next();
});
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/tasks-archive', express.static(path.join(__dirname, 'Task')));
app.use('/portal', express.static(path.resolve(__dirname, '..', '00. TV Europe Sales Management Portal')));

// Initialize Local Deterministic Engine
const ruleEngine = new LocalRuleEngine(__dirname);

// API 1: Health & Runtime Info
app.get('/api/health', (req, res) => {
  res.json({
    status: "online",
    mode: "server",
    timestamp: new Date().toISOString(),
    agentsCount: AGENTS.length
  });
});

// API 2: Sub-Agent Registry & Live Status
app.get('/api/agents', (req, res) => {
  const status = getAgentStatusSummary(__dirname);
  res.json({
    success: true,
    count: status.length,
    agents: status
  });
});

// API 3: Master Data Bundle
app.get('/api/bundle', (req, res) => {
  const bundlePath = path.join(__dirname, 'public', 'master_data_bundle.json');
  if (fs.existsSync(bundlePath)) {
    res.sendFile(bundlePath);
  } else {
    res.status(404).json({ error: "Master bundle not found. Run 'node build_bundle.js' first." });
  }
});

// API 4: Unified Query & Orchestration
app.post('/api/query', async (req, res) => {
  try {
    const { query, apiKey, model } = req.body;
    if (!query || typeof query !== 'string') {
      return res.status(400).json({ error: "query string is required" });
    }

    // Process with Local Deterministic Rule & Data Engine
    const result = await ruleEngine.processQuery(query, { apiKey, model });

    return res.json({
      success: true,
      data: result
    });
  } catch (error) {
    console.error("[server] /api/query error:", error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// API 4-1: Strategic Reports FTS Search
app.get('/api/strategic-reports/search', async (req, res) => {
  try {
    const { keyword, subsidiary, limit } = req.query;
    const results = await ruleEngine.realDataEngine.searchStrategicReports(keyword, {
      subsidiary,
      limit: parseInt(limit, 10) || 5
    });
    res.json({
      success: true,
      count: results ? results.length : 0,
      keyword: keyword || '',
      results: results || []
    });
  } catch (error) {
    console.error("[server] /api/strategic-reports/search error:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API 4-2: Strategic Reports Summary & Catalog Stats
app.get('/api/strategic-reports/summary', async (req, res) => {
  try {
    const summary = await ruleEngine.realDataEngine.getStrategicReportsSummary();
    res.json({
      success: true,
      data: summary
    });
  } catch (error) {
    console.error("[server] /api/strategic-reports/summary error:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API 5: Safe Pipeline Execution Runner
app.post('/api/pipeline/run', (req, res) => {
  const { agentId, confirmToken } = req.body;
  if (!agentId) {
    return res.status(400).json({ error: "agentId is required" });
  }

  const agent = getAgentById(agentId);
  if (!agent || !agent.pipelineScript) {
    return res.status(404).json({ error: `Agent '${agentId}' does not have an executable pipeline script.` });
  }

  const { type, script, cwd } = agent.pipelineScript;
  const targetDir = path.resolve(__dirname, cwd);
  const targetScript = path.resolve(targetDir, script);

  if (!fs.existsSync(targetScript)) {
    return res.status(404).json({ error: `Pipeline script not found: ${targetScript}` });
  }

  console.log(`⚡ [Pipeline Runner] Executing ${type} ${script} in ${targetDir}...`);

  const cmd = type === 'python' ? 'python' : 'node';
  const child = spawn(cmd, [script], {
    cwd: targetDir,
    shell: true
  });

  let stdoutData = '';
  let stderrData = '';

  child.stdout.on('data', (data) => {
    stdoutData += data.toString();
  });

  child.stderr.on('data', (data) => {
    stderrData += data.toString();
  });

  child.on('close', (code) => {
    console.log(`[Pipeline Runner] Completed with code ${code}`);
    res.json({
      success: code === 0,
      exitCode: code,
      agentId,
      script,
      output: stdoutData,
      error: stderrData,
      completedAt: new Date().toISOString()
    });
  });

  child.on('error', (err) => {
    console.error(`[Pipeline Runner] Error:`, err);
    res.status(500).json({
      success: false,
      error: err.message
    });
  });
});

// API 6: Antigravity Bridge Task Creation (Sales Portal & Master Agent UI)
app.post('/api/bridge/task', (req, res) => {
  try {
    const { query, apiKey, conversationId, executionMode, source } = req.body;
    if (!query) return res.status(400).json({ error: "query is required" });

    const taskId = 'task_' + Date.now();
    const inboxDir = path.join(__dirname, 'agent_bridge', 'inbox');
    if (!fs.existsSync(inboxDir)) fs.mkdirSync(inboxDir, { recursive: true });
    const inboxFile = path.join(inboxDir, `${taskId}.json`);
    const taskData = {
      taskId,
      query,
      apiKey: apiKey || undefined,
      conversationId: conversationId || undefined,
      executionMode: executionMode || 'autonomous',
      source: source || 'sales_portal',
      createdAt: new Date().toISOString()
    };

    fs.writeFileSync(inboxFile, JSON.stringify(taskData, null, 2), 'utf8');
    console.log(`[Bridge Server] Dispatched task ${taskId} (${taskData.source}) to Antigravity Inbox`);

    res.json({
      success: true,
      taskId,
      status: "queued"
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// API 6.1: List Active & Recent Antigravity Brain Conversations (Sidecar Session Picker)
app.get('/api/bridge/conversations', (req, res) => {
  try {
    const limit = parseInt(req.query.limit || '15', 10);
    const conversations = listBrainConversations(limit);
    res.json({
      success: true,
      count: conversations.length,
      conversations
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// API 6.2: Live Mirror of Antigravity Conversation transcript.jsonl
app.get('/api/bridge/transcript/:conversationId', (req, res) => {
  try {
    const { conversationId } = req.params;
    const maxSteps = parseInt(req.query.maxSteps || '60', 10);
    const transcript = readConversationTranscript(conversationId, maxSteps);
    if (!transcript) {
      return res.status(404).json({ success: false, error: "Transcript not found for conversationId" });
    }
    res.json({
      success: true,
      ...transcript
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// API 6.3: Recent Autonomous Task Archives & Downloadable Deliverables (Task/YYYYMMDD_...)
app.get('/api/tasks/recent', (req, res) => {
  try {
    const limit = parseInt(req.query.limit || '15', 10);
    const tasks = scanTaskDeliverables(limit);
    res.json({
      success: true,
      count: tasks.length,
      tasks
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// API 7: Antigravity Bridge Task Status & Progress Polling
app.get('/api/bridge/status/:taskId', (req, res) => {
  const { taskId } = req.params;
  const outboxFile = path.join(__dirname, 'agent_bridge', 'outbox', `result_${taskId}.json`);
  const progressFile = path.join(__dirname, 'agent_bridge', 'progress', `${taskId}.json`);

  if (fs.existsSync(outboxFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(outboxFile, 'utf8'));
      return res.json({
        status: "completed",
        result: data
      });
    } catch (e) {}
  }

  if (fs.existsSync(progressFile)) {
    try {
      const prog = JSON.parse(fs.readFileSync(progressFile, 'utf8'));
      return res.json({
        status: "running",
        progress: prog
      });
    } catch (e) {}
  }

  res.json({ status: "queued" });
});

// API 8: DuckDB Analytics Status & Quality Gate Report
app.get('/api/analytics/status', async (req, res) => {
  const duckdbPath = path.join(__dirname, 'data', 'master_analytics.duckdb');
  if (!fs.existsSync(duckdbPath)) {
    return res.status(404).json({ error: "Master DuckDB not initialized yet." });
  }
  try {
    const duckdb = require('duckdb');
    const db = new duckdb.Database(duckdbPath, duckdb.OPEN_READONLY);
    const queryAsync = (sql) => new Promise((resolve) => {
      db.all(sql, (err, rows) => {
        if (err) console.warn('[server] DuckDB query error:', err.message);
        resolve(err ? [] : rows);
      });
    });
    const [statuses, alerts, priceCount, pnlCount, selloutCount, msCount] = await Promise.all([
      queryAsync('SELECT * FROM agent_sync_status ORDER BY last_sync_timestamp DESC'),
      queryAsync('SELECT * FROM data_anomaly_alerts ORDER BY created_at DESC LIMIT 20'),
      queryAsync('SELECT count(*) as cnt FROM fact_prices_daily'),
      queryAsync('SELECT count(*) as cnt FROM fact_pnl_monthly'),
      queryAsync('SELECT count(*) as cnt FROM fact_sellout_weekly'),
      queryAsync('SELECT count(*) as cnt FROM fact_market_share')
    ]);
    const serializeRows = (rows) => rows.map(row => {
      const clean = {};
      for (const [k, v] of Object.entries(row)) {
        clean[k] = typeof v === 'bigint' ? Number(v) : v;
      }
      return clean;
    });

    res.json({
      success: true,
      timestamp: new Date().toISOString(),
      agentSyncStatus: serializeRows(statuses),
      anomalyAlerts: serializeRows(alerts),
      tableCounts: {
        fact_prices_daily: Number(priceCount[0]?.cnt || 0),
        fact_pnl_monthly: Number(pnlCount[0]?.cnt || 0),
        fact_sellout_weekly: Number(selloutCount[0]?.cnt || 0),
        fact_market_share: Number(msCount[0]?.cnt || 0)
      }
    });
  } catch (e) {
    res.status(500).json({ success: false, error: e.message });
  }
});

// SSE Clients & Broadcast Function
let sseClients = [];
function broadcastSSE(payload) {
  const data = JSON.stringify(payload);
  sseClients.forEach(client => {
    try {
      client.write(`data: ${data}\n\n`);
    } catch (e) {}
  });
}

// API 9: Real-time Server-Sent Events (SSE) Stream for Dashboard Toasts
app.get('/api/events', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
  });
  res.write(`data: ${JSON.stringify({ event: 'CONNECTED', timestamp: new Date().toISOString() })}\n\n`);
  sseClients.push(res);

  req.on('close', () => {
    sseClients = sseClients.filter(c => c !== res);
  });
});

// API 10: One-Click Firebase Hosting Deploy
app.post('/api/analytics/deploy', (req, res) => {
  console.log('🚀 [Deploy] Triggering Firebase Hosting deployment...');
  const proc = spawn('cmd.exe', ['/c', 'firebase deploy --only hosting:master-agent'], { cwd: __dirname });

  let output = '';
  proc.stdout.on('data', d => { output += d.toString(); });
  proc.stderr.on('data', d => { output += d.toString(); });

  proc.on('close', code => {
    if (code === 0) {
      console.log('✅ [Deploy] Firebase deployment successful!');
      broadcastSSE({ event: 'DEPLOY_COMPLETED', timestamp: new Date().toISOString() });
      res.json({ success: true, message: "Firebase deployment completed successfully!" });
    } else {
      console.error('❌ [Deploy] Firebase deployment failed:', output);
      res.status(500).json({ success: false, error: output });
    }
  });
});

// Fallback to index.html for SPA
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start Server & Initialize File Watcher
if (require.main === module) {
  const { ExcelSourceWatcher } = require('./scripts/fileWatcher');
  const watcher = new ExcelSourceWatcher();
  
  watcher.on('sync_started', data => {
    console.log(`[SSE] Sync Started: ${data.agentId} (${data.fileName})`);
    broadcastSSE({ event: 'SYNC_STARTED', ...data });
  });

  watcher.on('sync_completed', data => {
    console.log(`[SSE] Sync Completed: ${data.agentId} (${data.fileName})`);
    broadcastSSE({ event: 'SYNC_COMPLETED', ...data });
  });

  watcher.on('sync_failed', data => {
    console.log(`[SSE] Sync Failed: ${data.agentId} (${data.fileName})`);
    broadcastSSE({ event: 'SYNC_FAILED', ...data });
  });

  app.listen(PORT, () => {
    console.log(`========================================================`);
    console.log(`🤖 TV Europe Master AI Agent Server Running`);
    console.log(`🌐 URL: http://localhost:${PORT}`);
    console.log(`📊 Registered Sub-Agents: ${AGENTS.length}`);
    console.log(`========================================================`);

    // Start background file watcher
    watcher.start();

    // Start Antigravity Sidecar & Inbox Bridge Worker in-process
    try {
      require('./watch_bridge');
    } catch (err) {
      console.warn('[Server] Could not start watch_bridge in-process:', err.message);
    }
  });
}

module.exports = app;
