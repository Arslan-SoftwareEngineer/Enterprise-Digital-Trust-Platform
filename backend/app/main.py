"""
Enterprise Digital Identity, Trust & Deepfake Detection Platform
FastAPI Application Entrypoint & API Gateway
"""

import os
import sys
import traceback

_repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from .config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise Digital Identity, Trust & Deepfake Detection Platform with Multi-Modal AI, Knowledge Graph & Blockchain Audit.",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin enterprise frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_init_error = None
try:
    from .routers import (
        verification_router,
        analytics_router,
        graph_router,
        alerts_router,
        copilot_router
    )
    # Mount API Routers under /api/v1
    app.include_router(verification_router, prefix=settings.API_PREFIX)
    app.include_router(analytics_router, prefix=settings.API_PREFIX)
    app.include_router(graph_router, prefix=settings.API_PREFIX)
    app.include_router(alerts_router, prefix=settings.API_PREFIX)
    app.include_router(copilot_router, prefix=settings.API_PREFIX)
except Exception as ex:
    _init_error = traceback.format_exc()
    print("CRITICAL: Failed to mount routers:\n", _init_error, file=sys.stderr)


@app.get("/health", tags=["System"])
async def health_check():
    """System health check and engine readiness probe."""
    if _init_error:
        return {
            "status": "DEGRADED",
            "error": _init_error
        }
    return {
        "status": "HEALTHY",
        "project": settings.PROJECT_NAME,
        "code": settings.PROJECT_CODE,
        "version": settings.VERSION,
        "engines_online": [
            "IdentityVerificationEngine",
            "FaceLivenessEngine",
            "DeepfakeDetector",
            "VoiceAuthenticator",
            "DocumentIntelligence",
            "TrustScoringEngine",
            "IdentityKnowledgeGraph",
            "BehavioralBiometricsEngine",
            "AIIdentityCopilot",
            "BlockchainAuditLedger"
        ]
    }


# Static Frontend Serving
_candidate_dirs = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend")),
    os.path.abspath(os.path.join(os.getcwd(), "frontend")),
    os.path.abspath("frontend"),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../frontend")),
]
frontend_dir = next((d for d in _candidate_dirs if os.path.isdir(d)), _candidate_dirs[0])

if os.path.isdir(frontend_dir):
    try:
        app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
    except Exception as e:
        print("WARNING: Static mount failed:", e, file=sys.stderr)

@app.get("/", tags=["Dashboard UI"])
async def serve_index():
    if _init_error:
        return HTMLResponse(
            f"<h1>Application Router Error</h1><pre style='background:#111;color:#ff5555;padding:20px;'>{_init_error}</pre>",
            status_code=500
        )
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "ONLINE",
        "project": settings.PROJECT_NAME,
        "message": "FastAPI Gateway is operational. Access /docs for interactive Swagger API Explorer.",
        "docs_url": "/docs",
        "health_url": "/health"
    }
