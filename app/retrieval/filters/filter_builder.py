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
    Applies metadata filters to SearchResult objects and
    builds ChromaDB metadata filters.
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
    # Build Chroma Where Clause
    # ---------------------------------------------------------

    @staticmethod
    def build(
        filter: SearchFilter | None,
    ) -> dict | None:
        """
        Convert SearchFilter into a ChromaDB where clause.

        ChromaDB supports:
        - equals
        - !=
        - >
        - >=
        - <
        - <=

        Operators such as contains, startswith and endswith
        are handled using post-retrieval filtering.
        """

        if filter is None:
            return None

        property_name = filter.property
        value = filter.value
        constraint = filter.constraint

        if constraint == "equals":

            return {
                property_name: value,
            }

        if constraint == "!=":

            return {
                property_name: {
                    "$ne": value,
                }
            }

        if constraint == ">":

            return {
                property_name: {
                    "$gt": value,
                }
            }

        if constraint == ">=":

            return {
                property_name: {
                    "$gte": value,
                }
            }

        if constraint == "<":

            return {
                property_name: {
                    "$lt": value,
                }
            }

        if constraint == "<=":

            return {
                property_name: {
                    "$lte": value,
                }
            }

        # Unsupported by ChromaDB
        if constraint in [
            "contains",
            "startswith",
            "endswith",
        ]:
            return None

        raise ValueError(
            f"Unsupported filter constraint: "
            f"{constraint}"
        )

    # ---------------------------------------------------------
    # Match
    # ---------------------------------------------------------

    @classmethod
    def matches(
        cls,
        metadata: dict,
        filter: SearchFilter,
    ) -> bool:
        """
        Determine whether metadata satisfies the supplied filter.
        """

        actual = metadata.get(
            filter.property,
        )

        operator = cls.OPERATORS.get(
            filter.constraint,
        )

        if operator is None:

            raise ValueError(
                f"Unsupported filter constraint: "
                f"{filter.constraint}"
            )

        return operator(
            actual,
            filter.value,
        )

    # ---------------------------------------------------------
    # Filter Results
    # ---------------------------------------------------------

    @classmethod
    def filter_results(
        cls,
        results: list[SearchResult],
        filter: SearchFilter | None,
    ) -> list[SearchResult]:
        """
        Apply metadata filtering to retrieval results.

        This is primarily used for operators unsupported by
        ChromaDB such as:

        - contains
        - startswith
        - endswith

        BM25 retrieval also relies on this method because
        BM25 has no native metadata filtering support.
        """

        if filter is None:
            return results

        filtered = []

        for result in results:

            metadata = result.metadata or {}

            if cls.matches(
                metadata,
                filter,
            ):
                filtered.append(result)

        return filtered