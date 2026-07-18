"""
sync_models.py

Models used by the Incremental Sync pipeline.
"""

from dataclasses import dataclass, field


# ==========================================================
# Changed Files
# ==========================================================

@dataclass
class ChangedFiles:
    """
    Stores the list of files detected by Git.

    Attributes
    ----------
    added:
        Newly added files.

    modified:
        Existing files that were modified.

    deleted:
        Files removed from the repository.
    """

    added: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)


# ==========================================================
# Sync State
# ==========================================================

@dataclass
class SyncState:
    """
    Stores the repository synchronization state.
    """

    repository_name: str

    last_commit: str | None = None

    last_sync_time: str | None = None


# ==========================================================
# Sync Result
# ==========================================================

@dataclass
class SyncResult:
    """
    Final result after a synchronization run.
    """

    updated_files: int = 0

    deleted_files: int = 0

    added_files: int = 0

    success: bool = True

    message: str = ""