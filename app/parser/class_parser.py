"""
class_parser.py

Extracts classes and their methods from a Python AST.
"""

import ast

from app.builders.method_builder import MethodBuilder
from app.builders.class_builder import ClassBuilder

from app.utils.ast_utils import (
    get_annotation,
    get_decorators,
    get_signature,
    get_source_code,
    extract_parameters,
)

from app.utils.path_utils import (
    build_repo_path,
    build_github_url,
    build_module_name,
)


class ClassParser:

    def parse_classes(
        self,
        tree,
        source,
        file_path,
        repository_root,
        github_repo,
        repository_name,
        branch,
    ):
        """
        Parse all classes from an AST.
        """

        classes = []

        repo_path = build_repo_path(
            file_path,
            repository_root,
        )

        for node in ast.walk(tree):

            if not isinstance(node, ast.ClassDef):
                continue

            methods = []

            inherits = [
                ast.unparse(base)
                for base in node.bases
            ]

            # ---------------------------------------------
            # Parse Methods
            # ---------------------------------------------

            for item in node.body:

                if not isinstance(
                    item,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                    ),
                ):
                    continue

                parameters = extract_parameters(item)

                decorators = get_decorators(item)

                signature = get_signature(item)

                method_github_url = build_github_url(
                    github_repo=github_repo,
                    repo_path=repo_path,
                    start_line=item.lineno,
                    end_line=getattr(
                        item,
                        "end_lineno",
                        item.lineno,
                    ),
                )

                parsed_method = MethodBuilder.build(

                    repository_name=repository_name,

                    branch=branch,

                    github_repository=github_repo,

                    file=file_path.name,

                    repo_path=repo_path,

                    github_url=method_github_url,

                    module=build_module_name(repo_path),

                    class_name=node.name,

                    method_name=item.name,

                    parameters=parameters,

                    return_type=get_annotation(item.returns),

                    docstring=ast.get_docstring(item),

                    method_signature=signature,

                    method_code=get_source_code(source, item),

                    start_line=item.lineno,

                    end_line=getattr(
                        item,
                        "end_lineno",
                        item.lineno,
                    ),

                    is_async=isinstance(
                        item,
                        ast.AsyncFunctionDef,
                    ),

                    is_private=item.name.startswith("_"),

                    is_static="staticmethod" in decorators,

                    decorators=decorators,
                )

                methods.append(parsed_method)

            # ---------------------------------------------
            # Build GitHub URL for Class
            # ---------------------------------------------

            class_github_url = build_github_url(
                github_repo=github_repo,
                repo_path=repo_path,
                start_line=node.lineno,
                end_line=getattr(
                    node,
                    "end_lineno",
                    node.lineno,
                ),
            )

            # ---------------------------------------------
            # Build Parsed Class
            # ---------------------------------------------

            classes.append(

                ClassBuilder.build(

                    repository_name=repository_name,

                    branch=branch,

                    github_repository=github_repo,

                    file=file_path.name,

                    repo_path=repo_path,

                    github_url=class_github_url,

                    class_name=node.name,

                    inherits=inherits,

                    class_docstring=ast.get_docstring(node),

                    class_code=get_source_code(source, node),

                    start_line=node.lineno,

                    end_line=getattr(
                        node,
                        "end_lineno",
                        node.lineno,
                    ),

                    methods=methods,

                    inheritance_info=[],
                )
            )

        return classes