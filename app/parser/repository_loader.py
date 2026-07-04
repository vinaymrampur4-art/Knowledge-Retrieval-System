"""
repository_loader.py

Loads a repository and discovers supported Python files.
"""

import os
from pathlib import Path

from app.core.config import REPOSITORIES_DIR
from app.core.logger import logger
from app.parser.file_filter import (
    is_supported_file,
    should_ignore_directory,
)


class RepositoryLoader:

    def __init__(self, repository_name: str):

        self.repository_name = repository_name

        self.repository_path = REPOSITORIES_DIR / repository_name

        if not self.repository_path.exists():
            raise FileNotFoundError(
                f"Repository '{repository_name}' not found."
            )

    @staticmethod
    def list_repositories() -> list[str]:
        """
        Returns all repositories inside the repositories folder.
        """

        return sorted(
            [
                repo.name
                for repo in REPOSITORIES_DIR.iterdir()
                if repo.is_dir()
            ]
        )

    def discover_files(self) -> list[Path]:
        """
        Discover all supported Python files.
        """

        discovered_files = []

        logger.info(
            f"Scanning repository: {self.repository_name}"
        )

        for root, dirs, files in os.walk(self.repository_path):

            # Skip ignored directories
            dirs[:] = [
                d
                for d in dirs
                if not should_ignore_directory(Path(d))
            ]

            for file in files:

                file_path = Path(root) / file

                if is_supported_file(file_path):

                    discovered_files.append(file_path)

        logger.info(
            f"Found {len(discovered_files)} Python files."
        )

        return sorted(discovered_files)