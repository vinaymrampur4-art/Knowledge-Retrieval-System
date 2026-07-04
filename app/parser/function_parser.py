"""
function_parser.py

Extracts top-level functions from a Python AST.
"""

import ast

from app.builders.function_builder import FunctionBuilder

from app.utils.path_utils import (
    build_repo_path,
    build_github_url,
    build_module_name,
)


class FunctionParser:

    def get_annotation(self, annotation):
        """
        Convert an AST annotation into a string.
        """

        if annotation is None:
            return None

        try:
            return ast.unparse(annotation)

        except Exception:
            return None

    # --------------------------------------------------------

    def get_decorators(self, node):
        """
        Return decorators applied to a function.
        """

        decorators = []

        for decorator in node.decorator_list:

            try:
                decorators.append(
                    ast.unparse(decorator)
                )

            except Exception:
                pass

        return decorators

    # --------------------------------------------------------

    def parse_functions(
        self,
        tree,
        source,
        file_path,
        repository_root,
        github_repo,
    ):
        """
        Extract top-level functions.
        """

        functions = []

        repo_path = build_repo_path(
            file_path,
            repository_root,
        )

        module = build_module_name(repo_path)

        # ----------------------------------------------------
        # Only inspect module-level nodes
        # ----------------------------------------------------

        for node in tree.body:

            if not isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
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

            parameters = []

            for arg in node.args.args:

                parameters.append(
                    {
                        "name": arg.arg,
                        "datatype": self.get_annotation(
                            arg.annotation
                        ),
                    }
                )

            decorators = self.get_decorators(node)

            parsed_function = FunctionBuilder.build(

                file=file_path.name,

                repo_path=repo_path,

                github_url=github_url,

                module=module,

                function_name=node.name,

                parameters=parameters,

                return_type=self.get_annotation(
                    node.returns,
                ),

                docstring=ast.get_docstring(node),

                function_signature=(
                    ast.unparse(node)
                    .split(":")[0]
                    .strip()
                ),

                function_code=ast.get_source_segment(
                    source,
                    node,
                ),

                start_line=node.lineno,

                end_line=getattr(
                    node,
                    "end_lineno",
                    node.lineno,
                ),

                is_async=isinstance(
                    node,
                    ast.AsyncFunctionDef,
                ),

                decorators=decorators,
            )

            functions.append(parsed_function)

        return functions