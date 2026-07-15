"""
chunk_utils.py

Utility functions for the AST-aware Chunking Engine.

These helpers provide:
- Stable chunk ID generation
- Code cleanup
- Token estimation
- Small chunk merging helpers
- Large chunk splitting helpers
"""

from __future__ import annotations

from app.core.config import (
    CHUNK_MAX_TOKENS,
)

import hashlib
import re




def generate_chunk_id(
    file_path: str,
    chunk_type: str,
    name: str,
    start_line: int,
    end_line: int,
) -> str:
    """
    Generate a deterministic unique ID for a chunk.

    Example:
        class-fastapi/app.py-FastAPI-42-96
    """

    raw = f"{file_path}:{chunk_type}:{name}:{start_line}:{end_line}"

    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def estimate_tokens(text: str) -> int:
    """
    Rough token estimation.

    GPT models average:
        1 token ≈ 4 characters
    """

    if not text:
        return 0

    return max(1, len(text) // 4)


def clean_code(code: str) -> str:
    """
    Normalize whitespace while preserving indentation.
    """

    if not code:
        return ""

    code = code.rstrip()

    code = re.sub(r"\n{3,}", "\n\n", code)

    return code


def split_large_chunk(
    code: str,
    max_tokens: int = CHUNK_MAX_TOKENS,
) -> list[str]:
    """
    Split overly large chunks into smaller pieces.

    Initial implementation:
    split by lines.

    Later we can improve using AST boundaries.
    """

    if estimate_tokens(code) <= max_tokens:
        return [code]

    lines = code.splitlines()

    pieces = []

    current = []

    current_tokens = 0

    for line in lines:

        current.append(line)

        current_tokens += estimate_tokens(line)

        if current_tokens >= max_tokens:

            pieces.append("\n".join(current))

            current = []

            current_tokens = 0

    if current:
        pieces.append("\n".join(current))

    return pieces


def merge_small_chunks(
    chunks: list[str],
    min_tokens: int = 80,
) -> list[str]:
    """
    Merge tiny neighbouring chunks.

    Useful after splitting.
    """

    if not chunks:
        return []

    merged = []

    buffer = ""

    for chunk in chunks:

        if estimate_tokens(buffer) < min_tokens:
            buffer += "\n" + chunk
        else:
            merged.append(buffer.strip())
            buffer = chunk

    if buffer:
        merged.append(buffer.strip())

    return merged