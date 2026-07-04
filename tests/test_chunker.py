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
"""

from app.parser.repository_parser import RepositoryParser
from app.chunker.ast_chunker import ASTChunker

from app.core.config import REPOSITORIES_DIR

from app.chunker.splitter import ChunkSplitter  

from app.exporter.json_exporter import JSONExporter
from app.exporter.manifest import ManifestBuilder
from app.exporter.statistics import StatisticsBuilder

from app.core.config import JSON_OUTPUT_DIR


def main():

    repo_path = REPOSITORIES_DIR / "fastapi-master"

    print("=" * 60)
    print("Parsing Repository...")
    print("=" * 60)

    parser = RepositoryParser()

    parser_result = parser.parse(repo_path)

    print()

    print("=" * 60)
    print("Generating Semantic Chunks...")
    print("=" * 60)

    chunker = ASTChunker()

    chunk_result = chunker.build(parser_result)

    splitter = ChunkSplitter(max_tokens=500)

    chunk_result = splitter.split(chunk_result)

    chunks = chunk_result.chunks

    print()

    print("=" * 60)
    print("STATISTICS")
    print("=" * 60)

    print(f"Total Chunks      : {len(chunks)}")

    class_chunks = sum(
        1 for c in chunks if c.chunk_type == "class"
    )

    method_chunks = sum(
        1 for c in chunks if c.chunk_type == "method"
    )

    function_chunks = sum(
        1 for c in chunks if c.chunk_type == "function"
    )

    import_chunks = sum(
        1 for c in chunks if c.chunk_type == "import"
    )

    constant_chunks = sum(
        1 for c in chunks if c.chunk_type == "constant"
    )

    print(f"Classes           : {class_chunks}")
    print(f"Methods           : {method_chunks}")
    print(f"Functions         : {function_chunks}")
    print(f"Imports           : {import_chunks}")
    print(f"Constants         : {constant_chunks}")

    total_tokens = sum(
        chunk.token_count
        for chunk in chunks
    )

    print(f"Estimated Tokens  : {total_tokens}")

    print()

    print("=" * 60)
    print("FIRST FIVE CHUNKS")
    print("=" * 60)

    for chunk in chunks[:5]:

        print()

        print(f"ID      : {chunk.chunk_id}")
        print(f"TYPE    : {chunk.chunk_type}")
        print(f"TITLE   : {chunk.title}")
        print(f"TOKENS  : {chunk.token_count}")
        print(f"PARENT  : {chunk.parent_id}")

        print("-" * 50)

        exporter = JSONExporter()

    exporter.export(
        chunk_result,
        JSON_OUTPUT_DIR,
    )

    ManifestBuilder().build(
        chunk_result,
        JSON_OUTPUT_DIR,
        "fastapi-master",
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

