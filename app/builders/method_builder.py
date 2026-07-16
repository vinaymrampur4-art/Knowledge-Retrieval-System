"""
method_builder.py

Builder responsible for creating ParsedMethod objects.
"""

from app.builders.base_builder import BaseBuilder
from app.models.parsed_method import ParsedMethod


class MethodBuilder(BaseBuilder):

    @classmethod
    def build(
        cls,
        *,
        repository_name: str,
        branch: str,
        github_repository: str,
        file: str,
        repo_path: str,
        github_url: str,
        module: str,
        class_name: str,
        method_name: str,
        parameters: list,
        return_type: str | None,
        docstring: str | None,
        method_signature: str | None,
        method_code: str | None,
        start_line: int,
        end_line: int,
        is_async: bool = False,
        is_private: bool = False,
        is_static: bool = False,
        decorators: list | None = None,
    ) -> ParsedMethod:
        """
        Create a ParsedMethod model.
        """

        if not method_name:
            raise ValueError("Method name cannot be empty.")

        return ParsedMethod(
            repository_name=repository_name,
            branch=branch,
            github_repository=github_repository,
            file=file,
            repo_path=repo_path,
            github_url=github_url,
            module=module,
            class_name=class_name,
            method_name=method_name,
            parameters=parameters or [],
            return_type=return_type,
            docstring=docstring,
            method_signature=method_signature,
            method_code=method_code,
            start_line=start_line,
            end_line=end_line,
            is_async=is_async,
            is_private=is_private,
            is_static=is_static,
            decorators=decorators or [],
        )