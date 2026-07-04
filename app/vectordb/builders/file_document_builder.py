"""
Builds File documents for ChromaDB.
"""

from app.schemas.chroma_document import ChromaDocument

from app.core.config import (
    FILES_COLLECTION,
)


class FileDocumentBuilder:

    @staticmethod
    def build(
        parsed_file,
        embedding: list[float],
    ) -> ChromaDocument:

        # --------------------------------------------------
        # Extract Information
        # --------------------------------------------------

        class_names = [
            cls.class_name
            for cls in parsed_file.classes
        ]

        function_names = [
            fn.function_name
            for fn in parsed_file.functions
        ]

        import_names = [
            imp.module
            for imp in parsed_file.imports
        ]

        constant_names = [
            constant.constant_name
            for constant in parsed_file.constants
        ]

        # --------------------------------------------------
        # Human Readable Document
        # --------------------------------------------------

        document = "\n\n".join(
            [
                "DOCUMENT TYPE\nPython File",

                f"MODULE\n{parsed_file.module_name}",

                f"FILE PATH\n{parsed_file.repo_path}",

                f"PURPOSE\n{parsed_file.docstring or 'No module documentation available.'}",

                "IMPORTS\n" + (
                    "\n".join(import_names)
                    if import_names else "None"
                ),

                "CLASSES\n" + (
                    "\n".join(class_names)
                    if class_names else "None"
                ),

                "FUNCTIONS\n" + (
                    "\n".join(function_names)
                    if function_names else "None"
                ),

                "GLOBAL CONSTANTS\n" + (
                    "\n".join(constant_names)
                    if constant_names else "None"
                ),

                (
                    "SUMMARY\n"
                    f"This Python module contains "
                    f"{len(class_names)} classes, "
                    f"{len(function_names)} functions, "
                    f"{len(import_names)} imports, and "
                    f"{len(constant_names)} global constants."
                ),
            ]
        )

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = {

            "document_type":
                "file",

            "module_name":
                parsed_file.module_name,

            "file_path":
                parsed_file.repo_path,

            "github_repo_path":
                parsed_file.github_url,

            "class_count":
                len(parsed_file.classes),

            "function_count":
                len(parsed_file.functions),

            "imports":
                ",".join(import_names),

            "global_constants":
                ",".join(constant_names),

            "docstring":
                parsed_file.docstring,

            "branch":
                "master",

            "language":
                "python",
        }

        # --------------------------------------------------
        # Document ID
        # --------------------------------------------------

        document_id = (
            f"master::{parsed_file.repo_path}"
        )

        return ChromaDocument(

            collection_name=FILES_COLLECTION,

            id=document_id,

            document=document,

            embedding=embedding,

            metadata=metadata,
        )