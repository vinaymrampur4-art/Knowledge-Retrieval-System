"""
file_filter.py
"""

from pathlib import Path

IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "env",
    ".idea",
    ".vscode",
    "node_modules",
    "dist",
    "build",

    # Repository folders
    "tests",
    "docs",
    "scripts",
    "examples",
}

SUPPORTED_EXTENSIONS = {
    ".py",
}


def should_ignore_directory(path: Path) -> bool:
    return path.name in IGNORED_DIRECTORIES


def is_supported_file(path: Path) -> bool:
    return (
        path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )