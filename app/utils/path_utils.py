"""
path_utils.py

Helper functions for repository and GitHub paths.
"""


def build_repo_path(file_path, repository_root):
    """
    Build repository-relative path.

    Example:
        repositories/fastapi-master/fastapi/routing.py
            ↓
        fastapi/routing.py
    """

    return str(
        file_path.relative_to(repository_root)
    ).replace("\\", "/")


from pathlib import Path


def build_github_url(
    github_repo: str,
    repo_path: str,
    start_line: int | None = None,
    end_line: int | None = None,
    branch: str = "master",
) -> str:
    """
    Build GitHub URL.

    Examples
    --------
    File:
        https://github.com/fastapi/fastapi/blob/master/fastapi/routing.py

    Object:
        https://github.com/fastapi/fastapi/blob/master/fastapi/routing.py#L120-L180
    """

    repo_path = repo_path.replace("\\", "/")

    url = f"{github_repo}/blob/{branch}/{repo_path}"

    if start_line is not None:

        end_line = end_line or start_line

        url += f"#L{start_line}-L{end_line}"

    return url
    

    

def build_module_name(repo_path: str) -> str:
    """
    Convert a repository path into a Python module name.

    Example:
        fastapi/routing.py -> fastapi.routing
        fastapi/security/oauth2.py -> fastapi.security.oauth2
    """
    return (
        repo_path
        .replace("/", ".")
        .replace("\\", ".")
        .removesuffix(".py")
    )