from dataclasses import dataclass

from app.models.parsed_chunk import ParsedChunk


@dataclass
class Embedding:

    chunk: ParsedChunk

    vector: list[float]