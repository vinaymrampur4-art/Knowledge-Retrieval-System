"""
Dense retriever wrapper.
"""

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

        top_k : int
            Number of results to return.

        Returns
        -------
        list[SearchResult]
        """

        embedding = self.embedder.embed(query)

        return self.retriever.search(

            query_embedding=embedding,

            collections=collections,

            top_k=top_k,

        )