"""
tokenizer.py

Code-aware tokenizer for BM25.

Splits:

- snake_case
- camelCase
- PascalCase

while also keeping the original identifier.
"""

import re


class BM25Tokenizer:

    # ---------------------------------------------------------

    def _split_identifier(
        self,
        token: str,
    ) -> list[str]:

        parts = []

        # Keep original identifier
        parts.append(token.lower())

        # -----------------------------------------
        # snake_case
        # -----------------------------------------

        snake = token.replace("_", " ")

        # -----------------------------------------
        # CamelCase / PascalCase
        # -----------------------------------------

        camel = re.sub(

            r"([a-z])([A-Z])",

            r"\1 \2",

            snake,

        )

        camel = re.sub(

            r"([A-Z]+)([A-Z][a-z])",

            r"\1 \2",

            camel,

        )

        for part in camel.split():

            part = part.lower()

            if len(part) > 1:

                parts.append(part)

        return parts

    # ---------------------------------------------------------

    def tokenize(
        self,
        text: str,
    ) -> list[str]:

        identifiers = re.findall(

            r"[A-Za-z_][A-Za-z0-9_]*",

            text,

        )

        tokens = []

        for identifier in identifiers:

            tokens.extend(

                self._split_identifier(

                    identifier

                )

            )

        # Remove duplicates while preserving order

        seen = set()

        output = []

        for token in tokens:

            if token not in seen:

                seen.add(token)

                output.append(token)

        return output