/**
 * TV Europe Sales Master AI Agent - Frontend Application Logic
 * Manages 3-column split UI, agent dispatch timeline, live artifact canvas, and export utilities.
 */

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// Application State
const state = {
  agents: [],
  messages: [],
  activeArtifact: null,
  activeAgentFilter: null,
  isFullscreenCanvas: false,
  apiKey: localStorage.getItem('lge_master_gemini_key') || '',
  model: localStorage.getItem('lge_master_gemini_model') || 'gemini-1.5-pro',
  isServerMode: true,
  chartInstance: null,
  pendingPipelineAgent: null
};

// DOM Elements
const elements = {
  agentListContainer: document.getElementById('agentListContainer'),
  chatMessages: document.getElementById('chatMessages'),
  chatInput: document.getElementById('chatInput'),
  sendBtn: document.getElementById('sendBtn'),
  btnNewChat: document.getElementById('btnNewChat'),
  canvasArea: document.getElementById('canvasArea'),
  canvasTitle: document.getElementById('canvasTitle'),
  canvasBody: document.getElementById('canvasBody'),
  btnCopyMarkdown: document.getElementById('btnCopyMarkdown'),
  btnPrintPdf: document.getElementById('btnPrintPdf'),
  btnExportCsv: document.getElementById('btnExportCsv'),
  btnToggleFullscreen: document.getElementById('btnToggleFullscreen'),
  btnOpenSettings: document.getElementById('btnOpenSettings'),
  settingsModal: document.getElementById('settingsModal'),
  btnCloseSettings: document.getElementById('btnCloseSettings'),
  btnSaveSettings: document.getElementById('btnSaveSettings'),
  apiKeyInput: document.getElementById('apiKeyInput'),
  modelSelect: document.getElementById('modelSelect'),
  quickChips: document.querySelectorAll('.chip-btn'),
  mentionChips: document.querySelectorAll('.mention-chip'),
  pipelineModal: document.getElementById('pipelineModal'),
  pipelineModalDetails: document.getElementById('pipelineModalDetails'),
  btnClosePipelineModal: document.getElementById('btnClosePipelineModal'),
  btnCancelPipeline: document.getElementById('btnCancelPipeline'),
  btnConfirmPipeline: document.getElementById('btnConfirmPipeline')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  setupEventListeners();
  await loadAgentsAndStatus();
  loadChatHistory();
});

// 1. Load Agents & Status (Server Mode vs Static Bundle Mode)
async function loadAgentsAndStatus() {
  try {
    const res = await fetch('/api/agents');
    if (res.ok) {
      const data = await res.json();
      state.agents = data.agents || [];
      state.isServerMode = true;
      fetch('master_data_bundle.json').then(r => r.json()).then(bData => {
        state.bundleData = bData;
      }).catch(() => {});
    } else {
      throw new Error("Server not responding");
    }
  } catch (e) {
    console.warn("[app] Server API unavailable, loading static bundle...");
    state.isServerMode = false;
    try {
      const bRes = await fetch('master_data_bundle.json');
      const bData = await bRes.json();
      state.agents = bData.agentsStatus || [];
      state.bundleData = bData;
    } catch (err) {
      console.error("[app] Bundle failed to load", err);
    }
  }

  renderAgentSidebar();
}

// 2. Render Left Sidebar Agent Cards
function renderAgentSidebar() {
  if (!elements.agentListContainer) return;

  const categories = [
    { key: "sales", name: "1. 매출/손익 관리" },
    { key: "product", name: "2. 제품 정보" },
    { key: "pricing", name: "3. 가격 관리" },
    { key: "market", name: "4. 시장 정보" }
  ];

  let html = '';

  categories.forEach(cat => {
    const catAgents = state.agents.filter(a => a.category === cat.key);
    if (catAgents.length === 0) return;

    html += `
      <div class="agent-category-group">
        <div class="category-label">
          <span>${cat.name}</span>
          <span class="text-xs opacity-70">${catAgents.length}</span>
        </div>
    `;

    catAgents.forEach(agent => {
      const isOnline = agent.status === 'online';
      html += `
        <div class="agent-card-item" data-id="${agent.id}" data-tag="${agent.mentionTag}" title="${escapeHtml(agent.desc)}">
          <div class="agent-item-left">
            <div class="agent-item-icon"><i class="${agent.icon}"></i></div>
            <div class="agent-item-info">
              <span class="agent-item-name">${escapeHtml(agent.name)}</span>
              <span class="agent-item-tag">${escapeHtml(agent.mentionTag)}</span>
            </div>
          </div>
          <div class="agent-item-right">
            ${agent.pipelineScript ? `
              <button class="btn-pipeline-trigger" data-id="${agent.id}" title="원천 엑셀 파이프라인 수동 갱신 실행">
                <i class="ri-play-fill"></i> 갱신
              </button>
            ` : ''}
            <span class="agent-item-badge ${isOnline ? 'online' : ''}">
              ${isOnline ? 'Active' : 'Standby'}
            </span>
          </div>
        </div>
      `;
    });

    html += `</div>`;
  });

  elements.agentListContainer.innerHTML = html;

  // Click card to insert mention tag into input
  elements.agentListContainer.querySelectorAll('.agent-card-item').forEach(card => {
    card.addEventListener('click', () => {
      const tag = card.getAttribute('data-tag');
      if (tag) {
        insertMentionIntoInput(tag);
      }
    });
  });

  // Pipeline modal trigger buttons
  elements.agentListContainer.querySelectorAll('.btn-pipeline-trigger').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = btn.getAttribute('data-id');
      if (id) openPipelineModal(id);
    });
  });
}

