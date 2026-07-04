"""
index_stats_service.py

Provides statistics about the indexed repository.
"""

from pathlib import Path

from app.core.config import (
    REPOSITORY_NAME,
    EMBEDDING_MODEL,
    BM25_INDEX_FILE,
    FILES_COLLECTION,
    CLASSES_COLLECTION,
    METHODS_COLLECTION,
    FUNCTIONS_COLLECTION,
    CODE_BLOCK_COLLECTION,
)

from app.vectordb.chroma_client import ChromaClient

from mcp_server.models import (
    IndexStatsResponse,
)


class IndexStatsService:
    """
    Reads indexing statistics directly from ChromaDB and BM25.
    """

    def __init__(self):

        self.client = ChromaClient.get_client()

    # ---------------------------------------------------------
    # Collection Count
    # ---------------------------------------------------------

    def _count_collection(
        self,
        collection_name: str,
    ) -> int:

        try:

            collection = self.client.get_collection(
                name=collection_name,
            )

            return collection.count()

        except Exception:

            return 0

    # ---------------------------------------------------------
    # Embedding Dimension
    # ---------------------------------------------------------

    def _embedding_dimension(self) -> int:

        collections = [

            FILES_COLLECTION,

            CLASSES_COLLECTION,

            METHODS_COLLECTION,

            FUNCTIONS_COLLECTION,

            CODE_BLOCK_COLLECTION,

        ]

        for name in collections:

            try:

                collection = self.client.get_collection(name=name)

                result = collection.peek(limit=1)

                embeddings = result.get("embeddings")

                if embeddings:

                    return len(embeddings[0])

            except Exception:

                pass

        return 0

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def get_stats(
        self,
    ) -> IndexStatsResponse:

        files = self._count_collection(
            FILES_COLLECTION,
        )

        classes = self._count_collection(
            CLASSES_COLLECTION,
        )

        methods = self._count_collection(
            METHODS_COLLECTION,
        )

        functions = self._count_collection(
            FUNCTIONS_COLLECTION,
        )

        code_blocks = self._count_collection(
            CODE_BLOCK_COLLECTION,
        )

        total_documents = (

            files

            + classes

            + methods

            + functions

            + code_blocks

        )

        embedding_dimension = (
            self._embedding_dimension()
        )

        return IndexStatsResponse(

            repository=REPOSITORY_NAME,

            files=files,

            classes=classes,

            methods=methods,

            functions=functions,

            code_blocks=code_blocks,

            total_documents=total_documents,

            embedding_model=EMBEDDING_MODEL,

            embedding_dimension=embedding_dimension,

            bm25_ready=Path(BM25_INDEX_FILE).exists(),

            chroma_ready=True,

        )