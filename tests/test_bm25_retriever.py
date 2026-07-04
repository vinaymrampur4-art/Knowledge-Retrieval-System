"""
Test BM25 retrieval on indexed repository.
"""

from app.parser.repository_parser import RepositoryParser

from app.indexing.index_pipeline import IndexPipeline

from app.retrieval.sparse.bm25_retriever import BM25Retriever

from app.core.config import REPOSITORIES_DIR


repository = REPOSITORIES_DIR / "fastapi-master"

parser = RepositoryParser()

parser_result = parser.parse(repository)

pipeline = IndexPipeline()

pipeline.run(parser_result)

retriever = BM25Retriever()

results = retriever.search(

    query="Where is APIRouter implemented?",

    top_k=10,

)

print()

print("=" * 100)
print("BM25 Retrieval")
print("=" * 100)

for index, result in enumerate(results, start=1):

    print()

    print("-" * 100)

    print(f"Result #{index}")

    print("-" * 100)

    print(f"Score      : {result.score:.4f}")

    print(f"ID         : {result.id}")

    print(f"Collection : {result.collection}")

    print()

    print("Metadata")

    for key, value in result.metadata.items():

        print(f"{key:20}: {value}")