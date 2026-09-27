"""
Behavioral Biometrics & Continuous Authentication Engine
Bonus Challenge: Keystroke Dynamics, Mouse Kinematics, and Session Anomaly Scoring.
"""

from typing import Optional
from ..models.schemas import BehavioralInput, BehavioralBiometricsResult


class BehavioralBiometricsEngine:
    """
    Evaluates continuous subconscious behavioral signals (typing cadence,
    mouse trajectory smoothness, cursor jitter) to distinguish genuine humans
    from automated bots or credential stuffers.
    """

    def analyze_behavior(self, data: Optional[BehavioralInput]) -> BehavioralBiometricsResult:
        if data is None:
            return BehavioralBiometricsResult(
                typing_biometrics_valid=True,
                mouse_kinematics_valid=True,
                session_anomaly_score=0.08,
                behavioral_trust_index=0.92
            )

        # 1. Keystroke cadence validation:
        # Human flight time is typically 80 - 250 ms, dwell time 50 - 140 ms.
        # Bots have near-zero flight time or uniform static intervals (entropy < 0.20).
        flight_valid = 60.0 <= data.typing_flight_time_avg_ms <= 350.0
        dwell_valid = 40.0 <= data.typing_dwell_time_avg_ms <= 200.0
        rhythm_organic = data.typing_rhythm_entropy >= 0.45

        typing_valid = flight_valid and dwell_valid and rhythm_organic

        # 2. Mouse kinematics:
        # Human cursor trajectories have non-zero curvature entropy and natural micro-jitter.
        # Straight-line synthetic mouse moves have zero jitter.
        mouse_valid = data.mouse_curvature_entropy >= 0.35 and data.mouse_velocity_jitter > 2.0

        anomaly_score = 0.05
        if not typing_valid:
            anomaly_score += 0.45
        if not mouse_valid:
            anomaly_score += 0.40

        trust_index = max(0.0, 1.0 - anomaly_score)

        return BehavioralBiometricsResult(
            typing_biometrics_valid=typing_valid,
            mouse_kinematics_valid=mouse_valid,
            session_anomaly_score=round(anomaly_score, 4),
            behavioral_trust_index=round(trust_index, 4)
        )


behavioral_biometrics_engine = BehavioralBiometricsEngine()
