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

    def _search_collection(
        self,
        collection: str,
        query_embedding: list[float],
        filter: SearchFilter | None,
        top_k: int,
    ) -> list[SearchResult]:
        """
        Search a single collection.
        """

        try:

            return self.retriever.search(
                collection_name=collection,
                query_embedding=query_embedding,
                filter=filter,
                top_k=top_k,
            )

        except Exception as e:

            print(
                f"[WARNING] Failed searching {collection}: {e}"
            )

            return []

    # ---------------------------------------------------------

    def _search_collection_batch(
        self,
        collection: str,
        query_embeddings: list[list[float]],
        filter: SearchFilter | None,
        top_k: int,
    ) -> list[list[SearchResult]]:
        """
        Search a single collection for multiple queries.
        """

        try:

            return self.retriever.search_batch(
                collection_name=collection,
                query_embeddings=query_embeddings,
                filter=filter,
                top_k=top_k,
            )

        except Exception as e:

            print(
                f"[WARNING] Failed searching {collection}: {e}"
            )

            return [[] for _ in query_embeddings]

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

        # -----------------------------------------------------
        # Search all collections sequentially
        # -----------------------------------------------------

        for collection in collections:

            results = self._search_collection(
                collection=collection,
                query_embedding=query_embedding,
                filter=filter,
                top_k=top_k,
            )

            all_results.extend(results)

        return self._rank_results(
            all_results,
            top_k,
        )

    # ---------------------------------------------------------

    def search_batch(
        self,
        query_embeddings: list[list[float]],
        collections: list[str] | None = None,
        filter: SearchFilter | None = None,
        top_k: int = 5,
    ) -> list[list[SearchResult]]:
        """
        Search multiple collections for multiple queries.

        Parameters
        ----------
        query_embeddings : list[list[float]]
            Embedded user queries.

        collections : list[str] | None
            Collections to search.

        filter : SearchFilter | None
            Optional metadata filter.

        top_k : int
            Number of results per collection.

        Returns
        -------
        list[list[SearchResult]]
            Ranked results for each query.
        """

        if collections is None:
            collections = self.DEFAULT_COLLECTIONS

        all_query_results: list[list[SearchResult]] = [
            [] for _ in query_embeddings
        ]

        for collection in collections:

            collection_results = self._search_collection_batch(
                collection=collection,
                query_embeddings=query_embeddings,
                filter=filter,
                top_k=top_k,
            )

            for index, results in enumerate(collection_results):
                all_query_results[index].extend(results)

        ranked_results: list[list[SearchResult]] = []

        for results in all_query_results:
            ranked_results.append(
                self._rank_results(
                    results,
                    top_k,
                )
            )

        return ranked_results

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