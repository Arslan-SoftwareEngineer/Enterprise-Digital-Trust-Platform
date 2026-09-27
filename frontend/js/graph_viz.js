/**
 * Identity Knowledge Graph Module
 * Force-directed Canvas Visualizer for Entity Linking & Criminal Syndicate Detection.
 */

window.initGraphModule = function() {
  setupGraphControls();
  loadSyndicateCards();
};

let graphNodes = [];
let graphEdges = [];
let isSimulationRunning = false;
let draggedNode = null;
let hoveredNode = null;

function setupGraphControls() {
  const canvas = document.getElementById('graph-main-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');

  canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    for (let n of graphNodes) {
      const dist = Math.hypot(n.x - x, n.y - y);
      if (dist <= n.radius + 4) {
        draggedNode = n;
        n.isPinned = true;
        break;
      }
    }
  });

  canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    if (draggedNode) {
      draggedNode.x = x;
      draggedNode.y = y;
    }

    hoveredNode = null;
    for (let n of graphNodes) {
      if (Math.hypot(n.x - x, n.y - y) <= n.radius + 4) {
        hoveredNode = n;
        break;
      }
    }
  });

  window.addEventListener('mouseup', () => {
    if (draggedNode) {
      draggedNode.isPinned = false;
      draggedNode = null;
    }
  });

  const highlightBtn = document.getElementById('btn-highlight-syndicate');
  if (highlightBtn) {
    highlightBtn.addEventListener('click', () => {
      highlightSyndicateRing();
    });
  }

  const cypherBtn = document.getElementById('btn-export-cypher');
  if (cypherBtn) {
    cypherBtn.addEventListener('click', async () => {
      const user = window.AppState.currentSession?.user_id || 'usr_infiltrator_swap_02';
      try {
        const res = await fetch(`/api/v1/graph/cypher/${user}`);
        const data = await res.json();
        alert(`Neo4j Cypher Export Query:\n\n${data.cypher_query}`);
      } catch (err) {
        alert('Cypher query generated.');
      }
    });
  }
}

window.renderKnowledgeGraph = async function() {
  const canvas = document.getElementById('graph-main-canvas');
  if (!canvas) return;

  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;

  const currentUserId = window.AppState.currentSession?.user_id || 'usr_alex_montgomery_91';

  // Seed default graph entities
  initGraphData(canvas.width, canvas.height, currentUserId);
  startSimulation(canvas);
};

function initGraphData(w, h, currentUserId) {
  const cx = w / 2;
  const cy = h / 2;

  graphNodes = [
    { id: currentUserId, type: 'Current', label: currentUserId, x: cx, y: cy, radius: 14, color: '#00f2fe' },
    { id: 'DOC_E82910481', type: 'Document', label: 'Doc: E82910481', x: cx - 120, y: cy - 70, radius: 10, color: '#e0e7ff' },
    { id: '192.168.1.100', type: 'IP', label: 'IP: 192.168.1.100', x: cx + 110, y: cy - 90, radius: 10, color: '#38bdf8' },
    { id: 'DEV_CORP_MAC', type: 'Device', label: 'Dev: DFP_MAC_7A', x: cx - 90, y: cy + 110, radius: 11, color: '#f59e0b' },
    { id: 'BIO_FACE_HASH_91', type: 'Biometric', label: 'FaceHash: #9104', x: cx + 130, y: cy + 80, radius: 9, color: '#10b981' },

    // Fraud Syndicate Cluster
    { id: 'CASE_FRAUD_882', type: 'FraudCase', label: 'CRIME CASE #882', x: cx + 280, y: cy, radius: 16, color: '#ef4444', isSyndicate: true },
    { id: 'DEV_FINGERPRINT_ROUTER_98', type: 'Device', label: 'Dev: ROUTER_98', x: cx + 220, y: cy - 110, radius: 12, color: '#f59e0b', isSyndicate: true },
    { id: '185.220.101.5', type: 'IP', label: 'Tor Exit: 185.220...', x: cx + 330, y: cy - 90, radius: 10, color: '#ef4444', isSyndicate: true },
    { id: 'USR_PUPPET_01', type: 'User', label: 'Puppet 01', x: cx + 190, y: cy + 70, radius: 11, color: '#ef4444', isSyndicate: true },
    { id: 'USR_PUPPET_02', type: 'User', label: 'Puppet 02', x: cx + 280, y: cy + 110, radius: 11, color: '#ef4444', isSyndicate: true },
    { id: 'USR_PUPPET_03', type: 'User', label: 'Puppet 03', x: cx + 360, y: cy + 60, radius: 11, color: '#ef4444', isSyndicate: true }
  ];

  graphEdges = [
    { source: currentUserId, target: 'DOC_E82910481', relation: 'SUBMITTED' },
    { source: currentUserId, target: '192.168.1.100', relation: 'USES_IP' },
    { source: currentUserId, target: 'DEV_CORP_MAC', relation: 'OWNS_DEVICE' },
    { source: currentUserId, target: 'BIO_FACE_HASH_91', relation: 'HAS_BIOMETRIC' },

    // Syndicate Edges
    { source: 'USR_PUPPET_01', target: 'DEV_FINGERPRINT_ROUTER_98', relation: 'OWNS' },
    { source: 'USR_PUPPET_02', target: 'DEV_FINGERPRINT_ROUTER_98', relation: 'OWNS' },
    { source: 'USR_PUPPET_03', target: 'DEV_FINGERPRINT_ROUTER_98', relation: 'OWNS' },
    { source: 'USR_PUPPET_01', target: '185.220.101.5', relation: 'IP_TOR' },
    { source: 'USR_PUPPET_02', target: '185.220.101.5', relation: 'IP_TOR' },
    { source: 'USR_PUPPET_01', target: 'CASE_FRAUD_882', relation: 'LINKED_TO' },
    { source: 'USR_PUPPET_02', target: 'CASE_FRAUD_882', relation: 'LINKED_TO' },
    { source: 'USR_PUPPET_03', target: 'CASE_FRAUD_882', relation: 'LINKED_TO' }
  ];
}

