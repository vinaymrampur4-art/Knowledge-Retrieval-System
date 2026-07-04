from app.retrieval.sparse.bm25_index_builder import (
    BM25IndexBuilder,
)
from app.retrieval.sparse.bm25_retriever import (
    BM25Retriever,
)

documents = [

    {
        "id": "1",

        "content": "class APIRouter",

        "metadata": {
            "file": "routing.py",
        },
    },

    {
        "id": "2",

        "content": "class FastAPI",

        "metadata": {
            "file": "applications.py",
        },
    },

    {
        "id": "3",

        "content": "def include_router",

        "metadata": {
            "file": "routing.py",
        },
    },
]

builder = BM25IndexBuilder()

index = builder.build(documents)

retriever = BM25Retriever(

    index,

    builder.get_store(),

)

results = retriever.search(

    "APIRouter",

    top_k=5,

)

print()

print("=" * 80)

for result in results:

    print(result.id)

    print(result.score)

    print(result.content)

    print(result.metadata)

    print("-" * 80)