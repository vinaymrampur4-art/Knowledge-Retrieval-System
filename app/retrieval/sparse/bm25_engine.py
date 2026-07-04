"""
Global BM25 engine.

Loads the serialized BM25 index if it exists.
"""

from app.retrieval.sparse.bm25_index_builder import BM25IndexBuilder
from app.retrieval.sparse.bm25_serializer import BM25Serializer


class BM25Engine:

    _builder = None

    @classmethod
    def get_builder(cls):

        if cls._builder is None:

            builder = BM25IndexBuilder()

            serializer = BM25Serializer()

            if serializer.exists():

                print("Loading BM25 index...")

                builder = serializer.load(builder)

            else:

                print(
                    "WARNING: No BM25 index found.\n"
                    "Run:\n"
                    "python -m tests.test_index_pipeline"
                )

            cls._builder = builder

        return cls._builder