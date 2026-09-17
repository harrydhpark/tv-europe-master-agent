/**
 * Antigravity Session Bridge Watcher
 * Monitors agent_bridge/inbox for tasks from the Web Dashboard.
 * Emits alert logs to stdout to trigger Antigravity Reactive Wakeup.
 */

const fs = require('fs');
const path = require('path');

const BASE_DIR = __dirname;
const INBOX_DIR = path.join(BASE_DIR, 'agent_bridge', 'inbox');
const PROGRESS_DIR = path.join(BASE_DIR, 'agent_bridge', 'progress');
const OUTBOX_DIR = path.join(BASE_DIR, 'agent_bridge', 'outbox');

// Ensure directories exist
[INBOX_DIR, PROGRESS_DIR, OUTBOX_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

console.log('====================================================');
console.log('🤖 Antigravity Session Bridge Watcher Active');
console.log(`📂 Monitoring Inbox: ${INBOX_DIR}`);
console.log('====================================================');

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

        // Update progress immediately so dashboard knows Antigravity received the question
        const progressFile = path.join(PROGRESS_DIR, `${taskId}.json`);
        fs.writeFileSync(progressFile, JSON.stringify({
          taskId,
          step: 1,
          totalSteps: 2,
          currentAgent: "Antigravity AI Agent",
          desc: `안티그래비티 세션이 질의를 수신하여 로컬 원천 파일들을 자율 탐색·분석하고 있습니다...`,
          timestamp: new Date().toISOString()
        }, null, 2), 'utf8');

        console.log(`\n🚨 [ANTIGRAVITY_QUERY_ALERT] Task: ${taskId}`);
        console.log(`📝 Query: "${content.query}"`);
        console.log(`⏰ Time: ${content.createdAt || new Date().toISOString()}`);
        console.log(`👉 Pending Action: Antigravity Session is requested to analyze this query and write result to agent_bridge/outbox/result_${taskId}.json\n`);
      } catch (err) {
        console.error(`[Watcher] Error reading ${file}:`, err);
      }
    }
  } catch (err) {
    console.error('[Watcher] Poll error:', err);
  }
}

// Watch inbox every 400ms
setInterval(checkInbox, 400);
