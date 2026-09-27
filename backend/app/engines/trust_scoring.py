"""
Trust Scoring Engine
Module 6: Real-Time Multi-Signal Bayesian & Rule-Based Trust Scoring (0-1000),
Risk Tier Classification, and SHAP-Style Explainable AI (XAI) Attribution.
"""

from typing import Dict, List, Any, Tuple
from ..models.schemas import (
    RiskLevel, VerificationDecision, TrustScoreResult,
    IdentityVerificationResult, FaceLivenessResult, DeepfakeDetectionResult,
    VoiceAuthenticationResult, DocumentIntelligenceResult, KnowledgeGraphResult,
    BehavioralBiometricsResult, DeviceInput
)


class TrustScoringEngine:
    """
    Consolidated Bayesian Trust and Risk Intelligence Engine.
    Aggregates multi-modal signals into a continuous 0-1000 trust score
    with granular SHAP-style Explainable AI attributions.
    """

    WEIGHTS = {
        "identity_signals": 0.25,
        "biometric_intelligence": 0.25,
        "deepfake_and_voice": 0.20,
        "device_and_behavioral": 0.15,
        "knowledge_graph": 0.15
    }

    def compute_trust_score(
        self,
        identity_res: IdentityVerificationResult,
        face_res: FaceLivenessResult,
        deepfake_res: DeepfakeDetectionResult,
        doc_res: DocumentIntelligenceResult,
        graph_res: KnowledgeGraphResult,
        voice_res: Optional[VoiceAuthenticationResult] = None,
        device_input: Optional[DeviceInput] = None,
        behavioral_res: Optional[BehavioralBiometricsResult] = None
    ) -> TrustScoreResult:
        """
        Calculates normalized component trust indices (0 - 1000),
        computes weighted sum, evaluates critical hard-penalty gates,
        and derives SHAP-style explainable attributions.
        """
        shap_waterfall: List[Dict[str, Any]] = []
        positive_mitigators: List[str] = []
        negative_fraud_indicators: List[str] = []

        # 1. Identity Signals Component (250 pts max)
        id_score = identity_res.confidence_score * 1000.0
        if not identity_res.mrz_checksum_valid:
            id_score -= 300.0
            negative_fraud_indicators.append("MRZ check-digit cryptographic validation failed")
        elif identity_res.mrz_checksum_valid and identity_res.country_supported:
            positive_mitigators.append("ICAO Doc 9303 MRZ cryptographic checksum verified")

        if identity_res.expiry_status == "EXPIRED":
            id_score -= 400.0
            negative_fraud_indicators.append("Document has expired")

        id_score = max(0.0, min(1000.0, id_score))
        shap_waterfall.append({
            "feature": "Official Document Validity & MRZ",
            "weight": 0.25,
            "raw_score": round(id_score, 1),
            "impact": "+Positive" if id_score >= 750 else "-Negative",
            "attribution": round((id_score - 500) * 0.25, 1)
        })

        # 2. Biometric Intelligence Component (250 pts max)
        bio_score = face_res.overall_liveness_confidence * 1000.0
        if face_res.spoof_detected:
            bio_score = min(bio_score, 150.0)
            attack_type = face_res.presentation_attack_type or "SPOOF_ATTACK"
            negative_fraud_indicators.append(f"Presentation Attack Detected: {attack_type}")
        else:
            positive_mitigators.append("Active and passive 3D anatomical liveness confirmed")

        if not face_res.face_match_passed:
            bio_score -= 350.0
            negative_fraud_indicators.append("Facial cosine similarity below security threshold")
        else:
            positive_mitigators.append(f"Facial match confirmed with reference (similarity: {face_res.face_match_score:.2f})")

        bio_score = max(0.0, min(1000.0, bio_score))
        shap_waterfall.append({
            "feature": "Facial Biometrics & 3D PAD Liveness",
            "weight": 0.25,
            "raw_score": round(bio_score, 1),
            "impact": "+Positive" if bio_score >= 750 else "-Negative",
            "attribution": round((bio_score - 500) * 0.25, 1)
        })

        # 3. Deepfake & Voice Analysis (200 pts max)
        media_naturalness = (1.0 - deepfake_res.deepfake_probability)
        voice_naturalness = (1.0 - voice_res.voice_clone_probability) if voice_res else 0.95
        deepfake_component = ((media_naturalness * 0.6) + (voice_naturalness * 0.4)) * 1000.0

        if deepfake_res.deepfake_detected:
            deepfake_component = min(deepfake_component, 100.0)
            negative_fraud_indicators.append(f"AI Deepfake Media Detected (Probability: {deepfake_res.deepfake_probability*100:.1f}%)")
        else:
            positive_mitigators.append("Absence of generative AI / diffusion spectral artifacts (2D FFT clean)")

        if voice_res and not voice_res.is_authentic_voice:
            deepfake_component -= 300.0
            negative_fraud_indicators.append("AI Voice Cloning / Synthetic Vocoder detected")
        elif voice_res and voice_res.is_authentic_voice:
            positive_mitigators.append("Natural voice acoustic resonance confirmed")

        deepfake_component = max(0.0, min(1000.0, deepfake_component))
        shap_waterfall.append({
            "feature": "Deepfake & Voice Authenticity",
            "weight": 0.20,
            "raw_score": round(deepfake_component, 1),
            "impact": "+Positive" if deepfake_component >= 750 else "-Negative",
            "attribution": round((deepfake_component - 500) * 0.20, 1)
        })

        # 4. Device & Behavioral Biometrics (150 pts max)
        dev_score = 900.0
        if device_input:
            if device_input.is_tor:
                dev_score -= 500.0
                negative_fraud_indicators.append("Tor anonymizing network exit-node detected")
            elif device_input.is_vpn or device_input.is_proxy:
                dev_score -= 200.0
                negative_fraud_indicators.append("Anonymous VPN / Datacenter proxy IP detected")
            else:
                positive_mitigators.append(f"Residential IP reputation verified ({device_input.geo_city}, {device_input.geo_country})")

        if behavioral_res:
            dev_score = (dev_score * 0.6) + (behavioral_res.behavioral_trust_index * 1000.0 * 0.4)
            if not behavioral_res.typing_biometrics_valid or not behavioral_res.mouse_kinematics_valid:
                negative_fraud_indicators.append("Non-human behavioral cadence / bot automation patterns detected")
            else:
                positive_mitigators.append("Organic human keystroke and cursor kinematics verified")

        dev_score = max(0.0, min(1000.0, dev_score))
        shap_waterfall.append({
            "feature": "Device Intelligence & Behavior",
            "weight": 0.15,
            "raw_score": round(dev_score, 1),
            "impact": "+Positive" if dev_score >= 700 else "-Negative",
            "attribution": round((dev_score - 500) * 0.15, 1)
        })

        # 5. Knowledge Graph & Historical Activity (150 pts max)
        graph_score = 950.0
        if graph_res.syndicate_detected:
            graph_score = 80.0
            negative_fraud_indicators.append(f"Syndicate Alert: Linked to coordinated fraud ring ({graph_res.syndicate_id})")
        else:
            if graph_res.shared_devices_count > 0:
                graph_score -= 250.0 * graph_res.shared_devices_count
                negative_fraud_indicators.append(f"Device collision with {graph_res.shared_devices_count} other accounts")
            if graph_res.shared_biometric_hashes > 0:
                graph_score -= 400.0
                negative_fraud_indicators.append("Face embedding shared with other applicant IDs")

            if not negative_fraud_indicators:
                positive_mitigators.append("Zero syndicate linkage or device collision in Knowledge Graph")

        graph_score = max(0.0, min(1000.0, graph_score))
        shap_waterfall.append({
            "feature": "Knowledge Graph & Entity Linkage",
            "weight": 0.15,
            "raw_score": round(graph_score, 1),
            "impact": "+Positive" if graph_score >= 750 else "-Negative",
            "attribution": round((graph_score - 500) * 0.15, 1)
        })

        # Weighted Consolidation
        base_trust = (
            id_score * self.WEIGHTS["identity_signals"] +
            bio_score * self.WEIGHTS["biometric_intelligence"] +
            deepfake_component * self.WEIGHTS["deepfake_and_voice"] +
            dev_score * self.WEIGHTS["device_and_behavioral"] +
            graph_score * self.WEIGHTS["knowledge_graph"]
        )

        # Critical Hard-Gating Overrides:
        # A deepfake or confirmed fake document CANNOT achieve a passing score regardless of other metrics.
        if deepfake_res.deepfake_detected or face_res.spoof_detected or doc_res.tampering_detected or graph_res.syndicate_detected:
            base_trust = min(base_trust, 380.0)

        final_trust = int(round(base_trust))
        final_trust = max(0, min(1000, final_trust))

        # Risk Classification & Decision
        if final_trust >= 800:
            risk_level = RiskLevel.LOW
            decision = VerificationDecision.APPROVED
            summary = "High trust verified identity. Passed all document, 3D biometric, and deepfake forensic tests."
        elif final_trust >= 650:
            risk_level = RiskLevel.MEDIUM
            decision = VerificationDecision.APPROVED
            summary = "Moderate trust verified identity. Passed core gates with minor low-risk anomalies."
        elif final_trust >= 450:
            risk_level = RiskLevel.HIGH
            decision = VerificationDecision.MANUAL_REVIEW
            summary = "Elevated risk profile. Borderline biometric or anomaly flags require security analyst review."
        else:
            risk_level = RiskLevel.CRITICAL
            decision = VerificationDecision.REJECTED
            summary = f"Critical risk detected. Rejected due to {len(negative_fraud_indicators)} severe fraud indicators."

        component_scores = {
            "identity_signals": round(id_score, 1),
            "biometric_intelligence": round(bio_score, 1),
            "deepfake_and_voice": round(deepfake_component, 1),
            "device_and_behavioral": round(dev_score, 1),
            "knowledge_graph": round(graph_score, 1)
        }

        return TrustScoreResult(
            trust_score=final_trust,
            risk_level=risk_level,
            recommended_decision=decision,
            component_scores=component_scores,
            shap_waterfall=shap_waterfall,
            positive_mitigators=positive_mitigators,
            negative_fraud_indicators=negative_fraud_indicators,
            explanation_summary=summary
        )


trust_scoring_engine = TrustScoringEngine()
