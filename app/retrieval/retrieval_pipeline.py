"""
retrieval_pipeline.py

Coordinates the complete retrieval workflow.
"""

import time

from app.retrieval.query_embedder import QueryEmbedder
from app.retrieval.multi_collection_retriever import (
    MultiCollectionRetriever,
)
from app.retrieval.retrieval_result import RetrievalResult


class RetrievalPipeline:
    """
    Complete semantic retrieval pipeline.
    """

    def __init__(self):

        self.embedder = QueryEmbedder()

        self.retriever = MultiCollectionRetriever()

    # ---------------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> RetrievalResult:

        total_start = time.perf_counter()

        embedding_start = time.perf_counter()

        query_embedding = self.embedder.embed(query)

        embedding_time = (
            time.perf_counter()
            - embedding_start
        )

        results = self.retriever.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        retrieval_time = (
            time.perf_counter()
            - total_start
        )

        return RetrievalResult(

            query=query,

            total_results=len(results),

            results=results,

            retrieval_time=retrieval_time,

            embedding_time=embedding_time,
        )