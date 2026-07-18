"""
git_service.py

Git utilities used by the Incremental Sync pipeline.
"""

from __future__ import annotations

from datetime import datetime
import json
import subprocess

from app.core.config import (
    REPOSITORIES_DIR,
    SYNC_OUTPUT_DIR,
)

from dataclasses import asdict

from app.incremental_sync.sync_models import (
    ChangedFiles,
    SyncState,
)


class GitService:
    """
    Handles Git operations and synchronization state
    for a repository.
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

        self.sync_file = (
            SYNC_OUTPUT_DIR /
            f"{repository_name}.json"
        )

    # ==========================================================
    # Repository
    # ==========================================================

    def repository_exists(
        self,
    ) -> bool:
        """
        Returns True if the repository exists
        and is a valid Git repository.
        """

        if not self.repository_path.exists():
            return False

        return (
            self.repository_path /
            ".git"
        ).exists()

    # ==========================================================
    # Sync State
    # ==========================================================

    def sync_file_exists(self) -> bool:
        return self.sync_file.exists()

    def load_sync_state(self) -> SyncState | None:

        if not self.sync_file.exists():
            return None

        with open(self.sync_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        return SyncState(
            repository_name=data["repository_name"],
            last_commit=data.get("last_commit"),
            last_sync_time=data.get("last_sync_time"),
        )

    def save_sync_state(self, state: SyncState) -> None:

        with open(self.sync_file, "w", encoding="utf-8") as file:
            json.dump(asdict(state), file, indent=4)

    def get_last_synced_commit(self) -> str | None:

        state = self.load_sync_state()

        if state is None:
            return None

        return state.last_commit

    # ==========================================================
    # Git
    # ==========================================================

    def get_latest_commit(self) -> str:

        if not self.repository_exists():
            raise FileNotFoundError(
                f"Repository not found: {self.repository_path}"
            )

        result = subprocess.run(
            ["git", "-C", str(self.repository_path), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()

    def get_current_branch(self) -> str:

        if not self.repository_exists():
            raise FileNotFoundError(
                f"Repository not found: {self.repository_path}"
            )

        result = subprocess.run(
            ["git", "-C", str(self.repository_path), "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()

    def save_latest_sync_state(self) -> None:          # BUG 1 FIXED: now inside class
        """
        Updates the synchronization state.
        """

        state = SyncState(
            repository_name=self.repository_name,
            last_commit=self.get_latest_commit(),
            last_sync_time=datetime.now().isoformat(),
        )

        self.save_sync_state(state)

    # ==========================================================
    # Incremental Sync
    # ==========================================================

    def get_changed_files(self, last_commit: str) -> ChangedFiles:

        if not self.repository_exists():
            raise FileNotFoundError(
                f"Repository not found: {self.repository_path}"
            )

        try:
            subprocess.run(
                [
                    "git", "-C", str(self.repository_path),
                    "cat-file", "-e", f"{last_commit}^{{commit}}",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            raise ValueError(
                f"Invalid commit hash '{last_commit}' "
                f"found in synchronization state."
            ) from exc

        # BUG 2 FIXED: actually run the diff command
        result = subprocess.run(
            [
                "git", "-C", str(self.repository_path),
                "diff", "--name-status", last_commit, "HEAD",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        changes = ChangedFiles()

        for line in result.stdout.splitlines():

            if not line.strip():
                continue

            parts = line.split("\t")

            if len(parts) < 2:
                continue
            status = parts[0]

            if status == "A":
                changes.added.append(parts[1])

            elif status == "M":
                changes.modified.append(parts[1])

            elif status == "D":
                changes.deleted.append(parts[1])

            elif status.startswith("R"):
                changes.deleted.append(parts[1])
                changes.added.append(parts[2])

        return changes