"""
import_builder.py

Builder responsible for creating ParsedImport objects.
"""

from app.builders.base_builder import BaseBuilder
from app.models.parsed_import import ParsedImport


class ImportBuilder(BaseBuilder):

    @classmethod
    def build(
        cls,
        *,
        file: str,
        repo_path: str,
        github_url: str,
        module: str | None,
        imported_name: str | None,
        alias: str | None,
        import_type: str,
        line_number: int,
    ) -> ParsedImport:
        """
        Create a ParsedImport model.
        """

        return ParsedImport(
            file=file,
            repo_path=repo_path,
            github_url=github_url,
            module=module or "",
            imported_name=imported_name,
            alias=alias,
            import_type=import_type,
            line_number=line_number,
        )