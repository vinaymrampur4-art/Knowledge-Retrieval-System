"""
tests/test_sync_manager.py
"""

from app.incremental_sync.sync_manager import SyncManager


def main():

    manager = SyncManager(
        repository_name="fastapi-master",
    )

    print("=" * 80)
    print("FIRST SYNC")
    print("=" * 80)

    print(manager.is_first_sync())

    print()

    print("=" * 80)
    print("LAST SYNCED COMMIT")
    print("=" * 80)

    print(manager.get_last_synced_commit())

    print()

    print("=" * 80)
    print("LATEST COMMIT")
    print("=" * 80)

    print(manager.git_service.get_latest_commit())

    print()

    print("=" * 80)
    print("CHANGED FILES")
    print("=" * 80)

    changes = manager.get_changed_files()

    print("Added Files")
    print(changes.added)

    print()

    print("Modified Files")
    print(changes.modified)

    print()

    print("Deleted Files")
    print(changes.deleted)

    print()

    print("=" * 80)
    print("SAVING SYNC STATE")
    print("=" * 80)

    manager.save_sync_state()

    print("Sync State Saved Successfully")

    print()

    print("=" * 80)
    print("UPDATED SYNC STATE")
    print("=" * 80)

    print(
        manager.git_service.load_sync_state()
    )


if __name__ == "__main__":
    main()