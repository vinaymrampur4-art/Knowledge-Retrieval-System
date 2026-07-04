"""
bm25_index_builder.py

Builds the BM25 index from searchable documents.
"""

from app.retrieval.sparse.bm25_store import (
    BM25Store,
    BM25Document,
)
from app.retrieval.sparse.bm25_index import BM25Index


class BM25IndexBuilder:
    """
    Builds the BM25 index.
    """

    def __init__(self):

        self.store = BM25Store()

        self.index = BM25Index()

    # ---------------------------------------------------------

    def build(
        self,
        documents: list[dict],
    ) -> BM25Index:
        """
        Build BM25 index from documents.

        Parameters
        ----------
        documents : list[dict]

            [
                {
                    "id": "...",
                    "content": "...",
                    "metadata": {...}
                }
            ]
        """

        self.store.clear()

        for document in documents:

            self.store.add_document(

                BM25Document(

                    id=document["id"],

                    content=document["content"],

                    metadata=document.get(
                        "metadata",
                        {},
                    ),

                )

            )

        self.index.build(self.store)

        return self.index

    # ---------------------------------------------------------

    def get_store(self) -> BM25Store:

        return self.store