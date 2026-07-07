"""
chroma_retriever.py

Performs semantic similarity search and direct document lookup
on a ChromaDB collection.

Responsibilities
----------------
1. Connect to a Chroma collection.
2. Execute vector similarity search.
3. Retrieve documents by ID.
4. Retrieve documents using metadata filters.
5. Convert raw Chroma output into SearchResult objects.
"""

from mcp_server.models import SearchFilter

from app.retrieval.search_result import SearchResult
from app.vectordb.chroma_client import ChromaClient
from app.retrieval.filters.filter_builder import FilterBuilder


class ChromaRetriever:
    """
    Retrieves documents from a ChromaDB collection.
    """

    def __init__(self):

        self.client = ChromaClient.get_client()

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        collection_name: str,
        query_embedding: list[float],
        filter: SearchFilter | None = None,
        top_k: int = 5,
    ) -> list[SearchResult]:
        """
        Search a Chroma collection using semantic similarity.

        Parameters
        ----------
        collection_name : str
            Chroma collection name.

        query_embedding : list[float]
            Embedded query vector.

        filter : SearchFilter | None
            Optional metadata filter.

        top_k : int
            Number of nearest neighbours to retrieve.

        Returns
        -------
        list[SearchResult]
        """

        print("=" * 80)
        print("CHROMA FILTER")
        print(type(filter))
        print(filter)
        print("=" * 80)

        collection = self.client.get_collection(
            name=collection_name,
        )

        response = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        results = self._build_results(
            collection_name,
            response,
        )

        results = FilterBuilder.filter_results(
            results,
            filter,
        )

        return results

    # ---------------------------------------------------------
    # Get By ID
    # ---------------------------------------------------------

    def get_by_id(
        self,
        collection_name: str,
        document_id: str,
    ) -> SearchResult | None:
        """
        Retrieve a document using its unique ID.
        """

        collection = self.client.get_collection(
            name=collection_name,
        )

        response = collection.get(
            ids=[document_id],
            include=[
                "documents",
                "metadatas",
            ],
        )

        ids = response.get("ids", [])

        if len(ids) == 0:
            return None

        documents = response.get("documents", [])
        metadatas = response.get("metadatas", [])

        return SearchResult(
            id=ids[0],
            score=1.0,
            content=documents[0],
            collection=collection_name,
            metadata=metadatas[0] if metadatas else {},
        )

    # ---------------------------------------------------------
    # Get By Attributes
    # ---------------------------------------------------------

    def get_by_attributes(
        self,
        collection_name: str,
        attributes: dict,
    ) -> list[SearchResult]:
        """
        Retrieve documents matching metadata attributes.
        """

        collection = self.client.get_collection(
            name=collection_name,
        )

        response = collection.get(
            where=attributes,
            include=[
                "documents",
                "metadatas",
            ],
        )

        ids = response.get("ids", [])
        documents = response.get("documents", [])
        metadatas = response.get("metadatas", [])

        results: list[SearchResult] = []

        for doc_id, document, metadata in zip(
            ids,
            documents,
            metadatas,
        ):

            results.append(
                SearchResult(
                    id=doc_id,
                    score=1.0,
                    content=document,
                    collection=collection_name,
                    metadata=metadata or {},
                )
            )

        return results

    # ---------------------------------------------------------
    # Internal Helpers
    # ---------------------------------------------------------

    def _build_results(
        self,
        collection_name: str,
        response: dict,
    ) -> list[SearchResult]:
        """
        Convert a Chroma query response into SearchResult objects.
        """

        search_results: list[SearchResult] = []

        ids = response.get("ids", [[]])[0]
        documents = response.get("documents", [[]])[0]
        metadatas = response.get("metadatas", [[]])[0]
        distances = response.get("distances", [[]])[0]

        for doc_id, document, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):

            score = 1.0 - float(distance)

            search_results.append(
                SearchResult(
                    id=doc_id,
                    score=score,
                    content=document,
                    collection=collection_name,
                    metadata=metadata or {},
                )
            )

        return search_results