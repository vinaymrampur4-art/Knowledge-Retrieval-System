"""
run.py

Entry point for the Knowledge Retrieval System.
"""

from app.core.config import REPOSITORY_FOLDER
from app.parser.repository_loader import RepositoryLoader
from app.parser.ast_parser import ASTParser
from app.writers.output_writer import OutputWriter


def main():
    """
    Main execution flow.
    """

    import sys

    repository_name = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "fastapi-master"
    )

    # -----------------------------------------
    # Load Repository
    # -----------------------------------------

    loader = RepositoryLoader(repository_name)

    python_files = loader.discover_files()

    # -----------------------------------------
    # Parse Repository
    # -----------------------------------------

    parser = ASTParser()

    result = parser.parse(python_files,loader.repository_path,)

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