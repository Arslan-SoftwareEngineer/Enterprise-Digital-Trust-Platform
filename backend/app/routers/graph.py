"""
Identity Knowledge Graph Router
Enables visual exploration of entity relationships, syndicate clusters, and Neo4j sync.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from ..engines.knowledge_graph import identity_knowledge_graph
from ..models.schemas import KnowledgeGraphResult

router = APIRouter(prefix="/graph", tags=["Knowledge Graph"])


@router.get("/subgraph/{user_id}", response_model=KnowledgeGraphResult)
async def get_user_subgraph(user_id: str) -> KnowledgeGraphResult:
    """Returns the 2-hop neighborhood of an applicant for visual graph rendering."""
    return identity_knowledge_graph.analyze_identity_risk(user_id)


@router.get("/syndicates")
async def list_syndicates() -> List[Dict[str, Any]]:
    """Returns detected organized criminal syndicate rings."""
    return [
        {
            "syndicate_id": "SYNDICATE_ALPHA_7",
            "name": "Ghost Device Replay Ring",
            "primary_hub": "DEV_FINGERPRINT_ROUTER_98",
            "connected_identities": ["USR_PUPPET_01", "USR_PUPPET_02", "USR_PUPPET_03"],
            "fraud_type": "Synthetic Identity Laundering",
            "risk_score": 98.4,
            "associated_ip": "185.220.101.5 (Tor Exit)"
        },
        {
            "syndicate_id": "SYNDICATE_BRAVO_9",
            "name": "ElevenLabs Banking Voice Mimic Syndicate",
            "primary_hub": "VOIP_GATEWAY_CLUSTER_14",
            "connected_identities": ["usr_infiltrator_08", "usr_infiltrator_09"],
            "fraud_type": "High-Net-Worth Account Takeover (ATO)",
            "risk_score": 94.1,
            "associated_ip": "194.26.29.112 (Proxy VPN)"
        }
    ]


@router.get("/cypher/{user_id}")
async def get_cypher_export(user_id: str) -> Dict[str, str]:
    """Generates ready-to-run Cypher query for enterprise Neo4j databases."""
    query = identity_knowledge_graph.generate_cypher_export(user_id)
    return {"user_id": user_id, "cypher_query": query}
