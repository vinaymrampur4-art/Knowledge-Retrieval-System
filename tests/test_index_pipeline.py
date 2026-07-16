from app.parser.repository_parser import RepositoryParser

from app.indexing.index_pipeline import (
    IndexPipeline,
)

from app.core.config import (
    REPOSITORIES_DIR,
    REPOSITORY_FOLDER,
)

repository = (
    REPOSITORIES_DIR / REPOSITORY_FOLDER
)

parser = RepositoryParser()

result = parser.parse(
    repository
)

repository_name = result.files[0].repository_name

pipeline = IndexPipeline(
    repository_name
)

pipeline.run(result)