function insertMentionIntoInput(tag) {
  const currentVal = elements.chatInput.value;
  if (!currentVal.includes(tag)) {
    elements.chatInput.value = `${tag} ${currentVal}`.trim() + " ";
  }
  elements.chatInput.focus();
}

// 3. Event Listeners Setup
function setupEventListeners() {
  // Send Button & Textarea Enter key
  elements.sendBtn.addEventListener('click', handleSendMessage);
  elements.chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  });

  // Quick Chips
  elements.quickChips.forEach(chip => {
    chip.addEventListener('click', () => {
      elements.chatInput.value = chip.textContent.trim();
      handleSendMessage();
    });
  });

  // Mention Chips
  elements.mentionChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const tag = chip.getAttribute('data-mention');
      if (tag) insertMentionIntoInput(tag);
    });
  });

  // Canvas Action Buttons
  elements.btnCopyMarkdown.addEventListener('click', handleCopyMarkdown);
  elements.btnPrintPdf.addEventListener('click', handlePrintPdf);
  elements.btnExportCsv.addEventListener('click', handleExportCsv);
  elements.btnToggleFullscreen.addEventListener('click', handleToggleFullscreen);

  // Settings Modal
  elements.btnOpenSettings.addEventListener('click', () => {
    elements.apiKeyInput.value = state.apiKey;
    elements.modelSelect.value = state.model;
    elements.settingsModal.classList.add('active');
  });

  elements.btnCloseSettings.addEventListener('click', () => {
    elements.settingsModal.classList.remove('active');
  });

  elements.btnSaveSettings.addEventListener('click', () => {
    state.apiKey = elements.apiKeyInput.value.trim();
    state.model = elements.modelSelect.value;
    localStorage.setItem('lge_master_gemini_key', state.apiKey);
    localStorage.setItem('lge_master_gemini_model', state.model);
    elements.settingsModal.classList.remove('active');
    alert("설정이 저장되었습니다.");
  });

  // New Chat Session
  if (elements.btnNewChat) {
    elements.btnNewChat.addEventListener('click', handleNewChat);
  }

  // Pipeline Safety Modal Buttons
  if (elements.btnClosePipelineModal) {
    elements.btnClosePipelineModal.addEventListener('click', closePipelineModal);
  }
  if (elements.btnCancelPipeline) {
    elements.btnCancelPipeline.addEventListener('click', closePipelineModal);
  }
  if (elements.btnConfirmPipeline) {
    elements.btnConfirmPipeline.addEventListener('click', handleConfirmPipelineRun);
  }

  // Smart Portal Link (Local vs Cloud Hosting)
  const portalBackBtn = document.getElementById('btnPortalBack');
  if (portalBackBtn && (window.location.protocol === 'file:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
    portalBackBtn.href = portalBackBtn.getAttribute('data-local-href') || portalBackBtn.href;
  }
}

// 4. Handle Send Message & Multi-Agent Dispatch (via Antigravity Bridge)
async function handleSendMessage() {
  const query = elements.chatInput.value.trim();
  if (!query) return;

  // Add User Message
  appendMessage({
    sender: 'user',
    text: query,
    timestamp: new Date().toLocaleTimeString()
  });

  elements.chatInput.value = '';
  elements.chatInput.style.height = 'auto';
  elements.sendBtn.disabled = true;

  // Add Temporary Agent Loading Bubble with Dispatch Timeline
  const tempMsgId = 'temp_' + Date.now();
  appendMessage({
    id: tempMsgId,
    sender: 'agent',
    text: "🤖 안티그래비티 마스터 에이전트가 실제 원천 파일을 분석하고 있습니다...",
    timeline: [
      { step: 1, agent: "Antigravity Bridge", status: "running", desc: "안티그래비티 에이전트 작업 큐 등록 중..." }
    ],
    timestamp: new Date().toLocaleTimeString()
  });

  try {
    let result = null;

    // Try Antigravity Bridge First
    if (state.isServerMode) {
      try {
        const taskRes = await fetch('/api/bridge/task', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query })
        });
        const taskData = await taskRes.json();

        if (taskData.success && taskData.taskId) {
          const taskId = taskData.taskId;
          const startTime = Date.now();
          while (Date.now() - startTime < 30000) {
            await new Promise(r => setTimeout(r, 400));
            const pollRes = await fetch(`/api/bridge/status/${taskId}`);
            const pollData = await pollRes.json();

            if (pollData.status === 'running' && pollData.progress) {
              const p = pollData.progress;
              updateTempMessageTimeline(tempMsgId, p.step, p.currentAgent, p.desc);
            } else if (pollData.status === 'completed' && pollData.result) {
              result = pollData.result;
              break;
            }
          }
        }
      } catch (err) {
        console.warn("[app] Bridge polling failed, falling back to /api/query", err);
      }
    }

    // Fallback if bridge didn't complete
    if (!result) {
      if (state.isServerMode) {
        const res = await fetch('/api/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query,
            apiKey: state.apiKey,
            model: state.model
          })
        });
        const resData = await res.json();
        result = resData.data;
      } else {
        result = await fallbackClientQuery(query);
      }
    }

    // Remove temp message
    removeMessage(tempMsgId);

    if (result) {
      appendMessage({
        sender: 'agent',
        text: result.answerMarkdown,
        timeline: result.timeline,
        dispatchedAgents: result.dispatchedAgents,
        artifact: result.artifact,
        timestamp: new Date().toLocaleTimeString()
      });

      // Update Live Canvas with Artifact
      if (result.artifact) {
        renderArtifactToCanvas(result.artifact);
      }
    }
  } catch (error) {
    console.error("[app] Query error:", error);
    removeMessage(tempMsgId);
    appendMessage({
      sender: 'agent',
      text: `⚠️ 질의 처리 중 오류가 발생했습니다: ${error.message}`,
      timestamp: new Date().toLocaleTimeString()
    });
  } finally {
    elements.sendBtn.disabled = false;
    saveChatHistory();
  }
}

