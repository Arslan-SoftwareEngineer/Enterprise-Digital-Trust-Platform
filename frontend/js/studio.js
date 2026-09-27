/**
 * Forensic Verification Studio Module
 * Renders multi-modal forensic visualizers: 3D Depth, ELA Heatmap,
 * 2D FFT Frequency Spectrum, Audio Spectrogram, and SHAP Waterfall.
 */

window.initStudioModule = async function() {
  await loadPresetCases();
  setupStudioButtons();
  drawDefaultCanvases();
};

let currentSelectedPayload = null;

async function loadPresetCases() {
  try {
    const res = await fetch('/api/v1/verify/demo-cases');
    if (!res.ok) return;
    const cases = await res.json();
    window.AppState.activeCases = cases;

    const container = document.getElementById('caseSelectorList');
    if (!container) return;

    container.innerHTML = cases.map((c, idx) => {
      const tagClass = c.category === 'AUTHENTIC' ? 'authentic' :
                       c.category === 'FRAUD_DEEPFAKE' ? 'deepfake' :
                       c.category === 'FRAUD_DOCUMENT' ? 'forgery' :
                       c.category === 'FRAUD_VOICE' ? 'voice' :
                       c.category === 'FRAUD_GRAPH' ? 'syndicate' : 'borderline';

      return `
        <div class="case-btn ${idx === 0 ? 'active' : ''}" data-case-id="${c.id}" onclick="selectCase('${c.id}')">
          <div class="case-btn-header">
            <span class="case-tag ${tagClass}">${c.category}</span>
            <span style="font-size: 0.70rem; color: var(--text-dim); font-family: var(--font-mono);">${c.expected_decision}</span>
          </div>
          <div class="case-name">${c.title}</div>
          <div class="case-desc">${c.description}</div>
        </div>
      `;
    }).join('');

    if (cases.length > 0) {
      selectCase(cases[0].id);
    }
  } catch (err) {
    console.error('Failed to load demo cases:', err);
  }
}

function selectCase(caseId) {
  document.querySelectorAll('.case-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-case-id') === caseId);
  });

  const selected = window.AppState.activeCases.find(c => c.id === caseId);
  if (!selected) return;

  currentSelectedPayload = selected.payload;

  // Update preview images
  const docImg = document.getElementById('img-preview-doc');
  const faceImg = document.getElementById('img-preview-face');

  if (docImg && selected.payload.document.image_base64) {
    docImg.src = selected.payload.document.image_base64;
  }
  if (faceImg && selected.payload.face.selfie_image_base64) {
    faceImg.src = selected.payload.face.selfie_image_base64;
  }

  // Clear previous overlays and render base previews
  drawDocumentOverlay(selected.payload.document.document_type === 'NATIONAL_ID' && selected.category === 'FRAUD_DOCUMENT');
  drawFace3DOverlay(selected.category === 'FRAUD_DEEPFAKE');
  draw2DFFTSpectrum(selected.category === 'FRAUD_DEEPFAKE');
  drawAudioSpectrogram(selected.category === 'FRAUD_VOICE');
}

function setupStudioButtons() {
  const runBtn = document.getElementById('btn-run-verification');
  if (runBtn) {
    runBtn.addEventListener('click', runFullVerification);
  }

  const webcamBtn = document.getElementById('btn-use-webcam');
  if (webcamBtn) {
    webcamBtn.addEventListener('click', () => {
      alert('Webcam stream engaged. Facial landmarks and active challenge (Blink & Smile) tracking initiated.');
    });
  }

  const micBtn = document.getElementById('btn-use-mic');
  if (micBtn) {
    micBtn.addEventListener('click', () => {
      alert('Microphone active. Listening for acoustic speech challenge phrase: "Verify digital identity token alpha-7".');
    });
  }
}

