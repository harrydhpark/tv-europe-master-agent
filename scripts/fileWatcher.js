/**
 * TV Europe Sales Master AI Agent - Automated Excel File Watcher
 * 
 * Watches sibling raw data folders for new/modified weekly Excel files (.xlsx, .xlsb).
 * Uses chokidar with awaitWriteFinish to safely wait for large file copy operations to complete.
 * Triggers idempotent DuckDB ingestion via sync_master_db.py, re-compiles bundle, and emits events.
 */

const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const EventEmitter = require('events');
const chokidar = require('chokidar');

const BASE_DIR = path.resolve(__dirname, '..');
const AX_ROOT = path.resolve(BASE_DIR, '..');

// Python runner path (GDMI portable Python environment)
const PYTHON_PATH = path.resolve(AX_ROOT, '01. GDMI_Weekly_Sellout_Analysis-main', '.agents', 'python', 'python.exe');
const SYNC_SCRIPT = path.resolve(__dirname, 'sync_master_db.py');
const BUNDLE_SCRIPT = path.resolve(BASE_DIR, 'build_bundle.js');

// Target Directories & Watch Patterns
const WATCH_CONFIGS = [
  {
    agentId: 'kpi-sheet',
    name: '06. KPI Sheet',
    paths: [
      path.resolve(AX_ROOT, '06. KPI Sheet'),
      path.resolve(AX_ROOT, '06. KPI Sheet', 'Raw data')
    ],
    extensions: ['.xlsx', '.xlsb'],
    matchFile: (name) => name.includes('KPI') || name.includes('CPSI') || name.includes('매출장') || name.includes('Display')
  },
  {
    agentId: 'gdmi-weekly',
    name: '01. GDMI Weekly Sellout',
    paths: [
      path.resolve(AX_ROOT, '01. GDMI_Weekly_Sellout_Analysis-main', '00. Raw Data'),
      path.resolve(AX_ROOT, '01. GDMI_Weekly_Sellout_Analysis-main', '_data')
    ],
    extensions: ['.xlsx', '.xlsb', '.json'],
    matchFile: (name) => name.endsWith('.xlsb') || name.startsWith('metrics_') || name.includes('Raw')
  },
  {
    agentId: 'price-tracker',
    name: '04. Price Tracker',
    paths: [
      path.resolve(AX_ROOT, '04. Price Tracker', 'data')
    ],
    extensions: ['.xlsx', '.db'],
    matchFile: (name) => name.includes('price tracker') || name.endsWith('price_history.db')
  },
  {
    agentId: 'ms-trend',
    name: '08. MS Trend',
    paths: [
      path.resolve(AX_ROOT, '08. MS Trend'),
      path.resolve(AX_ROOT, '08. MS Trend', 'Databook')
    ],
    extensions: ['.xlsx', '.json'],
    matchFile: (name) => name.includes('Databook') || name.includes('ms_trend_data.json')
  },
  {
    agentId: 'pnl-analysis',
    name: '05. TV P&L Analysis',
    paths: [
      path.resolve(AX_ROOT, '05. TV P&L Analysis', '법인별')
    ],
    extensions: ['.html', '.xlsx', '.xlsb'],
    matchFile: (name) => name.includes('_Report.html') || name.includes('P&L Analysis')
  },
  {
    agentId: 'strategic-reports',
    name: '1.영업 주요보고 (전략회의/PD회의)',
    paths: [
      path.resolve(AX_ROOT, '..', '1.영업 주요보고')
    ],
    extensions: ['.pptx'],
    matchFile: (name) => !name.startsWith('~$') && name.endsWith('.pptx')
  }
];

class ExcelSourceWatcher extends EventEmitter {
  constructor(options = {}) {
    super();
    this.watcher = null;
    this.isProcessing = false;
    this.queue = [];
    this.stabilityThreshold = options.stabilityThreshold || 3000;
    this.pollInterval = options.pollInterval || 500;
  }

  start() {
    console.log('\n👁️ [Excel Watcher] Initializing background file system monitor...');
    
    // Gather all valid watch folders
    const watchPaths = [];
    WATCH_CONFIGS.forEach(cfg => {
      cfg.paths.forEach(p => {
        if (fs.existsSync(p)) {
          watchPaths.push(p);
        }
      });
    });

    console.log(`  -> Monitoring ${watchPaths.length} directories across AX Task sub-agents`);

    this.watcher = chokidar.watch(watchPaths, {
      ignored: [
        /(^|[\/\\])\../,            // dotfiles
        /(^|[\/\\])~\$/,            // Excel temporary lock files (~$*.xlsx)
        /\.tmp$/i,                  // temporary files
        /\.crdownload$/i,           // incomplete downloads
        /node_modules/,
        /\.git/,
        /__pycache__/
      ],
      persistent: true,
      ignoreInitial: true,          // Do NOT trigger on existing files during boot
      depth: 2,
      awaitWriteFinish: {
        stabilityThreshold: this.stabilityThreshold,
        pollInterval: this.pollInterval
      }
    });

    this.watcher
      .on('add', (filePath) => this.handleFileEvent('add', filePath))
      .on('change', (filePath) => this.handleFileEvent('change', filePath))
      .on('error', (err) => console.error('[Excel Watcher] Error:', err.message));

    console.log('✅ [Excel Watcher] Active and waiting for weekly Excel files.\n');
  }

