"""
Evaluate retrieval quality over a fixed benchmark set.

This script compares:

1. Dense Retrieval
2. BM25 Retrieval
3. Hybrid Retrieval (RRF + Reranker)

for a collection of representative software engineering queries.
"""

from app.retrieval.dense_retriever import DenseRetriever
from app.retrieval.sparse.bm25_retriever import BM25Retriever
from app.retrieval.hybrid.hybrid_retriever import HybridRetriever
from app.core.config import REPOSITORY_FOLDER

TEST_QUERIES = [

    "What is APIRouter?",

    "What is FastAPI?",

    "How do I create a FastAPI app?",

    "How do I include a router?",

    "How do I add a route?",

    "How do I create an API endpoint?",

    "How does dependency injection work?",

    "How do I add middleware?",

    "How do I create a websocket?",

    "Where is APIRouter defined?",

    "How are routes registered?",

    "How is OpenAPI generated?",

    "What is APIRoute?",

    "How do I mount a sub application?",

    "How do I validate request data?",

]


def print_results(title, results):

    print()
    print("=" * 100)
    print(title)
    print("=" * 100)

    for i, result in enumerate(results, start=1):

        metadata = result.metadata or {}

        name = (
            metadata.get("method_name")
            or metadata.get("function_name")
            or metadata.get("class_name")
            or metadata.get("module_name")
            or "Unknown"
        )

        print(
            f"{i:2d}. "
            f"{result.score:.4f} | "
            f"{result.collection:25} | "
            f"{name}"
        )


def main():

    print("=" * 100)
    print("Loading Retrievers")
    print("=" * 100)

    dense = DenseRetriever()

    repository_name = REPOSITORY_FOLDER

    bm25 = BM25Retriever(
        repository_name
    )

    hybrid = HybridRetriever(
        repository_name
    )

    for query in TEST_QUERIES:

        print("\n\n")
        print("#" * 100)
        print(query)
        print("#" * 100)

        dense_results = dense.search(
            query=query,
            top_k=5,
        )

        bm25_results = bm25.search(
            query=query,
            top_k=5,
        )

        hybrid_results = hybrid.search(
            query=query,
            top_k=5,
        )

        print_results(
            "DENSE",
            dense_results,
        )

        print_results(
            "BM25",
            bm25_results,
        )

        print_results(
            "HYBRID",
            hybrid_results,
        )


if __name__ == "__main__":
    main()