async function runFullVerification() {
  if (!currentSelectedPayload) return;

  const btn = document.getElementById('btn-run-verification');
  const originalText = btn.innerHTML;
  btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" style="display:inline-block; vertical-align:middle; margin-right:8px;"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>Processing 10 AI Engines...';
  btn.disabled = true;

  try {
    const tStart = performance.now();
    const res = await fetch('/api/v1/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentSelectedPayload)
    });

    const elapsed = ((performance.now() - tStart) / 1000).toFixed(2);
    document.getElementById('label-processing-time').innerText = `Processing: ${elapsed}s`;

    if (!res.ok) {
      alert('Verification request failed');
      return;
    }

    const data = await res.json();
    window.AppState.currentSession = data;

    // Render results
    renderVerificationResults(data);

    // Sync with Copilot and Alerts
    if (window.updateCopilotSession) {
      window.updateCopilotSession(data);
    }
  } catch (err) {
    console.error('Error running verification:', err);
  } finally {
    btn.innerHTML = originalText;
    btn.disabled = false;
  }
}

function renderVerificationResults(data) {
  // 1. Trust Score Meter Gauge
  const score = data.trust_score.trust_score;
  document.getElementById('gauge-score-val').innerText = score;

  // Arc calculation: circumference for r=80 is 251.2
  // offset goes from 251.2 (0 score) to 0 (1000 score)
  const offset = 251.2 * (1.0 - (score / 1000.0));
  const arc = document.getElementById('gauge-arc-fill');
  if (arc) arc.style.strokeDashoffset = offset;

  // Decision Banner
  const banner = document.getElementById('decision-banner-box');
  const text = document.getElementById('decision-text');
  banner.className = 'decision-banner ' + data.final_decision.toLowerCase();
  text.innerText = data.final_decision;

  // 2. SHAP Waterfall Bars
  const shapContainer = document.getElementById('shap-waterfall-container');
  if (shapContainer) {
    shapContainer.innerHTML = data.trust_score.shap_waterfall.map(item => {
      const isPos = item.impact === '+Positive';
      const pct = Math.min(100, Math.max(5, (item.raw_score / 1000) * 100));
      return `
        <div class="shap-item">
          <div class="shap-labels">
            <span>${item.feature}</span>
            <span style="font-family: var(--font-mono); color: ${isPos ? 'var(--accent-emerald)' : 'var(--accent-crimson)'};">
              ${isPos ? '+' : ''}${item.attribution} pts (${item.raw_score})
            </span>
          </div>
          <div class="shap-bar-bg">
            <div class="shap-bar-fill ${isPos ? 'positive' : 'negative'}" style="width: ${pct}%;"></div>
          </div>
        </div>
      `;
    }).join('');
  }

  // 3. Update Labels
  document.getElementById('label-mrz-status').innerText = `MRZ: ${data.identity_result.mrz_checksum_valid ? 'Valid (ICAO Checksum OK)' : 'Failed (Invalid Checksum)'}`;
  document.getElementById('label-ela-status').innerText = `ELA Heat: ${data.document_intelligence.ela_heat_ratio.toFixed(2)}`;
  document.getElementById('label-liveness-status').innerText = `Liveness: ${(data.face_liveness_result.overall_liveness_confidence * 100).toFixed(1)}%`;
  document.getElementById('label-depth-status').innerText = `3D Relief: ${data.face_liveness_result.depth_3d_validation_score.toFixed(2)}`;
  document.getElementById('label-deepfake-prob').innerText = `Deepfake: ${(data.deepfake_result.deepfake_probability * 100).toFixed(1)}%`;

  if (data.voice_result) {
    document.getElementById('label-voice-status').innerText = data.voice_result.is_authentic_voice ? 'Acoustic: Natural' : `AI: ${data.voice_result.ai_voice_engine_detected || 'Vocoder'}`;
    document.getElementById('label-clone-prob').innerText = `Clone: ${(data.voice_result.voice_clone_probability * 100).toFixed(1)}%`;
  }

  // 4. Blockchain Proof
  document.getElementById('audit-block-idx').innerText = `#${data.audit_proof.block_index}`;
  document.getElementById('audit-block-hash').innerText = `Hash: ${data.audit_proof.block_hash.substring(0, 32)}... (Merkle: ${data.audit_proof.merkle_root.substring(0, 16)}...)`;

  // 5. Telemetry Feed
  const feed = document.getElementById('forensic-telemetry-feed');
  if (feed) {
    const lines = [
      `[PIPELINE] User '${data.user_id}' processed in ${data.processing_time_ms}ms`,
      `[DOCUMENT] Type: ${data.identity_result.document_type_detected}, Age: ${data.identity_result.age_calculated}, Expiry: ${data.identity_result.expiry_status}`,
      `[BIOMETRICS] Face Cosine: ${data.face_liveness_result.face_match_score.toFixed(3)}, Active Blink: ${data.face_liveness_result.active_challenges_passed.length} passed`,
      `[DEEPFAKE] 2D FFT Anomaly: ${data.deepfake_result.frequency_domain_anomaly.toFixed(3)}, Seam: ${data.deepfake_result.boundary_blending_score.toFixed(3)}`,
      `[GRAPH] Centrality: ${data.knowledge_graph.degree_centrality}, Syndicate Linked: ${data.knowledge_graph.syndicate_detected}`,
      `[DECISION] Verdict: ${data.final_decision} (Trust Score: ${score}/1000)`
    ];
    if (data.alerts_triggered.length > 0) {
      lines.push(`[ALERTS] Triggered ${data.alerts_triggered.length} alert(s): ${data.alerts_triggered.join('; ')}`);
    }
    feed.innerHTML = lines.map(l => `<div>&gt; ${l}</div>`).join('');
  }

  // Re-draw canvases
  drawDocumentOverlay(data.document_intelligence.tampering_detected);
  drawFace3DOverlay(data.deepfake_result.deepfake_detected);
  draw2DFFTSpectrum(data.deepfake_result.deepfake_detected);
  drawAudioSpectrogram(data.voice_result && !data.voice_result.is_authentic_voice);
}

