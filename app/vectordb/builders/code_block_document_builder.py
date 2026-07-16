"""
Builds executable code block documents for ChromaDB.

Unlike MethodDocumentBuilder and FunctionDocumentBuilder,
this builder stores executable source code with lightweight
metadata so semantic search focuses on implementation.
"""

from app.schemas.chroma_document import ChromaDocument

from app.core.config import (
    CODE_BLOCK_COLLECTION,
)


class CodeBlockDocumentBuilder:

    @staticmethod
    def build(
        parsed_object,
        embedding: list[float],
    ) -> ChromaDocument:

        # --------------------------------------------------
        # Determine Block Type
        # --------------------------------------------------

        if hasattr(parsed_object, "method_name"):

            block_type = "method"

            block_name = parsed_object.method_name

            class_name = parsed_object.class_name

            source_code = (
                parsed_object.method_code or ""
            )

        else:

            block_type = "function"

            block_name = (
                parsed_object.function_name
            )

            class_name = ""

            source_code = (
                parsed_object.function_code or ""
            )

        # --------------------------------------------------
        # Search Document
        # --------------------------------------------------

        header = [
            f"Repository: {parsed_object.repository_name}",
            f"Branch: {parsed_object.branch}",
            f"Type: {block_type}",
            f"Name: {block_name}",
            f"Class: {class_name or 'None'}",
            f"File: {parsed_object.repo_path}",
            "",
        ]

        document = (
            "\n".join(header)
            + source_code
        )

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = {

            "document_type":
                "code_block",

            "repository_name":
                parsed_object.repository_name,

            "branch":
                parsed_object.branch,

            "github_repository":
                parsed_object.github_repository,

            "block_type":
                block_type,

            "block_name":
                block_name,

            "class_name":
                class_name,

            "file_path":
                parsed_object.repo_path,

            "github_repo_path":
                parsed_object.github_url,

            "start_line":
                parsed_object.start_line,

            "end_line":
                parsed_object.end_line,

            "language":
                "python",
        }

        # --------------------------------------------------
        # Unique ID
        # --------------------------------------------------

        if block_type == "method":

            document_id = (

                f"code::"

                f"{parsed_object.repository_name}::"

                f"{parsed_object.branch}::"

                f"{parsed_object.repo_path}::"

                f"{parsed_object.class_name}::"

                f"{parsed_object.method_name}::"

                f"{parsed_object.start_line}"
            )

        else:

            document_id = (

                f"code::"

                f"{parsed_object.repository_name}::"

                f"{parsed_object.branch}::"

                f"{parsed_object.repo_path}::"

                f"{parsed_object.function_name}::"

                f"{parsed_object.start_line}"
            )

        # --------------------------------------------------
        # Build Document
        # --------------------------------------------------

        return ChromaDocument(

            collection_name=CODE_BLOCK_COLLECTION,

            id=document_id,

            document=document,

            embedding=embedding,

            metadata=metadata,
        )