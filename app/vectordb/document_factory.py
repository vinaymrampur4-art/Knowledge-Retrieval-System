"""
Converts parser models into Chroma documents.
"""

from app.vectordb.builders.file_document_builder import (
    FileDocumentBuilder,
)

from app.vectordb.builders.class_document_builder import (
    ClassDocumentBuilder,
)

from app.vectordb.builders.method_document_builder import (
    MethodDocumentBuilder,
)

from app.vectordb.builders.function_document_builder import (
    FunctionDocumentBuilder,
)

from app.vectordb.builders.code_block_document_builder import (
    CodeBlockDocumentBuilder,
)


class DocumentFactory:

    # ---------------------------------------------------------
    # File
    # ---------------------------------------------------------

    @staticmethod
    def build_file(
        parsed_file,
        embedding,
    ):
        return FileDocumentBuilder.build(
            parsed_file,
            embedding,
        )

    # ---------------------------------------------------------
    # Class
    # ---------------------------------------------------------

    @staticmethod
    def build_class(
        parsed_class,
        embedding,
    ):
        return ClassDocumentBuilder.build(
            parsed_class,
            embedding,
        )

    # ---------------------------------------------------------
    # Method
    # ---------------------------------------------------------

    @staticmethod
    def build_method(
        parsed_method,
        embedding,
    ):
        return MethodDocumentBuilder.build(
            parsed_method,
            embedding,
        )

    # ---------------------------------------------------------
    # Function
    # ---------------------------------------------------------

    @staticmethod
    def build_function(
        parsed_function,
        embedding,
    ):
        return FunctionDocumentBuilder.build(
            parsed_function,
            embedding,
        )

    # ---------------------------------------------------------
    # Code Block
    # ---------------------------------------------------------

    @staticmethod
    def build_code_block(
        parsed_object,
        embedding,
    ):
        """
        Build a code block document from either a
        ParsedMethod or ParsedFunction.
        """

        return CodeBlockDocumentBuilder.build(
            parsed_object,
            embedding,
        )