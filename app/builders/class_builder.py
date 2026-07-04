"""
class_builder.py

Builder responsible for creating ParsedClass objects.
"""

from app.builders.base_builder import BaseBuilder
from app.models.parsed_class import ParsedClass
from app.models.parsed_method import ParsedMethod


class ClassBuilder(BaseBuilder):

    @classmethod
    def build(
        cls,
        *,
        file: str,
        repo_path: str,
        github_url: str,
        class_name: str,
        inherits: list | None = None,
        class_docstring: str | None = None,
        class_code,
        start_line: int = 0,
        end_line: int = 0,
        methods: list[ParsedMethod] | None = None,
        inheritance_info: list | None = None,
    ) -> ParsedClass:
        """
        Create a ParsedClass model.
        """

        if not class_name:
            raise ValueError("Class name cannot be empty.")

        return ParsedClass(
            file=file,
            repo_path=repo_path,
            github_url=github_url,
            class_name=class_name,
            inherits=inherits or [],
            class_docstring=class_docstring,
            class_code=class_code,
            start_line=start_line,
            end_line=end_line,
            methods=methods or [],
            inheritance_info=inheritance_info or [],
        )