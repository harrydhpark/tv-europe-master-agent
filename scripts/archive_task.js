const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const TASK_BASE_DIR = path.join(ROOT_DIR, 'Task');

if (!fs.existsSync(TASK_BASE_DIR)) {
  fs.mkdirSync(TASK_BASE_DIR, { recursive: true });
}

function cleanFolderName(dateStr, queryShort) {
  const safeDate = dateStr || new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const cleanTitle = (queryShort || '작업내용')
    .replace(/[\\/:*?"<>|]/g, '')
    .replace(/\s+/g, '')
    .slice(0, 15);
  return `${safeDate}_${cleanTitle}`;
}

function updateTaskIndex(folderName, dateStr, shortTitle, query, dispatchedAgents, archivedArtifacts) {
  const mainReadmePath = path.join(TASK_BASE_DIR, 'README.md');
  if (!fs.existsSync(mainReadmePath)) return;

  let content = fs.readFileSync(mainReadmePath, 'utf8');
  if (content.includes(`[${folderName}]`)) {
    console.log(`[Archive] Task ${folderName} already indexed in Task/README.md`);
    return;
  }

  const dateFormatted = dateStr ? `${dateStr.slice(0,4)}-${dateStr.slice(4,6)}-${dateStr.slice(6,8)}` : new Date().toISOString().slice(0, 10);
  const titleSummary = (query || shortTitle).slice(0, 30).replace(/\|/g, '-');
  const agentSummary = dispatchedAgents.map(a => a.replace(/^\d+\.\s*/, '').replace(/TV\s*/, '')).join(', ') || 'Master Agent';
  
  let artifactIcons = [];
  archivedArtifacts.forEach(art => {
    if (art.endsWith('.docx')) artifactIcons.push('📄 Word 보고서');
    else if (art.endsWith('.html')) artifactIcons.push('🌐 Web 리포트');
    else if (art.endsWith('.xlsx')) artifactIcons.push('📊 Excel');
  });
  const artifactText = artifactIcons.length > 0 ? artifactIcons.join(', ') : '📄 보고서';

  const newRow = `| **${dateFormatted}** | [${folderName}](./${folderName}) | ${titleSummary} | ${agentSummary} | ${artifactText} |\n`;

  // Insert after table header
  const tableHeaderIndex = content.indexOf('| :---: | :--- | :--- | :--- | :---: |');
  if (tableHeaderIndex !== -1) {
    const endOfHeaderLine = content.indexOf('\n', tableHeaderIndex);
    content = content.slice(0, endOfHeaderLine + 1) + newRow + content.slice(endOfHeaderLine + 1);
    fs.writeFileSync(mainReadmePath, content, 'utf8');
    console.log(`[Archive] Updated Task/README.md registry with: ${folderName}`);
  }
}

function archiveTask({
  dateStr,
  shortTitle,
  query,
  answerMarkdown,
  summary,
  dispatchedAgents = [],
  artifactPaths = [],
  moveArtifacts = false
}) {
  const folderName = cleanFolderName(dateStr, shortTitle);
  const taskDir = path.join(TASK_BASE_DIR, folderName);

  if (!fs.existsSync(taskDir)) {
    fs.mkdirSync(taskDir, { recursive: true });
  }

  const archivedArtifacts = [];

  artifactPaths.forEach(artPath => {
    const fullSrc = path.isAbsolute(artPath) ? artPath : path.resolve(ROOT_DIR, artPath);
    if (fs.existsSync(fullSrc)) {
      const fileName = path.basename(fullSrc);
      const fullDst = path.join(taskDir, fileName);

      if (moveArtifacts) {
        fs.renameSync(fullSrc, fullDst);
        console.log(`[Archive] Moved: ${fileName} -> ${folderName}/`);
      } else {
        fs.copyFileSync(fullSrc, fullDst);
        console.log(`[Archive] Copied: ${fileName} -> ${folderName}/`);
      }
      archivedArtifacts.push(fileName);
    } else {
      const fileName = path.basename(artPath);
      const fullDst = path.join(taskDir, fileName);
      if (fs.existsSync(fullDst)) {
        archivedArtifacts.push(fileName);
      } else {
        console.warn(`[Archive] Warning: Artifact not found: ${artPath}`);
      }
    }
  });

  let readme = `# [Task] ${folderName}\n\n`;
  readme += `## 1. 질의 개요 (User Request)\n`;
  readme += `- **실행 일시**: ${dateStr ? `${dateStr.slice(0,4)}-${dateStr.slice(4,6)}-${dateStr.slice(6,8)}` : new Date().toISOString()}\n`;
  readme += `- **사용자 질의 원문**:\n> "${query.trim().replace(/\n/g, '\n> ')}"\n\n`;

  if (dispatchedAgents && dispatchedAgents.length > 0) {
    readme += `- **연계 에이전트 (Dispatched Agents)**:\n`;
    dispatchedAgents.forEach(ag => {
      readme += `  - \`${ag}\`\n`;
    });
    readme += `\n`;
  }

  readme += `## 2. 생성 산출물 (Artifacts)\n`;
  if (archivedArtifacts.length > 0) {
    archivedArtifacts.forEach(art => {
      readme += `- 📄 **[${art}](./${encodeURIComponent(art)})**\n`;
    });
  } else {
    readme += `- (별도 산출 파일 없음 - 마크다운 답변 보관)\n`;
  }
  readme += `\n---\n\n`;

  if (summary) {
    readme += `## 3. 핵심 요약 (Executive Summary)\n`;
    readme += `${summary.trim()}\n\n---\n\n`;
  }

  readme += `## 4. 상세 분석 및 실행 답변 (Execution Output)\n\n`;
  readme += `${answerMarkdown.trim()}\n`;

  const readmePath = path.join(taskDir, 'README.md');
  fs.writeFileSync(readmePath, readme, 'utf8');
  console.log(`[Archive] Successfully archived task into: Task/${folderName}/README.md`);

  // Update master registry index
  try {
    updateTaskIndex(folderName, dateStr, shortTitle, query, dispatchedAgents, archivedArtifacts);
  } catch (err) {
    console.warn(`[Archive] Warning: Could not update Task/README.md: ${err.message}`);
  }

  return { folderName, taskDir, readmePath, artifacts: archivedArtifacts };
}

module.exports = {
  archiveTask,
  cleanFolderName,
  TASK_BASE_DIR
};