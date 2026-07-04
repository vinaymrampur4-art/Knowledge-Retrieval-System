from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SearchResult:

    id: str

    score: float

    content: str

    collection: str

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:

        return {
            "id": self.id,
            "score": self.score,
            "content": self.content,
            "collection": self.collection,
            "metadata": self.metadata,
        }