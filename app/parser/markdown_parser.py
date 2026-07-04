from pathlib import Path
import json
import re


class MarkdownParser:
    def __init__(self, docs_root):
        self.docs_root = Path(docs_root)

    def extract_title(self, content):
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        return match.group(1).strip() if match else "Untitled"

    def extract_headings(self, content):
        headings = re.findall(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE)
        return [heading[1].strip() for heading in headings]

    def parse_file(self, file_path):
        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            return {
                "file_path": str(
                    file_path.relative_to(self.docs_root)
                ),
                "title": self.extract_title(content),
                "headings": self.extract_headings(content),
                "content": content
            }

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def parse_all(self):
        markdown_files = list(
            self.docs_root.rglob("*.md")
        )

        print(
            f"Found {len(markdown_files)} markdown files"
        )

        documents = []

        for file in markdown_files:
            doc = self.parse_file(file)

            if doc:
                documents.append(doc)

        return documents

    def save_json(self, documents, output_file):
        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                documents,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Saved {len(documents)} documents to {output_file}"
        )