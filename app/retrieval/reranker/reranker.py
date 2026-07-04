"""
reranker.py

CrossEncoder reranker.

The CrossEncoder reranks only the candidates produced by
Hybrid Retrieval (Dense + BM25 + RRF).
"""

from app.retrieval.search_result import SearchResult
from app.retrieval.reranker.model import RerankerModel


class Reranker:

    def __init__(self):

        self.model = RerankerModel.get_model()

    # ---------------------------------------------------------

    def _build_rerank_text(
        self,
        result: SearchResult,
    ) -> str:
        """
        Build a compact natural-language representation
        for the CrossEncoder.

        Avoid passing long source code because CrossEncoders
        work best on concise semantic descriptions.
        """

        metadata = result.metadata or {}

        parts = []

        # --------------------------------------------------
        # Document Type
        # --------------------------------------------------

        collection = result.collection.replace("_", " ")

        parts.append(f"Document Type: {collection}")

        # --------------------------------------------------
        # File
        # --------------------------------------------------

        if metadata.get("file_path"):

            parts.append(
                f"File: {metadata['file_path']}"
            )

        # --------------------------------------------------
        # Class
        # --------------------------------------------------

        if metadata.get("class_name"):

            parts.append(
                f"Class: {metadata['class_name']}"
            )

        # --------------------------------------------------
        # Method
        # --------------------------------------------------

        if metadata.get("method_name"):

            parts.append(
                f"Method: {metadata['method_name']}"
            )

        # --------------------------------------------------
        # Function
        # --------------------------------------------------

        if metadata.get("function_name"):

            parts.append(
                f"Function: {metadata['function_name']}"
            )

        # --------------------------------------------------
        # Signature
        # --------------------------------------------------

        signature = (

            metadata.get("method_signature")

            or

            metadata.get("function_signature")

        )

        if signature:

            parts.append(

                f"Signature: {signature}"

            )

        # --------------------------------------------------
        # Parameters
        # --------------------------------------------------

        if metadata.get("parameters"):

            parts.append(

                f"Parameters: {metadata['parameters']}"

            )

        # --------------------------------------------------
        # Return Type
        # --------------------------------------------------

        if metadata.get("return_type"):

            parts.append(

                f"Returns: {metadata['return_type']}"

            )

        # --------------------------------------------------
        # Docstring
        # --------------------------------------------------

        if metadata.get("docstring"):

            parts.append(

                metadata["docstring"]

            )

        # --------------------------------------------------
        # Small preview
        # --------------------------------------------------

        preview = result.content

        # Remove common headings

        preview = preview.replace(
            "DOCUMENT TYPE",
            "",
        )

        preview = preview.replace(
            "METHOD NAME",
            "",
        )

        preview = preview.replace(
            "CLASS NAME",
            "",
        )

        preview = preview.replace(
            "CLASS",
            "",
        )

        preview = preview.replace(
            "FUNCTION NAME",
            "",
        )

        preview = preview.replace(
            "FILE PATH",
            "",
        )

        preview = preview.replace(
            "SOURCE CODE",
            "",
        )

        preview = preview.replace(
            "SUMMARY",
            "",
        )

        preview = preview.replace(
            "SIGNATURE",
            "",
        )

        preview = preview.replace(
            "PARAMETERS",
            "",
        )

        preview = preview.replace(
            "RETURN TYPE",
            "",
        )

        preview = preview.strip()

        # Only a short preview

        parts.append(preview[:250])

        return "\n".join(parts)

    # ---------------------------------------------------------

    def rerank(
        self,
        query: str,
        results: list[SearchResult],
        top_k: int = 5,
    ) -> list[SearchResult]:

        if not results:
            return []

        pairs = [

            (

                query,

                self._build_rerank_text(result),

            )

            for result in results

        ]

        scores = self.model.predict(
            pairs,
            show_progress_bar=False,
        )

        for result, score in zip(results, scores):

            result.score = float(score)

        results.sort(

            key=lambda r: r.score,

            reverse=True,

        )

        return results[:top_k]