"""
Test Reciprocal Rank Fusion.
"""

from app.retrieval.search_result import SearchResult
from app.retrieval.hybrid.rrf_ranker import RRFRanker


dense_results = [

    SearchResult(
        id="doc_1",
        score=0.95,
        content="APIRouter class",
        collection="Dense",
        metadata={
            "file_path": "fastapi/routing.py",
        },
    ),

    SearchResult(
        id="doc_2",
        score=0.92,
        content="FastAPI class",
        collection="Dense",
        metadata={
            "file_path": "fastapi/applications.py",
        },
    ),

    SearchResult(
        id="doc_3",
        score=0.89,
        content="include_router function",
        collection="Dense",
        metadata={
            "file_path": "fastapi/routing.py",
        },
    ),

]

bm25_results = [

    SearchResult(
        id="doc_3",
        score=14,
        content="include_router function",
        collection="BM25",
        metadata={
            "file_path": "fastapi/routing.py",
        },
    ),

    SearchResult(
        id="doc_1",
        score=13,
        content="APIRouter class",
        collection="BM25",
        metadata={
            "file_path": "fastapi/routing.py",
        },
    ),

    SearchResult(
        id="doc_4",
        score=11,
        content="APIRoute class",
        collection="BM25",
        metadata={
            "file_path": "fastapi/routing.py",
        },
    ),

]

ranker = RRFRanker()

results = ranker.rank(

    [dense_results, bm25_results],

    top_k=10,

)

print()

print("=" * 80)
print("RRF RESULTS")
print("=" * 80)

for i, result in enumerate(results, start=1):

    print()

    print(f"Rank {i}")

    print("-" * 80)

    print(f"ID         : {result.id}")

    print(f"Score      : {result.score:.6f}")

    print(f"Collection : {result.collection}")

    print(f"Content    : {result.content}")

    print(f"Metadata   : {result.metadata}")