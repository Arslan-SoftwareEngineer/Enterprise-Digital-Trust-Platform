"""
Security, Cryptographic Hashing, and Token Utilities
"""

import hashlib
import hmac
import secrets
from typing import Optional


def hash_token(data: str) -> str:
    """Generate SHA-256 fingerprint for biometric / document payloads."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def compute_hmac(secret: str, message: str) -> str:
    """Compute HMAC-SHA256 signature for API integrity."""
    return hmac.new(secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()


def generate_session_id(prefix: str = "kyc_sess_") -> str:
    """Generate random cryptographically secure KYC session ID."""
    return f"{prefix}{secrets.token_hex(8)}"
