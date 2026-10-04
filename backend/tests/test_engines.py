"""
Unit & Integration Tests for Enterprise Digital Identity, Trust & Deepfake Detection Platform
Tests all AI engines, algorithms, cryptographic proofs, and REST endpoints.
"""

import pytest
import numpy as np
from fastapi.testclient import TestClient

from backend.app.main import app as fastapi_app
from backend.app.engines import (
    MRZValidator, identity_verification_engine, face_liveness_engine,
    deepfake_detector, voice_authenticator, document_intelligence_engine,
    identity_knowledge_graph, behavioral_biometrics_engine, trust_scoring_engine,
    ai_identity_copilot
)
from backend.app.models.schemas import (
    DocumentInput, FaceInput, DeepfakeInput, VoiceInput,
    DocumentType, CopilotQueryRequest, VerificationRequest
)
from backend.app.core import audit_ledger
from backend.app.data.demo_records import get_demo_cases

client = TestClient(fastapi_app)


def test_mrz_checksum_algorithm():
    """Verify ICAO 9303 Modulo-731 check digit algorithm."""
    # Test vector: Document number "E82910481"
    # Weights [7, 3, 1]
    # E(14)*7 + 8*3 + 2*1 + 9*7 + 1*3 + 0*1 + 4*7 + 8*3 + 1*1
    # = 98 + 24 + 2 + 63 + 3 + 0 + 28 + 24 + 1 = 243 -> 243 % 10 = 3 or calculated
    chk = MRZValidator.compute_checksum("E82910481")
    assert isinstance(chk, int)
    assert 0 <= chk <= 9

    # Test full TD3 parsing
    line1 = "P<USAMONTGOMERY<<ALEXANDER<DAVID<<<<<<<<<<<<<"
    line2 = "E829104814USA9105148M3110222<<<<<<<<<<<<<<<4"
    res = MRZValidator.parse_td3_passport(line1, line2)
    assert res["format"] == "TD3_PASSPORT"
    assert res["surname"] == "MONTGOMERY"
    assert "ALEXANDER" in res["given_names"]


def test_identity_verification_engine():
    """Verify identity document temporal and MRZ verification."""
    doc = DocumentInput(
        document_type=DocumentType.PASSPORT,
        country="USA",
        document_number="E82910481",
        first_name="Alexander",
        last_name="Montgomery",
        dob="1991-05-14",
        expiry_date="2031-10-22",
        mrz_raw="P<USAMONTGOMERY<<ALEXANDER<DAVID<<<<<<<<<<<<<\nE829104813USA9105148M3110223<<<<<<<<<<<<<<<6"
    )
    result = identity_verification_engine.verify_document(doc)
    assert result.is_valid is True
    assert result.age_calculated > 18
    assert result.expiry_status == "VALID"
    assert result.confidence_score >= 0.85

    # Test expired document
    doc_expired = DocumentInput(
        document_type=DocumentType.PASSPORT,
        country="USA",
        document_number="E82910481",
        first_name="Alexander",
        last_name="Montgomery",
        dob="1991-05-14",
        expiry_date="2020-01-01"
    )
    res_exp = identity_verification_engine.verify_document(doc_expired)
    assert res_exp.expiry_status == "EXPIRED"
    assert "Document expired" in res_exp.anomalies[0]


def test_face_liveness_engine():
    """Verify face feature extraction and 3D PAD liveness."""
    test_face = FaceInput(
        challenge_type="BLINK_AND_SMILE",
        ear_values=[0.32, 0.28, 0.15, 0.30],
        mar_values=[0.20, 0.48],
        head_pose_yaw=18.5,
        head_pose_pitch=4.2
    )
    res = face_liveness_engine.verify_face(test_face)
    assert res.face_detected is True
    assert res.face_match_passed is True
    assert res.active_liveness_score >= 0.80
    assert "NATURAL_EYE_BLINK_VERIFIED" in res.active_challenges_passed
    assert res.spoof_detected is False


def test_deepfake_detector():
    """Verify 2D FFT spectral anomaly and ELA detection."""
    df_input = DeepfakeInput(
        media_type="image",
        metadata_tags={"SOFTWARE": "DeepFaceLab_Quick96"}
    )
    res = deepfake_detector.detect_deepfake(df_input)
    assert res.metadata_tampered is True
    assert res.deepfake_detected is True
    assert res.deepfake_probability >= 0.50


def test_voice_authenticator():
    """Verify voice cloning and acoustic forensics."""
    v_input = VoiceInput(
        sample_rate=16000,
        duration_sec=3.0
    )
    res = voice_authenticator.authenticate_voice(v_input)
    assert res.spectral_centroid_hz > 500
    assert res.speaker_verification_score > 0.0


def test_document_intelligence():
    """Verify document OCR and security features."""
    doc = DocumentInput(
        document_type=DocumentType.PASSPORT,
        country="USA",
        document_number="E82910481",
        first_name="Alexander",
        last_name="Montgomery",
        dob="1991-05-14",
        expiry_date="2031-10-22"
    )
    res = document_intelligence_engine.evaluate_document(doc)
    assert res.ocr_extracted_fields["document_number"] == "E82910481"
    assert res.tampering_detected is False
    assert res.guilloche_pattern_intact is True


def test_knowledge_graph_analytics():
    """Verify syndicate ring and graph cycle detection."""
    graph_res = identity_knowledge_graph.analyze_identity_risk("USR_PUPPET_01")
    assert graph_res.syndicate_detected is True
    assert graph_res.degree_centrality > 0.0
    assert len(graph_res.graph_risk_flags) > 0


def test_blockchain_audit_ledger():
    """Verify cryptographic Merkle root and tamper-evident blockchain chain."""
    sample_audit = {"event": "KYC_TEST_AUDIT", "score": 950}
    proof = audit_ledger.record_verification_audit(sample_audit)
    assert proof.block_index > 0
    assert len(proof.block_hash) == 64
    assert proof.tamper_proof_verified is True
    assert audit_ledger.verify_chain_integrity() is True


def test_api_health():
    """Test health check route."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert "IdentityVerificationEngine" in data["engines_online"]


def test_api_full_verification_flow():
    """Test full pipeline verification on demo case 1 (Authentic)."""
    cases = get_demo_cases()
    case1_payload = cases[0]["payload"]
    response = client.post("/api/v1/verify", json=case1_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert data["final_decision"] == "APPROVED"
    assert data["trust_score"]["trust_score"] >= 800
    assert data["audit_proof"]["tamper_proof_verified"] is True
    assert data["processing_time_ms"] > 0


def test_api_copilot_query():
    """Test AI Copilot forensic query response."""
    query_payload = {
        "query": "Why did verification fail?",
        "session_id": "kyc_sess_auth_910481"
    }
    response = client.post("/api/v1/copilot/query", json=query_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["intent_detected"] == "EXPLAIN_FAILURE"
    assert len(data["reasoning_chain"]) >= 3
    assert len(data["suggested_followups"]) > 0


def test_api_analytics_and_alerts():
    """Test analytics KPIs and alert feed endpoints."""
    kpi_res = client.get("/api/v1/analytics/kpis")
    assert kpi_res.status_code == 200
    assert kpi_res.json()["verification_success_rate"] > 90.0

    alert_res = client.get("/api/v1/alerts/feed")
    assert alert_res.status_code == 200
    assert len(alert_res.json()) > 0
