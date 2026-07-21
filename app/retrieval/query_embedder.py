"""
query_embedder.py

Generates embeddings for user search queries.
"""

from sentence_transformers import SentenceTransformer

from app.core.config import EMBEDDING_MODEL


class QueryEmbedder:
    """
    Converts natural language queries into embedding vectors.
    """

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL,
    ):

        print(
            f"Loading query embedding model: {model_name}"
        )

        self.model = SentenceTransformer(
            model_name
        )

    # ---------------------------------------------------------
    # Single Query
    # ---------------------------------------------------------

    def embed(
        self,
        query: str,
    ) -> list[float]:

        vector = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return vector.tolist()

    # ---------------------------------------------------------
    # Batch Queries
    # ---------------------------------------------------------

    def embed_batch(
        self,
        queries: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple queries in one model call.

        Parameters
        ----------
        queries : list[str]
            List of user queries.

        Returns
        -------
        list[list[float]]
            Embedding vector for each query.
        """

        vectors = self.model.encode(
            queries,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return vectors.tolist()