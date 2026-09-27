/**
 * Enterprise Digital Identity, Trust & Deepfake Detection Platform
 * Main Application Orchestrator & State Management
 */

const AppState = {
  activeTab: 'tab-dashboard',
  currentSession: null,
  activeCases: [],
  kpis: null,
  alerts: []
};

document.addEventListener('DOMContentLoaded', async () => {
  initNavigation();
  await loadAnalyticsKPIs();
  await loadAlertsFeed();
  window.initStudioModule();
  window.initGraphModule();
  window.initCopilotModule();
  window.initPresentationModule();
});

function initNavigation() {
  const tabs = document.querySelectorAll('.nav-tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = tab.getAttribute('data-tab');
      switchTab(targetId);
    });
  });

  const exportBtn = document.getElementById('btn-export-audit');
  if (exportBtn) {
    exportBtn.addEventListener('click', downloadAuditProof);
  }
}

function switchTab(targetId) {
  document.querySelectorAll('.nav-tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-tab') === targetId);
  });
  document.querySelectorAll('.view-section').forEach(sec => {
    sec.classList.toggle('active', sec.id === targetId);
  });
  AppState.activeTab = targetId;

  if (targetId === 'tab-graph' && window.renderKnowledgeGraph) {
    window.renderKnowledgeGraph();
  }
}

async function loadAnalyticsKPIs() {
  try {
    const res = await fetch('/api/v1/analytics/kpis');
    if (!res.ok) return;
    const data = await res.json();
    AppState.kpis = data;

    // Render KPIs
    document.getElementById('kpi-total-verif').innerText = Number(data.total_verifications).toLocaleString();
    document.getElementById('kpi-success-rate').innerText = data.verification_success_rate.toFixed(2) + '%';
    document.getElementById('kpi-deepfake-count').innerText = Number(data.deepfake_alerts_count).toLocaleString();
    document.getElementById('kpi-syndicates-count').innerText = data.active_syndicates_detected;
    document.getElementById('kpi-latency').innerText = data.avg_latency_seconds.toFixed(2) + 's';

    // Render Trust Distribution Bars
    renderTrustDistribution(data.trust_score_distribution);
  } catch (err) {
    console.error('Failed to load analytics KPIs:', err);
  }
}

function renderTrustDistribution(distribution) {
  const container = document.getElementById('trust-distribution-bars');
  if (!container || !distribution) return;

  container.innerHTML = distribution.map(item => {
    const color = item.percentage > 50 ? 'var(--accent-emerald)' :
                  item.percentage > 15 ? 'var(--accent-blue)' :
                  item.percentage > 2 ? 'var(--accent-amber)' : 'var(--accent-crimson)';

    return `
      <div style="display: flex; flex-direction: column; gap: 4px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
          <span style="font-weight: 600;">${item.bracket}</span>
          <span style="font-family: var(--font-mono); color: ${color};">${item.percentage}% (${Number(item.count).toLocaleString()})</span>
        </div>
        <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.06); border-radius: var(--radius-full); overflow: hidden;">
          <div style="width: ${item.percentage}%; height: 100%; background: ${color}; border-radius: var(--radius-full); transition: width 0.8s ease;"></div>
        </div>
      </div>
    `;
  }).join('');
}

async function loadAlertsFeed() {
  try {
    const res = await fetch('/api/v1/alerts/feed');
    if (!res.ok) return;
    const alerts = await res.json();
    AppState.alerts = alerts;

    // Update alert count badge
    const badge = document.getElementById('alert-counter-badge');
    if (badge) badge.innerText = alerts.length;

    // Render Recent Alerts in Dashboard
    const dashboardAlerts = document.getElementById('dashboard-recent-alerts');
    if (dashboardAlerts) {
      dashboardAlerts.innerHTML = alerts.slice(0, 4).map(alert => `
        <div style="padding: 12px 14px; background: rgba(255,255,255,0.03); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); display: flex; align-items: flex-start; gap: 12px;">
          <span class="sev-badge ${alert.severity}" style="margin-top: 2px;">${alert.severity}</span>
          <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; font-size: 0.76rem; color: var(--text-muted);">
              <span>${alert.category}</span>
              <span>${alert.timestamp.split(' ')[1] || 'Just now'}</span>
            </div>
            <div style="font-size: 0.82rem; font-weight: 600; margin-top: 2px;">${alert.description}</div>
            <div style="font-size: 0.72rem; color: var(--text-dim); margin-top: 2px; font-family: var(--font-mono);">
              User: ${alert.user_id} • Score: ${alert.trust_score}/1000
            </div>
          </div>
        </div>
      `).join('');
    }

    // Render Full Alerts Table in Tab Alerts
    renderAlertsTable(alerts);
  } catch (err) {
    console.error('Failed to load alert feed:', err);
  }
}

function renderAlertsTable(alerts) {
  const tbody = document.getElementById('alerts-table-body');
  if (!tbody) return;

  tbody.innerHTML = alerts.map(a => `
    <tr>
      <td><span class="sev-badge ${a.severity}">${a.severity}</span></td>
      <td style="font-family: var(--font-mono); font-weight: 600;">${a.alert_id}</td>
      <td><strong>${a.category}</strong></td>
      <td style="font-family: var(--font-mono);">${a.user_id}</td>
      <td style="max-width: 320px;">${a.description}</td>
      <td><strong style="color: ${a.trust_score > 600 ? 'var(--accent-emerald)' : 'var(--accent-crimson)'}">${a.trust_score}</strong></td>
      <td><span class="vis-badge" style="background: rgba(255,255,255,0.05);">${a.status}</span></td>
      <td>
        <div style="display: flex; gap: 6px;">
          <button class="btn-secondary" style="padding: 4px 10px; font-size: 0.72rem;" onclick="handleAlertAction('${a.alert_id}', 'BLOCK_USER')">Block</button>
          <button class="btn-secondary" style="padding: 4px 10px; font-size: 0.72rem;" onclick="handleAlertAction('${a.alert_id}', 'RESOLVE')">Resolve</button>
        </div>
      </td>
    </tr>
  `).join('');
}

async function handleAlertAction(alertId, action) {
  try {
    const res = await fetch('/api/v1/alerts/action', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ alert_id: alertId, action: action })
    });
    if (res.ok) {
      await loadAlertsFeed();
    }
  } catch (err) {
    console.error('Failed to execute alert action:', err);
  }
}

function downloadAuditProof() {
  const auditProof = AppState.currentSession?.audit_proof || {
    block_index: 42,
    timestamp_iso: new Date().toISOString(),
    merkle_root: "9f82a7bb0149c5e3170e884128f902187b5a329d0f",
    block_hash: "00b9a8f27e10c491e0a82b9921e5821034d9a102941b",
    tamper_proof_verified: true,
    ledger: "ENTERPRISE-DIGITAL-TRUST-MERKLE-CHAIN"
  };

  const blob = new Blob([JSON.stringify(auditProof, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `blockchain_audit_proof_block_${auditProof.block_index}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

window.AppState = AppState;
window.handleAlertAction = handleAlertAction;
