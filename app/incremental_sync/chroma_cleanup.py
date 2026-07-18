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

    Documents are identified using metadata instead
    of document id prefixes.
    """

    def __init__(
        self,
    ) -> None:

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
        Returns a Chroma collection.
        """

        return self.client.get_or_create_collection(
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
        Builds the metadata filter used for cleanup.
        """

        return {

            "repository_name":
                repository_name,

            "branch":
                branch,

            "file_path":
                file_path,

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
        Deletes every document belonging to a file
        from a single Chroma collection.
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

            f"Cleaning collection "

            f"{collection_name} "

            f"for "

            f"{repository_name}/"

            f"{branch}/"

            f"{file_path}"

        )

        try:

            collection.delete(

                where=where,

            )

        except Exception:

            logger.exception(

                f"Failed cleaning "

                f"{collection_name}"

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
        Deletes every document generated from the given
        source file across every Chroma collection.

        Parameters
        ----------
        repository_name:
            Repository containing the file.

        branch:
            Repository branch.

        file_path:
            Repository-relative path of the file.
        """

        logger.info(
            f"Starting Chroma cleanup for "
            f"{repository_name}/{branch}/{file_path}"
        )

        for collection_name in self.collection_names:

            self.delete_from_collection(
                collection_name=collection_name,
                repository_name=repository_name,
                branch=branch,
                file_path=file_path,
            )

        logger.info(
            f"Finished Chroma cleanup for "
            f"{repository_name}/{branch}/{file_path}"
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

        Parameters
        ----------
        repository_name:
            Repository containing the files.

        branch:
            Repository branch.

        file_paths:
            Repository-relative file paths.
        """

        if not file_paths:

            logger.info(
                "No files supplied for cleanup."
            )

            return

        logger.info(
            f"Cleaning {len(file_paths)} files "
            f"from ChromaDB."
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