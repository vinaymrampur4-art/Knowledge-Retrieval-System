import ast
import os
from pathlib import Path

from git import repo

from app.core.config import REPOSITORY_FOLDER
from app.core.logger import logger

from app.models.parser_result import ParserResult
from app.parser.class_parser import ClassParser

from app.parser.inheritance import InheritanceResolver

from app.parser.function_parser import FunctionParser

from app.parser.import_parser import ImportParser

from app.parser.constant_parser import ConstantParser

from app.builders.project_builder import ProjectBuilder

# TODO: Move this into .env later
GITHUB_REPO = os.getenv(
    "GITHUB_REPO",
    "https://github.com/fastapi/fastapi/blob/master"
)


class ASTParser:

    def __init__(self):
        self.repository_root = None

        self.class_parser = ClassParser()

        self.inheritance_resolver = InheritanceResolver()

        self.function_parser = FunctionParser()

        self.import_parser = ImportParser()

        self.constant_parser = ConstantParser()



    def parse_file(self, file_path: Path,)-> ParserResult:

        try:

            source = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            tree = ast.parse(source)

            classes = self.class_parser.parse_classes(
                tree=tree,
                source=source,
                file_path=file_path,
                repository_root=self.repository_root,
                github_repo=GITHUB_REPO,
            )

            functions = self.function_parser.parse_functions(
                tree=tree,
                source=source,
                file_path=file_path,
                repository_root=self.repository_root,
                github_repo=GITHUB_REPO,
            )

            imports = self.import_parser.parse_imports(
                tree=tree,
                file_path=file_path,
                repository_root=self.repository_root,
                github_repo=GITHUB_REPO,
            )

            constants = self.constant_parser.parse_constants(
                tree=tree,
                file_path=file_path,
                repository_root=self.repository_root,
                github_repo=GITHUB_REPO,
            )

            return ProjectBuilder.build(
                classes=classes,
                functions=functions,
                imports=imports,
                constants=constants,
            )

        except Exception as e:

            logger.error(
                f"Error parsing {file_path}: {e}"
            )

            return ProjectBuilder.build()



    def parse(self, python_files: list[Path],repository_root: Path,)-> ParserResult:
        """
        Parse a list of Python files.

        Args:
        python_files (list[Path]):
            Files returned by RepositoryLoader.

        Returns:
            ParserResult:
                Parsed repository data including:

                - classes
                - methods
                - functions
                - imports
                - constants
        """
        if not python_files:
            logger.warning("No Python files found.")
            return ProjectBuilder.build()
        
        # TODO:
        # Remove this assumption.
        # RepositoryLoader should return both the repository root
        # and the list of Python files.
        repo = python_files[0]

        from app.core.config import REPOSITORY_FOLDER


        self.repository_root = repo

        self.repository_root = repository_root

        logger.info(
            f"Parsing {len(python_files)} Python files..."
        )

        all_classes = []
        all_functions = []
        all_imports = []
        all_constants = []

        for file in python_files:

            result = self.parse_file(file)

            all_classes.extend(
                result.classes
            )

            all_functions.extend(
                result.functions
            )

            all_imports.extend(
                result.imports
            )

            all_constants.extend(
                result.constants
            )

        all_classes = self.inheritance_resolver.resolve(
            all_classes
        )

        result = ProjectBuilder.build(
            classes=all_classes,
            functions=all_functions,
            imports=all_imports,
            constants=all_constants,
        )

        
        logger.info(
            f"Extracted {len(result.classes)} classes."
        )

        logger.info(
            f"Extracted {len(result.methods)} methods."
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

        