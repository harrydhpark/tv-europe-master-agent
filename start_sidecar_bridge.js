/**
 * ============================================================================
 * Antigravity Sidecar Launcher: AXIS Sales Portal <-> Master Agent Bridge
 * ============================================================================
 * Starts:
 * 1. 99. Master Agent HTTP + SSE Server (port 5050)
 * 2. Antigravity Bridge Watcher (watch_bridge.js) with agentapi + transcript.jsonl mirroring
 * 3. Sidecar runtime event watcher (sidecar_data/axis-portal-bridge/events/)
 */
const fs = require('fs');
const path = require('path');

const ROOT_DIR = __dirname;
const SIDECAR_EVENTS_DIR = path.join(
  process.env.USERPROFILE || 'C:\\Users\\harry.park',
  '.gemini',
  'antigravity',
  'sidecar_data',
  'axis-portal-bridge',
  'events'
);

if (!fs.existsSync(SIDECAR_EVENTS_DIR)) {
  try {
    fs.mkdirSync(SIDECAR_EVENTS_DIR, { recursive: true });
  } catch (e) {}
}

console.log('================================================================');
console.log('🚀 [AXIS Sidecar Bridge] Starting Server + Bridge Worker...');
console.log(`📂 Workspace: ${ROOT_DIR}`);
console.log('================================================================');

// 1. Start Express HTTP/SSE Server (if not already bound)
const app = require('./server');
const PORT = process.env.PORT || 5050;

const server = app.listen(PORT, () => {
  console.log(`✅ [AXIS Sidecar Bridge] HTTP & SSE Server listening on http://localhost:${PORT}`);
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.log(`ℹ️ [AXIS Sidecar Bridge] Port ${PORT} is already active; attaching Bridge Worker only.`);
  } else {
    console.error('❌ [AXIS Sidecar Bridge] Server error:', err.message);
  }
});

// 2. Start Bridge Inbox & Transcript Watcher
require('./watch_bridge');
