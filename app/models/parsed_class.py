from dataclasses import dataclass, field

from app.models.parsed_method import ParsedMethod


@dataclass
class ParsedClass:

    file: str

    repo_path: str

    github_url: str

    class_name: str

    inherits: list = field(default_factory=list)

    class_docstring: str | None = None

    class_code: str | None = None

    start_line: int = 0

    end_line: int = 0

    methods: list[ParsedMethod] = field(default_factory=list)

    inheritance_info: list = field(default_factory=list)