"""
index_pipeline.py

Complete indexing pipeline.

This pipeline is responsible for:

1. Building searchable documents.
2. Building a fresh BM25 index.
3. Saving the BM25 index to disk.
4. Generating dense embeddings.
5. Writing documents into ChromaDB.

This should only be run when the repository changes.
"""

from app.indexing.document_factory import (
    ParserDocumentFactory,
)

from app.indexing.embedding_generator import (
    DocumentEmbeddingGenerator,
)

from app.models.parser_result import (
    ParserResult,
)

from app.vectordb.indexer import (
    ChromaIndexer,
)

from app.retrieval.sparse.bm25_index_builder import (
    BM25IndexBuilder,
)

from app.retrieval.sparse.bm25_serializer import (
    BM25Serializer,
)


class IndexPipeline:
    """
    Handles full and incremental indexing operations.
    """

    def __init__(
        self,
        repository_name: str,
    ) -> None:

        self.repository_name = repository_name

        self.embedder = (
            DocumentEmbeddingGenerator()
        )

        self.indexer = (
            ChromaIndexer()
        )

        self.bm25_builder = (
            BM25IndexBuilder()
        )

        self.serializer = (
            BM25Serializer(
                repository_name
            )
        )

    # ---------------------------------------------------------
    # Full Indexing Pipeline
    # ---------------------------------------------------------

    def run(
        self,
        parser_result: ParserResult,
    ) -> None:
        """
        Executes the complete indexing pipeline.

        Steps
        -----
        1. Build searchable documents.
        2. Build BM25 index.
        3. Save BM25 index.
        4. Generate dense embeddings.
        5. Index documents into ChromaDB.
        """

        documents = self._build_documents(
            parser_result
        )

        self._build_bm25(
            documents
        )

        self._save_bm25()

        documents = self._generate_embeddings(
            documents
        )

        self._index_documents(
            documents
        )

    # ---------------------------------------------------------
    # Incremental Indexing Pipeline
    # ---------------------------------------------------------

    def run_incremental(
        self,
        parser_result: ParserResult,
    ) -> None:
        """
        Executes the incremental indexing pipeline.

        Unlike ``run()``, this method does not rebuild
        the BM25 index.

        Steps
        -----
        1. Build searchable documents.
        2. Generate embeddings.
        3. Update ChromaDB.
        """

        documents = self._build_documents(
            parser_result
        )

        documents = self._generate_embeddings(
            documents
        )

        self._index_documents(
            documents
        )

    # ---------------------------------------------------------
    # Rebuild BM25
    # ---------------------------------------------------------

    def rebuild_bm25(
        self,
        parser_result: ParserResult,
    ) -> None:
        """
        Rebuilds the complete BM25 index from the
        entire repository without generating embeddings
        or updating ChromaDB.
        """

        documents = self._build_documents(
            parser_result
        )

        self._build_bm25(
            documents
        )

        self._save_bm25()

    # ---------------------------------------------------------
    # Build Documents
    # ---------------------------------------------------------

    def _build_documents(
        self,
        parser_result: ParserResult,
    ):
        """
        Builds searchable documents from the parser output.
        """

        print("Building documents...")

        documents = ParserDocumentFactory.build(
            parser_result
        )

        print(
            f"Documents: {len(documents)}"
        )

        return documents

    # ---------------------------------------------------------
    # Build BM25
    # ---------------------------------------------------------

    def _build_bm25(
        self,
        documents,
    ) -> None:
        """
        Builds a fresh BM25 index.
        """

        print("Building BM25 index...")

        bm25_documents = []

        for document in documents:

            bm25_documents.append(
                {
                    "id": document.id,
                    "content": document.document,
                    "metadata": document.metadata,
                }
            )

        self.bm25_builder.build(
            bm25_documents
        )

    # ---------------------------------------------------------
    # Save BM25
    # ---------------------------------------------------------

    def _save_bm25(
        self,
    ) -> None:
        """
        Saves the BM25 index to disk.
        """

        print("Saving BM25 index...")

        self.serializer.save(
            self.bm25_builder
        )

        print("BM25 Saved.")
        print("BM25 Ready.")

    # ---------------------------------------------------------
    # Generate Embeddings
    # ---------------------------------------------------------

    def _generate_embeddings(
        self,
        documents,
    ):
        """
        Generates dense embeddings for searchable documents.
        """

        print("Generating embeddings...")

        return self.embedder.generate(
            documents
        )

    # ---------------------------------------------------------
    # Index Documents
    # ---------------------------------------------------------

    def _index_documents(
        self,
        documents,
    ) -> None:
        """
        Writes embedded documents into ChromaDB.
        """

        print("Writing to ChromaDB...")

        self.indexer.index_documents(
            documents
        )

        print("Done.")