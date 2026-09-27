"""
AI Identity Copilot Router
Provides interactive analyst conversational interface and automated SAR generation.
"""

from fastapi import APIRouter
from typing import Dict, Any, List
from ..models.schemas import CopilotQueryRequest, CopilotResponse
from ..engines.ai_copilot import ai_identity_copilot

router = APIRouter(prefix="/copilot", tags=["AI Copilot"])


@router.post("/query", response_model=CopilotResponse)
async def query_copilot(request: CopilotQueryRequest) -> CopilotResponse:
    """Security analyst conversational forensic query endpoint."""
    return ai_identity_copilot.analyze_query(request)


@router.get("/suggested-queries")
async def get_suggested_queries() -> List[str]:
    """Returns top prompt accelerators for security analysts."""
    return [
        "Why did verification fail?",
        "Explain the fraud indicators.",
        "Compare this face with previous records.",
        "Show deepfake probability.",
        "Generate investigation summary.",
        "Recommend verification action."
    ]
