# MCP 服务器与 llms.txt

## MCP 服务器

这个包自带一个 MCP 服务器（MCP server），用来提供本文档。
它在本机运行，走 stdio 传输；读的是随包安装的文档文件，不需要联网。

安装时带上 `mcp` 这个 extra：

```bash
python3 -m pip install "python-package-template[mcp]"
```

在 MCP 客户端的配置里加上这个服务器：

```json
{
  "mcpServers": {
    "python-package-template-docs": {
      "command": "python-package-template-mcp"
    }
  }
}
```

服务器提供三个工具：

| 工具 | 参数 | 返回 |
| --- | --- | --- |
| `list_docs` | `language`（`en` 或 `zh`，默认 `en`） | 每个页面的路径和标题。 |
| `read_doc` | `path`，例如 `zh/user/installation` | 该页面的 Markdown 源文件。 |
| `search_docs` | `query`、`language`、`limit`（默认 `10`） | 包含全部关键词的页面，以及命中的行。 |

:::{admonition} 模板占位
如果这个包的功能适合让 agent 直接调用，就在 `mcp_server.py` 里加上对应的工具，并补进上面的表。
:::

## llms.txt

文档站另外提供两个文件，供 agent 从网页读取：

- `llms.txt`：索引，列出每个页面的标题和链接。
- `llms-full.txt`：全文，所有页面合在一个文件里。

站点根目录下的两个文件是英文的，中文的在 `zh/` 下。
