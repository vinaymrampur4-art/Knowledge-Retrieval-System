"""
hierarchy.py

Maintains parent-child relationships between parsed chunks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ChunkNode:
    """
    Represents a chunk inside the hierarchy.
    """

    chunk_id: str
    name: str
    chunk_type: str

    parent_id: Optional[str] = None

    children: List[str] = field(default_factory=list)

    depth: int = 0

    def add_child(self, child_id: str) -> None:
        """Attach a child node."""
        if child_id not in self.children:
            self.children.append(child_id)


class ChunkHierarchy:
    """
    Stores and manages relationships between chunks.
    """

    def __init__(self):
        self.nodes: dict[str, ChunkNode] = {}

    def add_node(self, node: ChunkNode):
        self.nodes[node.chunk_id] = node

    def get(self, chunk_id: str) -> Optional[ChunkNode]:
        return self.nodes.get(chunk_id)

    def connect(
        self,
        parent_id: str,
        child_id: str,
    ):
        parent = self.get(parent_id)
        child = self.get(child_id)

        if not parent or not child:
            return

        parent.add_child(child_id)

        child.parent_id = parent_id

        child.depth = parent.depth + 1

    def roots(self):
        return [
            node
            for node in self.nodes.values()
            if node.parent_id is None
        ]