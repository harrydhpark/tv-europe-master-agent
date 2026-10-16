/**
 * 1. Syncs updated axis_portal_bridge.js & axis_portal_bridge.css into Sales Portal
 * 2. Ensures start_sidecar_bridge.js (Port 5050) is running persistently via WMI Win32_Process
 * 3. Executes a live verification of "스위스 8월 제품군별 점유율 확인해줘" & "/api/bridge/conversations"
 */
const http = require('http');
const path = require('path');
const { execSync } = require('child_process');
const { syncPortalBridgeFiles } = require('./antigravity_sidecar_engine');

function httpRequest(method, urlPath, bodyObj) {
  return new Promise((resolve, reject) => {
    const bodyStr = bodyObj ? JSON.stringify(bodyObj) : null;
    const req = http.request({
      hostname: '127.0.0.1',
      port: 5050,
      path: urlPath,
      method,
      headers: bodyStr ? {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr)
      } : {},
      timeout: 5000
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, json: JSON.parse(data) });
        } catch (e) {
          resolve({ status: res.statusCode, text: data });
        }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    if (bodyStr) req.write(bodyStr);
    req.end();
  });
}

async function main() {
  // 1. Sync bridge files into 00. TV Europe Sales Management Portal
  const syncRes = syncPortalBridgeFiles();
  console.log('1. Synced Portal Bridge Files:', JSON.stringify(syncRes));

  // 2. Check if port 5050 is running; if --restart is passed, terminate old listener first
  if (process.argv.includes('--restart')) {
    try {
      execSync(`powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 5050 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"`, { stdio: 'ignore' });
      await new Promise(r => setTimeout(r, 800));
    } catch (e) {}
  }

  let online = false;
  try {
    const h = await httpRequest('GET', '/api/health');
    if (h.status === 200) online = true;
  } catch (e) {}

  if (!online) {
    console.log('2. Starting Port 5050 Sidecar Bridge via WMI Win32_Process (persistent daemon)...');
    const baseDir = path.resolve(__dirname, '..');
    const scriptPath = path.join(baseDir, 'start_sidecar_bridge.js');
    const psScript = `
$cmd = '"${process.execPath}" "${scriptPath}"'
$cwd = '${baseDir}'
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $cmd; CurrentDirectory = $cwd }
`;
    const encoded = Buffer.from(psScript, 'utf16le').toString('base64');
    execSync(`powershell -NoProfile -EncodedCommand ${encoded}`, { stdio: 'inherit' });

    for (let i = 0; i < 15; i++) {
      await new Promise(r => setTimeout(r, 600));
      try {
        const h = await httpRequest('GET', '/api/health');
        if (h.status === 200) {
          online = true;
          console.log('   -> Port 5050 is LIVE:', JSON.stringify(h.json));
          break;
        }
      } catch (e) {}
    }
  } else {
    console.log('2. Port 5050 is already LIVE.');
  }

  // 3. Verify /api/bridge/conversations and /api/bridge/transcript/:id
  const convRes = await httpRequest('GET', '/api/bridge/conversations?limit=5');
  const convs = convRes.json?.conversations || [];
  console.log(`3. Active Brain Conversations: ${convs.length} found. Latest: ${convs[0]?.conversationId}`);
  if (convs[0]) {
    const trRes = await httpRequest('GET', `/api/bridge/transcript/${convs[0].conversationId}?maxSteps=10`);
    console.log(`   -> Transcript steps for ${convs[0].conversationId.slice(0, 8)}: ${trRes.json?.steps?.length} steps (totalLines=${trRes.json?.totalLines})`);
  }

  // 4. Test the exact user prompt: "스위스 8월 제품군별 점유율 확인해줘"
  console.log('4. Submitting test prompt: "스위스 8월 제품군별 점유율 확인해줘"...');
  const taskRes = await httpRequest('POST', '/api/bridge/task', {
    query: '스위스 8월 제품군별 점유율 확인해줘',
    executionMode: 'autonomous',
    source: 'sales_portal'
  });
  const taskId = taskRes.json?.taskId;
  console.log('   -> Dispatched taskId:', taskId);

  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 800));
    const st = await httpRequest('GET', `/api/bridge/status/${taskId}`);
    if (st.json?.status === 'completed') {
      const r = st.json.result;
      console.log('   -> COMPLETED! Engine:', r.engine);
      console.log('   -> Task Archive Folder:', r.taskArchive?.folderName);
      console.log('   -> Deliverables:', (r.deliverables || []).map(d => d.name).join(', '));
      console.log('\n--- REPORT PREVIEW ---\n' + (r.answerMarkdown || '').slice(0, 1500));
      break;
    }
  }
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
