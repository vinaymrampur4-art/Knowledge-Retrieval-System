"""
tests/test_git_service.py
"""

from app.incremental_sync.git_service import GitService


def main():

    service = GitService(
        repository_name="fastapi-master",
    )

    print("=" * 80)
    print("REPOSITORY EXISTS")
    print("=" * 80)

    print(
        service.repository_exists()
    )

    print()

    print("=" * 80)
    print("SYNC FILE EXISTS")
    print("=" * 80)

    print(
        service.sync_file_exists()
    )

    print()

    print("=" * 80)
    print("SAVING STATE")
    print("=" * 80)

    service.save_sync_state(
        {
            "last_commit": "abc123",
            "last_sync_time": "2026-07-18T21:00:00",
        }
    )

    print("State Saved")

    print()

    print("=" * 80)
    print("LOADING STATE")
    print("=" * 80)

    print(
        service.load_sync_state()
    )

    print()

    print("=" * 80)
    print("CURRENT BRANCH")
    print("=" * 80)

    print(
        service.get_current_branch()
    )

    print()

    print("=" * 80)
    print("LATEST COMMIT")
    print("=" * 80)

    print(
        service.get_latest_commit()
    )


if __name__ == "__main__":
    main()