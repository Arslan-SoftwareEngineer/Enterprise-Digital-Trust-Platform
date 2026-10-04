"""
Enterprise Digital Identity, Trust & Deepfake Detection Platform
Root Entrypoint for Cloud Deployments (Vercel, Render, Railway, etc.)
"""
import os
import sys

_root = os.path.dirname(os.path.abspath(__file__))
if _root not in sys.path:
    sys.path.insert(0, _root)

from backend.app.main import app

__all__ = ["app"]
