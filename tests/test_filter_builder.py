"""
test_filter_builder.py

Unit tests for FilterBuilder.

Tests supported metadata filter operators:
- equals
- contains
- startswith
- endswith
- !=
- >
- >=
- <
- <=
"""

from app.retrieval.filters.filter_builder import FilterBuilder
from app.retrieval.search_result import SearchResult
from mcp_server.models import SearchFilter


# ==========================================================
# Helper
# ==========================================================

def make_result(metadata: dict) -> SearchResult:
    """
    Create a dummy SearchResult for testing.
    """

    return SearchResult(
        id="test-id",
        score=1.0,
        collection="Methods",
        content="dummy content",
        metadata=metadata,
    )


# ==========================================================
# Equals
# ==========================================================

def test_equals():

    result = make_result(
        {
            "class_name": "APIRouter",
        }
    )

    search_filter = SearchFilter(
        property="class_name",
        constraint="equals",
        value="APIRouter",
    )

    filtered = FilterBuilder.filter_results(
        [result],
        search_filter,
    )

    assert len(filtered) == 1


# ==========================================================
# Contains
# ==========================================================

def test_contains():

    result = make_result(
        {
            "file_path": "fastapi/routing.py",
        }
    )

    search_filter = SearchFilter(
        property="file_path",
        constraint="contains",
        value="routing",
    )

    filtered = FilterBuilder.filter_results(
        [result],
        search_filter,
    )

    assert len(filtered) == 1


# ==========================================================
# Startswith
# ==========================================================

def test_startswith():

    result = make_result(
        {
            "class_name": "APIRouter",
        }
    )

    search_filter = SearchFilter(
        property="class_name",
        constraint="startswith",
        value="API",
    )

    filtered = FilterBuilder.filter_results(
        [result],
        search_filter,
    )

    assert len(filtered) == 1


# ==========================================================
# Endswith
# ==========================================================

def test_endswith():

    result = make_result(
        {
            "file_path": "fastapi/routing.py",
        }
    )

    search_filter = SearchFilter(
        property="file_path",
        constraint="endswith",
        value=".py",
    )

    filtered = FilterBuilder.filter_results(
        [result],
        search_filter,
    )

    assert len(filtered) == 1


# ==========================================================
# Not Equal
# ==========================================================

def test_not_equal():

    result = make_result(
        {
            "branch": "master",
        }
    )

    search_filter = SearchFilter(
        property="branch",
        constraint="!=",
        value="develop",
    )

    filtered = FilterBuilder.filter_results(
        [result],
        search_filter,
    )

    assert len(filtered) == 1


# ==========================================================
# Greater Than
# ==========================================================

def test_greater():

    result = make_result(
        {
            "start_line": 500,
        }
    )

    search_filter = SearchFilter(
        property="start_line",
        constraint=">",
        value=400,
    )

    filtered = FilterBuilder.filter_results(
        [result],
        search_filter,
    )

    assert len(filtered) == 1


# ==========================================================
# Greater Than Or Equal
# ==========================================================

def test_greater_equal():

    result = make_result(
        {
            "start_line": 500,
        }
    )

    search_filter = SearchFilter(
        property="start_line",
        constraint=">=",
        value=500,
    )

    filtered = FilterBuilder.filter_results(
        [result],
        search_filter,
    )

    assert len(filtered) == 1


# ==========================================================
# Less Than
# ==========================================================

def test_less():

    result = make_result(
        {
            "start_line": 100,
        }
    )

    search_filter = SearchFilter(
        property="start_line",
        constraint="<",
        value=200,
    )

    filtered = FilterBuilder.filter_results(
        [result],
        search_filter,
    )

    assert len(filtered) == 1


# ==========================================================
# Less Than Or Equal
# ==========================================================

def test_less_equal():

    result = make_result(
        {
            "start_line": 100,
        }
    )

    search_filter = SearchFilter(
        property="start_line",
        constraint="<=",
        value=100,
    )

    filtered = FilterBuilder.filter_results(
        [result],
        search_filter,
    )

    assert len(filtered) == 1


# ==========================================================
# Missing Metadata
# ==========================================================

def test_missing_metadata():

    result = make_result(
        {
            "class_name": "APIRouter",
        }
    )

    search_filter = SearchFilter(
        property="file_path",
        constraint="contains",
        value="routing",
    )

    filtered = FilterBuilder.filter_results(
        [result],
        search_filter,
    )

    assert len(filtered) == 0


# ==========================================================
# Unsupported Operator
# ==========================================================

def test_invalid_operator():

    result = make_result(
        {
            "class_name": "APIRouter",
        }
    )

    search_filter = SearchFilter(
        property="class_name",
        constraint="invalid_operator",
        value="APIRouter",
    )

    try:

        FilterBuilder.filter_results(
            [result],
            search_filter,
        )

        assert False

    except ValueError:

        assert True