"""
Pydantic Schemas for Enterprise Digital Identity, Trust & Deepfake Detection Platform
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    NATIONAL_ID = "NATIONAL_ID"
    PASSPORT = "PASSPORT"
    DRIVING_LICENSE = "DRIVING_LICENSE"
    EMPLOYEE_ID = "EMPLOYEE_ID"
    RESIDENCE_PERMIT = "RESIDENCE_PERMIT"


class RiskLevel(str, Enum):
    LOW = "LOW"             # 800 - 1000 (Auto-Approve)
    MEDIUM = "MEDIUM"       # 650 - 799 (Conditional / Low Risk)
    HIGH = "HIGH"           # 450 - 649 (Manual Review Required)
    CRITICAL = "CRITICAL"   # 0 - 449 (Auto-Reject / Fraud Alert)


class VerificationDecision(str, Enum):
    APPROVED = "APPROVED"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    REJECTED = "REJECTED"
    STEP_UP_KYC = "STEP_UP_KYC"


class AlertCategory(str, Enum):
    DEEPFAKE_DETECTED = "DEEPFAKE_DETECTED"
    FAKE_DOCUMENT = "FAKE_DOCUMENT"
    VOICE_CLONE_ATTEMPT = "VOICE_CLONE_ATTEMPT"
    IDENTITY_THEFT = "IDENTITY_THEFT"
    DEVICE_ANOMALY = "DEVICE_ANOMALY"
    MULTIPLE_IDENTITY_USAGE = "MULTIPLE_IDENTITY_USAGE"
    SYNTHETIC_SYNDICATE = "SYNTHETIC_SYNDICATE"


# -------------------------------------------------------------
# Input Payload Schemas
# -------------------------------------------------------------

class DocumentInput(BaseModel):
    document_type: DocumentType = DocumentType.PASSPORT
    country: str = Field(default="USA", description="ISO Alpha-3 country code")
    document_number: str = Field(..., description="Document ID / Passport number")
    first_name: str = Field(..., description="Holder given name(s)")
    last_name: str = Field(..., description="Holder surname")
    dob: str = Field(..., description="Date of birth YYYY-MM-DD")
    expiry_date: str = Field(..., description="Expiry date YYYY-MM-DD")
    issue_date: Optional[str] = Field(default="2020-01-01", description="Issue date YYYY-MM-DD")
    mrz_raw: Optional[str] = Field(default=None, description="Raw MRZ 2 or 3 lines")
    image_base64: Optional[str] = Field(default=None, description="Base64 encoded document image")


class FaceInput(BaseModel):
    selfie_image_base64: Optional[str] = Field(default=None, description="Captured selfie/frame base64")
    reference_face_base64: Optional[str] = Field(default=None, description="Reference portrait from ID doc")
    challenge_type: Optional[str] = Field(default="BLINK_AND_SMILE", description="Active liveness challenge")
    ear_values: Optional[List[float]] = Field(default=None, description="Eye Aspect Ratio series across frames")
    mar_values: Optional[List[float]] = Field(default=None, description="Mouth Aspect Ratio series")
    head_pose_yaw: Optional[float] = Field(default=0.0, description="Yaw rotation in degrees")
    head_pose_pitch: Optional[float] = Field(default=0.0, description="Pitch angle in degrees")


class DeepfakeInput(BaseModel):
    media_type: str = Field(default="image", description="'image' or 'video'")
    media_base64: Optional[str] = Field(default=None, description="Media frame or snippet base64")
    optical_flow_frames: Optional[List[str]] = Field(default=None, description="Consecutive frame samples")
    metadata_tags: Optional[Dict[str, Any]] = Field(default_factory=dict, description="EXIF & container metadata")


class VoiceInput(BaseModel):
    audio_base64: Optional[str] = Field(default=None, description="WAV/MP3 audio payload base64")
    sample_rate: int = Field(default=16000, description="Sampling rate in Hz")
    duration_sec: float = Field(default=3.5, description="Audio duration")
    claimed_speaker_id: Optional[str] = Field(default=None, description="User ID for speaker verification")


class DeviceInput(BaseModel):
    ip_address: str = Field(default="192.168.1.100")
    user_agent: str = Field(default="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
    device_fingerprint: str = Field(default="dfp_8f9104b2a4e")
    geo_country: str = Field(default="USA")
    geo_city: str = Field(default="San Francisco")
    is_vpn: bool = False
    is_proxy: bool = False
    is_tor: bool = False


class BehavioralInput(BaseModel):
    typing_flight_time_avg_ms: float = Field(default=120.0)
    typing_dwell_time_avg_ms: float = Field(default=85.0)
    typing_rhythm_entropy: float = Field(default=0.82)
    mouse_curvature_entropy: float = Field(default=0.78)
    mouse_velocity_jitter: float = Field(default=14.2)
    session_idle_ratio: float = Field(default=0.15)


class VerificationRequest(BaseModel):
    user_id: str = Field(..., description="Unique customer/applicant identifier")
    session_id: Optional[str] = Field(default=None, description="KYC session identifier")
    phone_number: Optional[str] = Field(default="+14155552671")
    email: Optional[str] = Field(default="user@enterprise.org")
    document: DocumentInput
    face: FaceInput
    deepfake: DeepfakeInput
    voice: Optional[VoiceInput] = None
    device: Optional[DeviceInput] = None
    behavioral: Optional[BehavioralInput] = None


# -------------------------------------------------------------
# Engine Output Schemas
# -------------------------------------------------------------

class IdentityVerificationResult(BaseModel):
    is_valid: bool
    document_type_detected: str
    country_supported: bool
    mrz_checksum_valid: bool
    mrz_parsed_data: Dict[str, Any]
    temporal_consistency_valid: bool
    age_calculated: int
    expiry_status: str
    anomalies: List[str]
    confidence_score: float  # 0.0 - 1.0


class FaceLivenessResult(BaseModel):
    face_detected: bool
    face_match_score: float  # Cosine similarity 0.0 - 1.0
    face_match_passed: bool
    active_liveness_score: float
    active_challenges_passed: List[str]
    passive_liveness_score: float
    moiré_pattern_detected: bool
    chromatic_distortion_score: float
    laplacian_sharpness: float
    depth_3d_validation_score: float  # Planar vs 3D anatomical surface
    presentation_attack_type: Optional[str] = None  # None, "PRINT_ATTACK", "2D_SCREEN_REPLAY", "3D_SILICONE_MASK"
    spoof_detected: bool
    overall_liveness_confidence: float


class DeepfakeDetectionResult(BaseModel):
    deepfake_detected: bool
    deepfake_probability: float  # 0.0 - 1.0
    frequency_domain_anomaly: float  # 2D FFT spectral artifact score
    boundary_blending_score: float  # Poisson face-swap blending seam score
    error_level_analysis_score: float  # ELA recompression gradient
    temporal_flicker_score: float  # Optical flow frame consistency
    lip_sync_correlation: float  # Phoneme-viseme correlation
    metadata_tampered: bool
    tampering_indicators: List[str]
    generative_model_fingerprint: Optional[str] = None  # "StyleGAN3", "StableDiffusion", "FaceSwap", "None"


class VoiceAuthenticationResult(BaseModel):
    is_authentic_voice: bool
    voice_clone_probability: float
    speaker_verification_score: float
    spectral_flux: float
    spectral_centroid_hz: float
    zero_crossing_rate: float
    replay_attack_detected: bool
    room_reverberation_decay: float
    synthetic_silence_detected: bool
    ai_voice_engine_detected: Optional[str] = None  # "ElevenLabs", "Bark", "VALL-E", "Tacotron2", "None"


class DocumentIntelligenceResult(BaseModel):
    ocr_extracted_fields: Dict[str, Any]
    font_consistency_score: float
    baseline_alignment_score: float
    tampering_detected: bool
    ela_heat_ratio: float
    signature_detected: bool
    signature_confidence: float
    hologram_verified: bool
    guilloche_pattern_intact: bool
    microprint_integrity: float
    cross_field_match: bool


class TrustScoreResult(BaseModel):
    trust_score: int = Field(..., ge=0, le=1000, description="Consolidated trust score 0-1000")
    risk_level: RiskLevel
    recommended_decision: VerificationDecision
    component_scores: Dict[str, float]  # identity, face, deepfake, voice, device, graph
    shap_waterfall: List[Dict[str, Any]]  # Explainable AI factors
    positive_mitigators: List[str]
    negative_fraud_indicators: List[str]
    explanation_summary: str


class KnowledgeGraphResult(BaseModel):
    node_id: str
    degree_centrality: float
    connected_users_count: int
    shared_devices_count: int
    shared_ips_count: int
    shared_phone_count: int
    shared_biometric_hashes: int
    syndicate_detected: bool
    syndicate_id: Optional[str] = None
    graph_risk_flags: List[str]
    subgraph_nodes: List[Dict[str, Any]]
    subgraph_edges: List[Dict[str, Any]]


class BehavioralBiometricsResult(BaseModel):
    typing_biometrics_valid: bool
    mouse_kinematics_valid: bool
    session_anomaly_score: float
    behavioral_trust_index: float


class BlockchainAuditProof(BaseModel):
    block_index: int
    timestamp_iso: str
    merkle_root: str
    previous_hash: str
    block_hash: str
    tamper_proof_verified: bool


class FullVerificationResponse(BaseModel):
    session_id: str
    user_id: str
    timestamp: str
    processing_time_ms: float
    status: str
    final_decision: VerificationDecision
    trust_score: TrustScoreResult
    identity_result: IdentityVerificationResult
    face_liveness_result: FaceLivenessResult
    deepfake_result: DeepfakeDetectionResult
    voice_result: Optional[VoiceAuthenticationResult] = None
    document_intelligence: DocumentIntelligenceResult
    knowledge_graph: KnowledgeGraphResult
    behavioral_biometrics: Optional[BehavioralBiometricsResult] = None
    audit_proof: BlockchainAuditProof
    alerts_triggered: List[str]


# -------------------------------------------------------------
# Copilot & Alert Schemas
# -------------------------------------------------------------

class CopilotQueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None


class CopilotResponse(BaseModel):
    query: str
    intent_detected: str
    reasoning_chain: List[str]
    answer_markdown: str
    fraud_indicators_cited: List[str]
    recommended_action: VerificationDecision
    suggested_followups: List[str]


class AlertItem(BaseModel):
    alert_id: str
    timestamp: str
    category: AlertCategory
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    user_id: str
    session_id: str
    description: str
    trust_score: int
    evidence: Dict[str, Any]
    status: str  # "NEW", "INVESTIGATING", "RESOLVED", "FALSE_POSITIVE", "BLOCKED"


class AlertActionRequest(BaseModel):
    alert_id: str
    action: str  # "RESOLVE", "BLOCK_USER", "MARK_FALSE_POSITIVE", "ESCALATE_SAR"
    notes: Optional[str] = None


class ExecutiveKPIs(BaseModel):
    total_verifications: int
    verification_success_rate: float
    deepfake_alerts_count: int
    fraud_attempts_blocked: int
    avg_latency_seconds: float
    active_syndicates_detected: int
    risk_breakdown: Dict[str, int]
    alerts_by_category: Dict[str, int]
    trust_score_distribution: List[Dict[str, Any]]
    timeline_trends: List[Dict[str, Any]]
