"""
incremental_sync_service.py

Executes the complete Incremental Sync workflow.

Workflow
--------
1. Detect changed files.
2. Delete stale documents from Chroma.
3. Parse only added/modified files.
4. Incrementally update ChromaDB.
5. Rebuild the BM25 index.
6. Save the latest synchronization state.
"""

from __future__ import annotations

from app.core.config import (
    REPOSITORIES_DIR,
)

from app.core.logger import (
    logger,
)

from app.incremental_sync.git_service import (
    GitService,
)

from app.incremental_sync.chroma_cleanup import (
    ChromaCleanupService,
)

from app.models import parser_result
from app.parser.repository_parser import (
    RepositoryParser,
)

from app.indexing.index_pipeline import (
    IndexPipeline,
)


class IncrementalSyncService:
    """
    Executes an incremental synchronization for a repository.
    """

    def __init__(
        self,
        repository_name: str,
    ) -> None:

        self.repository_name = repository_name

        self.repository_path = (
            REPOSITORIES_DIR /
            repository_name
        )

        self.git_service = GitService(
            repository_name
        )

        self.cleanup = ChromaCleanupService()

        self.parser = RepositoryParser()

        self.pipeline = IndexPipeline(
            repository_name
        )

    # ==========================================================
    # Public API
    # ==========================================================

    def sync(
        self,
    ) -> None:
        """
        Executes one incremental synchronization.
        """

        last_commit = (
            self.git_service.get_last_synced_commit()
        )

        if last_commit is None:

            raise RuntimeError(
                "Repository has never been indexed. "
                "Run a full indexing first."
            )

        changes = self.git_service.get_changed_files(
            last_commit
        )

        #
        # Nothing changed.
        #

        if (
            not changes.added
            and
            not changes.modified
            and
            not changes.deleted
        ):

            logger.info(
                "No repository changes detected."
            )

            return

        logger.info(
            "Added: %d | Modified: %d | Deleted: %d",
            len(changes.added),
            len(changes.modified),
            len(changes.deleted),
        )

        #
        # Remove deleted files.
        #

        self._cleanup_deleted_files(
            changes.deleted
        )

        #
        # Process added / modified files.
        #

        self._process_changed_files(
            changes.added +
            changes.modified
        )

        #
        # Rebuild BM25 from the complete repository.
        #

        logger.info(
            "Rebuilding BM25 index..."
        )

        full_parser_result = self.parser.parse(
            self.repository_path
        )

        self.pipeline.rebuild_bm25(
            full_parser_result
        )

        #
        # Save latest synchronization state.
        #

        self.git_service.save_latest_sync_state()

        logger.info(
            "Incremental synchronization completed."
        )

    # ==========================================================
    # Deleted Files
    # ==========================================================

    def _cleanup_deleted_files(
        self,
        deleted_files: list[str],
    ) -> None:
        """
        Removes deleted files from ChromaDB.
        """

        if not deleted_files:
            return

        branch = (
            self.git_service.get_current_branch()
        )

        self.cleanup.delete_multiple_files(
            repository_name=self.repository_name,
            branch=branch,
            file_paths=deleted_files,
        )

    # ==========================================================
    # Added / Modified Files
    # ==========================================================

    def _process_changed_files(
        self,
        changed_files: list[str],
    ) -> None:
        """
        Updates ChromaDB for added and modified files.
        """

        if not changed_files:
            return

        branch = (
            self.git_service.get_current_branch()
        )

        #
        # Remove stale documents.
        #

        self.cleanup.delete_multiple_files(
            repository_name=self.repository_name,
            branch=branch,
            file_paths=changed_files,
        )

        #
        # Parse changed files.
        #

        parser_result = self.parser.parse_files(
            repository_root=self.repository_path,
            file_paths=changed_files,
        )

        parser_result = self.parser.parse_files(
        repository_root=self.repository_path,
        file_paths=changed_files,
)

        

        #
        # Update Chroma incrementally.
        #

        self.pipeline.run_incremental(
            parser_result
        )