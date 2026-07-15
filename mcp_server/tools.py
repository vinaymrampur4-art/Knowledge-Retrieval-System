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

from mcp_server.mcp_instance import mcp

# ==========================================================
# GENERIC SEARCH
# ==========================================================

@mcp.tool()
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

@mcp.tool()
def search_methods(
    query: str,
    filter: SearchFilter | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed Methods Collection.

    This tool searches indexed Python methods using hybrid retrieval.

    Useful for:

    • understanding business logic
    • locating implementations
    • exploring object behaviour
    • tracing execution flow

    Retrieval Pipeline
    ------------------
    1. Dense Retrieval
    2. BM25 Retrieval
    3. Reciprocal Rank Fusion (RRF)
    4. CrossEncoder Reranking

    Args
    ----
    query : str
        Natural language description of the method.

    filter : SearchFilter | None
        Optional metadata filter.

        Supported operators:

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
        Maximum number of matching methods to return.

    alpha : float
        Hybrid retrieval weight controlling the balance between
        semantic similarity and keyword matching.

    Returns
    -------
    SearchResponse

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

@mcp.tool()
def search_classes(
    query: str,
    filter: SearchFilter | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed Classes Collection.

    This tool searches indexed Python classes using hybrid retrieval.

    Useful for:

    • understanding repository architecture
    • exploring inheritance relationships
    • locating abstractions
    • understanding responsibilities

    Args
    ----
    query : str
        Natural language description of the class.

    filter : SearchFilter | None
        Optional metadata filter.

    top_k : int
        Maximum number of matching classes returned.

    alpha : float
        Hybrid retrieval weight.

    Returns
    -------
    SearchResponse

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

@mcp.tool()
def search_files(
    query: str,
    filter: SearchFilter | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed Files Collection.

    This tool searches indexed repository files using hybrid retrieval.

    Useful for:

    • locating implementation files
    • discovering modules
    • exploring repository structure
    • understanding feature ownership

    Args
    ----
    query : str
        Natural language description of the file or feature.

    filter : SearchFilter | None
        Optional metadata filter.

    top_k : int
        Maximum number of matching files returned.

    alpha : float
        Hybrid retrieval weight.

    Returns
    -------
    SearchResponse

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

@mcp.tool()
def search_functions(
    query: str,
    filter: SearchFilter | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed Functions Collection.

    This tool searches standalone Python functions using hybrid retrieval.

    Useful for:

    • locating helper functions
    • discovering utility functions
    • finding decorators
    • understanding module behaviour

    Args
    ----
    query : str
        Natural language description of the function.

    filter : SearchFilter | None
        Optional metadata filter.

    top_k : int
        Maximum number of matching functions returned.

    alpha : float
        Hybrid retrieval weight.

    Returns
    -------
    SearchResponse

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

@mcp.tool()
def search_code(
    query: str,
    filter: SearchFilter | None = None,
    top_k: int = 5,
    alpha: float = 0.8,
) -> SearchResponse:
    """
    Search the indexed Code Blocks Collection.

    This tool searches implementation-level code blocks using hybrid retrieval.

    Useful for:

    • locating algorithms
    • finding implementation snippets
    • discovering control flow
    • understanding low-level logic

    Args
    ----
    query : str
        Natural language description of the code implementation.

    filter : SearchFilter | None
        Optional metadata filter.

    top_k : int
        Maximum number of matching code blocks returned.

    alpha : float
        Hybrid retrieval weight.

    Returns
    -------
    SearchResponse

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

@mcp.tool()
def lookup_by_id(
    id: str,
    collection_name: str | None = None,
) -> LookupResponse:
    """
    Retrieve an indexed document using its unique document ID.

    Unlike hybrid retrieval, this tool performs a direct lookup
    against indexed collections.

    Useful for:

    • opening retrieved documents
    • inspecting metadata
    • debugging retrieval results

    Args
    ----
    id : str
        Unique document identifier.

    collection_name : str | None
        Optional collection restriction.

    Returns
    -------
    LookupResponse

    Examples
    --------
    id="code::master::fastapi/routing.py::APIRouter::add_api_route"

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

@mcp.tool()
def get_id_by_attributes(
    attributes: dict,
    collection_name: str | None = None,
) -> AttributeLookupResponse:
    """
    Retrieve indexed documents using metadata attributes.

    This tool performs exact metadata lookup rather than semantic
    retrieval.

    Unlike hybrid search, this operation does not use embeddings,
    BM25 retrieval, or reranking. Results are returned only when
    the supplied metadata matches exactly.

    Useful for locating documents by:

    • class name
    • method name
    • function name
    • file path
    • repository branch
    • language
    • module name

    Args
    ----
    attributes : dict
        Metadata fields to match.

        Supported examples include:

        • class_name
        • method_name
        • function_name
        • file_path
        • branch
        • language
        • module_name

    collection_name : str | None
        Optional collection restriction.

        When omitted, all indexed collections are searched.

    Returns
    -------
    AttributeLookupResponse

    Examples
    --------
    Find APIRouter

    attributes={
        "class_name": "APIRouter"
    }

    Find add_api_route()

    attributes={
        "method_name": "add_api_route"
    }

    Find routing.py

    attributes={
        "file_path": "fastapi/routing.py"
    }

    Find Python files

    attributes={
        "language": "python"
    }

    Find documents from the master branch

    attributes={
        "branch": "master"
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

@mcp.tool()

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

@mcp.tool()

def list_repositories() -> RepositoryListResponse:
    """
    Return all repositories currently indexed by the system.

    Useful for:

    • repository discovery
    • multi-repository environments
    • debugging indexing pipelines

    Returns
    -------
    RepositoryListResponse
    """

    return execute_list_repositories()

# ==========================================================
# FILE REPORTS
# ==========================================================

@mcp.tool()

def list_files() -> FileListResponse:
    """
    Return metadata for all indexed repository files.

    Useful for:

    • repository exploration
    • debugging indexing issues
    • understanding project structure

    Returns
    -------
    FileListResponse
    """

    return execute_list_files()

# ==========================================================
# CLASS REPORTS
# ==========================================================
@mcp.tool()

def list_classes() -> ClassListResponse:
    """
    Return metadata for all indexed classes.

    Useful for:

    • architecture exploration
    • inheritance analysis
    • understanding object relationships

    Returns
    -------
    ClassListResponse
    """

    return execute_list_classes()

# ==========================================================
# METHOD REPORTS
# ==========================================================

@mcp.tool()

def list_methods() -> MethodListResponse:
    """
    Return metadata for all indexed methods.

    Useful for:

    • API discovery
    • repository exploration
    • method analysis

    Returns
    -------
    MethodListResponse
    """

    return execute_list_methods()

# ==========================================================
# BRANCH REPORTS
# ==========================================================

@mcp.tool()

def list_branches() -> BranchListResponse:
    """
    Return all indexed repository branches.

    Useful for:

    • multi-branch repositories
    • debugging indexing operations
    • branch comparison

    Returns
    -------
    BranchListResponse
    """

    return execute_list_branches()

# ==========================================================
# COMPLETE REPORT
# ==========================================================

@mcp.tool()

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