"""
Test ChromaRetriever.
"""

from app.retrieval.query_embedder import QueryEmbedder
from app.retrieval.chroma_retriever import ChromaRetriever


embedder = QueryEmbedder()

retriever = ChromaRetriever()

query = "Where is APIRouter implemented?"

query_embedding = embedder.embed(query)

results = retriever.search(
    collection_name="Classes_Collection_v1",
    query_embedding=query_embedding,
    top_k=5,
)

print()
print("=" * 100)
print(f"Query : {query}")
print("=" * 100)

for index, result in enumerate(results, start=1):

    print()
    print("-" * 100)
    print(f"Result #{index}")
    print("-" * 100)

    print(f"ID         : {result.id}")
    print(f"Score      : {result.score:.4f}")
    print(f"Collection : {result.collection}")

    print()

    print("Metadata")
    print("-" * 40)

    if result.metadata:

        for key, value in result.metadata.items():
            print(f"{key:20}: {value}")

    else:

        print("No metadata available.")

    print()

    print("Content")
    print("-" * 40)

    if result.content:
        print(result.content)
    else:
        print("No document content.")

print()
print("=" * 100)
print(f"Retrieved {len(results)} results.")
print("=" * 100)