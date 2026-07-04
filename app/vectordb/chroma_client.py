"""
Singleton ChromaDB client.
"""

import chromadb

from app.core.config import CHROMA_DB_PATH


class ChromaClient:

    _client = None

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = chromadb.PersistentClient(
                path=str(CHROMA_DB_PATH)
            )

        return cls._client