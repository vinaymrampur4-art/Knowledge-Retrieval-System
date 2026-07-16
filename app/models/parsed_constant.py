from dataclasses import dataclass


@dataclass
class ParsedConstant:

    repository_name: str

    branch: str

    github_repository: str

    file: str

    repo_path: str

    github_url: str

    constant_name: str

    value: str

    value_type: str

    line: int