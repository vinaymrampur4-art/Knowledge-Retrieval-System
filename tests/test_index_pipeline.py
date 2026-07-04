from app.parser.repository_parser import RepositoryParser

from app.indexing.index_pipeline import (
    IndexPipeline,
)

from app.core.config import (
    REPOSITORIES_DIR,
)

repository = (
    REPOSITORIES_DIR / "fastapi-master"
)

parser = RepositoryParser()

result = parser.parse(
    repository
)

pipeline = IndexPipeline()

pipeline.run(result)