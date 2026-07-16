"""
hybrid_retriever.py

Hybrid Retriever with optional debug output.
"""

from mcp_server.models import SearchFilter

from app.retrieval.dense_retriever import DenseRetriever
from app.retrieval.sparse.bm25_retriever import BM25Retriever
from app.retrieval.hybrid.rrf_ranker import RRFRanker
from app.retrieval.reranker.reranker import Reranker

from app.retrieval.search_result import SearchResult


class HybridRetriever:

    def __init__(
        self,
        repository_name: str,
    ):

        self.repository_name = repository_name

        self.dense = DenseRetriever()

        self.bm25 = BM25Retriever(
            repository_name
        )

        self.rrf = RRFRanker()

        self.reranker = Reranker()

    # ---------------------------------------------------------
    # Debug Helper
    # ---------------------------------------------------------

    def _print_results(
        self,
        title: str,
        results: list[SearchResult],
    ):

        print()

        print("=" * 80)

        print(title)

        print("=" * 80)

        for i, result in enumerate(
            results,
            start=1,
        ):

            metadata = (
                result.metadata or {}
            )

            name = (
                metadata.get(
                    "method_name"
                )
                or metadata.get(
                    "function_name"
                )
                or metadata.get(
                    "class_name"
                )
                or metadata.get(
                    "module_name"
                )
                or result.id
            )

            print(
                f"{i:2d}. "
                f"{result.score:.4f} | "
                f"{name}"
            )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
        collections: list[str] | None = None,
        filter: SearchFilter | None = None,
        top_k: int = 5,
        debug: bool = False,
    ) -> list[SearchResult]:

        candidate_k = max(
            20,
            top_k * 4,
        )

        # -----------------------------------------------------
        # Dense Retrieval
        # -----------------------------------------------------

        dense_results = (
            self.dense.search(
                query=query,
                collections=collections,
                filter=filter,
                top_k=candidate_k,
            )
        )

        if debug:

            self._print_results(
                "DENSE RESULTS",
                dense_results,
            )

        # -----------------------------------------------------
        # BM25 Retrieval
        # -----------------------------------------------------

        bm25_results = (
            self.bm25.search(
                query=query,
                filter=filter,
                top_k=candidate_k,
            )
        )

        if debug:

            self._print_results(
                "BM25 RESULTS",
                bm25_results,
            )

        # -----------------------------------------------------
        # RRF Fusion
        # -----------------------------------------------------

        hybrid_results = (
            self.rrf.rank(
                [
                    dense_results,
                    bm25_results,
                ],
                top_k=candidate_k,
            )
        )

        if debug:

            self._print_results(
                "RRF RESULTS",
                hybrid_results,
            )

        # -----------------------------------------------------
        # Cross Encoder Reranking
        # -----------------------------------------------------

        reranked_results = (
            self.reranker.rerank(
                query=query,
                results=hybrid_results,
                top_k=top_k,
            )
        )

        if debug:

            self._print_results(
                "RERANKED RESULTS",
                reranked_results,
            )

        return reranked_results