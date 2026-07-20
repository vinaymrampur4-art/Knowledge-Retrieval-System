"""
bm25_serializer.py

Saves and loads the BM25 index and document store.
"""

import pickle

from app.core.config import (
    BM25_OUTPUT_DIR,
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
    # Save
    # ---------------------------------------------------------

    def save(
        self,
        builder,
    ):

        print("\n" + "=" * 80)
        print("SAVING BM25")
        print("=" * 80)
        print(f"Repository     : {self.repository_name}")
        print(f"Repository Dir : {self.repository_dir.resolve()}")
        print(f"Index File     : {self.index_file.resolve()}")
        print(f"Store File     : {self.store_file.resolve()}")
        print("=" * 80)

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
    # Load
    # ---------------------------------------------------------

    def load(
        self,
        builder,
    ):

        print("\n" + "=" * 80)
        print("LOADING BM25")
        print("=" * 80)
        print(f"Repository     : {self.repository_name}")
        print(f"Index File     : {self.index_file.resolve()}")
        print(f"Store File     : {self.store_file.resolve()}")
        print("=" * 80)

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
    # Exists
    # ---------------------------------------------------------

    def exists(self):

        print("\n" + "=" * 80)
        print("BM25Serializer.exists()")
        print("=" * 80)

        print(f"Repository      : {self.repository_name}")
        print(f"Repository Dir  : {self.repository_dir.resolve()}")
        print(f"Index File      : {self.index_file.resolve()}")
        print(f"Store File      : {self.store_file.resolve()}")

        index_exists = self.index_file.exists()
        store_exists = self.store_file.exists()

        print(f"Index Exists    : {index_exists}")
        print(f"Store Exists    : {store_exists}")

        print("=" * 80 + "\n")

        return (
            index_exists
            and
            store_exists
        )