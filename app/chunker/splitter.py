"""
splitter.py

Splits oversized semantic chunks into embedding-sized chunks.
"""

from __future__ import annotations

from copy import deepcopy

from app.models.chunk_result import ChunkResult
from app.models.parsed_chunk import ParsedChunk

from app.chunker.chunk_utils import (
    split_large_chunk,
    estimate_tokens,
)

from app.core.config import (
    CHUNK_MAX_TOKENS,
)

class ChunkSplitter:

    def __init__(
        self,
        max_tokens: int = CHUNK_MAX_TOKENS,
    ):
        self.max_tokens = max_tokens

    def split(
        self,
        chunk_result: ChunkResult,
    ) -> ChunkResult:

        output = ChunkResult()

        for chunk in chunk_result.chunks:

            if chunk.token_count <= self.max_tokens:

                output.chunks.append(chunk)

                continue

            parts = split_large_chunk(
                chunk.content,
                self.max_tokens,
            )

            for index, content in enumerate(parts):

                new_chunk = deepcopy(chunk)

                new_chunk.chunk_id = (
                    f"{chunk.chunk_id}_{index+1}"
                )

                new_chunk.title = (
                    f"{chunk.title} (Part {index+1})"
                )

                new_chunk.content = content

                new_chunk.token_count = estimate_tokens(
                    content
                )

                new_chunk.metadata["part"] = index + 1
                new_chunk.metadata["total_parts"] = len(parts)

                output.chunks.append(new_chunk)

        return output