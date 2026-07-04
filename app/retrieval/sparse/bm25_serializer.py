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

    def __init__(self):

        BM25_OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------

    def save(
        self,
        builder,
    ):

        with open(
            BM25_INDEX_FILE,
            "wb",
        ) as file:

            pickle.dump(
                builder.index,
                file,
            )

        with open(
            BM25_STORE_FILE,
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
            BM25_INDEX_FILE,
            "rb",
        ) as file:

            builder.index = pickle.load(
                file
            )

        with open(
            BM25_STORE_FILE,
            "rb",
        ) as file:

            builder.store = pickle.load(
                file
            )

        return builder

    # ---------------------------------------------------------

    def exists(self):

        return (

            BM25_INDEX_FILE.exists()

            and

            BM25_STORE_FILE.exists()

        )