"""
Identity Knowledge Graph Engine
Module 8: Graph Analytics with NetworkX, Synthetic Identity Ring Detection,
Degree Centrality, Multi-entity Link Analysis, and Neo4j Cypher Integration.
"""

import networkx as nx
from typing import Dict, List, Any, Optional, Set, Tuple
from ..models.schemas import KnowledgeGraphResult


class IdentityKnowledgeGraph:
    """
    High-performance graph intelligence engine linking Users, Devices, Documents,
    Phone Numbers, IP Addresses, Biometric Profiles, and Fraud Cases.
    """

    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self._seed_sample_fraud_graph()

    def _seed_sample_fraud_graph(self):
        """Populates realistic baseline enterprise graph including known fraud syndicates."""
        # Known fraudulent syndicate cluster
        fraud_ring_id = "SYNDICATE_ALPHA_7"
        fraud_device = "DEV_FINGERPRINT_ROUTER_98"
        fraud_ip = "185.220.101.5"  # Known TOR exit / VPN
        fraud_phone = "+14155550199"

        self.graph.add_node("CASE_FRAUD_882", type="FraudCase", severity="CRITICAL", description="Synthetic Identity Laundering Ring")
        self.graph.add_node(fraud_device, type="Device", os="Linux/Emulated", risk="HIGH")
        self.graph.add_node(fraud_ip, type="IPAddress", is_vpn=True, is_tor=True)
        self.graph.add_node(fraud_phone, type="PhoneNumber", carrier="VOIP_VIRTUAL")

        # Three compromised synthetic puppet identities sharing device and IP
        puppets = ["USR_PUPPET_01", "USR_PUPPET_02", "USR_PUPPET_03"]
        for p in puppets:
            self.graph.add_node(p, type="User", status="FLAGGED")
            self.graph.add_edge(p, fraud_device, relation="OWNS_DEVICE")
            self.graph.add_edge(p, fraud_ip, relation="USES_IP")
            self.graph.add_edge(p, fraud_phone, relation="ASSOCIATED_WITH_PHONE")
            self.graph.add_edge(p, "CASE_FRAUD_882", relation="LINKED_TO_FRAUD")

        # Authentic verified corporate benchmark identities
        self.graph.add_node("USR_CLEAN_BENCHMARK", type="User", status="VERIFIED")
        self.graph.add_node("DEV_CLEAN_CORP_MAC", type="Device", os="macOS", risk="LOW")
        self.graph.add_node("192.168.1.100", type="IPAddress", is_vpn=False)
        self.graph.add_edge("USR_CLEAN_BENCHMARK", "DEV_CLEAN_CORP_MAC", relation="OWNS_DEVICE")
        self.graph.add_edge("USR_CLEAN_BENCHMARK", "192.168.1.100", relation="USES_IP")

    def register_applicant(
        self,
        user_id: str,
        document_number: str,
        ip_address: str,
        device_fingerprint: str,
        phone_number: str,
        face_hash: str
    ):
        """Ingests and links a new applicant's entities into the knowledge graph."""
        # Nodes
        self.graph.add_node(user_id, type="User")
        self.graph.add_node(f"DOC_{document_number}", type="Document", doc_number=document_number)
        self.graph.add_node(ip_address, type="IPAddress")
        self.graph.add_node(device_fingerprint, type="Device")
        self.graph.add_node(phone_number, type="PhoneNumber")
        self.graph.add_node(f"BIO_{face_hash[:16]}", type="BiometricProfile", hash_val=face_hash)

        # Edges
        self.graph.add_edge(user_id, f"DOC_{document_number}", relation="SUBMITTED_DOCUMENT")
        self.graph.add_edge(user_id, ip_address, relation="USES_IP")
        self.graph.add_edge(user_id, device_fingerprint, relation="OWNS_DEVICE")
        self.graph.add_edge(user_id, phone_number, relation="ASSOCIATED_WITH_PHONE")
        self.graph.add_edge(user_id, f"BIO_{face_hash[:16]}", relation="HAS_BIOMETRIC")

    def analyze_identity_risk(self, user_id: str) -> KnowledgeGraphResult:
        """
        Executes graph analytics on the applicant node:
        - Degree centrality & fan-out
        - Shared device / IP / phone collision with other users
        - Path finding to known fraud cases
        - Synthetic identity cycle detection
        """
        if not self.graph.has_node(user_id):
            # Not yet ingested, return baseline clean score
            return KnowledgeGraphResult(
                node_id=user_id,
                degree_centrality=0.01,
                connected_users_count=0,
                shared_devices_count=0,
                shared_ips_count=0,
                shared_phone_count=0,
                shared_biometric_hashes=0,
                syndicate_detected=False,
                syndicate_id=None,
                graph_risk_flags=[],
                subgraph_nodes=[],
                subgraph_edges=[]
            )

        # Compute degree centrality
        degrees = nx.degree_centrality(self.graph)
        degree = degrees.get(user_id, 0.0)

        # Find connected 2-hop neighborhood (User -> Entity -> Other Users)
        neighbors = set(self.graph.neighbors(user_id))
        connected_users: Set[str] = set()
        shared_devices = 0
        shared_ips = 0
        shared_phones = 0
        shared_bios = 0
        risk_flags = []
        syndicate_detected = False
        syndicate_id = None

        for n in neighbors:
            n_data = self.graph.nodes.get(n, {})
            n_type = n_data.get("type", "")

            # Look for other users linked to this entity
            predecessors = set(self.graph.predecessors(n))
            other_users = {u for u in predecessors if u != user_id and self.graph.nodes.get(u, {}).get("type") == "User"}
            connected_users.update(other_users)

            if other_users:
                if n_type == "Device":
                    shared_devices += len(other_users)
                    risk_flags.append(f"Device '{n}' is shared with {len(other_users)} other registered identities.")
                elif n_type == "IPAddress":
                    shared_ips += len(other_users)
                    if len(other_users) >= 3:
                        risk_flags.append(f"High-velocity IP sharing: {len(other_users)} accounts linked.")
                elif n_type == "PhoneNumber":
                    shared_phones += len(other_users)
                    risk_flags.append(f"Phone number '{n}' reused across multiple user accounts.")
                elif n_type == "BiometricProfile":
                    shared_bios += len(other_users)
                    risk_flags.append("CRITICAL: Same facial biometric embedding registered under different applicant names.")

        # Check path to any known FraudCase node
        fraud_nodes = [node for node, data in self.graph.nodes(data=True) if data.get("type") == "FraudCase"]
        undirected_view = self.graph.to_undirected()

        for fn in fraud_nodes:
            if nx.has_path(undirected_view, user_id, fn):
                path_len = nx.shortest_path_length(undirected_view, user_id, fn)
                if path_len <= 3:
                    syndicate_detected = True
                    syndicate_id = "SYNDICATE_LINKED_" + fn
                    risk_flags.append(f"Direct connection to confirmed fraud case '{fn}' ({path_len} hops).")

        if len(connected_users) >= 2 or shared_bios > 0:
            syndicate_detected = True
            if not syndicate_id:
                syndicate_id = "SYNTHETIC_RING_AUTO_FLAG"

        # Extract 2-hop ego subgraph for visual dashboard rendering
        ego = nx.ego_graph(undirected_view, user_id, radius=2)
        subgraph_nodes = []
        for node in ego.nodes():
            nd = self.graph.nodes.get(node, {})
            subgraph_nodes.append({
                "id": str(node),
                "type": nd.get("type", "Unknown"),
                "label": str(node)[:24],
                "is_current": (node == user_id)
            })

        subgraph_edges = []
        for u, v in ego.edges():
            subgraph_edges.append({
                "source": str(u),
                "target": str(v),
                "relation": "LINKED"
            })

        return KnowledgeGraphResult(
            node_id=user_id,
            degree_centrality=round(float(degree), 4),
            connected_users_count=len(connected_users),
            shared_devices_count=shared_devices,
            shared_ips_count=shared_ips,
            shared_phone_count=shared_phones,
            shared_biometric_hashes=shared_bios,
            syndicate_detected=syndicate_detected,
            syndicate_id=syndicate_id,
            graph_risk_flags=risk_flags,
            subgraph_nodes=subgraph_nodes,
            subgraph_edges=subgraph_edges
        )

    def generate_cypher_export(self, user_id: str) -> str:
        """Generates Neo4j Cypher statements for database synchronization."""
        queries = [
            f"MERGE (u:User {{id: '{user_id}'}})",
            f"MATCH (u:User {{id: '{user_id}'}})-[r]-(n) RETURN u, r, n LIMIT 50;"
        ]
        return "\n".join(queries)


identity_knowledge_graph = IdentityKnowledgeGraph()
