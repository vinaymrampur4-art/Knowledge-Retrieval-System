"""
indexer.py

Writes ChromaDocuments into ChromaDB.
"""

from __future__ import annotations

import json

from app.core.logger import logger
from app.vectordb.chroma_client import ChromaClient


class ChromaIndexer:

    def __init__(self):

        self.client = ChromaClient.get_client()

    # ---------------------------------------------------------
    # Metadata Sanitizer
    # ---------------------------------------------------------

    @staticmethod
    def _sanitize_metadata(metadata: dict) -> dict:
        """
        Convert metadata into ChromaDB compatible values.
        """

        cleaned = {}

        for key, value in metadata.items():

            if value is None:

                cleaned[key] = ""

            elif isinstance(
                value,
                (
                    str,
                    int,
                    float,
                    bool,
                ),
            ):

                cleaned[key] = value

            elif isinstance(
                value,
                (
                    list,
                    tuple,
                    set,
                ),
            ):

                cleaned[key] = ",".join(
                    map(str, value)
                )

            elif isinstance(value, dict):

                cleaned[key] = json.dumps(value)

            else:

                cleaned[key] = str(value)

        return cleaned

    # ---------------------------------------------------------
    # Index Documents
    # ---------------------------------------------------------

    def index_documents(
        self,
        documents,
    ):

        collections = {}

        total = len(documents)

        logger.info(
            f"Indexing {total} documents into ChromaDB..."
        )

        for i, document in enumerate(documents, start=1):

            collection_name = document.collection_name

            # ---------------------------------------------
            # Create collection if it doesn't exist
            # ---------------------------------------------

            if collection_name not in collections:

                collections[collection_name] = (

                    self.client.get_or_create_collection(

                        name=collection_name

                    )

                )

            metadata = self._sanitize_metadata(
                document.metadata
            )

            try:

                collections[collection_name].add(

                    ids=[
                        document.id
                    ],

                    documents=[
                        document.document
                    ],

                    embeddings=[
                        document.embedding
                    ],

                    metadatas=[
                        metadata
                    ],
                )

            except Exception:

                logger.exception(
                    f"Failed to index document: {document.id}"
                )

                raise

            if i % 100 == 0 or i == total:

                logger.info(
                    f"Indexed {i}/{total} documents..."
                )

        logger.info(
            f"Successfully indexed {total} documents."
        )