from dataclasses import dataclass, field


@dataclass
class ParserResult:

    files: list = field(default_factory=list)

    classes: list = field(default_factory=list)

    methods: list = field(default_factory=list)

    functions: list = field(default_factory=list)

    imports: list = field(default_factory=list)

    constants: list = field(default_factory=list)