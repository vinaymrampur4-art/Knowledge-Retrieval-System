from app.retrieval.multi_collection_retriever import (
    MultiCollectionRetriever,
)

from app.retrieval.query_embedder import (
    QueryEmbedder,
)


embedder = QueryEmbedder()

retriever = MultiCollectionRetriever()


query = "How does dependency injection work?"


embedding = embedder.embed(query)


results = retriever.search(
    query_embedding=embedding,
    top_k=10,
)


print()

print("=" * 80)

print(f"Retrieved {len(results)} Results")

print("=" * 80)

for result in results:

    print(f"Score      : {result.score:.4f}")

    print(f"Collection : {result.collection}")

    print(f"ID         : {result.id}")

    print(f"Metadata   : {result.metadata}")

    print("-" * 80)