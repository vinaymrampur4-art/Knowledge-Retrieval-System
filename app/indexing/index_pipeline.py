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

    def __init__(
        self,
        repository_name: str,
    ):

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
    # Run Pipeline
    # ---------------------------------------------------------

    def run(
        self,
        parser_result,
    ):

        # -----------------------------------------------------
        # Build Documents
        # -----------------------------------------------------

        print("Building documents...")

        documents = (
            ParserDocumentFactory.build(
                parser_result
            )
        )

        print(
            f"Documents: {len(documents)}"
        )

        # -----------------------------------------------------
        # Build BM25
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Save BM25
        # -----------------------------------------------------

        print("Saving BM25 index...")

        self.serializer.save(
            self.bm25_builder
        )

        print("BM25 Saved.")
        print("BM25 Ready.")

        # -----------------------------------------------------
        # Generate Embeddings
        # -----------------------------------------------------

        print("Generating embeddings...")

        documents = (
            self.embedder.generate(
                documents
            )
        )

        # -----------------------------------------------------
        # Write to ChromaDB
        # -----------------------------------------------------

        print("Writing to ChromaDB...")

        self.indexer.index_documents(
            documents
        )

        print("Done.")