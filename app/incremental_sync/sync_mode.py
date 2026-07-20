"""
Defines the supported synchronization modes.
"""

from enum import Enum


class SyncMode(str, Enum):
    """
    Supported synchronization modes.
    """

    FULL = "full"
    INCREMENTAL = "incremental"