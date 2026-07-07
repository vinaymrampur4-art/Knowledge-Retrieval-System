"""
filter_builder.py

Utility class for applying metadata filters to retrieval results.

This module is independent of ChromaDB and can therefore be used by
both Dense Retrieval and BM25 Retrieval.

Supported Constraints
---------------------
- equals
- contains
- startswith
- endswith
- !=
- >
- >=
- <
- <=

Future Extensions
-----------------
- AND
- OR
- NOT
"""

from app.retrieval.search_result import SearchResult
from mcp_server.models import SearchFilter


class FilterBuilder:
    """
    Applies metadata filters to SearchResult objects.
    """

    # ---------------------------------------------------------
    # Operator Implementations
    # ---------------------------------------------------------

    @staticmethod
    def _equals(actual, expected) -> bool:
        return actual == expected

    @staticmethod
    def _contains(actual, expected) -> bool:
        if actual is None:
            return False
        return str(expected) in str(actual)

    @staticmethod
    def _startswith(actual, expected) -> bool:
        if actual is None:
            return False
        return str(actual).startswith(str(expected))

    @staticmethod
    def _endswith(actual, expected) -> bool:
        if actual is None:
            return False
        return str(actual).endswith(str(expected))

    @staticmethod
    def _not_equal(actual, expected) -> bool:
        return actual != expected

    @staticmethod
    def _greater(actual, expected) -> bool:
        if actual is None:
            return False
        return actual > expected

    @staticmethod
    def _greater_equal(actual, expected) -> bool:
        if actual is None:
            return False
        return actual >= expected

    @staticmethod
    def _less(actual, expected) -> bool:
        if actual is None:
            return False
        return actual < expected

    @staticmethod
    def _less_equal(actual, expected) -> bool:
        if actual is None:
            return False
        return actual <= expected

    # ---------------------------------------------------------
    # Supported Operators
    # ---------------------------------------------------------

    OPERATORS = {
        "equals": _equals.__func__,
        "contains": _contains.__func__,
        "startswith": _startswith.__func__,
        "endswith": _endswith.__func__,
        "!=": _not_equal.__func__,
        ">": _greater.__func__,
        ">=": _greater_equal.__func__,
        "<": _less.__func__,
        "<=": _less_equal.__func__,
    }

    # ---------------------------------------------------------
    # Match
    # ---------------------------------------------------------

    @classmethod
    def matches(
        cls,
        metadata: dict,
        search_filter: SearchFilter,
    ) -> bool:
        """
        Determine whether metadata satisfies the supplied filter.
        """

        actual = metadata.get(search_filter.property)

        operator = cls.OPERATORS.get(
            search_filter.constraint,
        )

        if operator is None:

            raise ValueError(
                f"Unsupported filter constraint: "
                f"{search_filter.constraint}"
            )

        return operator(
            actual,
            search_filter.value,
        )

    # ---------------------------------------------------------
    # Filter Results
    # ---------------------------------------------------------

    @classmethod
    def filter_results(
        cls,
        results: list[SearchResult],
        search_filter: SearchFilter | None,
    ) -> list[SearchResult]:
        """
        Apply a metadata filter to retrieval results.
        """

        if search_filter is None:
            return results

        filtered = []

        for result in results:

            metadata = result.metadata or {}

            if cls.matches(
                metadata,
                search_filter,
            ):
                filtered.append(result)

        return filtered