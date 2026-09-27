/**
 * AI Identity Copilot Chat Module
 * Conversational analyst workbench rendering LangGraph reasoning chains and SAR reports.
 */

window.initCopilotModule = function() {
  setupCopilotUI();
};

function setupCopilotUI() {
  const sendBtn = document.getElementById('btn-copilot-send');
  const input = document.getElementById('copilot-input-text');

  if (sendBtn && input) {
    sendBtn.addEventListener('click', () => submitCopilotQuery(input.value));
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') submitCopilotQuery(input.value);
    });
  }

  // Quick prompt buttons
  document.querySelectorAll('.quick-prompt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const q = btn.getAttribute('data-query');
      if (input) input.value = q;
      submitCopilotQuery(q);
    });
  });

  const sarBtn = document.getElementById('btn-generate-sar-instant');
  if (sarBtn) {
    sarBtn.addEventListener('click', () => {
      submitCopilotQuery('Generate investigation summary.');
    });
  }

  // Initial welcome message
  appendCopilotMessage('assistant', `
    ### AI Identity Copilot Ready
    I am initialized with multi-modal reasoning across your verification pipeline.
    You can interrogate active sessions, analyze deepfake probability breakdowns, or generate FinCEN-compliant Suspicious Activity Reports (SAR).
  `, [
    "Step 1: Ingested telemetry from 6 active benchmark datasets",
    "Step 2: Connected to Identity Knowledge Graph & Blockchain Audit Ledger"
  ]);
}

window.updateCopilotSession = function(sessionData) {
  const label = document.getElementById('copilot-session-label');
  if (label && sessionData) {
    label.innerText = `Session: ${sessionData.session_id}`;
  }

  appendCopilotMessage('assistant', `
    **Updated Active Investigation Context:** Session \`${sessionData.session_id}\` (${sessionData.user_id}).
    - **Verdict:** \`${sessionData.final_decision}\`
    - **Trust Score:** \`${sessionData.trust_score.trust_score}/1000\`
    - **Deepfake Prob:** \`${(sessionData.deepfake_result.deepfake_probability * 100).toFixed(1)}%\`
    - **Active Anomaly Flags:** ${sessionData.alerts_triggered.length}
    Ask me: *"Why did verification fail?"* or *"Explain the fraud indicators."*
  `);
};

async function submitCopilotQuery(queryText) {
  if (!queryText || !queryText.trim()) return;

  const input = document.getElementById('copilot-input-text');
  if (input) input.value = '';

  // Append user message
  appendCopilotMessage('user', queryText);

  // Show thinking indicator
  const thinkingId = appendCopilotMessage('assistant', '<em>Analyzing multi-modal forensic telemetry and reasoning graph...</em>');

  try {
    const activeSessionId = window.AppState.currentSession?.session_id || 'kyc_sess_deepfake_0088';
    const activeUserId = window.AppState.currentSession?.user_id || 'usr_infiltrator_swap_02';

    const res = await fetch('/api/v1/copilot/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: queryText,
        session_id: activeSessionId,
        user_id: activeUserId
      })
    });

    // Remove thinking message
    const thinkingElem = document.getElementById(thinkingId);
    if (thinkingElem) thinkingElem.remove();

    if (!res.ok) {
      appendCopilotMessage('assistant', 'Unable to complete reasoning query. Please verify session state.');
      return;
    }

    const data = await res.json();
    appendCopilotMessage('assistant', data.answer_markdown, data.reasoning_chain);

  } catch (err) {
    console.error('Copilot query error:', err);
    appendCopilotMessage('assistant', 'Network error communicating with Copilot agent.');
  }
}

function appendCopilotMessage(sender, text, reasoningChain = null) {
  const container = document.getElementById('copilot-messages-list');
  if (!container) return null;

  const msgId = 'msg_' + Math.random().toString(36).substring(2, 9);
  const div = document.createElement('div');
  div.id = msgId;
  div.className = `message-bubble ${sender}`;

  let html = '';
  if (reasoningChain && reasoningChain.length > 0) {
    html += `
      <div class="reasoning-step-box">
        <strong style="color: var(--accent-cyan);">Multi-Agent Reasoning Chain:</strong><br>
        ${reasoningChain.map(step => `• ${step}`).join('<br>')}
      </div>
    `;
  }

  // Basic markdown formatting conversion (headers, bold, lists, tables)
  let formatted = text
    .replace(/^### (.*$)/gim, '<h4 style="margin: 8px 0; color: #fff;">$1</h4>')
    .replace(/^#### (.*$)/gim, '<h5 style="margin: 6px 0; color: var(--accent-cyan);">$1</h5>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code style="background: rgba(0,0,0,0.4); padding: 2px 6px; border-radius: 4px; font-family: var(--font-mono); color: var(--accent-cyan);">$1</code>')
    .replace(/^\- (.*$)/gim, '<li style="margin-left: 18px;">$1</li>')
    .replace(/\n/g, '<br>');

  html += formatted;
  div.innerHTML = html;

  container.appendChild(div);
  container.scrollTop = container.scrollHeight;

  return msgId;
}
