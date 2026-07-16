"""
bm25_retriever.py

Performs keyword retrieval using the BM25 index.
"""

from app.retrieval.search_result import SearchResult
from app.retrieval.sparse.bm25_engine import BM25Engine


from app.retrieval.base_retriever import BaseRetriever

from app.retrieval.filters.filter_builder import FilterBuilder
from mcp_server.models import SearchFilter


class BM25Retriever(BaseRetriever):

    def __init__(
        self,
        repository_name: str,
    ):

        builder = BM25Engine.get_builder(
            repository_name
        )

        self.index = builder.index

        self.store = builder.get_store()

    # ---------------------------------------------------------

    def search(
        self,
        query: str,
        filter: SearchFilter | None = None,
        top_k: int = 10,
    ) -> list[SearchResult]:

        ranked = self.index.search(
            query=query,
            top_k=top_k,
        )

        documents = self.store.get_documents()

        results = []

        for document_index, score in ranked:

            document = documents[document_index]

            results.append(

                SearchResult(

                    id=document.id,

                    score=float(score),

                    content=document.content,

                    collection="BM25",

                    metadata=document.metadata,

                )

            )

            print("=" * 80)
            print("BM25 FILTER")
            print(type(filter))
            print(filter)
            print("=" * 80)

        results = FilterBuilder.filter_results(
            results,
            filter,
        )

        return results