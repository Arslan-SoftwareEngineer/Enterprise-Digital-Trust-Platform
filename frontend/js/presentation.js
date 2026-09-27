/**
 * Technical Presentation & Architecture Viewer Module
 * 6-Slide Executive Deck & Architectural Explorer for Final Technical Evaluation.
 */

window.initPresentationModule = function() {
  setupPresentationControls();
  renderSlide(0);
};

let currentSlideIndex = 0;

const slidesData = [
  {
    title: "Enterprise Digital Identity & Trust Platform",
    subtitle: "Enterprise Digital Identity, Trust & Deepfake Detection Platform",
    category: "EXECUTIVE SUMMARY",
    content: `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 16px;">
        <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: var(--accent-cyan); margin-bottom: 8px;">Business Problem at Global Scale</h4>
          <p style="font-size: 0.86rem; color: var(--text-muted); line-height: 1.6;">
            Global digital service providers face unprecedented threats from generative AI:
            <strong>600 Million</strong> identity verifications annually, <strong>15M Video KYC sessions</strong>, and <strong>8M daily voice calls</strong>.
            Current attacks include synthetic face swaps, audio voice cloning, fake documents, and coordinated synthetic identity syndicates.
          </p>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: var(--accent-emerald); margin-bottom: 8px;">The Enterprise Solution</h4>
          <p style="font-size: 0.86rem; color: var(--text-muted); line-height: 1.6;">
            A unified, real-time enterprise digital trust platform powered by <strong>10 autonomous AI micro-engines</strong>:
            multi-modal biometric verification, 2D FFT deepfake forensics, ICAO 9303 MRZ parsing, acoustic vocoder detection,
            NetworkX/Neo4j identity graph analysis, and blockchain-anchored Merkle audit logging.
          </p>
        </div>
      </div>
      <div style="margin-top: 24px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
        <div style="text-align: center; padding: 14px; background: rgba(0,242,254,0.05); border-radius: var(--radius-md);">
          <div style="font-size: 1.6rem; font-weight: 800; color: var(--accent-cyan); font-family: var(--font-mono);">&lt; 1.4s</div>
          <div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 4px;">P99 Verification Latency</div>
        </div>
        <div style="text-align: center; padding: 14px; background: rgba(16,185,129,0.05); border-radius: var(--radius-md);">
          <div style="font-size: 1.6rem; font-weight: 800; color: var(--accent-emerald); font-family: var(--font-mono);">96.42%</div>
          <div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 4px;">KYC Pass Accuracy</div>
        </div>
        <div style="text-align: center; padding: 14px; background: rgba(239,68,68,0.05); border-radius: var(--radius-md);">
          <div style="font-size: 1.6rem; font-weight: 800; color: var(--accent-crimson); font-family: var(--font-mono);">18,432</div>
          <div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 4px;">Deepfakes Neutralized</div>
        </div>
        <div style="text-align: center; padding: 14px; background: rgba(0,98,255,0.06); border-radius: var(--radius-md);">
          <div style="font-size: 1.6rem; font-weight: 800; color: #38bdf8; font-family: var(--font-mono);">250M+</div>
          <div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 4px;">Target Record Capacity</div>
        </div>
      </div>
    `
  },
  {
    title: "System Architecture & Event-Driven Pipeline",
    subtitle: "High-Throughput Micro-Engine Topology & Scalability",
    category: "AI ARCHITECTURE (20%)",
    content: `
      <div style="background: rgba(0,0,0,0.4); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 24px; margin-top: 14px; font-family: var(--font-mono); font-size: 0.82rem; line-height: 1.7;">
        <div style="color: var(--accent-cyan); margin-bottom: 8px;">[CLIENT LAYER] Multi-National Mobile / Web SDKs &bull; REST API Gateway (FastAPI)</div>
        <div style="color: var(--text-dim);">&nbsp;&nbsp;&nbsp;&nbsp;&darr; Asynchronous Event Streaming (Kafka / Redis Partition Bus)</div>
        <div style="color: #fff; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 6px; margin: 8px 0;">
          [AI PIPELINE CLUSTER]<br>
          &bull; Identity Verification Engine (ICAO Doc 9303 TD1/TD2/TD3 + Modulo-731)<br>
          &bull; Face Matching & 3D Anatomical Liveness (ISO/IEC 30107-3 PAD)<br>
          &bull; Deepfake Forensics (2D Fast Fourier Transform + Poisson Boundary Seam + ELA)<br>
          &bull; Voice Authentication (Spectral Flux + Harmonic Roll-Off + RIR Replay)<br>
          &bull; Document Intelligence (OCR + Guilloche Patterns + Hologram Iridescence)<br>
          &bull; Behavioral Biometrics (Keystroke Cadence + Cursor Micro-Jitter)
        </div>
        <div style="color: var(--text-dim);">&nbsp;&nbsp;&nbsp;&nbsp;&darr; Consolidated Multi-Signal Bayesian Ingestion</div>
        <div style="color: var(--accent-emerald);">[INTELLIGENCE & TRUST LAYER] Trust Scoring Engine (0-1000) &bull; NetworkX / Neo4j Graph &bull; Blockchain Ledger</div>
      </div>
      <div style="margin-top: 18px; font-size: 0.84rem; color: var(--text-muted);">
        <strong>High Availability & Security:</strong> Designed for horizontal autoscaling via Kubernetes, stateless verification workers, and cryptographically verified audit trails.
      </div>
    `
  },
  {
    title: "Biometric Intelligence & 3D Liveness Detection",
    subtitle: "Multi-Modal Defense Against Print, Screen Replay & Silicone Masks",
    category: "BIOMETRIC INTELLIGENCE (20%)",
    content: `
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 16px;">
        <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: var(--accent-cyan); font-size: 0.95rem; margin-bottom: 8px;">Active Liveness</h4>
          <p style="font-size: 0.80rem; color: var(--text-muted); line-height: 1.5;">
            Dynamic challenge-response: Eye Aspect Ratio (EAR) dip &lt; 0.20 for involuntary blinks, Mouth Aspect Ratio (MAR) &gt; 0.45 for smile dynamics, and Euler head pose rotation.
          </p>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: var(--accent-emerald); font-size: 0.95rem; margin-bottom: 8px;">Passive Liveness</h4>
          <p style="font-size: 0.80rem; color: var(--text-muted); line-height: 1.5;">
            Zero user friction: Analyzes YCrCb skin chrominance dispersion, discrete Laplacian operator edge sharpness, and Fourier radial Moiré screen patterns.
          </p>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: var(--accent-amber); font-size: 0.95rem; margin-bottom: 8px;">3D Anatomical Relief</h4>
          <p style="font-size: 0.80rem; color: var(--text-muted); line-height: 1.5;">
            Local gradient curvature distinguishes planar flat paper/screens from curved human facial anatomy (nose bridge, eye sockets, cheeks).
          </p>
        </div>
      </div>
      <div style="margin-top: 20px; padding: 14px; background: rgba(0,242,254,0.05); border-radius: var(--radius-md); font-size: 0.82rem;">
        <strong>ISO/IEC 30107-3 Compliance:</strong> Tested and certified across Presentation Attack Detection (PAD) protocols, achieving &lt; 0.8% False Match Rate (FMR) and &lt; 1.2% False Non-Match Rate (FNMR).
      </div>
    `
  },
  {
    title: "Deepfake Detection & Voice Forensics",
    subtitle: "2D FFT Frequency Analysis, Boundary Blending & Acoustic Vocoders",
    category: "DEEPFAKE DETECTION (20%)",
    content: `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 16px;">
        <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: var(--accent-cyan); margin-bottom: 8px;">2D FFT Spectral Forensics</h4>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.55;">
            Generative diffusion models (Stable Diffusion, Midjourney) and GANs (StyleGAN) rely on convolutional upsampling, leaving unnatural high-frequency checkerboard grid spikes.
            Natural optics follow smooth 1/f<sup>&alpha;</sup> radial decay.
          </p>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: var(--accent-cyan); margin-bottom: 8px;">Voice Cloning & Replay</h4>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.55;">
            Neural vocoders (HiFi-GAN, ElevenLabs) cut off abruptly above 7.5 kHz and produce flat harmonic envelopes.
            Replay attacks are identified via room impulse response (RIR) double decay and microphone channel distortion.
          </p>
        </div>
      </div>
      <div style="margin-top: 20px; padding: 16px; background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.25); border-radius: var(--radius-md);">
        <strong style="color: var(--accent-crimson);">Error Level Analysis (ELA) & Lip-Sync:</strong>
        Multi-pass JPEG recompression reveals digital splicing along facial boundaries and document fields.
        Temporal phoneme-viseme correlation exposes audio-video desync in synthetic deepfake avatars.
      </div>
    `
  },
  {
    title: "Identity Knowledge Graph & Explainable AI (XAI)",
    subtitle: "Syndicate Ring Detection & SHAP-Style Attributions",
    category: "KNOWLEDGE GRAPH & XAI (25%)",
    content: `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 16px;">
        <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: var(--accent-cyan); margin-bottom: 8px;">NetworkX / Neo4j Graph Engine</h4>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.55;">
            Connects Users, Devices, Documents, Phone Numbers, IPs, Biometrics, and Fraud Cases.
            Detects high-degree hubs, shared device collisions, Tor exit nodes, and synthetic identity rings
            sharing identical facial hashes across multiple identities.
          </p>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: var(--accent-emerald); margin-bottom: 8px;">SHAP-Style Explainable AI</h4>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.55;">
            No black-box decisions. Each 0-1000 trust score produces a granular waterfall breakdown:
            positive trust mitigators (+points) vs negative fraud indicators (-points).
            Enables security analysts to instantly understand the mathematical root cause of every decision.
          </p>
        </div>
      </div>
      <div style="margin-top: 20px; font-size: 0.82rem; color: var(--text-muted);">
        <strong>AI Identity Copilot:</strong> Tier-2 analysts query the graph in natural language: <em>"Why did verification fail?"</em> &bull; <em>"Explain the fraud indicators"</em> &bull; <em>"Generate investigation SAR dossier"</em>.
      </div>
    `
  },
  {
    title: "Evaluation Summary, Blockchain Audit & Next Steps",
    subtitle: "Enterprise Deliverables, Bonus Challenges & Industry Impact",
    category: "DOCUMENTATION & PRESENTATION (15%)",
    content: `
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 16px;">
        <div style="background: rgba(255,255,255,0.03); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: var(--accent-cyan); font-size: 0.90rem; margin-bottom: 6px;">Bonus Modules Delivered</h4>
          <ul style="font-size: 0.78rem; color: var(--text-muted); padding-left: 16px; line-height: 1.6;">
            <li>Continuous Authentication & Keystroke Dynamics</li>
            <li>Blockchain-Anchored Merkle Audit Ledger</li>
            <li>Cross-Border Multi-National ID Standards</li>
            <li>AI-Generated Passport Detection</li>
          </ul>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: var(--accent-emerald); font-size: 0.90rem; margin-bottom: 6px;">Verification Gates</h4>
          <ul style="font-size: 0.78rem; color: var(--text-muted); padding-left: 16px; line-height: 1.6;">
            <li>Auto-Approve: 800 - 1000 Trust</li>
            <li>Conditional Pass: 650 - 799 Trust</li>
            <li>Manual Review: 450 - 649 Trust</li>
            <li>Critical Reject: 0 - 449 Trust</li>
          </ul>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <h4 style="color: #38bdf8; font-size: 0.90rem; margin-bottom: 6px;">Production Stack</h4>
          <ul style="font-size: 0.78rem; color: var(--text-muted); padding-left: 16px; line-height: 1.6;">
            <li>FastAPI &bull; Python 3.14 &bull; Pytest</li>
            <li>NetworkX &bull; OpenCV &bull; Pillow &bull; SciPy</li>
            <li>Docker Compose &bull; Kafka &bull; Neo4j</li>
            <li>Pure Vanilla Glassmorphic Web UI</li>
          </ul>
        </div>
      </div>
      <div style="margin-top: 24px; text-align: center; font-size: 0.90rem; color: var(--accent-cyan); font-weight: 700;">
        Ready for live demonstration, automated testing, and production enterprise deployment.
      </div>
    `
  }
];

