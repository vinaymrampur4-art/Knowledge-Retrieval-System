"""
Test ChromaDB native metadata filtering.
"""

from mcp_server.models import SearchFilter

from app.retrieval.query_embedder import QueryEmbedder
from app.retrieval.chroma_retriever import ChromaRetriever
from app.core.config import METHODS_COLLECTION


embedder = QueryEmbedder()

retriever = ChromaRetriever()

query = "router"

embedding = embedder.embed(query)

# ==========================================================
# Test 1: Equals
# ==========================================================

print("\n")
print("=" * 80)
print("EQUALS FILTER")
print("=" * 80)

results = retriever.search(
    collection_name=METHODS_COLLECTION,
    query_embedding=embedding,
    filter=SearchFilter(
        property="class_name",
        constraint="equals",
        value="APIRouter",
    ),
    top_k=10,
)

for result in results:
    print()
    print(result.id)
    print(result.metadata.get("class_name"))
    print(result.metadata.get("method_name"))
    print(result.score)

# ==========================================================
# Test 2: Contains
# ==========================================================

print("\n")
print("=" * 80)
print("CONTAINS FILTER")
print("=" * 80)

results = retriever.search(
    collection_name=METHODS_COLLECTION,
    query_embedding=embedding,
    filter=SearchFilter(
        property="file_path",
        constraint="contains",
        value="routing.py",
    ),
    top_k=10,
)

for result in results:
    print()
    print(result.id)
    print(result.metadata.get("file_path"))
    print(result.metadata.get("method_name"))
    print(result.score)

# ==========================================================
# Test 3: Not Equal
# ==========================================================

print("\n")
print("=" * 80)
print("NOT EQUAL FILTER")
print("=" * 80)

results = retriever.search(
    collection_name=METHODS_COLLECTION,
    query_embedding=embedding,
    filter=SearchFilter(
        property="class_name",
        constraint="!=",
        value="APIRouter",
    ),
    top_k=10,
)

for result in results:
    print()
    print(result.id)
    print(result.metadata.get("class_name"))
    print(result.metadata.get("method_name"))
    print(result.score)