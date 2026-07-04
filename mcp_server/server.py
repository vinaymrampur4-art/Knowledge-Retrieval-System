"""
server.py

HTTP MCP Server for the Knowledge Retrieval System.
"""

from fastmcp import FastMCP

from app.core.config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    MCP_HOST,
    MCP_PORT,
    MCP_PATH,
)

from mcp_server.tools import (
    search_via_query,
    search_methods,
    search_classes,
    search_files,
    search_functions,
    search_code,
    lookup_by_id,
    get_id_by_attributes,
)

# ==========================================================
# CREATE MCP SERVER
# ==========================================================

mcp = FastMCP(
    name=PROJECT_NAME,
    version=PROJECT_VERSION,
)

# ==========================================================
# SEARCH TOOLS
# ==========================================================

mcp.tool(search_via_query)

mcp.tool(search_methods)

mcp.tool(search_classes)

mcp.tool(search_files)

mcp.tool(search_functions)

mcp.tool(search_code)

# ==========================================================
# LOOKUP TOOLS
# ==========================================================

mcp.tool(lookup_by_id)

mcp.tool(get_id_by_attributes)

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