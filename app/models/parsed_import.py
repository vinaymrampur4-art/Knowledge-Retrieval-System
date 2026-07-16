from dataclasses import dataclass


@dataclass
class ParsedImport:

    repository_name: str

    branch: str

    github_repository: str

    file: str

    repo_path: str

    github_url: str

    module: str

    imported_name: str | None

    alias: str | None

    import_type: str

    line_number: int