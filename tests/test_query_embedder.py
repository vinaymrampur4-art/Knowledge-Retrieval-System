from app.retrieval.query_embedder import (
    QueryEmbedder,
)


embedder = QueryEmbedder()

vector = embedder.embed(
    "Where is APIRouter implemented?"
)

print(len(vector))
print(vector[:10])