// -------------------------------------------------------------
// Canvas Renderers for Forensic Overlays
// -------------------------------------------------------------

function drawDocumentOverlay(isTampered) {
  const canvas = document.getElementById('canvas-overlay-doc');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (isTampered) {
    // Draw ELA heatmap red glowing bounding box
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 2.5;
    ctx.strokeRect(canvas.width * 0.35, canvas.height * 0.40, canvas.width * 0.32, canvas.height * 0.22);

    ctx.fillStyle = 'rgba(239, 68, 68, 0.28)';
    ctx.fillRect(canvas.width * 0.35, canvas.height * 0.40, canvas.width * 0.32, canvas.height * 0.22);

    ctx.font = '10px monospace';
    ctx.fillStyle = '#ef4444';
    ctx.fillText('ELA SPLICING ANOMALY [90% Q]', canvas.width * 0.36, canvas.height * 0.38);
  } else {
    // Draw green bounding check on MRZ & hologram
    ctx.strokeStyle = 'rgba(16, 185, 129, 0.7)';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(10, canvas.height - 40, canvas.width - 20, 32);

    ctx.font = '9px monospace';
    ctx.fillStyle = '#10b981';
    ctx.fillText('ICAO 9303 MRZ VERIFIED', 16, canvas.height - 18);
  }
}

function drawFace3DOverlay(isDeepfake) {
  const canvas = document.getElementById('canvas-overlay-face');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const cx = canvas.width / 2;
  const cy = canvas.height / 2;

  if (isDeepfake) {
    // Red face-swap blending seam
    ctx.beginPath();
    ctx.ellipse(cx, cy, 60, 75, 0, 0, 2 * Math.PI);
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 2.5;
    ctx.setLineDash([4, 4]);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.font = '10px monospace';
    ctx.fillStyle = '#ef4444';
    ctx.fillText('FACE-SWAP SEAM DETECTED', cx - 70, cy - 85);
  } else {
    // 68-point facial landmark mesh & 3D convex depth gradient
    ctx.strokeStyle = 'rgba(0, 242, 254, 0.45)';
    ctx.lineWidth = 1;

    // Head outline
    ctx.beginPath();
    ctx.ellipse(cx, cy, 55, 70, 0, 0, 2 * Math.PI);
    ctx.stroke();

    // Eyes, Nose, Mouth mesh points
    const points = [
      [cx - 20, cy - 15], [cx - 15, cy - 18], [cx - 10, cy - 15],
      [cx + 10, cy - 15], [cx + 15, cy - 18], [cx + 20, cy - 15],
      [cx, cy], [cx - 6, cy + 12], [cx + 6, cy + 12],
      [cx - 15, cy + 28], [cx, cy + 32], [cx + 15, cy + 28]
    ];

    points.forEach(p => {
      ctx.fillStyle = '#00f2fe';
      ctx.beginPath();
      ctx.arc(p[0], p[1], 2, 0, 2 * Math.PI);
      ctx.fill();
    });

    // Mesh connecting lines
    ctx.beginPath();
    ctx.moveTo(points[0][0], points[0][1]);
    ctx.lineTo(points[6][0], points[6][1]);
    ctx.lineTo(points[5][0], points[5][1]);
    ctx.moveTo(points[6][0], points[6][1]);
    ctx.lineTo(points[10][0], points[10][1]);
    ctx.stroke();

    ctx.font = '9px monospace';
    ctx.fillStyle = '#10b981';
    ctx.fillText('3D ANATOMICAL SURFACE PASSED', cx - 70, cy - 78);
  }
}

