from dataclasses import dataclass, field
@dataclass
class ParsedMethod:

    repository_name: str

    branch: str

    github_repository: str

    method_name: str

    file: str = ""

    repo_path: str = ""

    github_url: str = ""

    module: str = ""

    class_name: str = ""

    parameters: list = field(default_factory=list)

    return_type: str | None = None

    docstring: str | None = None
    
    method_signature: str | None = None

    method_code: str | None = None

    start_line: int = 0

    end_line: int = 0

    is_async: bool = False

    is_private: bool = False

    is_static: bool = False

    decorators: list = field(default_factory=list)