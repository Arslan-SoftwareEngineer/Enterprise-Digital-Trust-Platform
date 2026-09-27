"""
Verification Router
Orchestrates the complete enterprise KYC pipeline across all biometric,
document, deepfake, voice, graph, and trust engines.
"""

import time
import uuid
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List

from ..models.schemas import (
    VerificationRequest, FullVerificationResponse, DocumentInput,
    FaceInput, DeepfakeInput, VoiceInput, IdentityVerificationResult,
    FaceLivenessResult, DeepfakeDetectionResult, VoiceAuthenticationResult,
    AlertCategory, AlertItem
)
from ..engines import (
    identity_verification_engine, face_liveness_engine, deepfake_detector,
    voice_authenticator, document_intelligence_engine, identity_knowledge_graph,
    behavioral_biometrics_engine, trust_scoring_engine, ai_identity_copilot
)
from ..core import audit_ledger, event_bus, hash_token, generate_session_id
from ..data.demo_records import get_demo_cases

router = APIRouter(prefix="/verify", tags=["Verification"])

# Global alerts repository for Alert Center
active_alerts: List[AlertItem] = []


@router.post("", response_model=FullVerificationResponse)
async def execute_full_verification(
    request: VerificationRequest,
    background_tasks: BackgroundTasks
) -> FullVerificationResponse:
    """
    Main Enterprise KYC Pipeline Endpoint.
    Executes concurrent and sequential verification across all 6 core modules,
    computes Bayesian trust score, anchors cryptographic blockchain proof,
    and publishes compliance events.
    """
    t_start = time.time()
    session_id = request.session_id or generate_session_id()

    # 1. Identity & Document Verification
    id_res = identity_verification_engine.verify_document(request.document)

    # 2. Face Matching & Liveness (3D PAD)
    face_res = face_liveness_engine.verify_face(request.face)

    # 3. Deepfake & Synthetic Media Forensics
    df_res = deepfake_detector.detect_deepfake(request.deepfake)

    # 4. Voice Authentication (if audio provided)
    voice_res = voice_authenticator.authenticate_voice(request.voice) if request.voice else None

    # 5. Document Intelligence & Tampering (ELA)
    doc_res = document_intelligence_engine.evaluate_document(request.document)

    # 6. Behavioral Biometrics (Bonus)
    beh_res = behavioral_biometrics_engine.analyze_behavior(request.behavioral) if request.behavioral else None

    # 7. Knowledge Graph Registration & Risk Scoring
    face_hash = hash_token(request.face.selfie_image_base64 or request.user_id)
    dev_fp = request.device.device_fingerprint if request.device else "dfp_unknown"
    ip_addr = request.device.ip_address if request.device else "127.0.0.1"
    phone_no = request.phone_number or "+10000000000"

    identity_knowledge_graph.register_applicant(
        user_id=request.user_id,
        document_number=request.document.document_number,
        ip_address=ip_addr,
        device_fingerprint=dev_fp,
        phone_number=phone_no,
        face_hash=face_hash
    )
    graph_res = identity_knowledge_graph.analyze_identity_risk(request.user_id)

    # 8. Real-Time Consolidated Trust Scoring & XAI
    trust_res = trust_scoring_engine.compute_trust_score(
        identity_res=id_res,
        face_res=face_res,
        deepfake_res=df_res,
        doc_res=doc_res,
        graph_res=graph_res,
        voice_res=voice_res,
        device_input=request.device,
        behavioral_res=beh_res
    )

    # 9. Blockchain-Anchored Audit Proof (Bonus)
    audit_data = {
        "session_id": session_id,
        "user_id": request.user_id,
        "trust_score": trust_res.trust_score,
        "decision": trust_res.recommended_decision.value,
        "risk_level": trust_res.risk_level.value,
        "deepfake_prob": df_res.deepfake_probability,
        "doc_valid": id_res.is_valid
    }
    audit_proof = audit_ledger.record_verification_audit(audit_data)

    # 10. Generate Automated Alerts if critical anomalies triggered
    alerts_triggered = []
    if df_res.deepfake_detected:
        alerts_triggered.append(f"DEEPFAKE_DETECTED: Probability {df_res.deepfake_probability*100:.1f}%")
        active_alerts.insert(0, AlertItem(
            alert_id=f"alt_df_{uuid.uuid4().hex[:6]}",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            category=AlertCategory.DEEPFAKE_DETECTED,
            severity="CRITICAL",
            user_id=request.user_id,
            session_id=session_id,
            description=f"Synthetic media detected with {df_res.deepfake_probability*100:.1f}% confidence.",
            trust_score=trust_res.trust_score,
            evidence={"fft_score": df_res.frequency_domain_anomaly, "seam_score": df_res.boundary_blending_score},
            status="NEW"
        ))

    if doc_res.tampering_detected or not id_res.mrz_checksum_valid:
        alerts_triggered.append("FAKE_DOCUMENT: Digital tampering / MRZ checksum mismatch detected")
        active_alerts.insert(0, AlertItem(
            alert_id=f"alt_doc_{uuid.uuid4().hex[:6]}",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            category=AlertCategory.FAKE_DOCUMENT,
            severity="CRITICAL",
            user_id=request.user_id,
            session_id=session_id,
            description="Document ELA compression discrepancy or invalid ICAO checksum.",
            trust_score=trust_res.trust_score,
            evidence={"ela_heat": doc_res.ela_heat_ratio, "mrz_valid": id_res.mrz_checksum_valid},
            status="NEW"
        ))

    if voice_res and not voice_res.is_authentic_voice:
        alerts_triggered.append("VOICE_CLONE_ATTEMPT: Synthetic speech detected")
        active_alerts.insert(0, AlertItem(
            alert_id=f"alt_voc_{uuid.uuid4().hex[:6]}",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            category=AlertCategory.VOICE_CLONE_ATTEMPT,
            severity="HIGH",
            user_id=request.user_id,
            session_id=session_id,
            description="AI Voice clone / vocoder acoustic fingerprint detected.",
            trust_score=trust_res.trust_score,
            evidence={"clone_prob": voice_res.voice_clone_probability},
            status="NEW"
        ))

    if graph_res.syndicate_detected:
        alerts_triggered.append(f"SYNTHETIC_SYNDICATE: Linked to {graph_res.syndicate_id}")
        active_alerts.insert(0, AlertItem(
            alert_id=f"alt_syn_{uuid.uuid4().hex[:6]}",
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            category=AlertCategory.SYNTHETIC_SYNDICATE,
            severity="CRITICAL",
            user_id=request.user_id,
            session_id=session_id,
            description=f"Multi-identity syndicate ring identified ({graph_res.syndicate_id}).",
            trust_score=trust_res.trust_score,
            evidence={"connected_users": graph_res.connected_users_count},
            status="NEW"
        ))

    elapsed_ms = (time.time() - t_start) * 1000.0

    response = FullVerificationResponse(
        session_id=session_id,
        user_id=request.user_id,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        processing_time_ms=round(elapsed_ms, 2),
        status="COMPLETED",
        final_decision=trust_res.recommended_decision,
        trust_score=trust_res,
        identity_result=id_res,
        face_liveness_result=face_res,
        deepfake_result=df_res,
        voice_result=voice_res,
        document_intelligence=doc_res,
        knowledge_graph=graph_res,
        behavioral_biometrics=beh_res,
        audit_proof=audit_proof,
        alerts_triggered=alerts_triggered
    )

    # Cache response in AI Copilot for interactive analyst investigations
    ai_identity_copilot.cache_session(response)

    # Publish async events to EventBus (simulated Kafka/Redis topic)
    background_tasks.add_task(
        event_bus.publish,
        "identity.verification.completed",
        {"session_id": session_id, "decision": response.final_decision.value, "trust_score": trust_res.trust_score}
    )

    return response


@router.get("/demo-cases")
async def list_demo_cases():
    """Returns 6 realistic benchmark KYC test cases."""
    return get_demo_cases()


@router.post("/document")
async def verify_document_standalone(document: DocumentInput) -> IdentityVerificationResult:
    """Standalone endpoint for document & MRZ validation."""
    return identity_verification_engine.verify_document(document)


@router.post("/face")
async def verify_face_standalone(face: FaceInput) -> FaceLivenessResult:
    """Standalone endpoint for facial matching and 3D PAD liveness."""
    return face_liveness_engine.verify_face(face)


@router.post("/deepfake")
async def verify_deepfake_standalone(deepfake: DeepfakeInput) -> DeepfakeDetectionResult:
    """Standalone endpoint for deepfake and synthetic image/video detection."""
    return deepfake_detector.detect_deepfake(deepfake)


@router.post("/voice")
async def verify_voice_standalone(voice: VoiceInput) -> VoiceAuthenticationResult:
    """Standalone endpoint for voice cloning and acoustic replay detection."""
    return voice_authenticator.authenticate_voice(voice)
