"""
chunk_result.py

Container for all generated semantic chunks.
"""

from dataclasses import dataclass, field

from app.models.parsed_chunk import ParsedChunk


@dataclass
class ChunkResult:

    chunks: list[ParsedChunk] = field(default_factory=list)