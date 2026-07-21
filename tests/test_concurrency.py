"""
test_concurrency.py

Benchmark concurrent HybridRetriever searches.

Measures:
- Individual query latency
- Average latency
- Min latency
- Max latency
- Total execution time
- Throughput (queries/sec)
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.retrieval.hybrid.hybrid_retriever import HybridRetriever

# ==========================================================
# Configuration
# ==========================================================

REPOSITORY = "fastapi-master"

CONCURRENT_USERS = 50

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

QUERIES = (QUERIES * 3)[:50]

# ==========================================================

retriever = HybridRetriever(
    repository_name=REPOSITORY,
)

# ==========================================================


def run_query(query: str) -> float:
    start = time.perf_counter()

    retriever.search(
        query=query,
        top_k=5,
    )

    return (time.perf_counter() - start) * 1000


# ==========================================================

print("=" * 80)
print("CONCURRENCY BENCHMARK")
print("=" * 80)
print(f"Repository        : {REPOSITORY}")
print(f"Concurrent Users  : {CONCURRENT_USERS}")
print(f"Queries Submitted : {len(QUERIES)}")
print("=" * 80)

overall_start = time.perf_counter()

latencies = []
failed = 0

with ThreadPoolExecutor(max_workers=CONCURRENT_USERS) as executor:

    future_to_query = {
        executor.submit(run_query, query): query
        for query in QUERIES
    }

    for future in as_completed(future_to_query):

        try:
            latency = future.result()
            latencies.append(latency)

        except Exception as e:
            failed += 1
            print(f"[ERROR] {future_to_query[future]} -> {e}")

overall_time = time.perf_counter() - overall_start

successful = len(latencies)

# ==========================================================

if successful:

    average_latency = sum(latencies) / successful
    minimum_latency = min(latencies)
    maximum_latency = max(latencies)
    throughput = successful / overall_time

    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)

    print(f"Successful Queries : {successful}")
    print(f"Failed Queries     : {failed}")
    print(f"Average Latency    : {average_latency:.2f} ms")
    print(f"Minimum Latency    : {minimum_latency:.2f} ms")
    print(f"Maximum Latency    : {maximum_latency:.2f} ms")
    print(f"Total Time         : {overall_time:.2f} sec")
    print(f"Throughput         : {throughput:.2f} queries/sec")

    print("=" * 80)

else:

    print("All queries failed.")