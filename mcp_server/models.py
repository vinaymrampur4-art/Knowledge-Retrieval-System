"""
models.py

Pydantic models used by the MCP Server.
"""

from typing import Any

from pydantic import BaseModel, Field

# ==========================================================
# Search Filter
# ==========================================================

class SearchFilter(BaseModel):
    """
    Metadata filter applied during retrieval.

    This model represents a single metadata constraint that can
    be applied to restrict search results.

    Examples
    --------
    SearchFilter(
        property="file_path",
        constraint="contains",
        value="routing.py",
    )

    SearchFilter(
        property="class_name",
        constraint="equals",
        value="APIRouter",
    )
    """

    property: str = Field(
        ...,
        description="Metadata field to filter on.",
    )

    constraint: str = Field(
        ...,
        description=(
            "Comparison operator used during filtering. "
            "Supported operators: "
            "equals, contains, startswith, endswith, "
            "!=, >, >=, <, <=."
        ),
    )

    value: Any = Field(
        ...,
        description=(
            "Value used during comparison. "
            "Supports strings, integers, floats and booleans."
        ),
    )
# ==========================================================
# Search Request
# ==========================================================

class SearchRequest(BaseModel):
    """
    Request received by the MCP search tool.
    """

    repository_name: str = Field(
        ...,
        description="Repository to search.",
    )

    query: str = Field(
        ...,
        description="Natural language search query.",
    )

    collection_name: str | None = Field(
        default=None,
        description=(
            "Optional collection to search. "
            "If omitted, all collections are searched."
        ),
    )

    alpha: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Hybrid search weight.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of results.",
    )

    filter: SearchFilter | None = Field(
        default=None,
        description=(
            "Optional metadata filter applied during retrieval."
        ),
    )


# ==========================================================
# Search Result
# ==========================================================

class SearchResultModel(BaseModel):
    """
    Single retrieved document.
    """

    score: float

    id: str

    collection: str

    content: str

    metadata: dict[str, Any]


# ==========================================================
# Search Response
# ==========================================================

class SearchResponse(BaseModel):
    """
    MCP search response.
    """

    query: str

    collection_name: str | None

    total_results: int

    execution_time: float

    results: list[SearchResultModel]


# ==========================================================
# Lookup Request
# ==========================================================

class LookupRequest(BaseModel):
    """
    Request received by the lookup tool.
    """

    id: str = Field(
        ...,
        description="Unique ChromaDB document ID.",
    )

    collection_name: str | None = Field(
        default=None,
        description=(
            "Optional collection to search. "
            "If omitted, all collections are searched."
        ),
    )


# ==========================================================
# Lookup Response
# ==========================================================

class LookupResponse(BaseModel):
    """
    Response returned by the lookup tool.
    """

    id: str

    collection: str

    content: str

    metadata: dict[str, Any]


# ==========================================================
# Attribute Lookup Request
# ==========================================================

class AttributeLookupRequest(BaseModel):
    """
    Lookup documents using metadata attributes.
    """

    attributes: dict[str, Any] = Field(
        ...,
        description="Metadata attributes used for lookup.",
    )

    collection_name: str | None = Field(
        default=None,
        description=(
            "Optional collection to search. "
            "If omitted, all collections are searched."
        ),
    )


# ==========================================================
# Attribute Lookup Result
# ==========================================================

class AttributeLookupResult(BaseModel):
    """
    Single attribute lookup match.
    """

    id: str

    collection: str

    metadata: dict[str, Any]


# ==========================================================
# Attribute Lookup Response
# ==========================================================

class AttributeLookupResponse(BaseModel):
    """
    Response returned by get_id_by_attributes().
    """

    total_matches: int

    results: list[AttributeLookupResult]

# ==========================================================
# Index Statistics
# ==========================================================

class IndexStatsResponse(BaseModel):
    """
    Response returned by check_index_stats().
    """

    repository: str = Field(
        ...,
        description="Indexed repository name.",
    )

    files: int = Field(
        ...,
        description="Number of indexed files.",
    )

    classes: int = Field(
        ...,
        description="Number of indexed classes.",
    )

    methods: int = Field(
        ...,
        description="Number of indexed methods.",
    )

    functions: int = Field(
        ...,
        description="Number of indexed functions.",
    )

    code_blocks: int = Field(
        ...,
        description="Number of indexed code blocks.",
    )

    total_documents: int = Field(
        ...,
        description="Total indexed documents across all collections.",
    )

    embedding_model: str = Field(
        ...,
        description="Embedding model used during indexing.",
    )

    embedding_dimension: int = Field(
        ...,
        description="Embedding vector dimension.",
    )

    bm25_ready: bool = Field(
        ...,
        description="True if the BM25 index exists.",
    )

    chroma_ready: bool = Field(
        ...,
        description="True if ChromaDB is available.",
    )

