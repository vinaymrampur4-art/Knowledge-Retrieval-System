"""
complete_stats_service.py

Provides a complete dashboard of the indexed repository.
"""

from app.core.config import (
    FILES_COLLECTION,
    CLASSES_COLLECTION,
    METHODS_COLLECTION,
    FUNCTIONS_COLLECTION,
    CODE_BLOCK_COLLECTION,
)

from app.reports.branch_report_service import (
    BranchReportService,
)

from app.services.index_stats_service import (
    IndexStatsService,
)

from mcp_server.models import (
    CompleteStatsResponse,
)


class CompleteStatsService:
    """
    Service responsible for producing a complete
    repository dashboard.
    """

    def __init__(self):

        self.index_stats = IndexStatsService()

        self.branch_service = BranchReportService()

    # ---------------------------------------------------------
    # Complete Statistics
    # ---------------------------------------------------------

    def get_complete_stats(
        self,
    ) -> CompleteStatsResponse:
        """
        Return the complete repository dashboard.
        """

        stats = self.index_stats.get_stats()

        branch_report = self.branch_service.list_branches()

        branch = branch_report.branches[0]

        return CompleteStatsResponse(

            repository=branch.repository_name,

            branch=branch.branch,

            files=stats.files,

            classes=stats.classes,

            methods=stats.methods,

            functions=stats.functions,

            code_blocks=stats.code_blocks,

            total_documents=stats.total_documents,

            embedding_model=stats.embedding_model,

            embedding_dimension=stats.embedding_dimension,

            bm25_ready=stats.bm25_ready,

            chroma_ready=stats.chroma_ready,

            collections=[

                FILES_COLLECTION,

                CLASSES_COLLECTION,

                METHODS_COLLECTION,

                FUNCTIONS_COLLECTION,

                CODE_BLOCK_COLLECTION,

            ],

        )