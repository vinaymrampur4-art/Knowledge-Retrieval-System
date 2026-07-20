"""
Manual test for Incremental Sync.
"""

from app.incremental_sync.sync_manager import SyncManager

REPOSITORY_NAME = "fastapi-master"


def main():

    print("=" * 80)
    print("Starting Incremental Sync")
    print("=" * 80)

    manager = SyncManager(
        REPOSITORY_NAME
    )

    manager.sync()

    print()

    print("=" * 80)
    print("Incremental Sync Finished Successfully")
    print("=" * 80)


if __name__ == "__main__":
    main()