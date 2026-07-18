"""
sync_manager.py

Orchestrates the Incremental Sync workflow.
"""

from __future__ import annotations

from app.incremental_sync.git_service import GitService
from app.incremental_sync.sync_models import (
    ChangedFiles,
)


class SyncManager:
    """
    Coordinates the Incremental Sync process.

    This class decides whether a full indexing run
    or an incremental synchronization is required.
    """

    def __init__(
        self,
        repository_name: str,
    ) -> None:

        self.repository_name = repository_name

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
        Returns True if this repository has never
        been synchronized before.
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
    # Incremental Sync
    # ==========================================================

    def get_changed_files(
        self,
    ) -> ChangedFiles:
        """
        Returns all changed files.

        If this is the first synchronization,
        an empty ChangedFiles object is returned.
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
    # Sync State Update
    # ==========================================================

    def save_sync_state(
        self,
    ) -> None:
        """
        Saves the latest synchronization state.
        """

        self.git_service.save_latest_sync_state()