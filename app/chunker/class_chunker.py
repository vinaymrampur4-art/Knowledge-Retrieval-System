"""
class_chunker.py

Converts parsed classes into semantic chunks.
"""

from app.builders.chunk_builder import ChunkBuilder


class ClassChunker:

    def build_chunks(
        self,
        classes,
    ):

        chunks = []

        for cls in classes:

            method_names = [
                method.method_name
                for method in cls.methods
            ]

            inherits = ", ".join(cls.inherits)

            description = (
                f"Class {cls.class_name}.\n"
                f"Inherits From: {inherits if inherits else 'None'}.\n\n"
                f"Docstring:\n"
                f"{cls.class_docstring or 'No documentation.'}\n\n"
                f"Methods:\n"
                + (
                    "\n".join(method_names)
                    if method_names
                    else "No methods."
                )
            )

            metadata = {

                "file": cls.file,

                "repo_path": cls.repo_path,

                "github_url": cls.github_url,

                "start_line": cls.start_line,

                "end_line": cls.end_line,

                "inherits": cls.inherits,

                "method_count": len(cls.methods),
            }

            chunk = ChunkBuilder.build(

                chunk_id=f"class::{cls.class_name}",

                chunk_type="class",

                title=cls.class_name,

                content=description,

                metadata=metadata,
            )

            chunks.append(chunk)

        return chunks