"""
services.py

Business logic for the MCP Server.

All retrieval logic should live here so it can be reused by:
    - MCP Server
    - REST APIs
    - CLI
    - Unit Tests
"""

import time

from app.core.collections import (
    get_collection,
    COLLECTION_MAP,
)

from app.retrieval.hybrid.hybrid_retriever import (
    HybridRetriever,
)

from app.retrieval.chroma_retriever import (
    ChromaRetriever,
)

from app.services.index_stats_service import (
    IndexStatsService,
)

from mcp_server.models import (
    SearchRequest,
    SearchResponse,
    SearchResultModel,
    LookupRequest,
    LookupResponse,
    AttributeLookupRequest,
    AttributeLookupResponse,
    AttributeLookupResult,
    IndexStatsResponse,
)

from app.reports.repository_report_service import (
    RepositoryReportService,
)

from mcp_server.models import (
    RepositoryListResponse,
)

from app.reports.file_report_service import (
    FileReportService,
)

from mcp_server.models import (
    FileListResponse,
)

from app.reports.class_report_service import (
    ClassReportService,
)

from mcp_server.models import (
    ClassListResponse,
)

from app.reports.method_report_service import (
    MethodReportService,
)

from mcp_server.models import (
    MethodListResponse,
)

from app.reports.branch_report_service import (
    BranchReportService,
)

from mcp_server.models import (
    BranchListResponse,
)

from app.reports.complete_stats_service import (
    CompleteStatsService,
)

from mcp_server.models import (
    CompleteStatsResponse,
)

# ==========================================================
# RETRIEVERS / SERVICES
# ==========================================================

retriever = HybridRetriever()

chroma = ChromaRetriever()

index_stats_service = IndexStatsService()

repository_report_service = RepositoryReportService()

file_report_service = FileReportService()

class_report_service = ClassReportService()

method_report_service = MethodReportService()

branch_report_service = BranchReportService()

complete_stats_service = CompleteStatsService()

# ==========================================================
# SEARCH SERVICE
# ==========================================================


def execute_search(
    request: SearchRequest,
) -> SearchResponse:
    """
    Execute hybrid search.
    """

    start_time = time.perf_counter()

    collections = get_collection(
        request.collection_name,
    )

    results = retriever.search(
        query=request.query,
        collections=collections,
        top_k=request.top_k,
    )

    execution_time = (
        time.perf_counter() - start_time
    )

    response_results = [

        SearchResultModel(
            score=result.score,
            id=result.id,
            collection=result.collection,
            content=result.content,
            metadata=result.metadata,
        )

        for result in results

    ]

    return SearchResponse(

        query=request.query,

        collection_name=request.collection_name,

        total_results=len(response_results),

        execution_time=execution_time,

        results=response_results,

    )


# ==========================================================
# LOOKUP SERVICE
# ==========================================================


def execute_lookup(
    request: LookupRequest,
) -> LookupResponse:
    """
    Retrieve a document directly by ID.
    """

    if request.collection_name:

        collections = [request.collection_name]

    else:

        collections = COLLECTION_MAP.values()

    for collection in collections:

        result = chroma.get_by_id(

            collection_name=collection,

            document_id=request.id,

        )

        if result is not None:

            return LookupResponse(

                id=result.id,

                collection=result.collection,

                content=result.content,

                metadata=result.metadata,

            )

    raise ValueError(
        f"Document '{request.id}' was not found."
    )


# ==========================================================
# ATTRIBUTE LOOKUP SERVICE
# ==========================================================


def execute_attribute_lookup(
    request: AttributeLookupRequest,
) -> AttributeLookupResponse:
    """
    Lookup documents using metadata attributes.
    """

    if request.collection_name:

        collections = [request.collection_name]

    else:

        collections = COLLECTION_MAP.values()

    matches: list[AttributeLookupResult] = []

    for collection in collections:

        results = chroma.get_by_attributes(

            collection_name=collection,

            attributes=request.attributes,

        )

        for result in results:

            matches.append(

                AttributeLookupResult(

                    id=result.id,

                    collection=result.collection,

                    metadata=result.metadata,

                )

            )

    return AttributeLookupResponse(

        total_matches=len(matches),

        results=matches,

    )


# ==========================================================
# INDEX STATISTICS SERVICE
# ==========================================================


def check_index_stats() -> IndexStatsResponse:
    """
    Return statistics about the indexed repository.

    Returns
    -------
    IndexStatsResponse
    """

    return index_stats_service.get_stats()

# ==========================================================
# REPOSITORY REPORT SERVICE
# ==========================================================

def execute_list_repositories() -> RepositoryListResponse:
    """
    Return all indexed repositories.

    Returns
    -------
    RepositoryListResponse
    """

    return repository_report_service.list_repositories()

# ==========================================================
# FILE REPORT SERVICE
# ==========================================================

def execute_list_files() -> FileListResponse:
    """
    Return all indexed files.

    Returns
    -------
    FileListResponse
    """

    return file_report_service.list_files()

# ==========================================================
# CLASS REPORT SERVICE
# ==========================================================

def execute_list_classes() -> ClassListResponse:
    """
    Return all indexed classes.

    Returns
    -------
    ClassListResponse
    """

    return class_report_service.list_classes()

# ==========================================================
# METHOD REPORT SERVICE
# ==========================================================

def execute_list_methods() -> MethodListResponse:
    """
    Return all indexed methods.
    """

    return method_report_service.list_methods()

# ==========================================================
# BRANCH REPORT SERVICE
# ==========================================================

def execute_list_branches() -> BranchListResponse:
    """
    Return all indexed branches.
    """

    return branch_report_service.list_branches()

# ==========================================================
# COMPLETE REPORT SERVICE
# ==========================================================

def execute_complete_stats() -> CompleteStatsResponse:
    """
    Return the complete repository dashboard.
    """

    return complete_stats_service.get_complete_stats()