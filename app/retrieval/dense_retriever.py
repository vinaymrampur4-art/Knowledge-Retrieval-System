"""
dense_retriever.py

Dense retriever wrapper.
"""

import time

from mcp_server.models import SearchFilter

from app.retrieval.base_retriever import BaseRetriever
from app.retrieval.query_embedder import QueryEmbedder
from app.retrieval.multi_collection_retriever import (
    MultiCollectionRetriever,
)
from app.retrieval.search_result import SearchResult


class DenseRetriever(BaseRetriever):

    def __init__(self):

        self.embedder = QueryEmbedder()

        self.retriever = MultiCollectionRetriever()

    # ---------------------------------------------------------

    def search(
        self,
        query: str,
        collections: list[str] | None = None,
        filter: SearchFilter | None = None,
        top_k: int = 10,
    ) -> list[SearchResult]:
        """
        Perform semantic search.

        Parameters
        ----------
        query : str
            User query.

        collections : list[str] | None
            Collections to search.
            If None, searches all collections.

        filter : SearchFilter | None
            Optional metadata filter applied to retrieved
            documents.

        top_k : int
            Number of results to return.

        Returns
        -------
        list[SearchResult]
            Ranked semantic search results.
        """

        print("=" * 80)
        print("DENSE FILTER")
        print(type(filter))
        print(filter)
        print("=" * 80)

        # ---------------------------------------------------------
        # Query Embedding Time
        # ---------------------------------------------------------

        embedding_start = time.perf_counter()

        embedding = self.embedder.embed(query)

        embedding_time = (
            time.perf_counter() - embedding_start
        ) * 1000

        # ---------------------------------------------------------
        # ChromaDB Search Time
        # ---------------------------------------------------------

        search_start = time.perf_counter()

        results = self.retriever.search(
            query_embedding=embedding,
            collections=collections,
            filter=filter,
            top_k=top_k,
        )

        search_time = (
            time.perf_counter() - search_start
        ) * 1000

        # ---------------------------------------------------------
        # Latency Report
        # ---------------------------------------------------------

        print("=" * 80)
        print("DENSE RETRIEVAL LATENCY")
        print("=" * 80)
        print(f"Query Embedding Time : {embedding_time:.2f} ms")
        print(f"Chroma Search Time   : {search_time:.2f} ms")
        print(
            f"Dense Total Time     : "
            f"{embedding_time + search_time:.2f} ms"
        )
        print("=" * 80)

        return results