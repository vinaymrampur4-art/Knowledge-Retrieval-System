"""
multi_collection_retriever.py

Searches one or more ChromaDB collections and returns
a unified ranked list of SearchResult objects.
"""

from mcp_server.models import SearchFilter

from app.core.config import (
    FILES_COLLECTION,
    CLASSES_COLLECTION,
    METHODS_COLLECTION,
    FUNCTIONS_COLLECTION,
    CODE_BLOCK_COLLECTION,
)

from app.retrieval.chroma_retriever import ChromaRetriever
from app.retrieval.search_result import SearchResult


class MultiCollectionRetriever:
    """
    Performs semantic search across one or more Chroma collections.
    """

    DEFAULT_COLLECTIONS = [
        FILES_COLLECTION,
        CLASSES_COLLECTION,
        METHODS_COLLECTION,
        FUNCTIONS_COLLECTION,
        CODE_BLOCK_COLLECTION,
    ]

    def __init__(self):

        self.retriever = ChromaRetriever()

    # ---------------------------------------------------------

    def search(
        self,
        query_embedding: list[float],
        collections: list[str] | None = None,
        filter: SearchFilter | None = None,
        top_k: int = 5,
    ) -> list[SearchResult]:
        """
        Search one or more collections and merge the results.

        Parameters
        ----------
        query_embedding : list[float]
            Embedded user query.

        collections : list[str] | None
            Collections to search.
            If None, searches all configured collections.

        filter : SearchFilter | None
            Optional metadata filter applied to retrieved
            documents.

        top_k : int
            Number of results to retrieve from each collection.

        Returns
        -------
        list[SearchResult]
            Ranked search results from all collections.
        """

        print("=" * 80)
        print("MULTI COLLECTION FILTER")
        print(type(filter))
        print(filter)
        print("=" * 80)

        if collections is None:
            collections = self.DEFAULT_COLLECTIONS

        all_results: list[SearchResult] = []

        for collection in collections:

            try:

                results = self.retriever.search(
                    collection_name=collection,
                    query_embedding=query_embedding,
                    filter=filter,
                    top_k=top_k,
                )

                all_results.extend(results)

            except Exception as e:

                print(
                    f"[WARNING] Failed searching {collection}: {e}"
                )

        return self._rank_results(
            all_results,
            top_k,
        )

    # ---------------------------------------------------------

    def _rank_results(
        self,
        results: list[SearchResult],
        top_k: int,
    ) -> list[SearchResult]:
        """
        Sort results by similarity score.

        Parameters
        ----------
        results : list[SearchResult]
            Results retrieved from all collections.

        top_k : int
            Maximum number of results to return.

        Returns
        -------
        list[SearchResult]
            Top ranked search results.
        """

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results[:top_k]