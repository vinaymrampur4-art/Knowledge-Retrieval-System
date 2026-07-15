"""
Test the complete AST Chunking pipeline.

Flow:

Repository
    ↓
RepositoryParser
    ↓
ParserResult
    ↓
ASTChunker
    ↓
ChunkResult
    ↓
ChunkSplitter
"""

from app.parser.repository_parser import RepositoryParser
from app.chunker.ast_chunker import ASTChunker
from app.chunker.splitter import ChunkSplitter

from app.exporter.json_exporter import JSONExporter
from app.exporter.manifest import ManifestBuilder
from app.exporter.statistics import StatisticsBuilder

from app.core.config import (
    REPOSITORIES_DIR,
    REPOSITORY_FOLDER,
    REPOSITORY_NAME,
    JSON_OUTPUT_DIR,
    CHUNK_MAX_TOKENS,
)


def main():

    repo_path = (
        REPOSITORIES_DIR /
        REPOSITORY_FOLDER
    )

    print("=" * 60)
    print("Parsing Repository...")
    print("=" * 60)

    parser = RepositoryParser()

    parser_result = parser.parse(
        repo_path
    )

    print()

    print("=" * 60)
    print("Generating Semantic Chunks...")
    print("=" * 60)

    chunker = ASTChunker()

    chunk_result = chunker.build(
        parser_result
    )

    # --------------------------------------------------------
    # Split oversized chunks using configured chunk size
    # --------------------------------------------------------

    splitter = ChunkSplitter(
        max_tokens=CHUNK_MAX_TOKENS,
    )

    chunk_result = splitter.split(
        chunk_result
    )

    chunks = chunk_result.chunks

    print()

    print("=" * 60)
    print("STATISTICS")
    print("=" * 60)

    print(
        f"Chunk Size Limit  : "
        f"{CHUNK_MAX_TOKENS}"
    )

    print(
        f"Total Chunks      : "
        f"{len(chunks)}"
    )

    class_chunks = sum(
        1
        for chunk in chunks
        if chunk.chunk_type == "class"
    )

    method_chunks = sum(
        1
        for chunk in chunks
        if chunk.chunk_type == "method"
    )

    function_chunks = sum(
        1
        for chunk in chunks
        if chunk.chunk_type == "function"
    )

    import_chunks = sum(
        1
        for chunk in chunks
        if chunk.chunk_type == "import"
    )

    constant_chunks = sum(
        1
        for chunk in chunks
        if chunk.chunk_type == "constant"
    )

    print(
        f"Classes           : "
        f"{class_chunks}"
    )

    print(
        f"Methods           : "
        f"{method_chunks}"
    )

    print(
        f"Functions         : "
        f"{function_chunks}"
    )

    print(
        f"Imports           : "
        f"{import_chunks}"
    )

    print(
        f"Constants         : "
        f"{constant_chunks}"
    )

    total_tokens = sum(
        chunk.token_count
        for chunk in chunks
    )

    print(
        f"Estimated Tokens  : "
        f"{total_tokens}"
    )

    print()

    print("=" * 60)
    print("FIRST FIVE CHUNKS")
    print("=" * 60)

    for chunk in chunks[:5]:

        print()

        print(
            f"ID      : "
            f"{chunk.chunk_id}"
        )

        print(
            f"TYPE    : "
            f"{chunk.chunk_type}"
        )

        print(
            f"TITLE   : "
            f"{chunk.title}"
        )

        print(
            f"TOKENS  : "
            f"{chunk.token_count}"
        )

        print(
            f"PARENT  : "
            f"{chunk.parent_id}"
        )

        print("-" * 50)

    # --------------------------------------------------------
    # Export Results
    # --------------------------------------------------------

    exporter = JSONExporter()

    exporter.export(
        chunk_result,
        JSON_OUTPUT_DIR,
    )

    ManifestBuilder().build(
        chunk_result,
        JSON_OUTPUT_DIR,
        REPOSITORY_NAME,
    )

    StatisticsBuilder().build(
        chunk_result,
        JSON_OUTPUT_DIR,
    )

    print()

    print("=" * 60)
    print("JSON EXPORT COMPLETED")
    print("=" * 60)

    print(JSON_OUTPUT_DIR)


if __name__ == "__main__":
    main()