from dataclasses import dataclass


@dataclass
class ParsedConstant:

    file: str

    repo_path: str

    github_url: str

    constant_name: str

    value: str

    value_type: str

    line: int