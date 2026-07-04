"""
constant_parser.py

Extracts module-level constants from a Python AST.
"""

import ast

from app.builders.constant_builder import ConstantBuilder

from app.utils.path_utils import (
    build_repo_path,
    build_github_url,
)


class ConstantParser:

    def parse_constants(
        self,
        tree,
        file_path,
        repository_root,
        github_repo,
    ):
        """
        Parse module-level constants.
        """

        constants = []

        repo_path = build_repo_path(
            file_path,
            repository_root,
        )

        for node in tree.body:

            if not isinstance(node, ast.Assign):
                continue

            github_url = build_github_url(
                github_repo=github_repo,
                repo_path=repo_path,
                start_line=node.lineno,
                end_line=getattr(
                    node,
                    "end_lineno",
                    node.lineno,
                ),
            )

            for target in node.targets:

                if not isinstance(target, ast.Name):
                    continue

                # Convention:
                # Only UPPER_CASE variables are treated as constants
                if not target.id.isupper():
                    continue

                try:
                    value = ast.unparse(node.value)
                except Exception:
                    value = ""

                try:
                    evaluated = ast.literal_eval(node.value)
                    value_type = type(evaluated).__name__

                except Exception:
                    # Expressions such as Depends(...), Field(...), etc.
                    value_type = type(node.value).__name__

                parsed_constant = ConstantBuilder.build(

                    file=file_path.name,

                    repo_path=repo_path,

                    github_url=github_url,

                    constant_name=target.id,

                    value=value,

                    value_type=value_type,

                    line=node.lineno,
                )

                constants.append(parsed_constant)

        return constants