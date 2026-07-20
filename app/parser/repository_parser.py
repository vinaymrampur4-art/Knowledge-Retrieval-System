"""
repository_parser.py

Scans an entire repository and delegates parsing to the
individual AST parsers.
"""

from __future__ import annotations

import ast
from pathlib import Path

from app.core.logger import logger
from app.core.config import (
    GITHUB_REPOSITORY,
    DEFAULT_BRANCH,
)

from app.models.parser_result import ParserResult
from app.models.parsed_file import ParsedFile

from app.parser.class_parser import ClassParser
from app.parser.function_parser import FunctionParser
from app.parser.import_parser import ImportParser
from app.parser.constant_parser import ConstantParser
from app.parser.inheritance import InheritanceResolver

from app.utils.path_utils import (
    build_repo_path,
    build_github_url,
    build_module_name,
)


class RepositoryParser:
    """
    Parses an entire repository.

    Automatically ignores directories that normally do not
    contain production source code.
    """

    IGNORE_DIRECTORIES = {
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".venv",
        "venv",
        ".git",
        ".github",
        "tests",
        "test",
        "docs",
        "docs_src",
        "scripts",
        "examples",
        "benchmarks",
        "site-packages",
        "node_modules",
    }

    def __init__(self):
        self.class_parser = ClassParser()
        self.function_parser = FunctionParser()
        self.import_parser = ImportParser()
        self.constant_parser = ConstantParser()
        self.inheritance_resolver = InheritanceResolver()

    # --------------------------------------------------------

    def _should_skip_file(
        self,
        file_path: Path,
    ) -> bool:
        """
        Returns True if the file is inside an ignored directory.
        """
        return any(
            part in self.IGNORE_DIRECTORIES
            for part in file_path.parts
        )

    # --------------------------------------------------------

    def _discover_python_files(
        self,
        repository_path: Path,
    ) -> list[Path]:
        """
        Discovers all Python files that should be parsed.

        Parameters
        ----------
        repository_path:
            Root of the repository.

        Returns
        -------
        list[Path]
            Python source files excluding ignored directories.
        """
        python_files: list[Path] = []

        for file_path in repository_path.rglob("*.py"):
            if self._should_skip_file(file_path):
                continue
            python_files.append(file_path)

        return python_files

    # --------------------------------------------------------

    def _parse_file(
        self,
        file_path: Path,
        repository_root: Path,
        repository_name: str,
        branch: str,
        github_repo: str,
        result: ParserResult,
    ) -> None:
        """
        Parses a single Python file and appends the extracted
        objects to the supplied ParserResult.
        """
        try:
            source = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
            tree = ast.parse(source)
        except Exception as e:
            logger.warning(
                f"Failed to parse {file_path}: {e}"
            )
            return

        repo_path = build_repo_path(
            file_path,
            repository_root,
        )

        github_url = build_github_url(
            github_repo,
            repo_path,
        )

        parsed_file = ParsedFile(
            repository_name=repository_name,
            branch=branch,
            github_repository=github_repo,
            file_name=file_path.name,
            repo_path=repo_path,
            github_url=github_url,
            module_name=build_module_name(repo_path),
            docstring=ast.get_docstring(tree),
            classes=[],
            functions=[],
            imports=[],
            constants=[],
        )

        try:
            parsed_file.classes = self.class_parser.parse_classes(
                tree=tree,
                source=source,
                file_path=file_path,
                repository_root=repository_root,
                github_repo=github_repo,
                repository_name=repository_name,
                branch=branch,
            )
            result.classes.extend(parsed_file.classes)
        except Exception:
            logger.exception(
                f"Class parser failed: {file_path}"
            )

        try:
            parsed_file.functions = self.function_parser.parse_functions(
                tree=tree,
                source=source,
                file_path=file_path,
                repository_root=repository_root,
                repository_name=repository_name,
                branch=branch,
                github_repo=github_repo,
            )
            result.functions.extend(parsed_file.functions)
        except Exception:
            logger.exception(
                f"Function parser failed: {file_path}"
            )

        try:
            parsed_file.imports = self.import_parser.parse_imports(
                tree=tree,
                file_path=file_path,
                repository_root=repository_root,
                repository_name=repository_name,
                branch=branch,
                github_repo=github_repo,
            )
            result.imports.extend(parsed_file.imports)
        except Exception:
            logger.exception(
                f"Import parser failed: {file_path}"
            )

        try:
            parsed_file.constants = self.constant_parser.parse_constants(
                tree=tree,
                file_path=file_path,
                repository_root=repository_root,
                repository_name=repository_name,
                branch=branch,
                github_repo=github_repo,
            )
            result.constants.extend(parsed_file.constants)
        except Exception:
            logger.exception(
                f"Constant parser failed: {file_path}"
            )

        result.files.append(parsed_file)

    # --------------------------------------------------------

    def _finalize_result(
        self,
        result: ParserResult,
    ) -> ParserResult:
        """
        Performs post-processing on the parsed result.
        """

        self.inheritance_resolver.resolve(
            result.classes
        )

        total_methods = sum(
            len(cls.methods)
            for cls in result.classes
        )

        logger.info(
            f"Extracted {len(result.files)} files."
        )

        logger.info(
            f"Extracted {len(result.classes)} classes."
        )

        logger.info(
            f"Extracted {total_methods} methods."
        )

        logger.info(
            f"Extracted {len(result.functions)} functions."
        )

        logger.info(
            f"Extracted {len(result.imports)} imports."
        )

        logger.info(
            f"Extracted {len(result.constants)} constants."
        )

        return result

    # --------------------------------------------------------

    def parse(
        self,
        repository_path: str | Path,
    ) -> ParserResult:
        repository_path = Path(repository_path)
        repository_root = repository_path
        repository_name = repository_path.name
        branch = DEFAULT_BRANCH
        github_repo = GITHUB_REPOSITORY

        result = ParserResult()

        logger.info(
            f"Scanning repository: {repository_path.name}"
        )

        python_files = self._discover_python_files(
            repository_path
        )

        logger.info(
            f"Found {len(python_files)} Python files."
        )

        logger.info(
            f"Parsing {len(python_files)} Python files..."
        )

        for file_path in python_files:
            self._parse_file(
                file_path=file_path,
                repository_root=repository_root,
                repository_name=repository_name,
                branch=branch,
                github_repo=github_repo,
                result=result,
            )

        return self._finalize_result(result)
    
    # --------------------------------------------------------

    def parse_files(
        self,
        repository_root: str | Path,
        file_paths: list[str | Path],
    ) -> ParserResult:
        """
        Parses only the supplied Python files.

        Parameters
        ----------
        repository_root:
            Root directory of the repository.

        file_paths:
            Repository-relative files to parse.

        Returns
        -------
        ParserResult
            Parsed objects extracted from the supplied files.
        """

        repository_root = Path(repository_root)

        repository_name = repository_root.name

        branch = DEFAULT_BRANCH

        github_repo = GITHUB_REPOSITORY

        result = ParserResult()

        logger.info(
            f"Parsing {len(file_paths)} changed Python files..."
        )

        for file_path in file_paths:

            file_path = Path(file_path)

            if not file_path.is_absolute():
                file_path = repository_root / file_path

            if not file_path.exists():
                logger.warning(
                    f"Changed file not found: {file_path}"
                )
                continue

            self._parse_file(
                file_path=file_path,
                repository_root=repository_root,
                repository_name=repository_name,
                branch=branch,
                github_repo=github_repo,
                result=result,
            )

        return self._finalize_result(result)