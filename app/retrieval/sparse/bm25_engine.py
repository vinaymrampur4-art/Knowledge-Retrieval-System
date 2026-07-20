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

            print("\n" + "=" * 80)
            print("BM25 ENGINE")
            print("=" * 80)
            print(f"Repository Requested : {repository_name}")

            builder = BM25IndexBuilder()

            serializer = BM25Serializer(
                repository_name
            )

            print(
                f"Serializer Exists    : {serializer.exists()}"
            )

            if serializer.exists():

                print(
                    f"Loading BM25 index for "
                    f"'{repository_name}'..."
                )

                builder = serializer.load(
                    builder
                )

                print("BM25 index loaded successfully.")

            else:

                print(
                    f"WARNING: No BM25 index found "
                    f"for '{repository_name}'."
                )

                print(
                    "Run the indexing pipeline first."
                )

            print("=" * 80 + "\n")

            cls._builders[
                repository_name
            ] = builder

        return cls._builders[
            repository_name
        ]