# ==========================================================
# Repository Reports
# ==========================================================

class RepositoryInfo(BaseModel):
    """
    Information about an indexed repository.
    """

    repository_name: str = Field(
        ...,
        description="Repository name.",
    )

    branch: str = Field(
        ...,
        description="Indexed branch.",
    )


class RepositoryListResponse(BaseModel):
    """
    Response returned by list_repositories().
    """

    total_repositories: int = Field(
        ...,
        description="Number of indexed repositories.",
    )

    repositories: list[RepositoryInfo]

# ==========================================================
# File Reports
# ==========================================================

class FileInfo(BaseModel):
    """
    Information about an indexed file.
    """

    file_path: str = Field(
        ...,
        description="Repository relative file path.",
    )

    language: str = Field(
        ...,
        description="Programming language.",
    )


class FileListResponse(BaseModel):
    """
    Response returned by list_files().
    """

    total_files: int = Field(
        ...,
        description="Number of indexed files.",
    )

    files: list[FileInfo]

# ==========================================================
# Class Reports
# ==========================================================

class ClassInfo(BaseModel):
    """
    Information about an indexed class.
    """

    class_name: str = Field(
        ...,
        description="Class name.",
    )

    file_path: str = Field(
        ...,
        description="Repository file path.",
    )

    method_count: int = Field(
        ...,
        description="Number of methods.",
    )

    inheritance: str = Field(
        ...,
        description="Parent class or inheritance.",
    )


class ClassListResponse(BaseModel):
    """
    Response returned by list_classes().
    """

    total_classes: int = Field(
        ...,
        description="Number of indexed classes.",
    )

    classes: list[ClassInfo]

# ==========================================================
# Method Reports
# ==========================================================

class MethodInfo(BaseModel):
    """
    Information about an indexed method.
    """

    method_name: str = Field(
        ...,
        description="Method name.",
    )

    class_name: str = Field(
        ...,
        description="Parent class.",
    )

    file_path: str = Field(
        ...,
        description="Repository file path.",
    )

    is_async: bool = Field(
        ...,
        description="Whether the method is async.",
    )


class MethodListResponse(BaseModel):
    """
    Response returned by list_methods().
    """

    total_methods: int = Field(
        ...,
        description="Number of indexed methods.",
    )

    methods: list[MethodInfo]

# ==========================================================
# Branch Reports
# ==========================================================

class BranchInfo(BaseModel):
    """
    Information about an indexed branch.
    """

    repository_name: str = Field(
        ...,
        description="Repository name.",
    )

    branch: str = Field(
        ...,
        description="Branch name.",
    )

    files: int = Field(
        ...,
        description="Indexed files.",
    )

    classes: int = Field(
        ...,
        description="Indexed classes.",
    )

    methods: int = Field(
        ...,
        description="Indexed methods.",
    )

    functions: int = Field(
        ...,
        description="Indexed functions.",
    )


class BranchListResponse(BaseModel):
    """
    Response returned by list_branches().
    """

    total_branches: int = Field(
        ...,
        description="Number of indexed branches.",
    )

    branches: list[BranchInfo]

# ==========================================================
# COMPLETE REPORT
# ==========================================================

class CompleteStatsResponse(BaseModel):
    """
    Complete dashboard of the indexed repository.
    """

    repository: str = Field(
        ...,
        description="Repository name.",
    )

    branch: str = Field(
        ...,
        description="Indexed branch.",
    )

    files: int = Field(
        ...,
        description="Number of indexed files.",
    )

    classes: int = Field(
        ...,
        description="Number of indexed classes.",
    )

    methods: int = Field(
        ...,
        description="Number of indexed methods.",
    )

    functions: int = Field(
        ...,
        description="Number of indexed functions.",
    )

    code_blocks: int = Field(
        ...,
        description="Number of indexed code blocks.",
    )

    total_documents: int = Field(
        ...,
        description="Total indexed documents.",
    )

    embedding_model: str = Field(
        ...,
        description="Embedding model.",
    )

    embedding_dimension: int = Field(
        ...,
        description="Embedding dimension.",
    )

    bm25_ready: bool = Field(
        ...,
        description="Whether BM25 index exists.",
    )

    chroma_ready: bool = Field(
        ...,
        description="Whether ChromaDB is available.",
    )

    collections: list[str] = Field(
        ...,
        description="Indexed collections.",
    )