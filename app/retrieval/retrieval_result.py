from dataclasses import dataclass, field

from app.retrieval.search_result import SearchResult


@dataclass(slots=True)
class RetrievalResult:

    query: str

    total_results: int

    results: list[SearchResult] = field(default_factory=list)

    retrieval_time: float = 0.0

    embedding_time: float = 0.0

    total_time: float = 0.0

    def to_dict(self) -> dict:

        return {

            "query": self.query,

            "total_results": self.total_results,

            "embedding_time": self.embedding_time,

            "retrieval_time": self.retrieval_time,

            "total_time": self.total_time,

            "results": [
                result.to_dict()
                for result in self.results
            ],
        }