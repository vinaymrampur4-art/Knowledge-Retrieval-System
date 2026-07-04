import json


class RAGChunker:

    def __init__(self, methods_file, classes_file):
        self.methods_file = methods_file
        self.classes_file = classes_file

    def load_methods(self):

        with open(
            self.methods_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def load_classes(self):

        with open(
            self.classes_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def create_method_chunks(self):

        methods = self.load_methods()

        chunks = []

        for method in methods:

            class_name = method.get(
                "class_name",
                ""
            )

            method_name = method.get(
                "method_name",
                ""
            )

            parameters = method.get(
                "parameters",
                []
            )

            return_type = method.get(
                "return_type"
            )

            inherits = method.get(
                "inherits",
                []
            )

            repo_path = method.get(
                "repo_path",
                ""
            )

            github_url = method.get(
                "github_url",
                ""
            )

            docstring = method.get(
                "docstring"
            )

            parameter_text = ", ".join(
                [
                    f"{p['name']} ({p['datatype']})"
                    if p.get("datatype")
                    else p["name"]
                    for p in parameters
                ]
            )

            text = (
                f"Class {class_name}. "
                f"Method {method_name}. "
            )

            if parameter_text:

                text += (
                    f"Parameters: "
                    f"{parameter_text}. "
                )

            if return_type:

                text += (
                    f"Returns: "
                    f"{return_type}. "
                )

            if inherits:

                text += (
                    f"Inherits From: "
                    f"{', '.join(inherits)}. "
                )

            if docstring:

                text += (
                    f"Description: "
                    f"{docstring}"
                )

            chunk = {

                "chunk_id":
                    f"{class_name}_{method_name}",

                "chunk_type":
                    "method",

                "class_name":
                    class_name,

                "method_name":
                    method_name,

                "source": {

                    "file":
                        method.get(
                            "file"
                        ),

                    "repo_path":
                        repo_path,

                    "github_url":
                        github_url
                },

                "inherits":
                    inherits,

                "parameters":
                    parameters,

                "return_type":
                    return_type,

                "description":
                    text
            }

            chunks.append(
                chunk
            )

        return chunks

    def create_class_chunks(self):

        classes = self.load_classes()

        chunks = []

        for cls in classes:

            class_name = cls.get(
                "class_name",
                ""
            )

            inherits = cls.get(
                "inherits",
                []
            )

            inheritance_info = cls.get(
                "inheritance_info",
                []
            )

            docstring = cls.get(
                "class_docstring"
            )

            text = (
                f"Class {class_name}. "
            )

            if inherits:

                text += (
                    f"Inherits From: "
                    f"{', '.join(inherits)}. "
                )

            if docstring:

                text += (
                    f"Description: "
                    f"{docstring}"
                )

            chunk = {

                "chunk_id":
                    class_name,

                "chunk_type":
                    "class",

                "class_name":
                    class_name,

                "source": {

                    "file":
                        cls.get(
                            "file"
                        ),

                    "repo_path":
                        cls.get(
                            "repo_path"
                        ),

                    "github_url":
                        cls.get(
                            "github_url"
                        )
                },

                "inherits":
                    inherits,

                "inheritance_info":
                    inheritance_info,

                "description":
                    text
            }

            chunks.append(
                chunk
            )

        return chunks

    def create_chunks(self):

        method_chunks = (
            self.create_method_chunks()
        )

        class_chunks = (
            self.create_class_chunks()
        )

        return (
            class_chunks +
            method_chunks
        )

    def save_chunks(
        self,
        output_file
    ):

        chunks = self.create_chunks()

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                chunks,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Saved {len(chunks)} chunks "
            f"to {output_file}"
        )