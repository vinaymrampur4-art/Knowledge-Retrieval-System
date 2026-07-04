"""
bm25_index.py

Creates an in-memory BM25 index.
"""

from rank_bm25 import BM25Okapi

from app.retrieval.sparse.tokenizer import BM25Tokenizer
from app.retrieval.sparse.bm25_store import BM25Store


class BM25Index:

    def __init__(self):

        self.tokenizer = BM25Tokenizer()

        self.bm25 = None

    # ---------------------------------------------------------

    def build(
        self,
        store: BM25Store,
    ) -> None:
        """
        Build the BM25 index from the document store.
        """

        corpus = []

        for document in store.get_documents():

            corpus.append(
                self.tokenizer.tokenize(
                    document.content
                )
            )

        self.bm25 = BM25Okapi(corpus)

    # ---------------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[tuple[int, float]]:
        """
        Search the BM25 index.

        Returns
        -------
        List[(document_index, score)]
        """

        if self.bm25 is None:
            raise RuntimeError(
                "BM25 index has not been built."
            )

        query_tokens = self.tokenizer.tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked[:top_k]