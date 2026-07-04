from app.parser.repository_loader import RepositoryLoader


def main():

    print("\nAvailable Repositories:")
    print("-" * 40)

    repos = RepositoryLoader.list_repositories()

    for repo in repos:
        print(repo)

    print("-" * 40)

    repository_name = input(
        "\nEnter repository name: "
    ).strip()

    loader = RepositoryLoader(repository_name)

    files = loader.discover_files()

    print("\n" + "=" * 80)
    print(f"Repository : {repository_name}")
    print(f"Python Files : {len(files)}")
    print("=" * 80)

    for file in files:
        print(file)


if __name__ == "__main__":
    main()