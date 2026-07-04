from dataclasses import dataclass


@dataclass
class ParsedImport:

    file: str

    repo_path: str

    github_url: str

    module: str

    imported_name: str | None

    alias: str | None

    import_type: str

    line_number: int