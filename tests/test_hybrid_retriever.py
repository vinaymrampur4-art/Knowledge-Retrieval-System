from app.parser.repository_parser import RepositoryParser
from app.indexing.index_pipeline import IndexPipeline
from app.retrieval.hybrid.hybrid_retriever import HybridRetriever
from app.core.config import REPOSITORIES_DIR, REPOSITORY_FOLDER

repository = REPOSITORIES_DIR / REPOSITORY_FOLDER

# Build indexes
parser = RepositoryParser()
parser_result = parser.parse(repository)

repository_name = parser_result.files[0].repository_name

pipeline = IndexPipeline(
    repository_name
)

pipeline.run(parser_result)

retriever = HybridRetriever(
    repository_name
)

results = retriever.search(
    query="Where is APIRouter implemented?",
    top_k=10,
)

print(results)