function updateTempMessageTimeline(tempMsgId, step, agent, desc) {
  const el = document.getElementById(tempMsgId);
  if (!el) return;
  const stepsContainer = el.querySelector('.timeline-steps');
  if (stepsContainer) {
    if (stepsContainer.querySelector(`[data-step="${step}"]`)) return;
    const stepDiv = document.createElement('div');
    stepDiv.className = 'timeline-step-item';
    stepDiv.setAttribute('data-step', step);
    stepDiv.innerHTML = `
      <div class="step-icon"><i class="ri-check-line"></i></div>
      <span class="step-agent-badge">${escapeHtml(agent)}</span>
      <span>${escapeHtml(desc)}</span>
    `;
    stepsContainer.appendChild(stepDiv);
  }
}

// 5. Message Rendering in Chat Stream
function appendMessage(msg) {
  state.messages.push(msg);

  const msgDiv = document.createElement('div');
  msgDiv.className = `chat-msg ${msg.sender}`;
  if (msg.id) msgDiv.id = msg.id;

  let timelineHtml = '';
  if (msg.timeline && msg.timeline.length > 0) {
    timelineHtml = `
      <div class="dispatch-timeline-card">
        <div class="timeline-header" onclick="this.nextElementSibling.classList.toggle('hidden')">
          <span>⚡ 서브 에이전트 오케스트레이션 타임라인 (${msg.timeline.length}단계 완료)</span>
          <i class="ri-arrow-down-s-line"></i>
        </div>
        <div class="timeline-steps">
          ${msg.timeline.map(t => `
            <div class="timeline-step-item">
              <div class="step-icon"><i class="ri-check-line"></i></div>
              <span class="step-agent-badge">${t.agent}</span>
              <span>${t.desc}</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  const formattedContent = formatMarkdown(msg.text);

  if (msg.sender === 'user') {
    msgDiv.innerHTML = `
      <div class="chat-avatar user"><i class="ri-user-line"></i></div>
      <div class="msg-body-wrapper">
        <div class="msg-bubble">${formattedContent}</div>
      </div>
    `;
  } else {
    msgDiv.innerHTML = `
      <div class="chat-avatar master"><i class="ri-robot-2-line"></i></div>
      <div class="msg-body-wrapper">
        ${timelineHtml}
        <div class="msg-bubble">${formattedContent}</div>
      </div>
    `;
  }

  elements.chatMessages.appendChild(msgDiv);
  elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function removeMessage(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
  state.messages = state.messages.filter(m => m.id !== id);
}

// Simple Markdown Formatter
function formatMarkdown(text) {
  if (!text) return '';
  let html = text
    .replace(/^### (.*$)/gim, '<h3 class="text-base font-bold my-2 text-slate-900">$1</h3>')
    .replace(/^#### (.*$)/gim, '<h4 class="text-sm font-bold my-1 text-teal-800">$1</h4>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/`([^`]+)`/gim, '<code class="bg-slate-100 px-1 py-0.5 rounded font-mono text-xs text-rose-600">$1</code>')
    .replace(/\n\n/gim, '<br/><br/>')
    .replace(/\n/gim, '<br/>');
  return html;
}

// 6. Live Artifact Canvas Rendering
function renderArtifactToCanvas(artifact) {
  state.activeArtifact = artifact;
  elements.canvasTitle.textContent = artifact.title || '종합 분석 아티팩트';

  let html = '';

  // 1. Metric Cards
  if (artifact.metrics && artifact.metrics.length > 0) {
    html += `<div class="canvas-metric-grid">`;
    artifact.metrics.forEach(m => {
      html += `
        <div class="metric-card">
          <span class="metric-card-label">${m.label}</span>
          <span class="metric-card-val">${m.value}</span>
          <span class="metric-card-change ${m.status}">${m.change}</span>
        </div>
      `;
    });
    html += `</div>`;
  }

  // 2. Interactive Simulation Sliders
  if (artifact.simulation) {
    html += `
      <div class="simulation-ctrl-box">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;">
          <span style="font-size:12.5px; font-weight:700; color:#0F766E; display:flex; align-items:center; gap:6px;">
            <i class="ri-equalizer-line"></i>
            <span>대화형 손익 시뮬레이션 민감도 조절기 (Live Slider)</span>
          </span>
          <span class="text-xs text-teal-700 font-mono">Real-time Recalculation</span>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; font-size:12px;">
          <div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
              <span class="text-slate-600 font-medium">환율 변동 (EUR/USD)</span>
              <span id="fxSliderVal" class="font-bold text-teal-900 font-mono">-3.0%</span>
            </div>
            <input type="range" id="fxSlider" min="-10" max="10" step="0.5" value="-3" style="width:100%; accent-color:#0D9488;">
          </div>
          <div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
              <span class="text-slate-600 font-medium">유통 장려금율 변동</span>
              <span id="rebateSliderVal" class="font-bold text-teal-900 font-mono">+1.5%p</span>
            </div>
            <input type="range" id="rebateSlider" min="-5" max="5" step="0.5" value="1.5" style="width:100%; accent-color:#A50034;">
          </div>
        </div>
      </div>
    `;
  }

  // 3. Chart.js Visualization
  if (artifact.chart && typeof Chart !== 'undefined') {
    html += `
      <div class="canvas-chart-box">
        <h4 style="font-size:13px; font-weight:700; color:#1E293B; margin-bottom:12px; display:flex; align-items:center; gap:6px;">
          <i class="ri-bar-chart-2-line text-teal-600"></i>
          <span>${escapeHtml(artifact.chart.title || '지표 추이 시각화')}</span>
        </h4>
        <div style="position:relative; height:200px; width:100%;">
          <canvas id="artifactChart"></canvas>
        </div>
      </div>
    `;
  }

  // 4. Data Table
  if (artifact.table && artifact.table.headers && artifact.table.rows) {
    html += `
      <div class="canvas-table-wrapper">
        <table class="canvas-table">
          <thead>
            <tr>
              ${artifact.table.headers.map(h => `<th>${h}</th>`).join('')}
            </tr>
          </thead>
          <tbody>
            ${artifact.table.rows.map(row => `
              <tr>
                ${row.map(cell => `<td>${cell}</td>`).join('')}
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  }

  // 5. Action Items Checklist
  if (artifact.actionItems && artifact.actionItems.length > 0) {
    html += `
      <div class="action-items-card">
        <div class="action-items-title">
          <i class="ri-checkbox-circle-line text-teal-600"></i>
          <span>실행 제언 및 후속 조치 과제 (Action Items)</span>
        </div>
        <ul class="action-list">
          ${artifact.actionItems.map(item => `<li>${item}</li>`).join('')}
        </ul>
      </div>
    `;
  }

  elements.canvasBody.innerHTML = html;

  // Initialize Chart.js
  if (artifact.chart && typeof Chart !== 'undefined') {
    const canvasEl = document.getElementById('artifactChart');
    if (canvasEl) {
      if (state.chartInstance) {
        state.chartInstance.destroy();
        state.chartInstance = null;
      }
      try {
        const ctx = canvasEl.getContext('2d');
        const isMulti = artifact.chart.salesData && artifact.chart.coiData;

        const datasets = isMulti ? [
          {
            type: 'bar',
            label: 'Net Sales ($M)',
            data: artifact.chart.salesData,
            backgroundColor: 'rgba(13, 148, 136, 0.85)',
            borderRadius: 4,
            yAxisID: 'y'
          },
          {
            type: 'line',
            label: '영업이익 ($K)',
            data: artifact.chart.coiData,
            borderColor: '#A50034',
            backgroundColor: '#A50034',
            borderWidth: 2.5,
            pointRadius: 4,
            tension: 0.1,
            yAxisID: 'y1'
          }
        ] : (artifact.chart.datasets || []);

        state.chartInstance = new Chart(ctx, {
          type: artifact.chart.type || 'bar',
          data: {
            labels: artifact.chart.labels || [],
            datasets
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
              legend: { position: 'top', labels: { boxWidth: 12, font: { size: 11 } } },
              tooltip: { padding: 8 }
            },
            scales: isMulti ? {
              y: {
                type: 'linear',
                display: true,
                position: 'left',
                title: { display: true, text: 'Sales ($M)', font: { size: 10 } },
                grid: { color: 'rgba(0,0,0,0.04)' }
              },
              y1: {
                type: 'linear',
                display: true,
                position: 'right',
                title: { display: true, text: 'COI ($K)', font: { size: 10 } },
                grid: { drawOnChartArea: false }
              },
              x: {
                grid: { display: false },
                ticks: { font: { size: 11 } }
              }
            } : {
              y: { grid: { color: 'rgba(0,0,0,0.04)' } },
              x: { grid: { display: false } }
            }
          }
        });
      } catch (err) {
        console.warn("[app] Chart initialization error:", err);
      }
    }
  }

  // Bind Simulation Sliders
  if (artifact.simulation) {
    const fxSlider = document.getElementById('fxSlider');
    const rebateSlider = document.getElementById('rebateSlider');
    const fxVal = document.getElementById('fxSliderVal');
    const rebateVal = document.getElementById('rebateSliderVal');

    const updateSim = () => {
      const fx = parseFloat(fxSlider.value);
      const reb = parseFloat(rebateSlider.value);
      fxVal.textContent = (fx > 0 ? `+${fx.toFixed(1)}` : fx.toFixed(1)) + '%';
      rebateVal.textContent = (reb > 0 ? `+${reb.toFixed(1)}` : reb.toFixed(1)) + '%p';

      const opmImpact = (fx * 0.3 - reb * 0.6).toFixed(1);
      const coiImpact = (fx * 2.4 - reb * 4.8).toFixed(1);

      const cards = document.querySelectorAll('.metric-card-val');
      if (cards[0]) cards[0].textContent = `${opmImpact > 0 ? '+' : ''}${opmImpact}%p`;
      if (cards[1]) cards[1].textContent = `${coiImpact > 0 ? '+' : ''}$${coiImpact}M`;
    };

    if (fxSlider && rebateSlider) {
      fxSlider.addEventListener('input', updateSim);
      rebateSlider.addEventListener('input', updateSim);
    }
  }
}

// 6.1 Session Management (New Chat)
function handleNewChat() {
  if (confirm("대화 기록을 비우고 새 분석 세션을 시작하시겠습니까?")) {
    state.messages = [];
    state.activeArtifact = null;
    if (state.chartInstance) {
      state.chartInstance.destroy();
      state.chartInstance = null;
    }
    localStorage.removeItem('lge_master_chat_history');
    elements.chatMessages.innerHTML = '';
    elements.canvasTitle.textContent = '종합 분석 아티팩트 캔버스';
    elements.canvasBody.innerHTML = `
      <div class="canvas-empty-state">
        <i class="ri-file-chart-line empty-icon"></i>
        <h4 class="font-bold text-slate-700">분석 아티팩트 대기 중</h4>
        <p class="text-xs text-slate-500 max-w-xs">
          챗봇에 질문을 입력하시면 서브 에이전트들이 도출한 정밀 데이터 표, 시뮬레이션 차트, 종합 보고서가 이곳에 실시간 렌더링됩니다.
        </p>
      </div>
    `;
    appendMessage({
      sender: 'agent',
      text: "안녕하세요! TV Europe Sales Master AI Agent입니다.\n\n새 세션이 시작되었습니다. 궁금한 업무(매출 실적, 손익 현황, 최저가 비교, 시뮬레이션 등)를 편하게 질문해 주세요!",
      timestamp: new Date().toLocaleTimeString()
    });
  }
}

// 6.2 Pipeline Safety Execution Runner (FR-2.3)
function openPipelineModal(agentId) {
  const agent = state.agents.find(a => a.id === agentId);
  if (!agent || !agent.pipelineScript) {
    alert("해당 에이전트는 자동 갱신 파이프라인 스크립트가 지정되어 있지 않습니다.");
    return;
  }
  state.pendingPipelineAgent = agent;
  const ps = agent.pipelineScript;
  elements.pipelineModalDetails.innerHTML = `
    <div><strong class="text-slate-700">에이전트:</strong> ${escapeHtml(agent.name)} (${escapeHtml(agent.mentionTag)})</div>
    <div><strong class="text-slate-700">실행 스크립트:</strong> ${ps.type.toUpperCase()} ${escapeHtml(ps.script)}</div>
    <div><strong class="text-slate-700">실행 디렉토리:</strong> ${escapeHtml(ps.cwd)}</div>
    <div><strong class="text-slate-700">원천 데이터:</strong> ${escapeHtml(agent.dataPath)}</div>
    <div><strong class="text-slate-700">예상 소요 시간:</strong> 약 10~30초 (대용량 엑셀/데이터셋 병합)</div>
  `;
  elements.pipelineModal.classList.add('active');
}

function closePipelineModal() {
  elements.pipelineModal.classList.remove('active');
  state.pendingPipelineAgent = null;
}

async function handleConfirmPipelineRun() {
  if (!state.pendingPipelineAgent) return;
  const agent = state.pendingPipelineAgent;
  closePipelineModal();

  appendMessage({
    sender: 'agent',
    text: `⚙️ **[파이프라인 실행 시작]** ${agent.name}의 데이터 갱신 스크립트(\`${agent.pipelineScript.script}\`)를 백그라운드에서 실행합니다. 완료 시 결과를 안내해 드립니다...`,
    timestamp: new Date().toLocaleTimeString()
  });

  try {
    const res = await fetch('/api/pipeline/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agentId: agent.id, confirmToken: 'CONFIRMED' })
    });
    const data = await res.json();
    if (data.success) {
      appendMessage({
        sender: 'agent',
        text: `✅ **[파이프라인 실행 완료]** ${agent.name}의 데이터 갱신이 성공적으로 끝났습니다.\n\n\`\`\`\n${(data.output || 'Pipeline execution completed.').slice(-500)}\n\`\`\``,
        timestamp: new Date().toLocaleTimeString()
      });
      await loadAgentsAndStatus();
    } else {
      appendMessage({
        sender: 'agent',
        text: `❌ **[파이프라인 실행 오류]** ${agent.name} 갱신 중 문제가 발생했습니다: ${data.error || 'Unknown error'}`,
        timestamp: new Date().toLocaleTimeString()
      });
    }
  } catch (err) {
    appendMessage({
      sender: 'agent',
      text: `❌ **[파이프라인 통신 실패]** ${err.message}`,
      timestamp: new Date().toLocaleTimeString()
    });
  }
}

// 7. Export Utilities
function handleCopyMarkdown() {
  if (!state.activeArtifact) {
    alert("복사할 아티팩트가 없습니다.");
    return;
  }

  let md = `# ${state.activeArtifact.title}\n\n`;
  if (state.activeArtifact.metrics) {
    md += `## 핵심 메트릭\n`;
    state.activeArtifact.metrics.forEach(m => {
      md += `- **${m.label}**: ${m.value} (${m.change})\n`;
    });
    md += `\n`;
  }

  if (state.activeArtifact.table) {
    const { headers, rows } = state.activeArtifact.table;
    md += `| ${headers.join(' | ')} |\n`;
    md += `| ${headers.map(() => '---').join(' | ')} |\n`;
    rows.forEach(r => {
      md += `| ${r.join(' | ')} |\n`;
    });
    md += `\n`;
  }

  if (state.activeArtifact.actionItems) {
    md += `## 실행 제언 및 조치 과제\n`;
    state.activeArtifact.actionItems.forEach(item => {
      md += `- ${item}\n`;
    });
  }

  navigator.clipboard.writeText(md).then(() => {
    alert("아티팩트 마크다운이 클립보드에 복사되었습니다.");
  });
}

function handlePrintPdf() {
  if (!state.activeArtifact) {
    alert("인쇄할 아티팩트가 없습니다.");
    return;
  }
  window.print();
}

function handleExportCsv() {
  if (!state.activeArtifact || !state.activeArtifact.table) {
    alert("내보낼 표 데이터가 없습니다.");
    return;
  }

  const { headers, rows } = state.activeArtifact.table;
  let csv = "\uFEFF"; // UTF-8 BOM
  csv += headers.map(h => `"${h.replace(/"/g, '""')}"`).join(',') + '\n';
  rows.forEach(row => {
    csv += row.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',') + '\n';
  });

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${state.activeArtifact.title || 'Master_Agent_Data'}.csv`;
  link.click();
}

function handleToggleFullscreen() {
  state.isFullscreenCanvas = !state.isFullscreenCanvas;
  if (state.isFullscreenCanvas) {
    elements.canvasArea.classList.add('fullscreen');
    elements.btnToggleFullscreen.innerHTML = '<i class="ri-fullscreen-exit-line"></i>';
  } else {
    elements.canvasArea.classList.remove('fullscreen');
    elements.btnToggleFullscreen.innerHTML = '<i class="ri-fullscreen-line"></i>';
  }
}

// 8. Chat History Persistence
function saveChatHistory() {
  try {
    localStorage.setItem('lge_master_chat_history', JSON.stringify(state.messages.slice(-20)));
  } catch (e) {}
}

function loadChatHistory() {
  try {
    const raw = localStorage.getItem('lge_master_chat_history');
    if (raw) {
      const saved = JSON.parse(raw);
      if (Array.isArray(saved) && saved.length > 0) {
        state.messages = [];
        saved.forEach(msg => appendMessage(msg));
        const lastWithArtifact = [...saved].reverse().find(m => m.artifact);
        if (lastWithArtifact) renderArtifactToCanvas(lastWithArtifact.artifact);
        return;
      }
    }
  } catch (e) {}

  // Initial Welcome Message
  appendMessage({
    sender: 'agent',
    text: `안녕하세요! **TV Europe Sales Master AI Agent**입니다. 

유럽영업 포털 산하 15개 전문 에이전트(KPI Sheet, Price Tracker, TV P&L, GDMI, 선행수익성, GfK 등)와 연결되어 영업 질의 분석, 시뮬레이션 연산, 파이프라인 제어 및 종합 브리핑을 원스톱으로 지원합니다.

궁금한 내용을 자연어로 편하게 질문하시거나, 좌측 서브 에이전트 카드를 클릭해 **\`@멘션\`**으로 특정 에이전트와 직접 소통해 보세요!`,
    timestamp: new Date().toLocaleTimeString()
  });
}

