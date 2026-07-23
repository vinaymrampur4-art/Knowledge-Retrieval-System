"""
run.py

Unified entry point for the Knowledge Retrieval System (KRS).

Usage:

    python run.py index
    python run.py server
    python run.py sync
    python run.py benchmark
    python run.py help
"""

import subprocess
import sys


COMMANDS = {
    "index": ["-m", "tests.test_index_pipeline"],
    "server": ["-m", "mcp_server.server"],
    "sync": ["-m", "tests.test_incremental_sync"],
    "benchmark": ["-m", "tests.test_concurrency"],
}


def print_help():
    print()
    print("=" * 70)
    print("Knowledge Retrieval System")
    print("=" * 70)
    print()
    print("Available Commands:\n")
    print("  index      Build parser output, embeddings and indexes")
    print("  server     Start the MCP server")
    print("  sync       Run Incremental Sync")
    print("  benchmark  Run concurrency benchmark")
    print("  help       Show this help message")
    print()
    print("Examples:")
    print("  python run.py index")
    print("  python run.py server")
    print("  python run.py sync")
    print("  python run.py benchmark")
    print()


def main():

    if len(sys.argv) != 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command in ("help", "-h", "--help"):
        print_help()
        return

    if command not in COMMANDS:
        print(f"\nUnknown command: {command}")
        print_help()
        return

    try:
        subprocess.run(
            [sys.executable] + COMMANDS[command],
            check=True,
        )
    except subprocess.CalledProcessError:
        print(f"\n'{command}' failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()