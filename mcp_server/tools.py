"""
tools.py

MCP tools for the Knowledge Retrieval System.
"""

from mcp_server.models import (
    SearchRequest,
    SearchResponse,
    LookupRequest,
    LookupResponse,
    AttributeLookupRequest,
    AttributeLookupResponse,
    IndexStatsResponse,
    RepositoryListResponse,
    FileListResponse,
    ClassListResponse,
    MethodListResponse,
    BranchListResponse,
    CompleteStatsResponse,
)

from mcp_server.services import (
    execute_search,
    execute_lookup,
    execute_attribute_lookup,
    check_index_stats,
    execute_list_repositories,
    execute_list_files,
    execute_list_classes,
    execute_list_methods,
    execute_list_branches,
    execute_complete_stats,
)

# ==========================================================
# GENERIC SEARCH
# ==========================================================

def search_via_query(
    query: str,
    collection_name: str | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed repository using natural language.
    """

    request = SearchRequest(
        query=query,
        collection_name=collection_name,
        top_k=top_k,
        alpha=alpha,
    )

    return execute_search(request)


# ==========================================================
# METHODS SEARCH
# ==========================================================

def search_methods(
    query: str,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:

    return search_via_query(
        query=query,
        collection_name="Methods_Collection_v1",
        top_k=top_k,
        alpha=alpha,
    )


# ==========================================================
# CLASSES SEARCH
# ==========================================================

def search_classes(
    query: str,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:

    return search_via_query(
        query=query,
        collection_name="Classes_Collection_v1",
        top_k=top_k,
        alpha=alpha,
    )


# ==========================================================
# FILES SEARCH
# ==========================================================

def search_files(
    query: str,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:

    return search_via_query(
        query=query,
        collection_name="Files_Collection_v1",
        top_k=top_k,
        alpha=alpha,
    )


# ==========================================================
# FUNCTIONS SEARCH
# ==========================================================

def search_functions(
    query: str,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:

    return search_via_query(
        query=query,
        collection_name="Functions_Collection_v1",
        top_k=top_k,
        alpha=alpha,
    )


# ==========================================================
# CODE SEARCH
# ==========================================================

def search_code(
    query: str,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:

    return search_via_query(
        query=query,
        collection_name="Code_Block_Collection_v1",
        top_k=top_k,
        alpha=alpha,
    )


# ==========================================================
# LOOKUP BY ID
# ==========================================================

def lookup_by_id(
    id: str,
    collection_name: str | None = None,
) -> LookupResponse:
    """
    Retrieve a document using its unique ID.
    """

    request = LookupRequest(
        id=id,
        collection_name=collection_name,
    )

    return execute_lookup(request)


# ==========================================================
# LOOKUP BY ATTRIBUTES
# ==========================================================

def get_id_by_attributes(
    attributes: dict,
    collection_name: str | None = None,
) -> AttributeLookupResponse:
    """
    Retrieve document IDs using metadata attributes.

    Examples
    --------
    attributes={
        "method_name": "add_api_route"
    }

    attributes={
        "class_name": "APIRouter"
    }

    attributes={
        "file_path": "fastapi/routing.py"
    }
    """

    request = AttributeLookupRequest(
        attributes=attributes,
        collection_name=collection_name,
    )

    return execute_attribute_lookup(request)


# ==========================================================
# INDEX STATISTICS
# ==========================================================

def get_index_statistics() -> IndexStatsResponse:
    """
    Return statistics about the indexed repository.

    Returns
    -------
    IndexStatsResponse
        Number of indexed files, classes, methods,
        functions, code blocks, embedding information,
        and index status.
    """

    return check_index_stats()

# ==========================================================
# REPOSITORY REPORTS
# ==========================================================

def list_repositories() -> RepositoryListResponse:
    """
    List all indexed repositories.

    Returns
    -------
    RepositoryListResponse
    """

    return execute_list_repositories()

# ==========================================================
# FILE REPORTS
# ==========================================================

def list_files() -> FileListResponse:
    """
    List all indexed files.

    Returns
    -------
    FileListResponse
    """

    return execute_list_files()

# ==========================================================
# CLASS REPORTS
# ==========================================================

def list_classes() -> ClassListResponse:
    """
    List all indexed classes.

    Returns
    -------
    ClassListResponse
    """

    return execute_list_classes()

# ==========================================================
# METHOD REPORTS
# ==========================================================

def list_methods() -> MethodListResponse:
    """
    List all indexed methods.
    """

    return execute_list_methods()

# ==========================================================
# BRANCH REPORTS
# ==========================================================

def list_branches() -> BranchListResponse:
    """
    List all indexed branches.
    """

    return execute_list_branches()

# ==========================================================
# COMPLETE REPORT
# ==========================================================

def complete_stats() -> CompleteStatsResponse:
    """
    Return a complete dashboard of the indexed repository.
    """

    return execute_complete_stats()