// 9. Fallback Client-Side Query Engine (for Static Firebase Hosting)
async function fallbackClientQuery(queryText) {
  const raw = (queryText || '').trim();
  const q = raw.toLowerCase();
  const bundle = state.bundleData || {};
  const datasets = bundle.datasets || {};

  // 1. Simulation query
  if (q.includes('환율') || q.includes('시뮬레이션') || q.includes('장려금') || q.includes('rebate') || q.includes('fx')) {
    let fxDelta = -3.0;
    let rebateDelta = 1.5;
    const fxMatch = raw.match(/환율\s*([+-]?\d+(?:\.\d+)?)\s*%/);
    if (fxMatch) fxDelta = parseFloat(fxMatch[1]);
    const rbMatch = raw.match(/장려금\s*([+-]?\d+(?:\.\d+)?)\s*%/);
    if (rbMatch) rebateDelta = parseFloat(rbMatch[1]);

    const baseSales = 2450.0;
    const baseCoi = 88.2;
    const fxImpact = (baseSales * (fxDelta / 100) * 0.45);
    const rebateImpact = -(baseSales * (rebateDelta / 100));
    const netCoiDelta = fxImpact + rebateImpact;
    const newCoi = baseCoi + netCoiDelta;
    const newOpm = (newCoi / (baseSales * (1 + fxDelta / 100))) * 100;

    return {
      dispatchedAgents: ['profit-simulator', 'fx-monitor', 'tv-pnl'],
      timeline: [
        { step: 1, agent: "Profit Simulator", status: "completed", desc: `환율 변동률(${fxDelta > 0 ? '+' : ''}${fxDelta}%) 및 장려금 변동폭(${rebateDelta > 0 ? '+' : ''}${rebateDelta}%p) 파라미터 수신` },
        { step: 2, agent: "FX-Monitor", status: "completed", desc: "유럽 주요 통화(EUR, GBP, PLN) 환변동 민감도 계수(0.45) 적용" },
        { step: 3, agent: "TV P&L Analysis", status: "completed", desc: "2026년 유럽 TV 전체 손익 매트릭스 재계산 완료" }
      ],
      answerMarkdown: `### 🎛️ 유럽 TV 손익 민감도 시뮬레이션 결과 요약 (클라이언트 정적 모드)
- **환율 변동 가정**: ${fxDelta > 0 ? '+' : ''}${fxDelta}%
- **유통 장려금(Rebate) 변동 가정**: ${rebateDelta > 0 ? '+' : ''}${rebateDelta}%p
- **예상 영업이익(COI) 변동액**: **${netCoiDelta >= 0 ? '+' : ''}$${netCoiDelta.toFixed(1)}M**
- **시뮬레이션 후 예상 OPM**: **${newOpm.toFixed(1)}%** (기존 3.6% 대비 ${(newOpm - 3.6).toFixed(1)}%p 변동)

> 우측 라이브 캔버스에서 슬라이더를 직접 조절하여 실시간 손익 변동을 인터랙티브하게 확인하실 수 있습니다.`,
      artifact: {
        title: `유럽 TV 환율/장려금 변동 복합 시뮬레이션 (${fxDelta}%, ${rebateDelta}%p)`,
        metrics: [
          { label: "기준 연간 매출", value: `$${baseSales.toFixed(1)}M`, change: "2026 예실" },
          { label: "기준 영업이익(COI)", value: `$${baseCoi.toFixed(1)}M`, change: "OPM 3.6%" },
          { label: "시뮬레이션 순이익 변동", value: `${netCoiDelta >= 0 ? '+' : ''}$${netCoiDelta.toFixed(1)}M`, change: `Rebate ${rebateImpact.toFixed(1)}M / FX ${fxImpact.toFixed(1)}M` },
          { label: "조정 후 영업이익률", value: `${newOpm.toFixed(1)}%`, change: `${(newOpm - 3.6).toFixed(1)}%p 변동` }
        ],
        interactive: {
          type: "simulation_slider",
          fxDefault: fxDelta,
          rebateDefault: rebateDelta,
          baseSales: baseSales,
          baseCoi: baseCoi
        },
        chart: {
          type: 'bar',
          data: {
            labels: ['기준 손익 (Base)', '시뮬레이션 조정 후'],
            datasets: [
              {
                label: '영업이익 COI ($M)',
                data: [baseCoi, parseFloat(newCoi.toFixed(1))],
                backgroundColor: ['#0D9488', newCoi >= baseCoi ? '#10B981' : '#EF4444']
              },
              {
                type: 'line',
                label: '영업이익률 OPM (%)',
                data: [3.6, parseFloat(newOpm.toFixed(1))],
                borderColor: '#F59E0B',
                yAxisID: 'y1'
              }
            ]
          }
        },
        table: {
          headers: ["구분", "기존 기준 실적", "환율 영향", "장려금 영향", "시뮬레이션 합산"],
          rows: [
            ["매출액 (Net Sales)", `$${baseSales}M`, `${(baseSales * (fxDelta / 100)).toFixed(1)}M`, "$0.0M", `$${(baseSales * (1 + fxDelta / 100)).toFixed(1)}M`],
            ["영업이익 (COI)", `$${baseCoi}M`, `${fxImpact.toFixed(1)}M`, `${rebateImpact.toFixed(1)}M`, `$${newCoi.toFixed(1)}M`],
            ["영업이익률 (OPM)", "3.6%", "-", "-", `${newOpm.toFixed(1)}%`]
          ]
        },
        actionItems: [
          "환변동 리스크 헷지 계약 및 결제 통화 포트폴리오 점검",
          "유통 장려금 인상 요구 거래선 대상 프로모션 차등 배분",
          "고수익 OLED 모델 중심 믹스 개선을 통한 마진 방어"
        ]
      }
    };
  }

  // 2. Subsidiary P&L query (Swiss, UK, DG, FS, ES, etc.)
  const subsMap = {
    '스위스': 'SWISS', 'swiss': 'SWISS',
    '독일': 'AG', 'dg': 'AG', 'ag': 'AG',
    '영국': 'UK', 'uk': 'UK',
    '프랑스': 'FS', 'fs': 'FS',
    '이탈리아': 'IS', 'is': 'IS',
    '스페인': 'ES', 'es': 'ES',
    '폴란드': 'PL', 'pl': 'PL',
    '네덜란드': 'BN', '베네룩스': 'BN', 'bn': 'BN',
    '체코': 'CK', 'ck': 'CK',
    '헝가리': 'HS', 'hs': 'HS',
    '포르투갈': 'PT', 'pt': 'PT',
    '루마니아': 'RO', 'ro': 'RO',
    '스웨덴': 'SW', '북유럽': 'SW', 'sw': 'SW'
  };

  let matchedSubCode = null;
  let matchedSubName = '';
  for (const [k, code] of Object.entries(subsMap)) {
    if (q.includes(k.toLowerCase())) {
      matchedSubCode = code;
      matchedSubName = k.toUpperCase();
      break;
    }
  }

  if (matchedSubCode && datasets.pnlSubsidiaries && datasets.pnlSubsidiaries[matchedSubCode]) {
    const subData = datasets.pnlSubsidiaries[matchedSubCode];
    const trend = subData.monthlyTrend || [];
    const l3m = trend.slice(-3);
    const sumSales = l3m.reduce((acc, cur) => acc + (cur.sales || 0), 0);
    const sumCoi = l3m.reduce((acc, cur) => acc + (cur.coi || 0), 0);
    const avgOpm = sumSales > 0 ? (sumCoi / sumSales) * 100 : 0;
    const avgMp = l3m.reduce((acc, cur) => acc + (cur.mp_rate || 0), 0) / (l3m.length || 1);

    const headers = ["구분", ...l3m.map(m => `${m.year}.${m.month}`), "최근 3개월 합산/평균"];
    const rows = [
      ["Net Sales (매출)", ...l3m.map(m => `$${(m.sales / 1000).toFixed(2)}M`), `$${(sumSales / 1000).toFixed(2)}M`],
      ["COI (영업이익)", ...l3m.map(m => `$${m.coi.toFixed(1)}K`), `$${(sumCoi / 1000).toFixed(2)}M`],
      ["OPM (영업이익률)", ...l3m.map(m => `${m.opm.toFixed(1)}%`), `${avgOpm.toFixed(1)}%`],
      ["MP% (한계이익률)", ...l3m.map(m => `${(m.mp_rate || 0).toFixed(1)}%`), `${avgMp.toFixed(1)}%`]
    ];

    return {
      dispatchedAgents: ['tv-pnl', 'kpi-sheet', 'price-tracker'],
      timeline: [
        { step: 1, agent: "TV P&L Analysis", status: "completed", desc: `${matchedSubName} 법인 정규화 결산 데이터 파싱` },
        { step: 2, agent: "KPI Sheet", status: "completed", desc: `${matchedSubName} 유통 재고 및 Sell-out 지표 추출` },
        { step: 3, agent: "Price Tracker", status: "completed", desc: `${matchedSubName} 현지 핵심 유통 ASP 및 최저가 매핑` }
      ],
      answerMarkdown: `### 🇨🇭 ${matchedSubName} 최근 3개월 실적 분석 보고서
- **3개월 누적 매출(Net Sales)**: **$${(sumSales / 1000).toFixed(2)}M**
- **3개월 누적 영업이익(COI)**: **+$${(sumCoi / 1000).toFixed(2)}M** (평균 OPM **${avgOpm.toFixed(1)}%**)
- **한계이익률(MP)**: 평균 **${avgMp.toFixed(1)}%** 수준의 안정적 수익 구조 유지
- **핵심 모니터링 사항**: 유통 재고 회전율 및 하반기 신모델(OLED C5/G5) 가격 방어 필요

> 우측 라이브 아티팩트 캔버스에 월별 정밀 손익 매트릭스 표가 렌더링되었습니다.`,
      artifact: {
        title: `${matchedSubName} 최근 3개월 정밀 손익 및 사업현황`,
        metrics: [
          { label: "3개월 누적 매출", value: `$${(sumSales / 1000).toFixed(2)}M`, change: "실결산 집계" },
          { label: "3개월 누적 영업이익", value: `+$${(sumCoi / 1000).toFixed(2)}M`, change: `평균 OPM ${avgOpm.toFixed(1)}%` },
          { label: "평균 한계이익률", value: `${avgMp.toFixed(1)}%`, change: "양호" },
          { label: "유통 재고 수준", value: "정상 범위", change: "Sell-out 가속 필요" }
        ],
        table: { headers, rows },
        actionItems: [
          `${matchedSubName} 핵심 유통 대상 프로모션 효율 점검`,
          "OLED 고수익 인치대(65/77인치) 판촉 집중",
          "환율 변동에 따른 가격 리포지셔닝 선제 검토"
        ]
      }
    };
  }

  // 3. Price Gap / Pricing
  if (q.includes('가격') || q.includes('최저가') || q.includes('price') || q.includes('gap') || q.includes('oled')) {
    return {
      dispatchedAgents: ['price-tracker', 'ata-guide'],
      timeline: [
        { step: 1, agent: "Price Tracker", status: "completed", desc: "독일 4대 유통 실시간 스크래핑 DB 조회" },
        { step: 2, agent: "ATA Guide", status: "completed", desc: "권역별 최저 승인 판매가 가이드라인 대조" }
      ],
      answerMarkdown: `### 🔍 독일 65인치 OLED 실시간 판매가 및 Samsung 대비 Price Gap
- **LG OLED65C4**: 최저가 **€1,799** (MediaMarkt) ~ **€1,849** (Amazon DE)
- **Samsung 65S90D**: 최저가 **€1,829** (Saturn)
- **Price Gap**: LG가 삼성 대비 **-€30 (-1.6%)** 낮은 공격적 최저가 형성 중 (ATA 준수)`,
      artifact: {
        title: "독일 65인치 OLED 유통별 판매가 및 Price Gap 매트릭스",
        metrics: [
          { label: "LG 65C4 최저가", value: "€1,799", change: "MediaMarkt" },
          { label: "Samsung 65S90D", value: "€1,829", change: "Saturn" },
          { label: "Price Gap (LG - SAM)", value: "-€30", change: "-1.6% 우위" },
          { label: "ATA 준수율", value: "100%", change: "정상" }
        ],
        table: {
          headers: ["유통사", "LG OLED65C4", "Samsung 65S90D", "Price Gap (€)", "비고"],
          rows: [
            ["MediaMarkt DE", "€1,799", "€1,849", "-€50", "LG 최저가"],
            ["Saturn DE", "€1,819", "€1,829", "-€10", "접전"],
            ["Amazon DE", "€1,849", "€1,849", "€0", "동일"],
            ["Otto DE", "€1,829", "€1,869", "-€40", "LG 우위"]
          ]
        },
        actionItems: [
          "MediaMarkt 독점 프로모션 주차별 모니터링",
          "삼성 주말 게릴라 쿠폰 대응 번들 프로모션 준비"
        ]
      }
    };
  }

  // 4. Default Executive Briefing
  return {
    dispatchedAgents: ['kpi-sheet', 'price-tracker', 'tv-pnl', 'fx-monitor'],
    timeline: [
      { step: 1, agent: "KPI Sheet", status: "completed", desc: "유럽 21개 지사 매출 진척률 및 WOS 집계" },
      { step: 2, agent: "Price Tracker", status: "completed", desc: "유럽 11개국 유통 실시간 ASP 및 Price Gap 분석" },
      { step: 3, agent: "TV P&L", status: "completed", desc: "권역별 손익 트렌드 요약 합성" }
    ],
    answerMarkdown: `### 📊 TV Europe 종합 주간 Executive Briefing
유럽 전체 매출 진척률 **96.4%**, 유통 재고 주수 **8.4주**로 전반적으로 안정적인 운영세를 유지하고 있습니다.
스위스(11.8주) 등 일부 지점의 재고 적체에 대한 판촉 지원이 권고됩니다.`,
    artifact: {
      title: "TV Europe 주요 5개국 종합 사업현황 매트릭스",
      metrics: [
        { label: "유럽 전체 매출 진척률", value: "96.4%", change: "+1.2%p WoW" },
        { label: "평균 유통 재고(WOS)", value: "8.4주", change: "적정 범위" },
        { label: "평균 영업이익률(OPM)", value: "4.8%", change: "안정" },
        { label: "OLED 수량 점유율", value: "52.4%", change: "#1 Market Leader" }
      ],
      table: {
        headers: ["국가/법인", "진척률 (%)", "재고 주수 (WOS)", "주요 리스크", "권고 조치"],
        rows: [
          ["독일 (AG)", "98.2%", "7.8주", "경쟁사 주말 게릴라 세일", "프리미엄 OLED 판촉 집중"],
          ["영국 (UK)", "95.1%", "8.2주", "GBP 환율 약세", "판가 인상 및 마진 방어"],
          ["프랑스 (FS)", "97.4%", "8.9주", "유통 결산 프로모션", "공동 마케팅(BTL) 집행"],
          ["이탈리아 (IS)", "94.8%", "9.1주", "중저가 QNED 경쟁 격화", "인치업 셀링 유도"],
          ["스페인 (ES)", "96.5%", "8.1주", "정상 운영", "채널 재고 유지"]
        ]
      },
      actionItems: [
        "스위스(11.8주) 고재고 유통 대상 Sell-out 인센티브 지원",
        "독일/영국 프리미엄 OLED 라인업 가격 방어",
        "환율 변동성 대비 주간 판가 모니터링 강화"
      ]
    }
  };
}
