# MCP server and llms.txt

## MCP server

The package contains an MCP server for this documentation.
The server runs on your machine and uses the stdio transport.
It reads the documentation files that the package installs, so it does not need a network connection.

Install the package with the `mcp` extra:

```bash
python3 -m pip install "python-package-template[mcp]"
```

Add the server to the configuration of your MCP client:

```json
{
  "mcpServers": {
    "python-package-template-docs": {
      "command": "python-package-template-mcp"
    }
  }
}
```

The server has three tools:

| Tool | Arguments | Result |
| --- | --- | --- |
| `list_docs` | `language` (`en` or `zh`, default `en`) | The path and the title of each page. |
| `read_doc` | `path`, for example `en/user/installation` | The Markdown source of the page. |
| `search_docs` | `query`, `language`, `limit` (default `10`) | The pages that contain all query terms, with the lines that match. |

:::{admonition} Template placeholder
If an agent can call the functions of your package, add tools for them in `mcp_server.py` and list them here.
:::

## llms.txt

The documentation site has two files for agents that read it from the web:

- `llms.txt`: an index with the title and the link of each page.
- `llms-full.txt`: the full text of all pages in one file.

The files at the site root are in English. The Chinese files are in `zh/`.
