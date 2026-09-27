# Enterprise Digital Identity, Trust & Deepfake Detection Platform
### REST API Specification Reference

---

## Base URL
`http://localhost:8000/api/v1`

---

## 1. Main KYC Verification Endpoint

### `POST /verify`
Orchestrates end-to-end multi-modal verification across all 6 core modules.

#### Request Body
```json
{
  "user_id": "usr_alex_montgomery_91",
  "session_id": "kyc_sess_auth_910481",
  "phone_number": "+14155552671",
  "email": "alex.montgomery@enterprise.org",
  "document": {
    "document_type": "PASSPORT",
    "country": "USA",
    "document_number": "E82910481",
    "first_name": "Alexander",
    "last_name": "Montgomery",
    "dob": "1991-05-14",
    "expiry_date": "2031-10-22",
    "mrz_raw": "P<USAMONTGOMERY<<ALEXANDER<DAVID<<<<<<<<<<<<<\nE829104813USA9105148M3110223<<<<<<<<<<<<<<<6",
    "image_base64": "<base64_encoded_png>"
  },
  "face": {
    "selfie_image_base64": "<base64_encoded_png>",
    "challenge_type": "BLINK_AND_SMILE",
    "ear_values": [0.31, 0.28, 0.16, 0.29, 0.32],
    "mar_values": [0.18, 0.22, 0.49, 0.44],
    "head_pose_yaw": 2.4,
    "head_pose_pitch": 1.1
  },
  "deepfake": {
    "media_type": "image",
    "media_base64": "<base64_encoded_png>",
    "metadata_tags": {
      "has_exif_camera": true,
      "MAKE": "Apple",
      "MODEL": "iPhone 15 Pro"
    }
  },
  "voice": {
    "sample_rate": 16000,
    "duration_sec": 3.2
  },
  "device": {
    "ip_address": "24.18.99.12",
    "device_fingerprint": "dfp_macbook_corp_7a",
    "geo_country": "USA",
    "geo_city": "San Francisco",
    "is_vpn": false
  },
  "behavioral": {
    "typing_flight_time_avg_ms": 130.0,
    "typing_dwell_time_avg_ms": 90.0,
    "typing_rhythm_entropy": 0.85,
    "mouse_curvature_entropy": 0.74,
    "mouse_velocity_jitter": 12.8
  }
}
```

#### Response (200 OK)
```json
{
  "session_id": "kyc_sess_auth_910481",
  "user_id": "usr_alex_montgomery_91",
  "timestamp": "2026-09-27T17:10:41Z",
  "processing_time_ms": 128.45,
  "status": "COMPLETED",
  "final_decision": "APPROVED",
  "trust_score": {
    "trust_score": 945,
    "risk_level": "LOW",
    "recommended_decision": "APPROVED",
    "component_scores": {
      "identity_signals": 950.0,
      "biometric_intelligence": 940.0,
      "deepfake_and_voice": 956.2,
      "device_and_behavioral": 928.0,
      "knowledge_graph": 950.0
    },
    "shap_waterfall": [
      {
        "feature": "Official Document Validity & MRZ",
        "weight": 0.25,
        "raw_score": 950.0,
        "impact": "+Positive",
        "attribution": 112.5
      }
    ],
    "positive_mitigators": [
      "ICAO Doc 9303 MRZ cryptographic checksum verified",
      "Active and passive 3D anatomical liveness confirmed",
      "Facial match confirmed with reference (similarity: 0.91)"
    ],
    "negative_fraud_indicators": [],
    "explanation_summary": "High trust verified identity. Passed all document, 3D biometric, and deepfake forensic tests."
  },
  "audit_proof": {
    "block_index": 14,
    "timestamp_iso": "2026-09-27T17:10:41Z",
    "merkle_root": "a4f891b0c...",
    "previous_hash": "00a29b4e1...",
    "block_hash": "00b9a8f27...",
    "tamper_proof_verified": true
  },
  "alerts_triggered": []
}
```

---

## 2. AI Identity Copilot Endpoints

### `POST /copilot/query`
Natural language query for tier-2 security analysts.

#### Request Body
```json
{
  "query": "Why did verification fail?",
  "session_id": "kyc_sess_deepfake_0088"
}
```

#### Response (200 OK)
```json
{
  "query": "Why did verification fail?",
  "intent_detected": "EXPLAIN_FAILURE",
  "reasoning_chain": [
    "Step 1 [Intent Classification]: Parsed intent as 'EXPLAIN_FAILURE'",
    "Step 2 [Context Ingestion]: Retrieved multi-modal telemetry and graph node state",
    "Step 3 [Anomaly Correlation]: Evaluated 3 fraud indicators against Trust Score 210/1000",
    "Step 4 [Causal Synthesis]: Tracing root-cause failure vectors across biometric & document pipelines",
    "Step 5 [Audit Logging]: Anchored copilot reasoning chain to compliance event bus"
  ],
  "answer_markdown": "### ❌ Root-Cause Failure Analysis (Session `kyc_sess_deepfake_0088`)\n\n...",
  "fraud_indicators_cited": [
    "AI Deepfake Media Detected (Probability: 94.2%)",
    "2D FFT Frequency anomaly detected (Grid upsampling artifact, score: 0.82)"
  ],
  "recommended_action": "REJECTED",
  "suggested_followups": [
    "Show deepfake probability.",
    "Explain the fraud indicators."
  ]
}
```

---

## 3. Knowledge Graph Endpoints

- `GET /graph/subgraph/{user_id}`: Returns 2-hop ego network for canvas rendering.
- `GET /graph/syndicates`: Returns detected criminal syndicate clusters.
- `GET /graph/cypher/{user_id}`: Generates ready-to-run Neo4j Cypher query.

---

## 4. Alert Center Endpoints

- `GET /alerts/feed?category={ALL|DEEPFAKE_DETECTED|...}`: Returns live security incidents stream.
- `POST /alerts/action`: Submits triage action (`BLOCK_USER`, `RESOLVE`, `MARK_FALSE_POSITIVE`, `ESCALATE_SAR`).

---

## 5. Executive Analytics Endpoints

- `GET /analytics/kpis`: Real-time enterprise aggregates (verification success rate, deepfake count, latency, trust score distributions, weekly trends).
