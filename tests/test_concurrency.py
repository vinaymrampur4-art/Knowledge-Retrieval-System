"""
test_concurrency.py

Benchmark Concurrent Dense Retrieval.

Measures:
- Concurrent Users
- Successful Queries
- Failed Queries
- Total Time
- Average Latency
- Throughput
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.retrieval.dense_retriever import DenseRetriever

# ==========================================================
# Configuration
# ==========================================================

QUERY = "what is fastapi"

CONCURRENCY_LEVELS = [
    1,
    5,
    10,
    25,
    50,
    100,
]

TOP_K = 5

retriever = DenseRetriever()

# ==========================================================


def execute_search():

    start = time.perf_counter()

    try:
        retriever.search(
            query=QUERY,
            top_k=TOP_K,
        )

        latency = time.perf_counter() - start

        return True, latency

    except Exception:

        latency = time.perf_counter() - start

        return False, latency


# ==========================================================

print("=" * 80)
print("DENSE RETRIEVAL CONCURRENCY BENCHMARK")
print("=" * 80)

results = []

# ==========================================================

for users in CONCURRENCY_LEVELS:

    print()
    print("=" * 80)
    print(f"Concurrent Users : {users}")
    print("=" * 80)

    benchmark_start = time.perf_counter()

    successful = 0
    failed = 0

    latencies = []

    with ThreadPoolExecutor(max_workers=users) as executor:

        futures = [
            executor.submit(execute_search)
            for _ in range(users)
        ]

        for future in as_completed(futures):

            ok, latency = future.result()

            latencies.append(latency)

            if ok:
                successful += 1
            else:
                failed += 1

    total_time = time.perf_counter() - benchmark_start

    avg_latency = (sum(latencies) / len(latencies)) * 1000
    throughput = successful / total_time

    results.append(
        (
            users,
            successful,
            failed,
            total_time,
            avg_latency,
            throughput,
        )
    )

    print(f"Successful Queries : {successful}")
    print(f"Failed Queries     : {failed}")
    print(f"Total Time         : {total_time:.2f} sec")
    print(f"Avg Latency        : {avg_latency:.2f} ms")
    print(f"Throughput         : {throughput:.2f} queries/sec")

# ==========================================================
# Final Report
# ==========================================================

print()
print("=" * 100)
print("CONCURRENCY MATRIX")
print("=" * 100)

print(
    f"{'Users':<10}"
    f"{'Success':<12}"
    f"{'Failed':<10}"
    f"{'Time(s)':<12}"
    f"{'Avg(ms)':<12}"
    f"{'Throughput':<15}"
)

print("-" * 100)

for row in results:

    users, success, failed, total, latency, throughput = row

    print(
        f"{users:<10}"
        f"{success:<12}"
        f"{failed:<10}"
        f"{total:<12.2f}"
        f"{latency:<12.2f}"
        f"{throughput:<15.2f}"
    )

print("=" * 100)