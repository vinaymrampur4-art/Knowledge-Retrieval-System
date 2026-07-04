"""
json_writer.py

Writes parser outputs into separate JSON files.
"""

import json
from dataclasses import asdict
from pathlib import Path


class JSONWriter:

    @staticmethod
    def write(path: Path, data):

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )