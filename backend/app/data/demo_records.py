"""
Pre-configured Enterprise Test Cases & Benchmark KYC Datasets
"""

from typing import List, Dict, Any
from ..models.schemas import (
    VerificationRequest, DocumentInput, FaceInput, DeepfakeInput,
    VoiceInput, DeviceInput, BehavioralInput, DocumentType
)
from .sample_assets import (
    SAMPLE_PASSPORT_B64, SAMPLE_FORGED_ID_B64,
    SAMPLE_DEEPFAKE_FACE_B64, SAMPLE_GENUINE_FACE_B64
)


def get_demo_cases() -> List[Dict[str, Any]]:
    """Returns 6 realistic enterprise verification case studies."""
    return [
        {
            "id": "CASE-101-GENUINE-PASSPORT",
            "title": "Case 1: Standard Verified Citizen Passport (High Trust - Clean KYC)",
            "description": "Legitimate citizen onboarding with valid US biometric passport, genuine 3D selfie with natural blink and smile clearance, residential IP, and clean Knowledge Graph.",
            "category": "AUTHENTIC",
            "expected_decision": "APPROVED",
            "expected_trust_range": "900 - 980",
            "payload": VerificationRequest(
                user_id="usr_alex_montgomery_91",
                session_id="kyc_sess_auth_910481",
                phone_number="+14155552671",
                email="alex.montgomery@enterprise.org",
                document=DocumentInput(
                    document_type=DocumentType.PASSPORT,
                    country="USA",
                    document_number="E82910481",
                    first_name="Alexander David",
                    last_name="Montgomery",
                    dob="1991-05-14",
                    expiry_date="2031-10-22",
                    issue_date="2021-10-22",
                    mrz_raw="P<USAMONTGOMERY<<ALEXANDER<DAVID<<<<<<<<<<<<<\nE829104813USA9105148M3110223<<<<<<<<<<<<<<<6",
                    image_base64=SAMPLE_PASSPORT_B64
                ),
                face=FaceInput(
                    selfie_image_base64=SAMPLE_GENUINE_FACE_B64,
                    reference_face_base64=SAMPLE_GENUINE_FACE_B64,
                    challenge_type="BLINK_AND_SMILE",
                    ear_values=[0.31, 0.28, 0.16, 0.29, 0.32],
                    mar_values=[0.18, 0.22, 0.49, 0.44],
                    head_pose_yaw=2.4,
                    head_pose_pitch=1.1
                ),
                deepfake=DeepfakeInput(
                    media_type="image",
                    media_base64=SAMPLE_GENUINE_FACE_B64,
                    metadata_tags={"has_exif_camera": True, "MAKE": "Apple", "MODEL": "iPhone 15 Pro"}
                ),
                voice=VoiceInput(
                    sample_rate=16000,
                    duration_sec=3.2,
                    claimed_speaker_id="usr_alex_montgomery_91"
                ),
                device=DeviceInput(
                    ip_address="24.18.99.12",
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    device_fingerprint="dfp_macbook_corp_7a",
                    geo_country="USA",
                    geo_city="San Francisco",
                    is_vpn=False,
                    is_proxy=False,
                    is_tor=False
                ),
                behavioral=BehavioralInput(
                    typing_flight_time_avg_ms=130.0,
                    typing_dwell_time_avg_ms=90.0,
                    typing_rhythm_entropy=0.85,
                    mouse_curvature_entropy=0.74,
                    mouse_velocity_jitter=12.8
                )
            ).model_dump()
        },
        {
            "id": "CASE-102-DEEPFAKE-VIDEO-ATTACK",
            "title": "Case 2: AI Deepfake Video KYC Attack (Generative Face Swap)",
            "description": "Adversary attempting live video KYC using deepfake face-swap overlay (RoOP / DeepFaceLab) with high-frequency 2D FFT spectral checkerboard grid and boundary seam discontinuity.",
            "category": "FRAUD_DEEPFAKE",
            "expected_decision": "REJECTED",
            "expected_trust_range": "150 - 350",
            "payload": VerificationRequest(
                user_id="usr_infiltrator_swap_02",
                session_id="kyc_sess_deepfake_0088",
                phone_number="+14155559812",
                email="victim.impersonation@tempmail.com",
                document=DocumentInput(
                    document_type=DocumentType.PASSPORT,
                    country="USA",
                    document_number="E82910481",
                    first_name="Alexander David",
                    last_name="Montgomery",
                    dob="1991-05-14",
                    expiry_date="2031-10-22",
                    issue_date="2021-10-22",
                    mrz_raw="P<USAMONTGOMERY<<ALEXANDER<DAVID<<<<<<<<<<<<<\nE829104814USA9105148M3110222<<<<<<<<<<<<<<<4",
                    image_base64=SAMPLE_PASSPORT_B64
                ),
                face=FaceInput(
                    selfie_image_base64=SAMPLE_DEEPFAKE_FACE_B64,
                    reference_face_base64=SAMPLE_GENUINE_FACE_B64,
                    challenge_type="BLINK_AND_SMILE",
                    ear_values=[0.29, 0.29, 0.28, 0.29],  # Unnatural no-blink
                    mar_values=[0.20, 0.20, 0.21],
                    head_pose_yaw=0.0,
                    head_pose_pitch=0.0
                ),
                deepfake=DeepfakeInput(
                    media_type="image",
                    media_base64=SAMPLE_DEEPFAKE_FACE_B64,
                    metadata_tags={"SOFTWARE": "DeepFaceLab_Quick96", "has_jfif_header": True}
                ),
                device=DeviceInput(
                    ip_address="194.26.29.112",
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    device_fingerprint="dfp_emulator_obs_virtual",
                    geo_country="Netherlands",
                    geo_city="Amsterdam",
                    is_vpn=True,
                    is_proxy=True
                )
            ).model_dump()
        },
        {
            "id": "CASE-103-FORGED-DOCUMENT-ELA",
            "title": "Case 3: Forged Physical ID Card (Digital Tampering & Failed Checksums)",
            "description": "Identity document with spliced date of birth and altered ID numbers. Error Level Analysis (ELA) reveals high recompression discrepancy, and MRZ Modulo-731 check digits fail.",
            "category": "FRAUD_DOCUMENT",
            "expected_decision": "REJECTED",
            "expected_trust_range": "100 - 250",
            "payload": VerificationRequest(
                user_id="usr_tampered_id_applicant",
                session_id="kyc_sess_tamper_4421",
                phone_number="+14155557731",
                email="forged.doc@inbox.com",
                document=DocumentInput(
                    document_type=DocumentType.NATIONAL_ID,
                    country="USA",
                    document_number="ID-908129-X",
                    first_name="John",
                    last_name="Smith",
                    dob="2004-01-01",
                    expiry_date="2023-12-15",  # Expired
                    issue_date="2018-01-01",
                    mrz_raw="I<USAID908129X0<<<<<<<<<<<<<<<\n0401019M2312158USA<<<<<<<<<<<1",  # Invalid check digits
                    image_base64=SAMPLE_FORGED_ID_B64
                ),
                face=FaceInput(
                    selfie_image_base64=SAMPLE_GENUINE_FACE_B64,
                    reference_face_base64=SAMPLE_FORGED_ID_B64
                ),
                deepfake=DeepfakeInput(
                    media_type="image",
                    media_base64=SAMPLE_FORGED_ID_B64,
                    metadata_tags={"SOFTWARE": "Adobe Photoshop 2024 (Windows)"}
                ),
                device=DeviceInput(
                    ip_address="198.51.100.42",
                    is_vpn=False
                )
            ).model_dump()
        },
        {
            "id": "CASE-104-VOICE-CLONE-ATTACK",
            "title": "Case 4: Voice Cloning Banking Replay Attack (Synthetic Vocoder)",
            "description": "Adversary attempting banking authorization KYC using an AI synthetic voice clone generated via ElevenLabs / neural vocoder with flat harmonic envelope and replay acoustics.",
            "category": "FRAUD_VOICE",
            "expected_decision": "REJECTED",
            "expected_trust_range": "250 - 420",
            "payload": VerificationRequest(
                user_id="usr_target_bank_victim",
                session_id="kyc_sess_voice_clone_091",
                phone_number="+14155558832",
                email="wealth.client@exec.com",
                document=DocumentInput(
                    document_type=DocumentType.PASSPORT,
                    country="USA",
                    document_number="E82910481",
                    first_name="Alexander David",
                    last_name="Montgomery",
                    dob="1991-05-14",
                    expiry_date="2031-10-22",
                    image_base64=SAMPLE_PASSPORT_B64
                ),
                face=FaceInput(
                    selfie_image_base64=SAMPLE_GENUINE_FACE_B64
                ),
                deepfake=DeepfakeInput(
                    media_type="image",
                    media_base64=SAMPLE_GENUINE_FACE_B64
                ),
                voice=VoiceInput(
                    sample_rate=16000,
                    duration_sec=4.0,
                    claimed_speaker_id="usr_target_bank_victim"
                ),
                device=DeviceInput(
                    ip_address="185.220.101.5",
                    is_vpn=True,
                    is_tor=True
                )
            ).model_dump()
        },
        {
            "id": "CASE-105-SYNTHETIC-SYNDICATE-RING",
            "title": "Case 5: Coordinated Synthetic Identity Syndicate (Multiple Personas on 1 Device)",
            "description": "A fraudulent persona operating within a known organized crime syndicate. Knowledge Graph detects that the device fingerprint and virtual phone number are linked to CASE_FRAUD_882.",
            "category": "FRAUD_GRAPH",
            "expected_decision": "REJECTED",
            "expected_trust_range": "80 - 220",
            "payload": VerificationRequest(
                user_id="USR_PUPPET_01",
                session_id="kyc_sess_syndicate_ring_01",
                phone_number="+14155550199",
                email="puppet.ring@darkweb.cc",
                document=DocumentInput(
                    document_type=DocumentType.NATIONAL_ID,
                    country="USA",
                    document_number="SYN-99102-A",
                    first_name="Marcus",
                    last_name="Vance",
                    dob="1988-04-12",
                    expiry_date="2029-06-18",
                    image_base64=SAMPLE_FORGED_ID_B64
                ),
                face=FaceInput(
                    selfie_image_base64=SAMPLE_DEEPFAKE_FACE_B64
                ),
                deepfake=DeepfakeInput(
                    media_type="image",
                    media_base64=SAMPLE_DEEPFAKE_FACE_B64
                ),
                device=DeviceInput(
                    ip_address="185.220.101.5",
                    device_fingerprint="DEV_FINGERPRINT_ROUTER_98",
                    is_tor=True,
                    is_vpn=True
                )
            ).model_dump()
        },
        {
            "id": "CASE-106-STEP-UP-KYC-REVIEW",
            "title": "Case 6: Borderline / Step-up KYC Case (Expiring Doc & Datacenter Proxy)",
            "description": "Genuine customer submitting valid passport expiring in 18 days, connecting through a commercial VPN from a hotel. Triggers Step-Up KYC or manual analyst review.",
            "category": "BORDERLINE",
            "expected_decision": "MANUAL_REVIEW",
            "expected_trust_range": "500 - 640",
            "payload": VerificationRequest(
                user_id="usr_traveler_vpn_user",
                session_id="kyc_sess_stepup_7719",
                phone_number="+14155553390",
                email="traveler.corp@business.com",
                document=DocumentInput(
                    document_type=DocumentType.PASSPORT,
                    country="USA",
                    document_number="E91029411",
                    first_name="Elena",
                    last_name="Rostova",
                    dob="1985-09-20",
                    expiry_date="2026-10-15",  # Expiring in less than 30 days
                    image_base64=SAMPLE_PASSPORT_B64
                ),
                face=FaceInput(
                    selfie_image_base64=SAMPLE_GENUINE_FACE_B64,
                    head_pose_yaw=16.0
                ),
                deepfake=DeepfakeInput(
                    media_type="image",
                    media_base64=SAMPLE_GENUINE_FACE_B64
                ),
                device=DeviceInput(
                    ip_address="195.181.164.22",
                    is_vpn=True,
                    geo_city="Frankfurt",
                    geo_country="Germany"
                )
            ).model_dump()
        }
    ]
