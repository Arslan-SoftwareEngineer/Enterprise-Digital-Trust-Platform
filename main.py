"""
Enterprise Digital Identity, Trust & Deepfake Detection Platform
Root Entrypoint for Cloud Deployments (Vercel, Render, Railway, etc.)
"""

from backend.app.main import app

__all__ = ["app"]
