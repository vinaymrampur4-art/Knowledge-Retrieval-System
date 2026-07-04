"""
ast_utils.py

Common AST helper functions used by all parsers.
"""

import ast


def get_annotation(annotation):
    """
    Convert an AST annotation into a string.
    """

    if annotation is None:
        return None

    try:
        text = ast.unparse(annotation)

        if text.startswith("Annotated["):
            text = (
                text[len("Annotated["):]
                .split(",", 1)[0]
                .strip()
            )

        return text

    except Exception:
        return None


def get_decorators(node):
    """
    Return a list of decorators.
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


def get_signature(node):
    """
    Return the function/class signature.
    """

    try:
        return (
            ast.unparse(node)
            .split(":")[0]
            .strip()
        )

    except Exception:
        return node.name


def get_source_code(source, node):
    """
    Return source code for a node.
    """

    return ast.get_source_segment(
        source,
        node,
    )


def extract_parameters(node):
    """
    Extract function parameters.
    """

    parameters = []

    for arg in node.args.args:

        if arg.arg in ("self", "cls"):
            continue

        parameters.append(
            {
                "name": arg.arg,
                "datatype": get_annotation(
                    arg.annotation
                ),
            }
        )

    return parameters