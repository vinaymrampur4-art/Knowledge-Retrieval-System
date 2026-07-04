"""
file_report_service.py

Provides file reports from the indexed repository.
"""

from app.core.config import (
    FILES_COLLECTION,
)

from app.vectordb.chroma_client import (
    ChromaClient,
)

from mcp_server.models import (
    FileInfo,
    FileListResponse,
)


class FileReportService:
    """
    Service responsible for file reports.
    """

    def __init__(self):

        self.client = ChromaClient.get_client()

    # ---------------------------------------------------------
    # List Files
    # ---------------------------------------------------------

    def list_files(
        self,
    ) -> FileListResponse:
        """
        Return all indexed files.

        Returns
        -------
        FileListResponse
        """

        collection = self.client.get_collection(
            name=FILES_COLLECTION,
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

        files = []

        for metadata in metadata_list:

            files.append(

                FileInfo(

                    file_path=metadata.get(
                        "file_path",
                        "",
                    ),

                    language=metadata.get(
                        "language",
                        "unknown",
                    ),

                )

            )

        files.sort(
            key=lambda file: file.file_path
        )

        return FileListResponse(

            total_files=len(files),

            files=files,

        )