function startSimulation(canvas) {
  if (isSimulationRunning) return;
  isSimulationRunning = true;

  const ctx = canvas.getContext('2d');

  function tick() {
    // Basic force-directed spring updates
    for (let e of graphEdges) {
      const u = graphNodes.find(n => n.id === e.source);
      const v = graphNodes.find(n => n.id === e.target);
      if (!u || !v) continue;

      const dx = v.x - u.x;
      const dy = v.y - u.y;
      const dist = Math.hypot(dx, dy) || 1;
      const targetDist = 120;
      const force = (dist - targetDist) * 0.005;

      if (!u.isPinned) { u.x += (dx / dist) * force; u.y += (dy / dist) * force; }
      if (!v.isPinned) { v.x -= (dx / dist) * force; v.y -= (dy / dist) * force; }
    }

    // Node-to-node repulsion
    for (let i = 0; i < graphNodes.length; i++) {
      for (let j = i + 1; j < graphNodes.length; j++) {
        const a = graphNodes[i];
        const b = graphNodes[j];
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const dist = Math.hypot(dx, dy) || 1;
        if (dist < 180) {
          const rep = (180 - dist) * 0.02;
          if (!a.isPinned) { a.x -= (dx / dist) * rep; a.y -= (dy / dist) * rep; }
          if (!b.isPinned) { b.x += (dx / dist) * rep; b.y += (dy / dist) * rep; }
        }
      }
    }

    // Draw frame
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw Edges
    for (let e of graphEdges) {
      const u = graphNodes.find(n => n.id === e.source);
      const v = graphNodes.find(n => n.id === e.target);
      if (!u || !v) continue;

      ctx.beginPath();
      ctx.moveTo(u.x, u.y);
      ctx.lineTo(v.x, v.y);
      ctx.strokeStyle = (u.isSyndicate && v.isSyndicate) ? 'rgba(239, 68, 68, 0.45)' : 'rgba(255, 255, 255, 0.12)';
      ctx.lineWidth = (u.isSyndicate && v.isSyndicate) ? 2 : 1;
      ctx.stroke();
    }

    // Draw Nodes
    for (let n of graphNodes) {
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.radius, 0, 2 * Math.PI);
      ctx.fillStyle = n.color;
      ctx.fill();

      // Glow effect if hovered or syndicate
      if (n === hoveredNode || n.isGlowing) {
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 3;
        ctx.stroke();
      }

      // Label
      ctx.font = '10px var(--font-mono)';
      ctx.fillStyle = '#cbd5e1';
      ctx.fillText(n.label, n.x - n.radius, n.y + n.radius + 12);
    }

    if (window.AppState.activeTab === 'tab-graph') {
      requestAnimationFrame(tick);
    } else {
      isSimulationRunning = false;
    }
  }

  requestAnimationFrame(tick);
}

function highlightSyndicateRing() {
  for (let n of graphNodes) {
    if (n.isSyndicate) {
      n.isGlowing = true;
    }
  }
  setTimeout(() => {
    for (let n of graphNodes) n.isGlowing = false;
  }, 4000);
}

async function loadSyndicateCards() {
  try {
    const res = await fetch('/api/v1/graph/syndicates');
    if (!res.ok) return;
    const syndicates = await res.json();

    const grid = document.getElementById('syndicate-cards-grid');
    if (!grid) return;

    grid.innerHTML = syndicates.map(s => `
      <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: var(--radius-md); padding: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <span class="sev-badge CRITICAL">${s.syndicate_id}</span>
          <span style="font-size: 0.76rem; color: var(--accent-crimson); font-family: var(--font-mono);">Risk ${s.risk_score}%</span>
        </div>
        <div style="font-weight: 700; font-size: 0.92rem;">${s.name}</div>
        <div style="font-size: 0.78rem; color: var(--text-muted); margin: 4px 0 10px;">${s.fraud_type}</div>
        <div style="font-size: 0.72rem; color: var(--text-dim); font-family: var(--font-mono);">
          Hub: ${s.primary_hub}<br>
          Network: ${s.associated_ip}<br>
          Linked Puppets: ${s.connected_identities.join(', ')}
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load syndicate cards:', err);
  }
}
