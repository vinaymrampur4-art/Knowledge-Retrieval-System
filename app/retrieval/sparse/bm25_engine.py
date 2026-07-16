"""
Global BM25 engine.

Loads serialized BM25 indexes per repository.
"""

from app.retrieval.sparse.bm25_index_builder import (
    BM25IndexBuilder,
)

from app.retrieval.sparse.bm25_serializer import (
    BM25Serializer,
)


class BM25Engine:

    _builders = {}

    @classmethod
    def get_builder(
        cls,
        repository_name: str,
    ):

        if repository_name not in cls._builders:

            builder = BM25IndexBuilder()

            serializer = BM25Serializer(
                repository_name
            )

            if serializer.exists():

                print(
                    f"Loading BM25 index for "
                    f"{repository_name}..."
                )

                builder = serializer.load(
                    builder
                )

            else:

                print(
                    f"WARNING: No BM25 index found for "
                    f"{repository_name}\n"
                    f"Run indexing first."
                )

            cls._builders[
                repository_name
            ] = builder

        return cls._builders[
            repository_name
        ]