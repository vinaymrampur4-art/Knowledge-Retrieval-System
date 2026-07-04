from dataclasses import dataclass, field
@dataclass
class ParsedFunction:
    # Required field (must come first)
    function_name: str

    # Metadata
    file: str = ""
    repo_path: str = ""
    github_url: str = ""
    module: str = ""

    # Function information
    parameters: list = field(default_factory=list)

    return_type: str | None = None

    docstring: str | None = None
    function_signature: str | None = None
    function_code: str | None = None
    start_line: int = 0
    end_line: int = 0
    is_async: bool = False
    decorators: list = field(default_factory=list)