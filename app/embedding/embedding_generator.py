"""
embedding_generator.py

Generates vector embeddings for semantic ParsedChunks.
"""

from __future__ import annotations

import time

from sentence_transformers import SentenceTransformer

from app.models.chunk_result import ChunkResult
from app.models.embedding import Embedding
from app.models.embedding_result import EmbeddingResult


class EmbeddingGenerator:
    """
    Generates vector embeddings for semantic code chunks.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
        batch_size: int = 128,
    ):

        self.batch_size = batch_size

        print(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(model_name)

    # --------------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------------

    def generate(
        self,
        chunk_result: ChunkResult,
    ) -> EmbeddingResult:

        result = EmbeddingResult()

        if not chunk_result.chunks:
            return result

        # ---------------------------------------------
        # Keep only semantic chunks
        # ---------------------------------------------

        semantic_chunks = [

            chunk

            for chunk in chunk_result.chunks

            if chunk.chunk_type in {
                "class",
                "method",
                "function",
            }

        ]

        print()

        print(f"Total Chunks    : {len(chunk_result.chunks)}")
        print(f"Semantic Chunks : {len(semantic_chunks)}")

        if not semantic_chunks:
            return result

        # ---------------------------------------------
        # Prepare texts
        # ---------------------------------------------

        texts = [

            chunk.content

            for chunk in semantic_chunks

        ]

        # ---------------------------------------------
        # Generate embeddings
        # ---------------------------------------------

        print()

        print("Generating embeddings...")

        start = time.perf_counter()

        vectors = self.model.encode(

            texts,

            batch_size=self.batch_size,

            convert_to_numpy=True,

            normalize_embeddings=True,

            show_progress_bar=True,

        )

        end = time.perf_counter()

        print()

        print(f"Embedding Time : {end - start:.2f} seconds")

        # ---------------------------------------------
        # Create Embedding objects
        # ---------------------------------------------

        for chunk, vector in zip(
            semantic_chunks,
            vectors,
        ):

            result.embeddings.append(

                Embedding(

                    chunk=chunk,

                    vector=vector.tolist(),

                )

            )

        print(f"Generated {len(result.embeddings)} embeddings.")

        return result