"""
model.py

Singleton CrossEncoder model used for reranking.
"""

from sentence_transformers import CrossEncoder

from app.core.config import RERANKER_MODEL


class RerankerModel:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print(
                f"Loading reranker model: {RERANKER_MODEL}"
            )

            cls._model = CrossEncoder(
                RERANKER_MODEL
            )

        return cls._model