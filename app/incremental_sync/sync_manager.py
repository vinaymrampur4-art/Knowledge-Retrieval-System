"""
sync_manager.py

Coordinates repository synchronization.
"""

from __future__ import annotations

from app.incremental_sync.git_service import GitService
from app.incremental_sync.sync_mode import SyncMode
from app.incremental_sync.full_sync_service import FullSyncService
from app.incremental_sync.incremental_sync_service import (
    IncrementalSyncService,
)

from app.core.logger import logger


class SyncManager:
    """
    Coordinates repository synchronization.

    Supported modes
    ---------------

    FULL
        Rebuilds the complete repository index.

    INCREMENTAL
        Updates only changed files.
    """

    def __init__(
        self,
        repository_name: str,
    ) -> None:

        self.repository_name = repository_name

        self.git_service = GitService(
            repository_name,
        )

        self.full_sync = FullSyncService(
            repository_name,
        )

        self.incremental_sync = (
            IncrementalSyncService(
                repository_name,
            )
        )

    # ==========================================================
    # Helpers
    # ==========================================================

    def is_first_sync(
        self,
    ) -> bool:
        """
        Returns True if no synchronization state exists.
        """

        return not self.git_service.sync_file_exists()

    # ==========================================================
    # Public API
    # ==========================================================

    def sync(
        self,
        mode: SyncMode | None = None,
    ) -> None:
        """
        Executes repository synchronization.

        Parameters
        ----------
        mode:
            Synchronization mode.

            If omitted:

            • First execution -> FULL

            • Later executions -> INCREMENTAL
        """

        if mode is None:

            if self.is_first_sync():

                mode = SyncMode.FULL

            else:

                mode = SyncMode.INCREMENTAL

        logger.info(
            "Synchronization mode: %s",
            mode.value,
        )

        if mode == SyncMode.FULL:

            self.full_sync.sync()

            return

        self.incremental_sync.sync()