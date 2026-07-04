from dataclasses import dataclass, field

from app.models.embedding import Embedding


@dataclass
class EmbeddingResult:

    embeddings: list[Embedding] = field(default_factory=list)