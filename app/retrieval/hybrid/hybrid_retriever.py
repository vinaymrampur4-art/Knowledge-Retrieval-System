"""
hybrid_retriever.py

Hybrid Retriever with optional debug output
and latency profiling.
"""

import time

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
                metadata.get("method_name")
                or metadata.get("function_name")
                or metadata.get("class_name")
                or metadata.get("module_name")
                or result.id
            )

            print(
                f"{i:2d}. "
                f"{result.score:.4f} | "
                f"{name}"
            )

    # ---------------------------------------------------------
    # Latency Helper
    # ---------------------------------------------------------

    def _print_latency(
        self,
        query: str,
        dense_ms: float,
        bm25_ms: float,
        rrf_ms: float,
        reranker_ms: float,
        total_ms: float,
    ):

        print()

        print("=" * 80)
        print("SEARCH LATENCY REPORT")
        print("=" * 80)

        print(f"Query              : {query}")
        print()

        print(f"Dense Retrieval    : {dense_ms:8.2f} ms")
        print(f"BM25 Retrieval     : {bm25_ms:8.2f} ms")
        print(f"RRF Fusion         : {rrf_ms:8.2f} ms")
        print(f"Cross Encoder      : {reranker_ms:8.2f} ms")

        print("-" * 80)

        print(f"TOTAL              : {total_ms:8.2f} ms")

        print("=" * 80)
        print()

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

        overall_start = time.perf_counter()

        candidate_k = max(
            20,
            top_k * 4,
        )

        # -----------------------------------------------------
        # Dense Retrieval
        # -----------------------------------------------------

        dense_start = time.perf_counter()

        dense_results = (
            self.dense.search(
                query=query,
                collections=collections,
                filter=filter,
                top_k=candidate_k,
            )
        )

        dense_ms = (
            time.perf_counter() - dense_start
        ) * 1000

        if debug:

            self._print_results(
                "DENSE RESULTS",
                dense_results,
            )

        # -----------------------------------------------------
        # BM25 Retrieval
        # -----------------------------------------------------

        bm25_start = time.perf_counter()

        bm25_results = (
            self.bm25.search(
                query=query,
                filter=filter,
                top_k=candidate_k,
            )
        )

        bm25_ms = (
            time.perf_counter() - bm25_start
        ) * 1000

        if debug:

            self._print_results(
                "BM25 RESULTS",
                bm25_results,
            )

        # -----------------------------------------------------
        # RRF Fusion
        # -----------------------------------------------------

        rrf_start = time.perf_counter()

        hybrid_results = (
            self.rrf.rank(
                [
                    dense_results,
                    bm25_results,
                ],
                top_k=candidate_k,
            )
        )

        rrf_ms = (
            time.perf_counter() - rrf_start
        ) * 1000

        if debug:

            self._print_results(
                "RRF RESULTS",
                hybrid_results,
            )

        # -----------------------------------------------------
        # Cross Encoder Reranking
        # -----------------------------------------------------

        reranker_start = time.perf_counter()

        reranked_results = (
            self.reranker.rerank(
                query=query,
                results=hybrid_results,
                top_k=top_k,
            )
        )

        reranker_ms = (
            time.perf_counter() - reranker_start
        ) * 1000

        if debug:

            self._print_results(
                "RERANKED RESULTS",
                reranked_results,
            )

        # -----------------------------------------------------
        # Total Latency
        # -----------------------------------------------------

        total_ms = (
            time.perf_counter() - overall_start
        ) * 1000

        self._print_latency(
            query=query,
            dense_ms=dense_ms,
            bm25_ms=bm25_ms,
            rrf_ms=rrf_ms,
            reranker_ms=reranker_ms,
            total_ms=total_ms,
        )

        return reranked_results