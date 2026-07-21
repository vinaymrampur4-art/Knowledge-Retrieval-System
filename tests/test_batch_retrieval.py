"""
test_batch_retrieval.py

Benchmark Sequential vs Batch Dense Retrieval.

Measures:
- Sequential retrieval latency
- Batch retrieval latency
- Throughput
- Average latency
"""

import time

from app.retrieval.dense_retriever import DenseRetriever

# ==========================================================
# Configuration
# ==========================================================

QUERIES = [
    "what is fastapi",
    "what is APIRouter",
    "what is dependency injection",
    "what is BaseModel",
    "how are routes created",
    "how middleware works",
    "how startup events work",
    "what is BackgroundTasks",
    "how request validation works",
    "how response models work",
    "what is Depends",
    "how exceptions are handled",
    "what is UploadFile",
    "how websocket works",
    "what is lifespan",
    "what is routing",
    "what is JSONResponse",
    "how security works",
    "what is OAuth2",
    "what is Header",
]

# Make exactly 50 queries
QUERIES = (QUERIES * 3)[:50]

TOP_K = 5

# ==========================================================

retriever = DenseRetriever()

# ==========================================================

print("=" * 80)
print("DENSE RETRIEVAL BENCHMARK")
print("=" * 80)
print(f"Queries Submitted : {len(QUERIES)}")
print(f"Top K             : {TOP_K}")
print("=" * 80)

# ==========================================================
# Sequential Retrieval
# ==========================================================

print()
print("=" * 80)
print("SEQUENTIAL RETRIEVAL")
print("=" * 80)

sequential_results = []

sequential_start = time.perf_counter()

for index, query in enumerate(QUERIES, start=1):

    print()
    print("-" * 80)
    print(f"Query {index}")
    print(f"Question : {query}")
    print("-" * 80)

    result = retriever.search(
        query=query,
        top_k=TOP_K,
    )

    sequential_results.append(result)

sequential_time = time.perf_counter() - sequential_start

# ==========================================================
# Batch Retrieval
# ==========================================================

print()
print("=" * 80)
print("BATCH RETRIEVAL")
print("=" * 80)

batch_start = time.perf_counter()

batch_results = retriever.search_batch(
    queries=QUERIES,
    top_k=TOP_K,
)

batch_time = time.perf_counter() - batch_start

# ==========================================================
# Statistics
# ==========================================================

successful = len(batch_results)
failed = len(QUERIES) - successful

sequential_throughput = successful / sequential_time
batch_throughput = successful / batch_time

avg_seq_latency = (sequential_time * 1000) / successful
avg_batch_latency = (batch_time * 1000) / successful

# ==========================================================
# Final Report
# ==========================================================

print()
print("=" * 80)
print("RESULTS")
print("=" * 80)

print(f"Queries                 : {len(QUERIES)}")
print(f"Successful Queries      : {successful}")
print(f"Failed Queries          : {failed}")

print()

print(f"Sequential Time         : {sequential_time:.2f} sec")
print(f"Sequential Throughput   : {sequential_throughput:.2f} queries/sec")
print(f"Avg Sequential Latency  : {avg_seq_latency:.2f} ms/query")

print()

print(f"Batch Time              : {batch_time:.2f} sec")
print(f"Batch Throughput        : {batch_throughput:.2f} queries/sec")
print(f"Avg Batch Latency       : {avg_batch_latency:.2f} ms/query")

print("=" * 80)