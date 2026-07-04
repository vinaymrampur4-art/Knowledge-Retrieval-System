"""
inheritance.py

Resolves class inheritance relationships.
"""


class InheritanceResolver:

    def build_class_index(
        self,
        classes,
    ):

        class_index = {}

        for cls in classes:

            class_index[cls.class_name] = {

                "file": cls.repo_path,

                "github_url": cls.github_url,
            }

        return class_index

    def resolve(
        self,
        classes,
    ):

        class_index = self.build_class_index(
            classes
        )

        for cls in classes:

            inheritance_info = []

            for parent in cls.inherits:

                parent_name = parent.split(".")[-1]

                if parent_name in class_index:

                    inheritance_info.append(
                        {

                            "parent_class": parent_name,

                            "parent_file": class_index[
                                parent_name
                            ]["file"],

                            "parent_github_url": class_index[
                                parent_name
                            ]["github_url"],
                        }
                    )

                else:

                    inheritance_info.append(
                        {

                            "parent_class": parent_name,

                            "parent_file": "External Dependency",

                            "parent_github_url": None,
                        }
                    )

            cls.inheritance_info = inheritance_info

        return classes