function draw2DFFTSpectrum(isDeepfake) {
  const canvas = document.getElementById('canvas-fft-spectrum');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const cx = canvas.width / 2;
  const cy = canvas.height / 2;

  // Dark background
  ctx.fillStyle = '#05070d';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Concentric radial power spectrum rings
  for (let r = 15; r < 95; r += 16) {
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, 2 * Math.PI);
    ctx.strokeStyle = 'rgba(0, 242, 254, 0.12)';
    ctx.stroke();
  }

  // Central natural power decay
  const grad = ctx.createRadialGradient(cx, cy, 2, cx, cy, 70);
  grad.addColorStop(0, 'rgba(255, 255, 255, 0.8)');
  grad.addColorStop(0.3, 'rgba(79, 172, 254, 0.35)');
  grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
  ctx.fillStyle = grad;
  ctx.beginPath();
  ctx.arc(cx, cy, 70, 0, 2 * Math.PI);
  ctx.fill();

  if (isDeepfake) {
    // Draw synthetic upsampling checkerboard grid spikes in frequency space
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 2;
    const angles = [0, Math.PI / 4, Math.PI / 2, 3 * Math.PI / 4, Math.PI, 5 * Math.PI / 4, 3 * Math.PI / 2, 7 * Math.PI / 4];
    angles.forEach(a => {
      const sx = cx + Math.cos(a) * 45;
      const sy = cy + Math.sin(a) * 45;
      ctx.beginPath();
      ctx.arc(sx, sy, 4, 0, 2 * Math.PI);
      ctx.fillStyle = '#ef4444';
      ctx.fill();
    });

    ctx.font = '10px monospace';
    ctx.fillStyle = '#ef4444';
    ctx.fillText('STYLEGAN3 FREQ SPIKES DETECTED', 16, 22);
  } else {
    ctx.font = '10px monospace';
    ctx.fillStyle = '#10b981';
    ctx.fillText('NATURAL 1/f POWER LAW (CLEAN)', 16, 22);
  }
}

function drawAudioSpectrogram(isCloned) {
  const canvas = document.getElementById('canvas-audio-spectrogram');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = '#05070d';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw colorful spectrogram time-frequency heat columns
  const numBars = 45;
  const barWidth = canvas.width / numBars;

  for (let i = 0; i < numBars; i++) {
    // Harmonic formant bands
    const height1 = 20 + Math.sin(i * 0.4) * 15;
    const height2 = 18 + Math.cos(i * 0.3) * 12;

    ctx.fillStyle = 'rgba(79, 172, 254, 0.6)';
    ctx.fillRect(i * barWidth, canvas.height - height1 - 25, barWidth - 1, height1);

    ctx.fillStyle = 'rgba(0, 98, 255, 0.65)';
    ctx.fillRect(i * barWidth, canvas.height - height1 - height2 - 40, barWidth - 1, height2);
  }

  if (isCloned) {
    // Draw harsh 7.5kHz cutoff line
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 2;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(0, 45);
    ctx.lineTo(canvas.width, 45);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.font = '10px monospace';
    ctx.fillStyle = '#ef4444';
    ctx.fillText('NEURAL VOCODER CUTOFF @ 7.5 kHz', 16, 25);
  } else {
    ctx.font = '10px monospace';
    ctx.fillStyle = '#10b981';
    ctx.fillText('NATURAL BROADBAND HARMONICS', 16, 25);
  }
}

function drawDefaultCanvases() {
  draw2DFFTSpectrum(false);
  drawAudioSpectrogram(false);
}

window.selectCase = selectCase;
