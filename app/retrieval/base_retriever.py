"""
Base retriever interface.
"""

from abc import ABC, abstractmethod

from app.retrieval.search_result import SearchResult


class BaseRetriever(ABC):

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[SearchResult]:
        """
        Execute retrieval.
        """
        pass