"""
sync_manager.py

Orchestrates repository synchronization.

This class decides whether to execute a full indexing
run or an incremental synchronization.
"""

from __future__ import annotations

from app.incremental_sync.git_service import GitService
from app.incremental_sync.incremental_sync_service import (
    IncrementalSyncService,
)
from app.incremental_sync.sync_models import (
    ChangedFiles,
)

from app.parser.repository_parser import (
    RepositoryParser,
)

from app.indexing.index_pipeline import (
    IndexPipeline,
)

from app.core.config import (
    REPOSITORIES_DIR,
)

from app.core.logger import logger


class SyncManager:
    """
    Coordinates repository synchronization.

    Workflow
    --------
    First Synchronization

        RepositoryParser.parse()

                ↓

        IndexPipeline.run()

                ↓

        Save Sync State

    Incremental Synchronization

        IncrementalSyncService.sync()
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
            repository_name=repository_name,
        )

    # ==========================================================
    # Sync State
    # ==========================================================

    def is_first_sync(
        self,
    ) -> bool:
        """
        Returns True if the repository has never
        been synchronized.
        """

        return not self.git_service.sync_file_exists()

    def get_last_synced_commit(
        self,
    ) -> str | None:
        """
        Returns the last synchronized commit.
        """

        state = self.git_service.load_sync_state()

        if state is None:
            return None

        return state.last_commit

    # ==========================================================
    # Changed Files
    # ==========================================================

    def get_changed_files(
        self,
    ) -> ChangedFiles:
        """
        Returns files changed since the previous
        synchronization.
        """

        if self.is_first_sync():
            return ChangedFiles()

        last_commit = self.get_last_synced_commit()

        if last_commit is None:
            return ChangedFiles()

        return self.git_service.get_changed_files(
            last_commit
        )

    # ==========================================================
    # Full Indexing
    # ==========================================================

    def _run_full_indexing(
        self,
    ) -> None:
        """
        Executes the initial full indexing pipeline.
        """

        logger.info(
            "Starting full repository indexing..."
        )

        parser = RepositoryParser()

        parser_result = parser.parse(
            self.repository_path
        )

        pipeline = IndexPipeline(
            self.repository_name
        )

        pipeline.run(
            parser_result
        )

        self.save_sync_state()

        logger.info(
            "Full indexing completed."
        )

    # ==========================================================
    # Incremental Sync
    # ==========================================================

    def _run_incremental_sync(
        self,
    ) -> None:
        """
        Executes incremental synchronization.
        """

        logger.info(
            "Starting incremental synchronization..."
        )

        service = IncrementalSyncService(
            self.repository_name
        )

        service.sync()

        logger.info(
            "Incremental synchronization completed."
        )

    # ==========================================================
    # Public API
    # ==========================================================

    def sync(
        self,
    ) -> None:
        """
        Synchronizes the repository.

        First execution
        ----------------
        Performs a complete repository indexing.

        Subsequent executions
        ---------------------
        Performs an incremental synchronization.
        """

        if self.is_first_sync():

            logger.info(
                "First synchronization detected."
            )

            self._run_full_indexing()

            return

        logger.info(
            "Existing synchronization detected."
        )

        self._run_incremental_sync()

    # ==========================================================
    # Sync State
    # ==========================================================

    def save_sync_state(
        self,
    ) -> None:
        """
        Saves the latest synchronization state.
        """

        self.git_service.save_latest_sync_state()