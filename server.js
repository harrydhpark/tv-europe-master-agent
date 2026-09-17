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

const app = express();
const PORT = process.env.PORT || 5050;

app.use(cors());
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Private-Network', 'true');
  next();
});
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

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

// API 6: Antigravity Bridge Task Creation
app.post('/api/bridge/task', (req, res) => {
  try {
    const { query } = req.body;
    if (!query) return res.status(400).json({ error: "query is required" });

    const taskId = 'task_' + Date.now();
    const inboxFile = path.join(__dirname, 'agent_bridge', 'inbox', `${taskId}.json`);
    const taskData = {
      taskId,
      query,
      createdAt: new Date().toISOString()
    };

    fs.writeFileSync(inboxFile, JSON.stringify(taskData, null, 2), 'utf8');
    console.log(`[Bridge Server] Dispatched task ${taskId} to Antigravity Inbox`);

    res.json({
      success: true,
      taskId,
      status: "queued"
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
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

// Fallback to index.html for SPA
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start Server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`========================================================`);
    console.log(`🤖 TV Europe Master AI Agent Server Running`);
    console.log(`🌐 URL: http://localhost:${PORT}`);
    console.log(`📊 Registered Sub-Agents: ${AGENTS.length}`);
    console.log(`========================================================`);
  });
}

module.exports = app;
