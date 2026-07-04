"""
base_builder.py

Base class for all builders in the Knowledge Retrieval System.
"""

from abc import ABC, abstractmethod


class BaseBuilder(ABC):
    """Base class for all builders."""

    @classmethod
    @abstractmethod
    def build(cls, *args, **kwargs):
        """
        Build and return the target model.
        """
        raise NotImplementedError