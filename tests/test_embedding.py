from app.parser.repository_parser import RepositoryParser
from app.chunker.ast_chunker import ASTChunker
from app.embedding.embedding_generator import EmbeddingGenerator

from app.core.config import REPOSITORIES_DIR


repository = REPOSITORIES_DIR / "fastapi-master"

# Parse
parser = RepositoryParser()
parser_result = parser.parse(repository)

# Chunk
chunker = ASTChunker()
chunk_result = chunker.build(parser_result)

# Embed
generator = EmbeddingGenerator()

embedding_result = generator.generate(chunk_result)

print()

print(f"Embeddings : {len(embedding_result.embeddings)}")

first = embedding_result.embeddings[0]

print()

print("Chunk Title :", first.chunk.title)
print("Chunk Type  :", first.chunk.chunk_type)
print("Vector Size :", len(first.vector))