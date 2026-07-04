"""
function_builder.py

Builder responsible for creating ParsedFunction objects.
"""

from app.builders.base_builder import BaseBuilder
from app.models.parsed_function import ParsedFunction


class FunctionBuilder(BaseBuilder):

    @classmethod
    def build(
        cls,
        *,
        file: str,
        repo_path: str,
        github_url: str,
        module=str,
        function_name: str,
        parameters: list,
        return_type: str | None,
        docstring: str | None,
        function_signature: str | None,
        function_code: str | None,
        start_line: int,
        end_line: int,
        is_async: bool = False,
        decorators: list | None = None,
    ) -> ParsedFunction:

        if not function_name:
            raise ValueError("Function name cannot be empty.")

        return ParsedFunction(
            file=file,
            repo_path=repo_path,
            github_url=github_url,
            module=module,
            function_name=function_name,
            parameters=parameters or [],
            return_type=return_type,
            docstring=docstring,
            function_signature=function_signature,
            function_code=function_code,
            start_line=start_line,
            end_line=end_line,
            is_async=is_async,
            decorators=decorators or [],
        )