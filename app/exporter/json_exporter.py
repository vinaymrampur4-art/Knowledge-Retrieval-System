"""
json_exporter.py

Exports semantic chunks into JSONL format.
"""

from __future__ import annotations

import json
from pathlib import Path
from dataclasses import asdict

from app.models.chunk_result import ChunkResult


class JSONExporter:

    def export(
        self,
        chunk_result: ChunkResult,
        output_dir: Path,
    ):

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        jsonl_file = output_dir / "chunks.jsonl"

        with open(
            jsonl_file,
            "w",
            encoding="utf-8",
        ) as f:

            for chunk in chunk_result.chunks:

                json.dump(
                    asdict(chunk),
                    f,
                    ensure_ascii=False,
                )

                f.write("\n")