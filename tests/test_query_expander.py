"""
retrieval_pipeline.py

Coordinates the complete semantic retrieval workflow.

Flow
----
User Query
    ↓
Query Expansion
    ↓
Embedding Generation
    ↓
Multi-Collection Retrieval
    ↓
Build RetrievalResult
"""

from time import perf_counter

from app.retrieval.query_embedder import QueryEmbedder
from app.retrieval.query_expander import QueryExpander
from app.retrieval.multi_collection_retriever import MultiCollectionRetriever
from app.retrieval.retrieval_result import RetrievalResult


class RetrievalPipeline:
    """
    Complete semantic retrieval pipeline.

    Responsibilities
    ----------------
    1. Expand the user query.
    2. Generate the query embedding.
    3. Search every collection.
    4. Build a RetrievalResult.
    """

    def __init__(self):

        self.expander = QueryExpander()

        self.embedder = QueryEmbedder()

        self.retriever = MultiCollectionRetriever()

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> RetrievalResult:
        """
        Execute a semantic search.

        Parameters
        ----------
        query : str
            User query.

        top_k : int
            Maximum number of results.

        Returns
        -------
        RetrievalResult
        """

        total_start = perf_counter()

        # -----------------------------------------------------
        # Expand Query
        # -----------------------------------------------------

        expanded_query = self.expander.expand(query)

        # -----------------------------------------------------
        # Generate Embedding
        # -----------------------------------------------------

        embedding_start = perf_counter()

        query_embedding = self.embedder.embed(
            expanded_query
        )

        embedding_time = (
            perf_counter()
            - embedding_start
        )

        # -----------------------------------------------------
        # Retrieve
        # -----------------------------------------------------

        retrieval_start = perf_counter()

        search_results = self.retriever.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        retrieval_time = (
            perf_counter()
            - retrieval_start
        )

        total_time = (
            perf_counter()
            - total_start
        )

        # -----------------------------------------------------
        # Build RetrievalResult
        # -----------------------------------------------------

        return RetrievalResult(

            query=query,

            total_results=len(search_results),

            results=search_results,

            retrieval_time=retrieval_time,

            embedding_time=embedding_time,

            total_time=total_time,
        )