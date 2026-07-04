"""
manifest.py
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

from app.models.chunk_result import ChunkResult


class ManifestBuilder:

    def build(
        self,
        chunk_result: ChunkResult,
        output_dir: Path,
        repository: str,
    ):

        manifest = {

            "repository": repository,

            "created_at": datetime.utcnow().isoformat(),

            "total_chunks": len(
                chunk_result.chunks
            ),

            "format": "jsonl",

            "chunk_file": "chunks.jsonl",

            "version": "1.0",
        }

        with open(
            output_dir / "manifest.json",
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                manifest,
                f,
                indent=4,
            )