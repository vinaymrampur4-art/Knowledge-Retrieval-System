"""
tools.py

MCP tools for the Knowledge Retrieval System.
"""

from mcp_server.models import (
    SearchFilter,
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
    filter: SearchFilter | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed repository using a natural language query.

    This is the primary retrieval tool of the Knowledge Retrieval System.
    It performs hybrid retrieval to locate relevant source code, classes,
    methods, functions, files, and code blocks.

    Retrieval Pipeline
    ------------------
    The search pipeline consists of four stages:

    1. Dense Retrieval
        Uses BAAI/bge-small-en-v1.5 embeddings for semantic search.

    2. BM25 Retrieval
        Performs keyword-based lexical retrieval.

    3. Reciprocal Rank Fusion (RRF)
        Combines dense and BM25 results.

    4. CrossEncoder Reranking
        Produces the final ranking.

    By default all indexed collections are searched.
    Optionally the search can be restricted to a single collection.

    Parameters
    ----------
    query : str
        Natural language search query.

    collection_name : str | None
        Optional collection restriction.

    filter : SearchFilter | None
        Optional metadata filter.

        Supported operators

        • equals
        • contains
        • startswith
        • endswith
        • !=
        • >
        • >=
        • <
        • <=

    top_k : int
        Maximum number of results.

    alpha : float
        Hybrid retrieval weight.

    Returns
    -------
    SearchResponse

    Examples
    --------
    Search all collections

        query="router"

    Search methods only

        collection_name="methods"

    Search routing.py

        filter=SearchFilter(
            property="file_path",
            constraint="contains",
            value="routing.py",
        )

    Explain APIRouter

        query="Explain APIRouter"
    """

    request = SearchRequest(
        query=query,
        collection_name=collection_name,
        top_k=top_k,
        alpha=alpha,
        filter=filter,
    )

    return execute_search(request)


# ==========================================================
# METHODS SEARCH
# ==========================================================

def search_methods(
    query: str,
    filter: SearchFilter | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed Methods Collection.

    This tool searches indexed Python methods using hybrid retrieval.
    It is useful for locating method implementations, understanding
    business logic, and exploring object behavior within the repository.

    Parameters
    ----------
    query : str
        Natural language description of the method to search.

    top_k : int, default=5
        Maximum number of matching methods to return.

    alpha : float, default=0.8
        Hybrid search weight controlling the balance between semantic
        vector search and keyword matching.

    Returns
    -------
    SearchResponse
        Ranked search results from the Methods Collection.

    Examples
    --------
    Explain APIRouter.add_api_route

    How is include_router implemented?

    Find dependency injection methods

    Search authentication methods
    """

    return search_via_query(
        query=query,
        collection_name="methods",
        filter=filter,
        top_k=top_k,
        alpha=alpha,
)


# ==========================================================
# CLASSES SEARCH
# ==========================================================

def search_classes(
    query: str,
    filter: SearchFilter | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed Classes Collection.

    This tool searches indexed Python classes using hybrid retrieval.
    It is useful for locating class definitions, understanding object
    responsibilities, inheritance relationships, and overall software
    architecture.

    Parameters
    ----------
    query : str
        Natural language description of the class to search.

    top_k : int, default=5
        Maximum number of matching classes to return.

    alpha : float, default=0.8
        Hybrid search weight controlling the balance between semantic
        vector search and keyword matching.

    Returns
    -------
    SearchResponse
        Ranked search results from the Classes Collection.

    Examples
    --------
    Explain APIRouter

    Find request classes

    Search response classes

    Locate authentication classes
    """

    return search_via_query(
        query=query,
        collection_name="classes",
        filter=filter,
        top_k=top_k,
        alpha=alpha,
    )


# ==========================================================
# FILES SEARCH
# ==========================================================

def search_files(
    query: str,
    filter: SearchFilter | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed Files Collection.

    This tool searches indexed source files using hybrid retrieval.
    It is useful for locating files that implement specific features,
    modules, or components within the repository.

    Parameters
    ----------
    query : str
        Natural language description of the file or feature to search.

    top_k : int, default=5
        Maximum number of matching files to return.

    alpha : float, default=0.8
        Hybrid search weight controlling the balance between semantic
        vector search and keyword matching.

    Returns
    -------
    SearchResponse
        Ranked search results from the Files Collection.

    Examples
    --------
    Find the routing module

    Search authentication files

    Locate dependency injection implementation

    Find middleware files
    """

    return search_via_query(
        query=query,
        collection_name="files",
        filter=filter,
        top_k=top_k,
        alpha=alpha,
    )


# ==========================================================
# FUNCTIONS SEARCH
# ==========================================================

def search_functions(
    query: str,
    filter: SearchFilter | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed Functions Collection.

    This tool searches standalone Python functions using hybrid
    retrieval. It is useful for locating helper functions, utility
    functions, decorators, and module-level implementations.

    Parameters
    ----------
    query : str
        Natural language description of the function to search.

    top_k : int, default=5
        Maximum number of matching functions to return.

    alpha : float, default=0.8
        Hybrid search weight controlling the balance between semantic
        vector search and keyword matching.

    Returns
    -------
    SearchResponse
        Ranked search results from the Functions Collection.

    Examples
    --------
    Find helper functions

    Search validation functions

    Locate authentication utilities

    Find startup functions
    """

    return search_via_query(
        query=query,
        collection_name="functions",
        filter=filter,
        top_k=top_k,
        alpha=alpha,
    )


# ==========================================================
# CODE SEARCH
# ==========================================================

def search_code(
    query: str,
    filter: SearchFilter | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed Code Blocks Collection.

    This tool searches code blocks extracted from the repository using
    hybrid retrieval. It is useful for locating implementation snippets,
    algorithms, control flow, and specific code patterns regardless of
    the enclosing class or function.

    Parameters
    ----------
    query : str
        Natural language description of the code or implementation to
        search.

    top_k : int, default=5
        Maximum number of matching code blocks to return.

    alpha : float, default=0.8
        Hybrid search weight controlling the balance between semantic
        vector search and keyword matching.

    Returns
    -------
    SearchResponse
        Ranked search results from the Code Blocks Collection.

    Examples
    --------
    Find JWT validation logic

    Search SQL query execution

    Locate exception handling code

    Find middleware implementation
    """

    return search_via_query(
        query=query,
        collection_name="code_blocks",
        filter=filter,
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
    Retrieve an indexed document using its unique document ID.

    Unlike hybrid retrieval, this tool performs a direct lookup
    from the indexed collections.

    Parameters
    ----------
    id : str
        Unique document identifier.

    collection_name : str | None
        Optional collection restriction.

    Returns
    -------
    LookupResponse

    Examples
    --------
    Lookup a method

    id="code::master::fastapi/routing.py::APIRouter::add_api_route"

    Lookup a file

    id="file::master::fastapi/routing.py"
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
    Retrieve indexed documents using metadata attributes.

    This tool performs exact metadata lookup rather than semantic
    retrieval.

    Useful for locating documents by

    • class name
    • method name
    • file path
    • repository branch
    • language

    Parameters
    ----------
    attributes : dict
        Metadata fields to match.

    collection_name : str | None
        Optional collection restriction.

    Returns
    -------
    AttributeLookupResponse

    Examples
    --------
    attributes={
        "class_name":"APIRouter"
    }

    attributes={
        "method_name":"add_api_route"
    }

    attributes={
        "file_path":"fastapi/routing.py"
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
    Return statistics describing the indexed repository.

    The returned information includes

    • repository name
    • indexed files
    • indexed classes
    • indexed methods
    • indexed functions
    • indexed code blocks
    • embedding model
    • embedding dimension
    • BM25 status
    • ChromaDB status

    Returns
    -------
    IndexStatsResponse
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
    Return a complete dashboard describing the indexed repository.

    The dashboard includes

    • repository information
    • branch
    • indexed files
    • indexed classes
    • indexed methods
    • indexed functions
    • indexed code blocks
    • embedding model
    • embedding dimension
    • BM25 status
    • ChromaDB status
    • indexed collections

    Returns
    -------
    CompleteStatsResponse
    """

    return execute_complete_stats()