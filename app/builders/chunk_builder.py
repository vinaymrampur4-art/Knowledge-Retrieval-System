"""
chunk_builder.py

Builder responsible for creating ParsedChunk objects.
"""

from app.builders.base_builder import BaseBuilder
from app.models.parsed_chunk import ParsedChunk


class ChunkBuilder(BaseBuilder):

    @classmethod
    def build(
        cls,
        *,
        chunk_id: str,
        chunk_type: str,
        title: str,
        content: str,
        metadata: dict | None = None,
    ) -> ParsedChunk:

        if not chunk_id:
            raise ValueError("Chunk id cannot be empty.")

        if not chunk_type:
            raise ValueError("Chunk type cannot be empty.")

        if not title:
            raise ValueError("Chunk title cannot be empty.")

        return ParsedChunk(
            chunk_id=chunk_id,
            chunk_type=chunk_type,
            title=title,
            content=content,
            metadata=metadata or {},
        )