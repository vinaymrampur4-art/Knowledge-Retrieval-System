"""
full_sync_service.py

Executes a complete synchronization of a repository.

Workflow
--------
1. Remove existing indexes.
2. Parse the complete repository.
3. Generate embeddings.
4. Build BM25.
5. Index ChromaDB.
6. Save synchronization state.
"""

from __future__ import annotations

from app.core.config import (
    REPOSITORIES_DIR,
)

from app.incremental_sync.git_service import (
    GitService,
)

from app.incremental_sync.chroma_cleanup import (
    ChromaCleanupService,
)

from app.parser.repository_parser import (
    RepositoryParser,
)

from app.indexing.index_pipeline import (
    IndexPipeline,
)


class FullSyncService:
    """
    Executes a complete synchronization for a repository.
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