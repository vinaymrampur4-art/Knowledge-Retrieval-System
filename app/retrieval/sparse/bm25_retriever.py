"""
bm25_retriever.py

Performs keyword retrieval using the BM25 index.
"""

from app.retrieval.search_result import SearchResult
from app.retrieval.sparse.bm25_engine import BM25Engine


from app.retrieval.base_retriever import BaseRetriever


class BM25Retriever(BaseRetriever):

    def __init__(self):

        builder = BM25Engine.get_builder()

        self.index = builder.index

        self.store = builder.get_store()

    # ---------------------------------------------------------

    def search(
        self,
        query: str,
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

        return results