"""
branch_report_service.py

Provides branch reports for the indexed repository.
"""

from app.core.config import (
    REPOSITORY_NAME,
    DEFAULT_BRANCH,
)

from app.services.index_stats_service import (
    IndexStatsService,
)

from mcp_server.models import (
    BranchInfo,
    BranchListResponse,
)


class BranchReportService:
    """
    Service responsible for branch reports.
    """

    def __init__(self):

        self.index_stats = IndexStatsService()

    # ---------------------------------------------------------
    # List Branches
    # ---------------------------------------------------------

    def list_branches(
        self,
    ) -> BranchListResponse:
        """
        Return all indexed branches.
        """

        stats = self.index_stats.get_stats()

        branches = [

            BranchInfo(

                repository_name=REPOSITORY_NAME,

                branch=DEFAULT_BRANCH,

                files=stats.files,

                classes=stats.classes,

                methods=stats.methods,

                functions=stats.functions,

            )

        ]

        return BranchListResponse(

            total_branches=len(branches),

            branches=branches,

        )