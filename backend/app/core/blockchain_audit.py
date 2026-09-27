"""
Blockchain-Based Immutable Audit Ledger & Merkle Tree Verification Engine
Bonus Challenge: Cryptographic verification of KYC and deepfake forensic decisions.
"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from ..models.schemas import BlockchainAuditProof


class MerkleTree:
    """Computes SHA-256 Merkle root across forensic data leaves."""

    @staticmethod
    def hash_leaf(data: Any) -> str:
        serialized = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    @classmethod
    def compute_root(cls, leaves: List[str]) -> str:
        if not leaves:
            return hashlib.sha256(b"empty_block").hexdigest()
        if len(leaves) == 1:
            return leaves[0]

        next_level = []
        for i in range(0, len(leaves), 2):
            left = leaves[i]
            right = leaves[i + 1] if i + 1 < len(leaves) else left
            combined = hashlib.sha256((left + right).encode("utf-8")).hexdigest()
            next_level.append(combined)

        return cls.compute_root(next_level)


class Block:
    """An individual immutable audit block in the ledger chain."""

    def __init__(
        self,
        index: int,
        timestamp: float,
        transactions: List[Dict[str, Any]],
        previous_hash: str,
        nonce: int = 0
    ):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()

    def calculate_merkle_root(self) -> str:
        leaf_hashes = [MerkleTree.hash_leaf(tx) for tx in self.transactions]
        return MerkleTree.compute_root(leaf_hashes)

    def calculate_hash(self) -> str:
        header = f"{self.index}{self.timestamp}{self.previous_hash}{self.merkle_root}{self.nonce}"
        return hashlib.sha256(header.encode("utf-8")).hexdigest()

    def mine_block(self, difficulty: int = 2):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()


class BlockchainLedger:
    """Decentralized style tamper-evident audit ledger for identity verification."""

    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = Block(
            index=0,
            timestamp=1700000000.0,
            transactions=[{"event": "GENESIS_BLOCK", "system": "ENTERPRISE-TRUST-CHAIN"}],
            previous_hash="0" * 64
        )
        genesis.mine_block(self.difficulty)
        self.chain.append(genesis)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def record_verification_audit(self, audit_record: Dict[str, Any]) -> BlockchainAuditProof:
        """Add verification event and mine an immutable block."""
        latest = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=[audit_record],
            previous_hash=latest.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

        return BlockchainAuditProof(
            block_index=new_block.index,
            timestamp_iso=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(new_block.timestamp)),
            merkle_root=new_block.merkle_root,
            previous_hash=new_block.previous_hash,
            block_hash=new_block.hash,
            tamper_proof_verified=self.verify_chain_integrity()
        )

    def verify_chain_integrity(self) -> bool:
        """Validates all cryptographic hashes and Merkle roots across the ledger."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
            if current.merkle_root != current.calculate_merkle_root():
                return False
        return True


# Global audit ledger instance
audit_ledger = BlockchainLedger(difficulty=2)
