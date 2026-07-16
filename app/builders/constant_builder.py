"""
constant_builder.py

Builder responsible for creating ParsedConstant objects.
"""

from app.builders.base_builder import BaseBuilder
from app.models.parsed_constant import ParsedConstant


class ConstantBuilder(BaseBuilder):

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
        constant_name: str,
        value: str,
        value_type: str,
        line: int,
    ) -> ParsedConstant:
        """
        Create a ParsedConstant model.
        """

        if not constant_name:
            raise ValueError("Constant name cannot be empty.")

        return ParsedConstant(
            repository_name=repository_name,
            branch=branch,
            github_repository=github_repository,
            file=file,
            repo_path=repo_path,
            github_url=github_url,
            constant_name=constant_name,
            value=value,
            value_type=value_type,
            line=line,
        )