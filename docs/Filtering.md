# Metadata Filtering

The retrieval system supports metadata filtering.

Supported operators:

- equals
- contains
- startswith
- endswith
- !=
- >
- >=
- <
- <=

---

## Native Chroma Filters

Supported operators are converted into ChromaDB where clauses whenever possible.

Example:

{
    "class_name": "APIRouter"
}

Example:

{
    "file_path": {
        "$contains": "routing.py"
    }
}