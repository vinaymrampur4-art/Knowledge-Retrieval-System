"""
method_report_service.py

Provides method reports from the indexed repository.
"""

from app.core.config import (
    METHODS_COLLECTION,
)

from app.vectordb.chroma_client import (
    ChromaClient,
)

from mcp_server.models import (
    MethodInfo,
    MethodListResponse,
)


class MethodReportService:
    """
    Service responsible for method reports.
    """

    def __init__(self):

        self.client = ChromaClient.get_client()

    # ---------------------------------------------------------
    # List Methods
    # ---------------------------------------------------------

    def list_methods(
        self,
    ) -> MethodListResponse:
        """
        Return all indexed methods.

        Returns
        -------
        MethodListResponse
        """

        collection = self.client.get_collection(
            name=METHODS_COLLECTION,
        )

        response = collection.get(
            include=[
                "metadatas",
            ],
        )

        metadata_list = response.get(
            "metadatas",
            [],
        )

        methods = []

        for metadata in metadata_list:

            methods.append(

                MethodInfo(

                    method_name=metadata.get(
                        "method_name",
                        "",
                    ),

                    class_name=metadata.get(
                        "class_name",
                        "",
                    ),

                    file_path=metadata.get(
                        "file_path",
                        "",
                    ),

                    is_async=bool(
                        metadata.get(
                            "is_async",
                            False,
                        )
                    ),

                )

            )

        methods.sort(
            key=lambda method: (
                method.class_name.lower(),
                method.method_name.lower(),
            )
        )

        return MethodListResponse(

            total_methods=len(methods),

            methods=methods,

        )