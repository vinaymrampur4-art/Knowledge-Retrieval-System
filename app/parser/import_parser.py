"""
import_parser.py

Extracts imports from a Python AST.
"""

import ast

from app.builders.import_builder import ImportBuilder

from app.utils.path_utils import (
    build_repo_path,
    build_github_url,
)


class ImportParser:

    def parse_imports(
        self,
        tree,
        file_path,
        repository_root,
        repository_name,
        branch,
        github_repo,
    ):
        """
        Parse all imports from an AST.
        """

        imports = []

        repo_path = build_repo_path(
            file_path,
            repository_root,
        )

        for node in ast.walk(tree):

            # -------------------------------------------------
            # import xxx
            # -------------------------------------------------

            if isinstance(node, ast.Import):

                github_url = build_github_url(
                    github_repo=github_repo,
                    repo_path=repo_path,
                    start_line=node.lineno,
                    end_line=node.lineno,
                )

                for alias in node.names:

                    parsed_import = ImportBuilder.build(

                        repository_name=repository_name,

                        branch=branch,

                        github_repository=github_repo,

                        file=file_path.name,

                        repo_path=repo_path,

                        github_url=github_url,

                        module=alias.name,

                        imported_name=None,

                        alias=alias.asname,

                        import_type="import",

                        line_number=node.lineno,
                    )

                    imports.append(parsed_import)

            # -------------------------------------------------
            # from xxx import yyy
            # -------------------------------------------------

            elif isinstance(node, ast.ImportFrom):

                github_url = build_github_url(
                    github_repo=github_repo,
                    repo_path=repo_path,
                    start_line=node.lineno,
                    end_line=node.lineno,
                )

                module = node.module or ""

                for alias in node.names:

                    parsed_import = ImportBuilder.build(

                        repository_name=repository_name,

                        branch=branch,

                        github_repository=github_repo,

                        file=file_path.name,

                        repo_path=repo_path,

                        github_url=github_url,

                        module=module,

                        imported_name=alias.name,

                        alias=alias.asname,

                        import_type="from",

                        line_number=node.lineno,
                    )

                    imports.append(parsed_import)

        return imports