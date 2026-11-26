"""MCP server that gives an agent access to the package documentation.

The server uses the stdio transport. Install the `mcp` extra, then start it
with the `python-package-template-mcp` command.
"""

from __future__ import annotations

import sys
from importlib.metadata import version
from typing import TYPE_CHECKING

from . import docs_index
from .docs_index import DocPage, SearchHit

if TYPE_CHECKING:
    from mcp.server.mcpserver import MCPServer

_INSTRUCTIONS = (
    "Documentation of python-package-template. "
    "Call list_docs to see the pages, search_docs to find a topic, "
    "and read_doc to get the Markdown source of a page. "
    "Start with the page en/agents/using."
)


def create_server() -> MCPServer:
    """Create the MCP server and register the documentation tools."""
    from mcp.server.mcpserver import MCPServer
    from mcp.server.mcpserver.exceptions import ToolError

    server = MCPServer(
        name="python-package-template-docs",
        instructions=_INSTRUCTIONS,
        version=version("python-package-template"),
    )

    @server.tool()
    def list_docs(language: str = "en") -> list[DocPage]:
        """List the documentation pages of one language ("en" or "zh")."""
        try:
            return docs_index.list_pages(language)
        except ValueError as error:
            raise ToolError(str(error)) from error

    @server.tool()
    def read_doc(path: str) -> str:
        """Return the Markdown source of one page, for example "en/index"."""
        try:
            return docs_index.read_page(path)
        except (ValueError, FileNotFoundError) as error:
            raise ToolError(str(error)) from error

    @server.tool()
    def search_docs(
        query: str, language: str = "en", limit: int = 10
    ) -> list[SearchHit]:
        """Search the pages of one language. Every query term must match."""
        try:
            return docs_index.search_pages(query, language, limit)
        except ValueError as error:
            raise ToolError(str(error)) from error

    return server


def main() -> None:
    """Run the server on stdio."""
    try:
        server = create_server()
    except ModuleNotFoundError as error:
        if error.name is None or not error.name.startswith("mcp"):
            raise
        sys.exit(
            "The MCP server needs the 'mcp' extra. "
            'Install it with: pip install "python-package-template[mcp]"'
        )
    server.run()


if __name__ == "__main__":
    main()
