"""
ast_chunker.py

Converts ParserResult into semantic ParsedChunks.

Pipeline:

Repository
    ↓
RepositoryParser
    ↓
ParserResult
    ↓
ASTChunker
    ↓
ChunkResult
"""

from __future__ import annotations

from app.models.parser_result import ParserResult
from app.models.chunk_result import ChunkResult
from app.models.parsed_chunk import ParsedChunk

from app.chunker.chunk_utils import (
    generate_chunk_id,
    estimate_tokens,
)

from app.chunker.hierarchy import (
    ChunkHierarchy,
    ChunkNode,
)


class ASTChunker:
    """
    Converts parsed objects into semantic chunks.
    """

    def __init__(self):
        self.result = ChunkResult()
        self.hierarchy = ChunkHierarchy()

    # --------------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------------

    def build(
        self,
        parser_result: ParserResult,
    ) -> ChunkResult:

        self.result = ChunkResult()
        self.hierarchy = ChunkHierarchy()

        self._process_classes(parser_result)

        self._process_functions(parser_result)

        self._process_imports(parser_result)

        self._process_constants(parser_result)

        return self.result

    # --------------------------------------------------------
    # CLASSES
    # --------------------------------------------------------

    def _process_classes(
        self,
        parser_result: ParserResult,
    ):

        for parsed_class in parser_result.classes:

            chunk = ParsedChunk(

                chunk_id=generate_chunk_id(
                    parsed_class.repo_path,
                    "class",
                    parsed_class.class_name,
                    parsed_class.start_line,
                    parsed_class.end_line,
                ),

                chunk_type="class",

                title=parsed_class.class_name,

                content=parsed_class.class_code,

                metadata={
                    "file": parsed_class.file,
                    "repo_path": parsed_class.repo_path,
                    "github_url": parsed_class.github_url,
                    "inherits": parsed_class.inherits,
                    "docstring": parsed_class.class_docstring,
                    "start_line": parsed_class.start_line,
                    "end_line": parsed_class.end_line,
                },
            )

            chunk.token_count = estimate_tokens(chunk.content)

            self.result.chunks.append(chunk)

            self.hierarchy.add_node(
                ChunkNode(
                    chunk_id=chunk.chunk_id,
                    name=chunk.title,
                    chunk_type="class",
                )
            )

            self._process_methods(
                parsed_class,
                chunk.chunk_id,
            )

    # --------------------------------------------------------
    # METHODS
    # --------------------------------------------------------

    def _process_methods(
        self,
        parsed_class,
        parent_chunk_id: str,
    ):

        for method in parsed_class.methods:

            chunk = ParsedChunk(

                chunk_id=generate_chunk_id(
                    method.repo_path,
                    "method",
                    method.method_name,
                    method.start_line,
                    method.end_line,
                ),

                chunk_type="method",

                title=method.method_name,

                content=method.method_code,

                metadata={
                    "class": method.class_name,
                    "parameters": method.parameters,
                    "return_type": method.return_type,
                    "decorators": method.decorators,
                    "docstring": method.docstring,
                    "start_line": method.start_line,
                    "end_line": method.end_line,
                    "is_async": method.is_async,
                    "is_private": method.is_private,
                    "is_static": method.is_static,
                },
            )

            chunk.parent_id = parent_chunk_id

            chunk.token_count = estimate_tokens(chunk.content)

            self.result.chunks.append(chunk)

            self.hierarchy.add_node(
                ChunkNode(
                    chunk_id=chunk.chunk_id,
                    name=chunk.title,
                    chunk_type="method",
                )
            )

            self.hierarchy.connect(
                parent_chunk_id,
                chunk.chunk_id,
            )

    # --------------------------------------------------------
    # FUNCTIONS
    # --------------------------------------------------------

    def _process_functions(
        self,
        parser_result: ParserResult,
    ):

        for function in parser_result.functions:

            chunk = ParsedChunk(

                chunk_id=generate_chunk_id(
                    function.repo_path,
                    "function",
                    function.function_name,
                    function.start_line,
                    function.end_line,
                ),

                chunk_type="function",

                title=function.function_name,

                content=function.function_code,

                metadata={
                    "parameters": function.parameters,
                    "return_type": function.return_type,
                    "decorators": function.decorators,
                    "docstring": function.docstring,
                    "is_async": function.is_async,
                    "start_line": function.start_line,
                    "end_line": function.end_line,
                },
            )

            chunk.token_count = estimate_tokens(chunk.content)

            self.result.chunks.append(chunk)

            self.hierarchy.add_node(
                ChunkNode(
                    chunk_id=chunk.chunk_id,
                    name=chunk.title,
                    chunk_type="function",
                )
            )

    # --------------------------------------------------------
    # IMPORTS
    # --------------------------------------------------------

    def _process_imports(
        self,
        parser_result: ParserResult,
    ):

        for imp in parser_result.imports:

            content = f"{imp.import_type} {imp.imported_name}"

            chunk = ParsedChunk(

                chunk_id=generate_chunk_id(
                    imp.repo_path,
                    "import",
                    imp.imported_name or "",
                    imp.line_number,
                    imp.line_number,
                ),

                chunk_type="import",

                title=imp.imported_name or imp.module,

                content=content,

                metadata={
                    "module": imp.module,
                    "alias": imp.alias,
                    "line": imp.line_number,
                },
            )

            chunk.token_count = estimate_tokens(chunk.content)

            self.result.chunks.append(chunk)

    # --------------------------------------------------------
    # CONSTANTS
    # --------------------------------------------------------

    def _process_constants(
        self,
        parser_result: ParserResult,
    ):

        for constant in parser_result.constants:

            chunk = ParsedChunk(

                chunk_id=generate_chunk_id(
                    constant.repo_path,
                    "constant",
                    constant.constant_name,
                    constant.line,
                    constant.line,
                ),

                chunk_type="constant",

                title=constant.constant_name,

                content=str(constant.value),

                metadata={
                    "type": constant.value_type,
                    "line": constant.line,
                },
            )

            chunk.token_count = estimate_tokens(chunk.content)

            self.result.chunks.append(chunk)