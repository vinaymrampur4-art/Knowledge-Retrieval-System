"""
Converts raw ChromaDB search results into RetrievalResult objects.
"""

from app.retrieval.search_result import RetrievalResult


class ResultFormatter:

    @staticmethod
    def format(results: dict):

        formatted = []

        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for doc_id, document, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):

            metadata = metadata or {}

            # -------------------------------------------------
            # Detect document type
            # -------------------------------------------------

            if "class_name" in metadata:

                doc_type = "Class"
                name = metadata.get("class_name", "")

            elif "method_name" in metadata:

                doc_type = "Method"
                name = metadata.get("method_name", "")

            elif "function_name" in metadata:

                doc_type = "Function"
                name = metadata.get("function_name", "")

            elif "imported_name" in metadata:

                doc_type = "Import"
                name = metadata.get("imported_name", "")

            elif "constant_name" in metadata:

                doc_type = "Constant"
                name = metadata.get("constant_name", "")

            elif "file_path" in metadata:

                doc_type = "File"
                name = metadata.get("file_path", "")

            else:

                doc_type = "Unknown"
                name = doc_id

            result = RetrievalResult(

                type=doc_type,

                name=name,

                file_path=metadata.get("file_path", ""),

                github_url=metadata.get("github_repo_path", ""),

                description=metadata.get("docstring", ""),

                module=metadata.get("module_name", ""),

                signature=(
                    metadata.get("method_signature")
                    or metadata.get("function_signature")
                    or ""
                ),

                parameters=metadata.get("parameters", []),

                return_type=metadata.get("return_type", ""),

                methods=(
                    metadata.get("method_names", "")
                    .split(",")
                    if metadata.get("method_names")
                    else []
                ),

                decorators=(
                    metadata.get("decorators", "")
                    .split(",")
                    if metadata.get("decorators")
                    else []
                ),

                similarity=1 - distance,

                metadata=metadata,
            )

            formatted.append(result)

        return formatted