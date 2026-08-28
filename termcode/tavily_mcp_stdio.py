"""Wrapper to run the Tavily MCP server with stdio transport.

The installed tavily_server_mcp package only supports HTTP mode via uvicorn.
This wrapper uses the same FastMCP server instance but runs it with stdio
transport, which is what termcode expects for command-based MCP servers.

IMPORTANT: termcode/mcp/ shadows the pip-installed "mcp" package, which
fastmcp depends on. We must remove the project root from sys.path before
importing the MCP server.
"""

import os
import sys

# Remove the project root from sys.path so that "import mcp.types" (needed
# by fastmcp) resolves to the pip-installed mcp package, not termcode/mcp/.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root in sys.path:
    sys.path.remove(_project_root)


def main() -> None:
    """Run the Tavily MCP server over stdio."""
    from tavily_server_mcp.tavily_mcp_server import mcp

    # FastMCP 3.x: mcp.run(transport="stdio") starts a stdio MCP server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
