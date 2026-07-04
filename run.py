"""
run.py

Entry point for the Knowledge Retrieval System.
"""

from app.parser.repository_loader import RepositoryLoader
from app.parser.ast_parser import ASTParser
from app.writers.output_writer import OutputWriter


def main():
    """
    Main execution flow.
    """

    repository_name = "fastapi-master"

    # -----------------------------------------
    # Load Repository
    # -----------------------------------------

    loader = RepositoryLoader(repository_name)

    python_files = loader.discover_files()

    # -----------------------------------------
    # Parse Repository
    # -----------------------------------------

    parser = ASTParser()

    result = parser.parse(python_files)

    # -----------------------------------------
    # Write Outputs
    # -----------------------------------------

    output_path = OutputWriter.write(
        repository_name=repository_name,
        result=result,
    )

    # -----------------------------------------
    # Summary
    # -----------------------------------------

    print()

    print("=" * 60)

    print("Repository parsed successfully.")

    print(f"Output written to:\n{output_path}")

    print("=" * 60)


if __name__ == "__main__":
    main()