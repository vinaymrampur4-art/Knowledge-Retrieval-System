"""
Builds Class documents for ChromaDB.
"""

from app.schemas.chroma_document import ChromaDocument

from app.core.config import (
    CLASSES_COLLECTION,
)


class ClassDocumentBuilder:

    @staticmethod
    def build(
        parsed_class,
        embedding: list[float],
    ) -> ChromaDocument:

        # --------------------------------------------------
        # Extract Information
        # --------------------------------------------------

        method_names = [
            method.method_name
            for method in parsed_class.methods
        ]

        base_classes = parsed_class.inherits or []

        # --------------------------------------------------
        # Human Readable Document
        # --------------------------------------------------

        document = "\n\n".join(
            [
                "DOCUMENT TYPE\nPython Class",

                f"CLASS NAME\n{parsed_class.class_name}",

                f"FILE PATH\n{parsed_class.repo_path}",

                "PURPOSE\n"
                f"{parsed_class.class_docstring or 'No class documentation available.'}",

                "BASE CLASSES\n" + (
                    "\n".join(base_classes)
                    if base_classes else "None"
                ),

                "METHODS\n" + (
                    "\n".join(method_names)
                    if method_names else "None"
                ),

                (
                    "SUMMARY\n"
                    f"The class '{parsed_class.class_name}' "
                    f"inherits from {len(base_classes)} base class(es) "
                    f"and contains {len(method_names)} method(s)."
                ),

                "SOURCE CODE\n"
                f"{parsed_class.class_code or 'Source code unavailable.'}",
            ]
        )

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = {

            "document_type":
                "class",

            "class_name":
                parsed_class.class_name,

            "file_path":
                parsed_class.repo_path,

            "github_repo_path":
                parsed_class.github_url,

            "start_line":
                parsed_class.start_line,

            "end_line":
                parsed_class.end_line,

            "inheritance_classes":
                ",".join(base_classes),

            "method_count":
                len(method_names),

            "method_names":
                ",".join(method_names),

            "docstring":
                parsed_class.class_docstring,

            "branch":
                "master",

            "language":
                "python",
        }

        # --------------------------------------------------
        # Document ID
        # --------------------------------------------------

        document_id = (
            f"master::"
            f"{parsed_class.repo_path}::"
            f"{parsed_class.class_name}"
        )

        return ChromaDocument(

            collection_name=CLASSES_COLLECTION,

            id=document_id,

            document=document,

            embedding=embedding,

            metadata=metadata,
        )