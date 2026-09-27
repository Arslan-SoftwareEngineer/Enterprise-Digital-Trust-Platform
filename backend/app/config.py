"""
System Configuration for Enterprise Digital Identity, Trust & Deepfake Detection Platform
"""

import os
from pydantic import BaseModel


class SystemSettings(BaseModel):
    PROJECT_NAME: str = "Enterprise Digital Identity, Trust & Deepfake Detection Platform"
    PROJECT_CODE: str = "ENTERPRISE-TRUST-v1"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # Server Bindings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Verification Engine Thresholds
    FACE_MATCH_THRESHOLD: float = 0.75
    ACTIVE_LIVENESS_THRESHOLD: float = 0.70
    PASSIVE_LIVENESS_THRESHOLD: float = 0.65
    DEEPFAKE_ALERT_THRESHOLD: float = 0.50
    VOICE_CLONE_THRESHOLD: float = 0.55
    DOCUMENT_TAMPER_THRESHOLD: float = 0.40

    # Trust Score Gates (0 - 1000)
    TRUST_AUTO_APPROVE: int = 800
    TRUST_CONDITIONAL_PASS: int = 650
    TRUST_MANUAL_REVIEW: int = 450

    # Infrastructure Fallback / Emulation
    USE_IN_MEMORY_EVENT_BUS: bool = True
    USE_IN_MEMORY_GRAPH: bool = True
    BLOCKCHAIN_DIFFICULTY: int = 2

    # Database / Broker URLs (for production deployment)
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "postgresql://admin:secret@localhost:5432/trust_identity")
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


settings = SystemSettings()