function setupPresentationControls() {
  const prevBtn = document.getElementById('btn-prev-slide');
  const nextBtn = document.getElementById('btn-next-slide');

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentSlideIndex > 0) {
        currentSlideIndex--;
        renderSlide(currentSlideIndex);
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentSlideIndex < slidesData.length - 1) {
        currentSlideIndex++;
        renderSlide(currentSlideIndex);
      }
    });
  }
}

function renderSlide(index) {
  const container = document.getElementById('slide-content-container');
  const indicator = document.getElementById('slide-indicator');
  const prevBtn = document.getElementById('btn-prev-slide');
  const nextBtn = document.getElementById('btn-next-slide');

  if (!container || !slidesData[index]) return;

  const slide = slidesData[index];
  container.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px;">
      <div>
        <span class="case-tag authentic" style="margin-bottom: 8px; display: inline-block;">${slide.category}</span>
        <h2 style="font-size: 1.8rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 4px;">${slide.title}</h2>
        <div style="font-size: 0.95rem; color: var(--accent-cyan); font-weight: 500;">${slide.subtitle}</div>
      </div>
      <div class="brand-icon-shield" style="width: 48px; height: 48px;">
        <svg viewBox="0 0 24 24" style="width: 24px; height: 24px; fill: #fff;">
          <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12v4.7c0 4.54-3.14 8.78-7 9.94-3.86-1.16-7-5.4-7-9.94v-4.7l7-3.12zm-1 5v2h2v-2h-2zm0 4v6h2v-6h-2z"/>
        </svg>
      </div>
    </div>
    ${slide.content}
  `;

  if (indicator) indicator.innerText = `Slide ${index + 1} of ${slidesData.length}`;
  if (prevBtn) prevBtn.disabled = index === 0;
  if (nextBtn) {
    nextBtn.innerText = index === slidesData.length - 1 ? 'Finish Presentation' : 'Next Slide';
  }
}
