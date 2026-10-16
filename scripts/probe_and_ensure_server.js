const http = require('http');
const path = require('path');
const { spawn, execSync } = require('child_process');

const ROOT_DIR = path.resolve(__dirname, '..');

function httpGetJson(urlPath) {
  return new Promise((resolve) => {
    const req = http.get({ hostname: '127.0.0.1', port: 5050, path: urlPath, timeout: 2000 }, (res) => {
      let body = '';
      res.on('data', chunk => { body += chunk; });
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(body) });
        } catch (e) {
          resolve({ status: res.statusCode, raw: body.slice(0, 200) });
        }
      });
    });
    req.on('error', () => resolve({ status: 0 }));
    req.on('timeout', () => { req.destroy(); resolve({ status: 0 }); });
  });
}

async function main() {
  let probe = await httpGetJson('/api/bridge/conversations');
  if (probe.status !== 200) {
    console.log('[Probe] Starting/Restarting AXIS Sidecar Bridge Server on port 5050...');
    try {
      // Check if an older process is holding port 5050
      const netstat = execSync('netstat -ano | findstr :5050 | findstr LISTENING', { encoding: 'utf8' });
      const lines = netstat.trim().split(/\r?\n/);
      for (const line of lines) {
        const parts = line.trim().split(/\s+/);
        const pid = parts[parts.length - 1];
        if (pid && /^\d+$/.test(pid) && pid !== '0') {
          try { execSync(`taskkill /F /PID ${pid}`); } catch (e) {}
        }
      }
    } catch (e) {}

    const child = spawn(process.execPath, [path.join(ROOT_DIR, 'start_sidecar_bridge.js')], {
      cwd: ROOT_DIR,
      detached: true,
      stdio: 'ignore',
      windowsHide: true
    });
    child.unref();

    for (let i = 0; i < 12; i++) {
      await new Promise(r => setTimeout(r, 500));
      probe = await httpGetJson('/api/bridge/conversations');
      if (probe.status === 200) break;
    }
  }

  const health = await httpGetJson('/api/health');
  const convs = await httpGetJson('/api/bridge/conversations');
  const tasks = await httpGetJson('/api/tasks/recent');
  const portal = await httpGetJson('/portal/index.html');

  console.log('[Probe] /api/health ->', health.status, JSON.stringify(health.data));
  console.log('[Probe] /api/bridge/conversations ->', convs.status, 'count:', convs.data && convs.data.conversations ? convs.data.conversations.length : 0);
  console.log('[Probe] /api/tasks/recent ->', tasks.status, 'count:', tasks.data && tasks.data.tasks ? tasks.data.tasks.length : 0);
  console.log('[Probe] /portal/index.html ->', portal.status);
}

main();
