"""
query_expander.py

Expands natural language queries before embedding.

The purpose is to provide additional semantic hints
to the embedding model.
"""


class QueryExpander:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def expand(
        self,
        query: str,
    ) -> str:
        """
        Expand a user query before embedding.

        Parameters
        ----------
        query : str

        Returns
        -------
        Expanded query.
        """

        query = query.strip()

        expanded = [query]

        lower = query.lower()

        # -----------------------------------------------------
        # Class
        # -----------------------------------------------------

        if "class" in lower:

            expanded.append("python class")

        # -----------------------------------------------------
        # Method
        # -----------------------------------------------------

        if "method" in lower:

            expanded.append("python method")

        # -----------------------------------------------------
        # Function
        # -----------------------------------------------------

        if "function" in lower:

            expanded.append("python function")

        # -----------------------------------------------------
        # Implementation
        # -----------------------------------------------------

        if "implemented" in lower:

            expanded.extend(
                [
                    "implementation",
                    "source code",
                    "definition",
                ]
            )

        # -----------------------------------------------------
        # APIRouter
        # -----------------------------------------------------

        if "apirouter" in lower:

            expanded.extend(
                [
                    "APIRouter class",
                    "router",
                    "routing.py",
                ]
            )

        # -----------------------------------------------------

        return "\n".join(expanded)