from dataclasses import dataclass, field


@dataclass
class ParsedFile:
    """
    Represents one Python source file.
    """
    repository_name: str

    branch: str

    github_repository: str

    file_name: str

    repo_path: str

    github_url: str

    module_name: str

    docstring: str | None = None

    imports: list = field(default_factory=list)

    classes: list = field(default_factory=list)

    functions: list = field(default_factory=list)

    constants: list = field(default_factory=list)