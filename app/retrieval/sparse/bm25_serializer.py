"""
bm25_serializer.py

Saves and loads the BM25 index and document store.
"""

import pickle

from app.core.config import (
    BM25_OUTPUT_DIR,
    BM25_INDEX_FILE,
    BM25_STORE_FILE,
)


class BM25Serializer:

    def __init__(
        self,
        repository_name: str,
    ):

        self.repository_name = repository_name

        self.repository_dir = (
            BM25_OUTPUT_DIR /
            repository_name
        )

        self.repository_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.index_file = (
            self.repository_dir /
            "bm25_index.pkl"
        )

        self.store_file = (
            self.repository_dir /
            "bm25_store.pkl"
        )

    # ---------------------------------------------------------

    def save(
        self,
        builder,
    ):

        with open(
            self.index_file,
            "wb",
        ) as file:

            pickle.dump(
                builder.index,
                file,
            )

        with open(
            self.store_file,
            "wb",
        ) as file:

            pickle.dump(
                builder.store,
                file,
            )

    # ---------------------------------------------------------

    def load(
        self,
        builder,
    ):

        with open(
            self.index_file,
            "rb",
        ) as file:

            builder.index = pickle.load(
                file
            )

        with open(
            self.store_file,
            "rb",
        ) as file:

            builder.store = pickle.load(
                file
            )

        return builder

    # ---------------------------------------------------------

    def exists(self):

        return (

            self.index_file.exists()

            and

            self.store_file.exists()

        )