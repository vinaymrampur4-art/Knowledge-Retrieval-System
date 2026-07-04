"""
embedding_model.py

Represents one embedded code chunk.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class EmbeddedChunk:
    """
    A code chunk together with its embedding vector.
    """

    # ---------------------------------------------------------
    # Identification
    # ---------------------------------------------------------

    id: str

    # ---------------------------------------------------------
    # Chunk information
    # ---------------------------------------------------------

    name: str

    chunk_type: str

    file_path: str

    repository: str

    start_line: int

    end_line: int

    # ---------------------------------------------------------
    # Original code
    # ---------------------------------------------------------

    content: str

    # ---------------------------------------------------------
    # Vector
    # ---------------------------------------------------------

    embedding: List[float] = field(default_factory=list)