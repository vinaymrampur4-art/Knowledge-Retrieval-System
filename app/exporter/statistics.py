"""
statistics.py
"""

from __future__ import annotations

import json
from pathlib import Path

from app.models.chunk_result import ChunkResult


class StatisticsBuilder:

    def build(
        self,
        chunk_result: ChunkResult,
        output_dir: Path,
    ):

        stats = {

            "repository": "fastapi-master",

            "total_chunks": len(chunk_result.chunks),

            "classes": 0,

            "methods": 0,

            "functions": 0,

            "imports": 0,

            "constants": 0,

            "total_tokens": 0,

            "average_tokens_per_chunk": 0,

            "largest_chunk": 0,

            "smallest_chunk": 999999,

        }

        for chunk in chunk_result.chunks:

            if chunk.chunk_type == "class":
                stats["classes"] += 1

            elif chunk.chunk_type == "method":
                stats["methods"] += 1

            elif chunk.chunk_type == "function":
                stats["functions"] += 1

            elif chunk.chunk_type == "import":
                stats["imports"] += 1

            elif chunk.chunk_type == "constant":
                stats["constants"] += 1

            stats["total_tokens"] += (
                chunk.token_count
            )

            stats["largest_chunk"] = max(
                stats["largest_chunk"],
                chunk.token_count,
            )

            stats["smallest_chunk"] = min(
                stats["smallest_chunk"],
                chunk.token_count,
            )

            stats["average_tokens_per_chunk"] = round(
                stats["total_tokens"] /
                len(chunk_result.chunks),
                2,
            )

        with open(
            output_dir / "statistics.json",
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                stats,
                f,
                indent=4,
            )