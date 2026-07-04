from dataclasses import dataclass, field


@dataclass
class ParsedChunk:

    chunk_id: str

    chunk_type: str

    title: str

    content: str

    metadata: dict = field(default_factory=dict)

    parent_id: str | None = None

    children: list[str] = field(default_factory=list)

    depth: int = 0

    token_count: int = 0