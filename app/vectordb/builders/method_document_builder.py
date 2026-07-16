"""
Builds Method documents for ChromaDB.
"""

from app.schemas.chroma_document import ChromaDocument

from app.core.config import (
    METHODS_COLLECTION,
)


class MethodDocumentBuilder:

    @staticmethod
    def build(
        parsed_method,
        embedding: list[float],
    ) -> ChromaDocument:

        # --------------------------------------------------
        # Parameters
        # --------------------------------------------------

        if parsed_method.parameters:

            parameter_lines = []

            for parameter in parsed_method.parameters:

                datatype = (
                    parameter.get("datatype")
                    or "Any"
                )

                parameter_lines.append(
                    f"{parameter['name']} : {datatype}"
                )

            parameters_document = "\n".join(
                parameter_lines
            )

            parameter_string = ", ".join(
                f"{p['name']}:{p.get('datatype') or 'Any'}"
                for p in parsed_method.parameters
            )

        else:

            parameters_document = "None"

            parameter_string = ""

        # --------------------------------------------------
        # Decorators
        # --------------------------------------------------

        decorators_document = (
            "\n".join(parsed_method.decorators)
            if parsed_method.decorators
            else "None"
        )

        # --------------------------------------------------
        # Return Type
        # --------------------------------------------------

        return_type = (
            parsed_method.return_type
            if parsed_method.return_type
            else "None"
        )

        # --------------------------------------------------
        # Human Readable Document
        # --------------------------------------------------

        document = "\n\n".join(
            [
                "DOCUMENT TYPE\nPython Method",

                f"REPOSITORY\n{parsed_method.repository_name}",

                f"BRANCH\n{parsed_method.branch}",

                f"METHOD NAME\n{parsed_method.method_name}",

                f"CLASS\n{parsed_method.class_name}",

                f"FILE PATH\n{parsed_method.repo_path}",

                "PURPOSE\n"
                f"{parsed_method.docstring or 'No method documentation available.'}",

                "SIGNATURE\n"
                f"{parsed_method.method_signature}",

                "PARAMETERS\n"
                f"{parameters_document}",

                "RETURN TYPE\n"
                f"{return_type}",

                "DECORATORS\n"
                f"{decorators_document}",

                "PROPERTIES\n"
                f"Async: {parsed_method.is_async}\n"
                f"Static: {parsed_method.is_static}\n"
                f"Private: {parsed_method.is_private}",

                (
                    "SUMMARY\n"
                    f"The method '{parsed_method.method_name}' "
                    f"belongs to class '{parsed_method.class_name}' "
                    f"in repository '{parsed_method.repository_name}'. "
                    f"It accepts {len(parsed_method.parameters)} "
                    f"parameter(s) and returns '{return_type}'."
                ),

                "SOURCE CODE\n"
                f"{parsed_method.method_code}",
            ]
        )

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = {

            "document_type":
                "method",

            "repository_name":
                parsed_method.repository_name,

            "branch":
                parsed_method.branch,

            "github_repository":
                parsed_method.github_repository,

            "method_name":
                parsed_method.method_name,

            "class_name":
                parsed_method.class_name,

            "file_path":
                parsed_method.repo_path,

            "github_repo_path":
                parsed_method.github_url,

            "start_line":
                parsed_method.start_line,

            "end_line":
                parsed_method.end_line,

            "method_signature":
                parsed_method.method_signature,

            "parameters":
                parameter_string,

            "return_type":
                return_type,

            "decorators":
                ",".join(parsed_method.decorators),

            "is_async":
                parsed_method.is_async,

            "is_private":
                parsed_method.is_private,

            "is_static":
                parsed_method.is_static,

            "docstring":
                parsed_method.docstring,

            "language":
                "python",
        }

        # --------------------------------------------------
        # Document ID
        # --------------------------------------------------

        document_id = (
            f"{parsed_method.repository_name}::"
            f"{parsed_method.branch}::"
            f"{parsed_method.repo_path}::"
            f"{parsed_method.class_name}::"
            f"{parsed_method.method_name}::"
            f"{parsed_method.start_line}"
        )

        return ChromaDocument(

            collection_name=METHODS_COLLECTION,

            id=document_id,

            document=document,

            embedding=embedding,

            metadata=metadata,
        )