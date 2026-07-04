"""
project_builder.py

Creates the final ParserResult object that contains
everything extracted from the repository.
"""

from app.builders.base_builder import BaseBuilder
from app.models.parser_result import ParserResult


class ProjectBuilder(BaseBuilder):

    @classmethod
    def build(
        cls,
        *,
        classes=None,
        functions=None,
        imports=None,
        constants=None,
    ) -> ParserResult:
        """
        Build the final ParserResult object.
        """

        return ParserResult(

            classes=classes or [],

            methods=[
                method
                for c in (classes or [])
                for method in c.methods
            ],

            functions=functions or [],

            imports=imports or [],

            constants=constants or [],
        )   