"""
dense_retriever.py

Dense retriever wrapper.
"""

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

        embedding = self.embedder.embed(query)

        return self.retriever.search(
            query_embedding=embedding,
            collections=collections,
            filter=filter,
            top_k=top_k,
        )