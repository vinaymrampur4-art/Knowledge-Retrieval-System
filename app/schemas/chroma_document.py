"""
Generic ChromaDB document.
"""

from dataclasses import dataclass, field


@dataclass
class ChromaDocument:
    """
    Generic document that will be inserted into ChromaDB.
    """

    collection_name: str

    id: str

    document: str

    embedding: list[float]

    metadata: dict = field(default_factory=dict)