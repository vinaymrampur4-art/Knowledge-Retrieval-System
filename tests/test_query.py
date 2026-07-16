"""
Interactive retrieval test.

This script assumes that the indexes have already been built using:

    python -m tests.test_index_pipeline

It only loads the existing indexes and performs retrieval.
"""

from app.retrieval.hybrid.hybrid_retriever import (
    HybridRetriever,
)

from app.core.config import (
    REPOSITORY_FOLDER,
)


def main():

    print("=" * 100)
    print("Knowledge Retrieval System")
    print("=" * 100)

    print("\nLoading indexes...")

    repository_name = REPOSITORY_FOLDER

    retriever = HybridRetriever(
        repository_name
    )

    print("Indexes Ready.")

    while True:

        query = input(
            "\nAsk a question (or 'exit'): "
        ).strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        results = retriever.search(
            query=query,
            top_k=5,
            debug=True,
        )

        print()
        print("=" * 100)
        print(f"Query: {query}")
        print("=" * 100)

        if not results:

            print("\nNo results found.")
            continue

        for i, result in enumerate(
            results,
            start=1,
        ):

            print(f"\nResult #{i}")
            print("-" * 80)

            print(
                f"Score      : "
                f"{result.score:.6f}"
            )

            print(
                f"Collection : "
                f"{result.collection}"
            )

            print(
                f"ID         : "
                f"{result.id}"
            )

            metadata = (
                result.metadata or {}
            )

            print(
                f"Repository : "
                f"{metadata.get('repository_name', 'N/A')}"
            )

            print(
                f"Branch     : "
                f"{metadata.get('branch', 'N/A')}"
            )

            print(
                f"File       : "
                f"{metadata.get('file_path', 'N/A')}"
            )

            if metadata.get(
                "class_name"
            ):
                print(
                    f"Class      : "
                    f"{metadata['class_name']}"
                )

            if metadata.get(
                "method_name"
            ):
                print(
                    f"Method     : "
                    f"{metadata['method_name']}"
                )

            if metadata.get(
                "function_name"
            ):
                print(
                    f"Function   : "
                    f"{metadata['function_name']}"
                )

            if metadata.get(
                "start_line"
            ):

                print(
                    f"Lines      : "
                    f"{metadata['start_line']} - "
                    f"{metadata.get('end_line')}"
                )

            print()

            print(
                result.content[:800]
            )

            if len(result.content) > 800:
                print("\n...")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()