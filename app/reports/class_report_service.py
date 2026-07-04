"""
class_report_service.py

Provides class reports from the indexed repository.
"""

from app.core.config import (
    CLASSES_COLLECTION,
)

from app.vectordb.chroma_client import (
    ChromaClient,
)

from mcp_server.models import (
    ClassInfo,
    ClassListResponse,
)


class ClassReportService:
    """
    Service responsible for class reports.
    """

    def __init__(self):

        self.client = ChromaClient.get_client()

    # ---------------------------------------------------------
    # List Classes
    # ---------------------------------------------------------

    def list_classes(
        self,
    ) -> ClassListResponse:
        """
        Return all indexed classes.

        Returns
        -------
        ClassListResponse
        """

        collection = self.client.get_collection(
            name=CLASSES_COLLECTION,
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

        classes = []

        for metadata in metadata_list:

            classes.append(

                ClassInfo(

                    class_name=metadata.get(
                        "class_name",
                        "",
                    ),

                    file_path=metadata.get(
                        "file_path",
                        "",
                    ),

                    method_count=int(
                        metadata.get(
                            "method_count",
                            0,
                        )
                    ),

                    inheritance=metadata.get(
                        "inheritance_classes",
                        "",
                    ),

                )

            )

        classes.sort(
            key=lambda cls: cls.class_name.lower()
        )

        return ClassListResponse(

            total_classes=len(classes),

            classes=classes,

        )