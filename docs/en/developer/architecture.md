# Architecture

:::{admonition} Template placeholder
Describe the design of the package: the main parts, how they work together, and why.
Record each important decision with its reason.
:::

## Repository layout

| Path | Content |
| --- | --- |
| `src/python_package_template/` | The package. |
| `src/python_package_template/docs_index.py` | Functions that list, read and search the documentation pages. |
| `src/python_package_template/mcp_server.py` | The MCP server for the documentation. |
| `tests/` | The tests. |
| `docs/en/`, `docs/zh/` | The English and the Chinese documentation. |
| `docs/conf.py`, `docs/build_docs.py` | The Sphinx configuration and the build script. |
| `.github/workflows/` | The CI, release and deployment workflows. |
