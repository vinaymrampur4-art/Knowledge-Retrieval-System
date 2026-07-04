"""
Builds ChromaDocuments from ParserResult.
"""

from app.vectordb.document_factory import (
    DocumentFactory,
)


class ParserDocumentFactory:

    @staticmethod
    def build(parser_result):

        documents = []

        # ---------------------------------------------------------
        # Files
        # ---------------------------------------------------------

        for parsed_file in parser_result.files:

            documents.append(
                DocumentFactory.build_file(
                    parsed_file,
                    embedding=[],
                )
            )

        # ---------------------------------------------------------
        # Classes
        # ---------------------------------------------------------

        for parsed_class in parser_result.classes:

            documents.append(
                DocumentFactory.build_class(
                    parsed_class,
                    embedding=[],
                )
            )

            # -----------------------------------------------------
            # Methods
            # -----------------------------------------------------

            for method in parsed_class.methods:

                # Metadata document
                documents.append(
                    DocumentFactory.build_method(
                        method,
                        embedding=[],
                    )
                )

                # Code block document
                documents.append(
                    DocumentFactory.build_code_block(
                        method,
                        embedding=[],
                    )
                )

        # ---------------------------------------------------------
        # Functions
        # ---------------------------------------------------------

        for function in parser_result.functions:

            # Metadata document
            documents.append(
                DocumentFactory.build_function(
                    function,
                    embedding=[],
                )
            )

            # Code block document
            documents.append(
                DocumentFactory.build_code_block(
                    function,
                    embedding=[],
                )
            )

        return documents