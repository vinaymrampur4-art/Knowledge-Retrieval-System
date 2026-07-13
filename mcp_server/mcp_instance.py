"""
mcp_instance.py

Shared FastMCP instance used across the application.
"""

from fastmcp import FastMCP

from app.core.config import (
    PROJECT_NAME,
    PROJECT_VERSION,
)

mcp = FastMCP(
    name=PROJECT_NAME,
    version=PROJECT_VERSION,
)