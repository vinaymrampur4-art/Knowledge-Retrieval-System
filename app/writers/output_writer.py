"""
output_writer.py

Writes every parser output separately.
"""

from dataclasses import asdict
from pathlib import Path

from app.writers.json_writer import JSONWriter


class OutputWriter:

    @classmethod
    def write(
        cls,
        repository_name: str,
        result,
    ):

        output_dir = Path("outputs/json")

        JSONWriter.write(
            output_dir / "classes.json",
            [asdict(c) for c in result.classes],
        )

        JSONWriter.write(
            output_dir / "methods.json",
            [asdict(m) for m in result.methods],
        )

        JSONWriter.write(
            output_dir / "functions.json",
            [asdict(f) for f in result.functions],
        )

        JSONWriter.write(
            output_dir / "imports.json",
            [asdict(i) for i in result.imports],
        )

        JSONWriter.write(
            output_dir / "constants.json",
            [asdict(c) for c in result.constants],
        )

        JSONWriter.write(
            output_dir / "project_summary.json",
            {
                "repository": repository_name,
                "classes": len(result.classes),
                "methods": len(result.methods),
                "functions": len(result.functions),
                "imports": len(result.imports),
                "constants": len(result.constants),
            },
        )
        return output_dir.resolve()