"""
Embeds ChromaDocuments.
"""

from sentence_transformers import SentenceTransformer
from app.core.config import EMBEDDING_MODEL

class DocumentEmbeddingGenerator:

    def __init__(
        self,
        model_name=EMBEDDING_MODEL,
        batch_size=128,
    ):

        self.batch_size = batch_size

        print(
            f"Loading embedding model: {model_name}"
        )

        self.model = SentenceTransformer(
            model_name
        )

    def generate(
        self,
        documents,
    ):

        if not documents:
            return documents

        texts = [
            doc.document
            for doc in documents
        ]

        vectors = self.model.encode(

            texts,

            batch_size=self.batch_size,

            convert_to_numpy=True,

            normalize_embeddings=True,

            show_progress_bar=True,
        )

        for document, vector in zip(
            documents,
            vectors,
        ):

            document.embedding = (
                vector.tolist()
            )

        return documents