"""
Builds Function documents for ChromaDB.
"""

from app.schemas.chroma_document import ChromaDocument

from app.core.config import (
    FUNCTIONS_COLLECTION,
)


class FunctionDocumentBuilder:

    @staticmethod
    def build(
        parsed_function,
        embedding: list[float],
    ) -> ChromaDocument:

        # --------------------------------------------------
        # Parameters
        # --------------------------------------------------

        if parsed_function.parameters:

            parameter_lines = []

            for parameter in parsed_function.parameters:

                datatype = parameter.get("datatype") or "Any"

                parameter_lines.append(
                    f"{parameter['name']} : {datatype}"
                )

            parameters_document = "\n".join(parameter_lines)

            parameter_string = ", ".join(
                f"{p['name']}:{p.get('datatype') or 'Any'}"
                for p in parsed_function.parameters
            )

        else:

            parameters_document = "None"

            parameter_string = ""

        # --------------------------------------------------
        # Decorators
        # --------------------------------------------------

        decorators_document = (
            "\n".join(parsed_function.decorators)
            if parsed_function.decorators
            else "None"
        )

        # --------------------------------------------------
        # Return Type
        # --------------------------------------------------

        return_type = (
            parsed_function.return_type
            if parsed_function.return_type
            else "None"
        )

        # --------------------------------------------------
        # Human Readable Document
        # --------------------------------------------------

        document = "\n\n".join(
            [
                "DOCUMENT TYPE\nPython Function",

                f"FUNCTION NAME\n{parsed_function.function_name}",

                f"FILE PATH\n{parsed_function.repo_path}",

                "PURPOSE\n"
                f"{parsed_function.docstring or 'No function documentation available.'}",

                "SIGNATURE\n"
                f"{parsed_function.function_signature}",

                "PARAMETERS\n"
                f"{parameters_document}",

                "RETURN TYPE\n"
                f"{return_type}",

                "DECORATORS\n"
                f"{decorators_document}",

                "PROPERTIES\n"
                f"Async: {parsed_function.is_async}",

                (
                    "SUMMARY\n"
                    f"The function '{parsed_function.function_name}' "
                    f"accepts {len(parsed_function.parameters)} parameter(s) "
                    f"and returns '{return_type}'."
                ),

                "SOURCE CODE\n"
                f"{parsed_function.function_code}",
            ]
        )

        # --------------------------------------------------
        # IDs
        # --------------------------------------------------

        file_id = (
            f"master::{parsed_function.repo_path}"
        )

        document_id = (
            f"master::"
            f"{parsed_function.repo_path}::"
            f"{parsed_function.function_name}::"
            f"{parsed_function.start_line}"
        )

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = {

            "document_type":
                "function",

            "function_name":
                parsed_function.function_name,

            "file_path":
                parsed_function.repo_path,

            "file_id":
                file_id,

            "github_repo_path":
                parsed_function.github_url,

            "start_line":
                parsed_function.start_line,

            "end_line":
                parsed_function.end_line,

            "function_signature":
                parsed_function.function_signature,

            "parameters":
                parameter_string,

            "return_type":
                return_type,

            "decorators":
                ",".join(parsed_function.decorators),

            "is_async":
                parsed_function.is_async,

            "docstring":
                parsed_function.docstring,

            "branch":
                "master",

            "language":
                "python",
        }

        return ChromaDocument(

            collection_name=FUNCTIONS_COLLECTION,

            id=document_id,

            document=document,

            embedding=embedding,

            metadata=metadata,
        )