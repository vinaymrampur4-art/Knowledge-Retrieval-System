"""
rrf_ranker.py

Reciprocal Rank Fusion (RRF).

Combines multiple ranked result lists into one.
"""

from collections import defaultdict

from app.retrieval.search_result import SearchResult


class RRFRanker:

    """
    Reciprocal Rank Fusion.

    Reference:
    Cormack et al. (2009)
    """

    def __init__(
        self,
        k: int = 60,
    ):

        self.k = k

    # ---------------------------------------------------------

    def rank(

        self,

        result_lists: list[list[SearchResult]],

        top_k: int = 10,

    ) -> list[SearchResult]:

        scores = defaultdict(float)

        unique_results = {}

        # -------------------------------------------------

        for results in result_lists:

            for rank, result in enumerate(results, start=1):

                rrf_score = 1.0 / (self.k + rank)

                scores[result.id] += rrf_score

                unique_results[result.id] = result

        # -------------------------------------------------

        ranked_ids = sorted(

            scores,

            key=scores.get,

            reverse=True,

        )

        final_results = []

        for document_id in ranked_ids[:top_k]:

            result = unique_results[document_id]

            result.score = scores[document_id]

            final_results.append(result)

        return final_results