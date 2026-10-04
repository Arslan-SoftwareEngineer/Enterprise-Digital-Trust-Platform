"""
Enterprise Digital Identity, Trust & Deepfake Detection Platform
FastAPI Application Entrypoint & API Gateway
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

from .config import settings
from .routers import (
    verification_router,
    analytics_router,
    graph_router,
    alerts_router,
    copilot_router
)

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

# Mount API Routers under /api/v1
app.include_router(verification_router, prefix=settings.API_PREFIX)
app.include_router(analytics_router, prefix=settings.API_PREFIX)
app.include_router(graph_router, prefix=settings.API_PREFIX)
app.include_router(alerts_router, prefix=settings.API_PREFIX)
app.include_router(copilot_router, prefix=settings.API_PREFIX)


@app.get("/health", tags=["System"])
async def health_check():
    """System health check and engine readiness probe."""
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

if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/", tags=["Dashboard UI"])
    async def serve_index():
        index_path = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "Frontend index.html under preparation"}
