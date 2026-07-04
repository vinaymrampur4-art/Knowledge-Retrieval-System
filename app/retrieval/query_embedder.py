"""
query_embedder.py

Generates embeddings for user search queries.
"""

from sentence_transformers import SentenceTransformer


class QueryEmbedder:
    """
    Converts a natural language query into an embedding vector.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):

        print(
            f"Loading query embedding model: {model_name}"
        )

        self.model = SentenceTransformer(
            model_name
        )

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