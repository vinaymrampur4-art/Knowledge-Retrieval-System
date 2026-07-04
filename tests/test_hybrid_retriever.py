from app.parser.repository_parser import RepositoryParser
from app.indexing.index_pipeline import IndexPipeline
from app.retrieval.hybrid.hybrid_retriever import HybridRetriever
from app.core.config import REPOSITORIES_DIR

repository = REPOSITORIES_DIR / "fastapi-master"

# Build indexes
parser = RepositoryParser()
parser_result = parser.parse(repository)

pipeline = IndexPipeline()
pipeline.run(parser_result)

# Hybrid retrieval
retriever = HybridRetriever()

results = retriever.search(
    query="Where is APIRouter implemented?",
    top_k=10,
)

print(results)