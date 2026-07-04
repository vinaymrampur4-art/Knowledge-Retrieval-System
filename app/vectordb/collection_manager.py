"""
Creates and manages Chroma collections.
"""

from app.vectordb.chroma_client import ChromaClient

from app.core.config import (
    FILES_COLLECTION,
    CLASSES_COLLECTION,
    METHODS_COLLECTION,
    FUNCTIONS_COLLECTION,
    CODE_BLOCK_COLLECTION,
)


class CollectionManager:

    def __init__(self):

        self.client = ChromaClient.get_client()

    def create_collections(self):

        self.client.get_or_create_collection(
            FILES_COLLECTION
        )

        self.client.get_or_create_collection(
            CLASSES_COLLECTION
        )

        self.client.get_or_create_collection(
            METHODS_COLLECTION
        )

        self.client.get_or_create_collection(
            FUNCTIONS_COLLECTION
        )

        self.client.get_or_create_collection(
            CODE_BLOCK_COLLECTION
        )

        print("Collections created.")