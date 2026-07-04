"""
collections.py

Maps client-facing collection names to the internal
ChromaDB collection names used by the Knowledge Retrieval System.
"""

from app.core.config import (
    FILES_COLLECTION,
    CLASSES_COLLECTION,
    METHODS_COLLECTION,
    FUNCTIONS_COLLECTION,
    CODE_BLOCK_COLLECTION,
)

# ==========================================================
# COLLECTION MAP
# ==========================================================

COLLECTION_MAP = {
    "files": FILES_COLLECTION,
    "classes": CLASSES_COLLECTION,
    "methods": METHODS_COLLECTION,
    "functions": FUNCTIONS_COLLECTION,
    "code_blocks": CODE_BLOCK_COLLECTION,
}

# ==========================================================
# AVAILABLE COLLECTIONS
# ==========================================================

AVAILABLE_COLLECTIONS = tuple(COLLECTION_MAP.keys())


# ==========================================================
# HELPERS
# ==========================================================

def get_collection(collection_name: str | None) -> list[str] | None:
    """
    Convert a client-facing collection name into the corresponding
    ChromaDB collection.

    Parameters
    ----------
    collection_name : str | None
        Name supplied by the client.

    Returns
    -------
    list[str] | None
        Returns:
            None -> Search all collections.
            [collection] -> Search only one collection.

    Raises
    ------
    ValueError
        If an invalid collection name is supplied.
    """

    if collection_name is None:
        return None

    collection = COLLECTION_MAP.get(collection_name)

    if collection is None:

        raise ValueError(

            f"Invalid collection '{collection_name}'. "
            f"Available collections are: "
            f"{', '.join(AVAILABLE_COLLECTIONS)}."

        )

    return [collection]