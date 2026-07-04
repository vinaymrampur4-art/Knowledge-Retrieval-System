"""
bm25_store.py

Stores all documents used by the BM25 retrieval engine.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class BM25Document:
    """
    Represents one BM25 searchable document.
    """

    id: str

    content: str

    metadata: dict[str, Any] = field(default_factory=dict)


class BM25Store:
    """
    Stores every searchable document.
    """

    def __init__(self):

        self.documents: list[BM25Document] = []

    # ---------------------------------------------------------

    def add_document(
        self,
        document: BM25Document,
    ) -> None:

        self.documents.append(document)

    # ---------------------------------------------------------

    def get_documents(
        self,
    ) -> list[BM25Document]:

        return self.documents

    # ---------------------------------------------------------

    def __len__(self):

        return len(self.documents)

    # ---------------------------------------------------------

    def clear(self):

        self.documents.clear()