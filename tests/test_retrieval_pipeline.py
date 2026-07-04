from app.retrieval.retrieval_pipeline import RetrievalPipeline

pipeline = RetrievalPipeline()

query = "Where is APIRouter implemented?"

result = pipeline.search(
    query=query,
    top_k=10,
)

print()
print("=" * 100)
print(f"Query           : {result.query}")
print(f"Total Results   : {result.total_results}")
print(f"Embedding Time  : {result.embedding_time:.4f}s")
print(f"Retrieval Time  : {result.retrieval_time:.4f}s")
print(f"Total Time      : {result.total_time:.4f}s")
print("=" * 100)

for index, item in enumerate(result.results, start=1):

    print()
    print("-" * 100)
    print(f"Result #{index}")
    print("-" * 100)

    print(f"Score      : {item.score:.4f}")
    print(f"Collection : {item.collection}")
    print(f"ID         : {item.id}")

    print("\nMetadata")
    print("-" * 40)

    for key, value in item.metadata.items():
        print(f"{key:20}: {value}")

    print()

    print("Content")
    print("-" * 40)

    print(item.content[:300])

print()
print("=" * 100)