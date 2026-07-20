"""
git_service.py

Git utilities used by the Incremental Sync pipeline.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import asdict
from datetime import datetime

from app.core.config import (
    REPOSITORIES_DIR,
    SYNC_OUTPUT_DIR,
)

from app.incremental_sync.sync_models import (
    ChangedFiles,
    SyncState,
)


class GitService:
    """
    Handles Git operations and synchronization state.
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

    def repository_exists(self) -> bool:
        """
        Returns True if the repository path exists
        and is inside a Git working tree.
        """

        

        if not self.repository_path.exists():
            return False

        try:

            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(self.repository_path),
                    "rev-parse",
                    "--is-inside-work-tree",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            

            return result.stdout.strip() == "true"

        except subprocess.CalledProcessError as exc:

            

            return False

    # ==========================================================
    # Sync State
    # ==========================================================

    def sync_file_exists(self) -> bool:
        return self.sync_file.exists()

    def load_sync_state(self) -> SyncState | None:

        if not self.sync_file.exists():
            return None

        with open(
            self.sync_file,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        return SyncState(
            repository_name=data.get(
                "repository_name",
                self.repository_name,
            ),
            last_commit=data.get(
                "last_commit",
            ),
            last_sync_time=data.get(
                "last_sync_time",
            ),
        )

    def save_sync_state(
        self,
        state: SyncState,
    ) -> None:

        with open(
            self.sync_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                asdict(state),
                file,
                indent=4,
            )

    def get_last_synced_commit(
        self,
    ) -> str | None:

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
            [
                "git",
                "-C",
                str(self.repository_path),
                "rev-parse",
                "HEAD",
            ],
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
            [
                "git",
                "-C",
                str(self.repository_path),
                "branch",
                "--show-current",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()

    def save_latest_sync_state(self) -> None:
        """
        Saves the latest synchronization state.
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

    def get_changed_files(
        self,
        last_commit: str,
    ) -> ChangedFiles:
        """
        Returns all files that have changed since the last synchronization.

        Detects:
        1. Changes committed after the last synchronized commit.
        2. Uncommitted working tree changes.
        """

        if not self.repository_exists():
            raise FileNotFoundError(
                f"Repository not found: {self.repository_path}"
            )

        # ----------------------------------------------------------
        # Validate commit
        # ----------------------------------------------------------

        try:

            subprocess.run(
                [
                    "git",
                    "-C",
                    str(self.repository_path),
                    "cat-file",
                    "-e",
                    f"{last_commit}^{{commit}}",
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

        changes = ChangedFiles()

        seen: set[str] = set()

        # ----------------------------------------------------------
        # 1. Changes between last synced commit and HEAD
        # ----------------------------------------------------------

        committed = subprocess.run(
            [
                "git",
                "-C",
                str(self.repository_path),
                "diff",
                "--name-status",
                last_commit,
                "HEAD",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        # ----------------------------------------------------------
        # 2. Working tree changes
        # ----------------------------------------------------------

        working_tree = subprocess.run(
            [
                "git",
                "-C",
                str(self.repository_path),
                "diff",
                "--name-status",
                "HEAD",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        # ----------------------------------------------------------
        # Parse helper
        # ----------------------------------------------------------

        def process(output: str) -> None:

            for line in output.splitlines():

                if not line.strip():
                    continue

                parts = line.split("\t")

                if len(parts) < 2:
                    continue

                status = parts[0]

                if status.startswith("R"):

                    old_path = parts[1]
                    new_path = parts[2]

                    if old_path not in seen:
                        changes.deleted.append(old_path)
                        seen.add(old_path)

                    if new_path not in seen:
                        changes.added.append(new_path)
                        seen.add(new_path)

                    continue

                path = parts[1]

                if path in seen:
                    continue

                seen.add(path)

                if status == "A":
                    changes.added.append(path)

                elif status == "M":
                    changes.modified.append(path)

                elif status == "D":
                    changes.deleted.append(path)

        process(committed.stdout)
        process(working_tree.stdout)

        repo_prefix = f"repositories/{self.repository_name}/".replace("\\", "/")

        changes.added = [
            path[len(repo_prefix):]
            for path in changes.added
            if path.replace("\\", "/").startswith(repo_prefix)
    ]

        changes.modified = [
            path[len(repo_prefix):]
            for path in changes.modified
            if path.replace("\\", "/").startswith(repo_prefix)
        ]

        changes.deleted = [
            path[len(repo_prefix):]
            for path in changes.deleted
            if path.replace("\\", "/").startswith(repo_prefix)
        ]

        return changes

