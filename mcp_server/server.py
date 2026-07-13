"""
server.py

HTTP MCP Server for the Knowledge Retrieval System.
"""

from app.core.config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    MCP_HOST,
    MCP_PORT,
    MCP_PATH,
)

from mcp_server.mcp_instance import mcp

# Import tools so that @mcp.tool() decorators execute
import mcp_server.tools

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print("=" * 80)
    print(PROJECT_NAME)
    print("=" * 80)
    print(f"Version   : {PROJECT_VERSION}")
    print(f"Transport : HTTP")
    print(f"Host      : {MCP_HOST}")
    print(f"Port      : {MCP_PORT}")
    print(f"Endpoint  : {MCP_PATH}")
    print("=" * 80)

    mcp.run(
        transport="http",
        host=MCP_HOST,
        port=MCP_PORT,
        path=MCP_PATH,
    )