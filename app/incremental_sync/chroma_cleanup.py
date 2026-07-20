"""
chroma_cleanup.py

Removes stale documents from ChromaDB during
incremental synchronization.
"""

from __future__ import annotations

from app.core.config import (
    FILES_COLLECTION,
    CLASSES_COLLECTION,
    METHODS_COLLECTION,
    FUNCTIONS_COLLECTION,
    CODE_BLOCK_COLLECTION,
)

from app.core.logger import logger

from app.vectordb.chroma_client import ChromaClient


class ChromaCleanupService:
    """
    Removes outdated documents from every ChromaDB
    collection before incremental re-indexing.
    """

    def __init__(self) -> None:

        self.client = ChromaClient.get_client()

        self.collection_names = [
            FILES_COLLECTION,
            CLASSES_COLLECTION,
            METHODS_COLLECTION,
            FUNCTIONS_COLLECTION,
            CODE_BLOCK_COLLECTION,
        ]

    # ==========================================================
    # Collection
    # ==========================================================

    def _get_collection(
        self,
        collection_name: str,
    ):
        """
        Returns an existing Chroma collection.
        """

        return self.client.get_collection(
            name=collection_name,
        )

    # ==========================================================
    # Helpers
    # ==========================================================

    @staticmethod
    def _build_where_clause(
        repository_name: str,
        branch: str,
        file_path: str,
    ) -> dict:
        """
        Builds the Chroma metadata filter.
        """

        return {
            "$and": [
                {
                    "repository_name": repository_name,
                },
                {
                    "branch": branch,
                },
                {
                    "file_path": file_path,
                },
            ]
        }

    @staticmethod
    def _build_repository_where_clause(
        repository_name: str,
        branch: str,
    ) -> dict:
        """
        Builds the Chroma metadata filter for an
        entire repository.
        """

        return {
            "$and": [
                {
                    "repository_name": repository_name,
                },
                {
                    "branch": branch,
                },
            ]
        }

    # ==========================================================
    # Cleanup
    # ==========================================================

    def delete_from_collection(
        self,
        collection_name: str,
        repository_name: str,
        branch: str,
        file_path: str,
    ) -> None:
        """
        Deletes all documents for a file
        from one Chroma collection.
        """

        collection = self._get_collection(
            collection_name
        )

        where = self._build_where_clause(
            repository_name,
            branch,
            file_path,
        )

        logger.info(
            "Cleaning collection %s for %s/%s/%s",
            collection_name,
            repository_name,
            branch,
            file_path,
        )

        try:

            collection.delete(
                where=where,
            )

        except Exception:

            logger.exception(
                "Failed cleaning collection %s",
                collection_name,
            )

            raise

    # ==========================================================
    # Public API
    # ==========================================================

    def delete_file_documents(
        self,
        repository_name: str,
        branch: str,
        file_path: str,
    ) -> None:
        """
        Deletes every document generated from a file
        across all Chroma collections.
        """

        logger.info(
            "Starting Chroma cleanup for %s/%s/%s",
            repository_name,
            branch,
            file_path,
        )

        for collection_name in self.collection_names:

            self.delete_from_collection(
                collection_name=collection_name,
                repository_name=repository_name,
                branch=branch,
                file_path=file_path,
            )

        logger.info(
            "Finished Chroma cleanup for %s/%s/%s",
            repository_name,
            branch,
            file_path,
        )

    # ==========================================================
    # Batch Cleanup
    # ==========================================================

    def delete_multiple_files(
        self,
        repository_name: str,
        branch: str,
        file_paths: list[str],
    ) -> None:
        """
        Deletes documents belonging to multiple files.
        """

        if not file_paths:

            logger.info(
                "No files supplied for cleanup."
            )

            return

        logger.info(
            "Cleaning %d files from ChromaDB.",
            len(file_paths),
        )

        for file_path in file_paths:

            self.delete_file_documents(
                repository_name=repository_name,
                branch=branch,
                file_path=file_path,
            )

        logger.info(
            "Batch cleanup completed."
        )

    # ==========================================================
    # Repository Cleanup
    # ==========================================================

    def delete_repository_documents(
        self,
        repository_name: str,
        branch: str,
    ) -> None:
        """
        Deletes every document belonging to a repository
        across all Chroma collections.
        """

        logger.info(
            "Starting repository cleanup for %s/%s",
            repository_name,
            branch,
        )

        where = self._build_repository_where_clause(
            repository_name,
            branch,
        )

        for collection_name in self.collection_names:

            logger.info(
                "Cleaning collection %s",
                collection_name,
            )

            collection = self._get_collection(
                collection_name
            )

            try:

                collection.delete(
                    where=where,
                )

            except Exception:

                logger.exception(
                    "Failed cleaning collection %s",
                    collection_name,
                )

                raise

        logger.info(
            "Repository cleanup completed."
        )