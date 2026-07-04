"""
repository_report_service.py

Provides repository level reports for the MCP server.
"""

from app.core.config import (
    REPOSITORY_NAME,
    DEFAULT_BRANCH,
)

from mcp_server.models import (
    RepositoryInfo,
    RepositoryListResponse,
)


class RepositoryReportService:
    """
    Service responsible for repository reports.
    """

    # ---------------------------------------------------------
    # List Repositories
    # ---------------------------------------------------------

    def list_repositories(
        self,
    ) -> RepositoryListResponse:
        """
        Return all indexed repositories.

        Returns
        -------
        RepositoryListResponse
        """

        repositories = [

            RepositoryInfo(

                repository_name=REPOSITORY_NAME,

                branch=DEFAULT_BRANCH,

            )

        ]

        return RepositoryListResponse(

            total_repositories=len(repositories),

            repositories=repositories,

        )