  handleFileEvent(eventType, filePath) {
    const fileName = path.basename(filePath);
    const ext = path.extname(filePath).toLowerCase();

    // Check temporary or hidden
    if (fileName.startsWith('~$') || fileName.startsWith('.')) return;

    // Identify target agent
    const matchedConfig = WATCH_CONFIGS.find(cfg => {
      if (!cfg.extensions.includes(ext)) return false;
      const belongsToPath = cfg.paths.some(p => filePath.startsWith(p));
      if (!belongsToPath) return false;
      return cfg.matchFile ? cfg.matchFile(fileName) : true;
    });

    if (!matchedConfig) return;

    console.log(`\n🔔 [Excel Watcher] ${eventType.toUpperCase()} event detected!`);
    console.log(`  • Agent: ${matchedConfig.agentId} (${matchedConfig.name})`);
    console.log(`  • File:  ${fileName}`);
    console.log(`  • Path:  ${filePath}`);

    this.queueTask(matchedConfig.agentId, filePath, fileName);
  }

  queueTask(agentId, filePath, fileName) {
    this.queue.push({ agentId, filePath, fileName, timestamp: new Date() });
    this.processQueue();
  }

  async processQueue() {
    if (this.isProcessing || this.queue.length === 0) return;
    this.isProcessing = true;

    const task = this.queue.shift();
    console.log(`🚀 [Excel Watcher] Executing ingestion pipeline for ${task.agentId}...`);

    this.emit('sync_started', {
      agentId: task.agentId,
      fileName: task.fileName,
      filePath: task.filePath,
      timestamp: new Date().toISOString()
    });

    try {
      // 1. Run sync_master_db.py --agent [agentId] --file [filePath]
      await this.runPythonSync(task.agentId, task.filePath);
      
      // 2. Automatically re-compile master_data_bundle.json
      await this.runBundleBuild();

      console.log(`✅ [Excel Watcher] ${task.agentId} auto-sync & bundle build completed!`);

      const completionPayload = {
        agentId: task.agentId,
        fileName: task.fileName,
        filePath: task.filePath,
        status: 'SUCCESS',
        timestamp: new Date().toISOString(),
        message: `W 주간 데이터가 중앙 DuckDB 및 정적 번들에 안전하게 반영되었습니다.`
      };

      this.emit('sync_completed', completionPayload);

    } catch (err) {
      console.error(`❌ [Excel Watcher] Pipeline failed for ${task.agentId}:`, err.message);
      this.emit('sync_failed', {
        agentId: task.agentId,
        fileName: task.fileName,
        error: err.message,
        timestamp: new Date().toISOString()
      });
    } finally {
      this.isProcessing = false;
      if (this.queue.length > 0) {
        this.processQueue();
      }
    }
  }

  runPythonSync(agentId, filePath) {
    return new Promise((resolve, reject) => {
      let pythonExe = PYTHON_PATH;
      let args = [SYNC_SCRIPT, '--agent', agentId, '--file', filePath];

      if (agentId === 'strategic-reports') {
        pythonExe = path.resolve(AX_ROOT, '04. Price Tracker', 'python_env', 'python.exe');
        args = [path.resolve(__dirname, 'parse_pptx_reports.py')];
      }

      console.log(`  [CMD] ${pythonExe} ${args.join(' ')}`);

      const proc = spawn(pythonExe, args, { cwd: BASE_DIR });

      let stdout = '';
      let stderr = '';

      proc.stdout.on('data', (d) => { stdout += d.toString(); });
      proc.stderr.on('data', (d) => { stderr += d.toString(); });

      proc.on('close', (code) => {
        if (code === 0) {
          resolve(stdout);
        } else {
          reject(new Error(`Exit code ${code}: ${stderr || stdout}`));
        }
      });
    });
  }

  runBundleBuild() {
    return new Promise((resolve, reject) => {
      console.log(`  [CMD] node ${BUNDLE_SCRIPT}`);
      const proc = spawn('node', [BUNDLE_SCRIPT], { cwd: BASE_DIR });

      let stdout = '';
      let stderr = '';
      proc.stdout.on('data', (d) => { stdout += d.toString(); });
      proc.stderr.on('data', (d) => { stderr += d.toString(); });

      proc.on('close', (code) => {
        if (code === 0) {
          resolve(stdout);
        } else {
          reject(new Error(`Bundle build failed (code ${code}): ${stderr || stdout}`));
        }
      });
    });
  }

  stop() {
    if (this.watcher) {
      this.watcher.close();
      console.log('🛑 [Excel Watcher] File watcher stopped.');
    }
  }
}

// Standalone runner execution
if (require.main === module) {
  const watcher = new ExcelSourceWatcher();
  watcher.start();
  
  watcher.on('sync_completed', (info) => {
    console.log(`🎉 [EVENT] Sync Completed: ${info.agentId} (${info.fileName})`);
  });
}

module.exports = { ExcelSourceWatcher, WATCH_CONFIGS };
