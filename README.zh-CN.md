# Python Package Template

[English](README.md)

一个 Python 包模板：`src` 布局，用 uv、ruff 和 pytest，自带中英文两套 Sphinx 文档、一个提供文档的 MCP 服务器，以及几个 GitHub Actions workflow。

## 快速开始

1. 在 GitHub 上点 "Use this template" 新建仓库，然后把新仓库克隆到本地。

2. 用包名、作者和邮箱初始化：

    ```bash
    bash init_package.sh --name your-package-name --author "Your Name" --email "your.email@example.com"
    ```

    | 选项 | 含义 |
    | --- | --- |
    | `--description TEXT` | 一句话简介，写进 `pyproject.toml` 和 README。 |
    | `--repo OWNER/NAME` | GitHub 仓库。默认取 `origin` 远程地址。 |
    | `--docs-url URL` | 文档站地址。默认是 `https://OWNER.github.io/NAME/`。 |

    脚本会改掉包名、作者、`LICENSE` 里的版权行、项目链接和两份 README。
    Linux 和 macOS 都能运行；它不会重命名仓库所在的目录。

3. 删除 `init_package.sh`。

4. 安装依赖并跑一遍检查：

    ```bash
    uv sync
    uv run ruff check
    uv run pytest
    uv run python docs/build_docs.py
    ```

5. 写文档。在 `docs/` 里搜索"模板占位"和 "Template placeholder"，就能找到需要填内容的页面。

6. （可选）更换许可证。默认是 MIT；要换的话，`LICENSE` 文件和 `pyproject.toml` 里的 `license` 字段一起改。

## GitHub Actions

Workflow 都在 `.github/workflows` 下，触发条件已经打开。
其中发布和部署的步骤要等你做完下表里的设置才会生效。

| Workflow | 触发 | 作用 | 需要的设置 |
| --- | --- | --- | --- |
| `tests.yml` | 推送到 `main`、pull request | lint、测试、构建文档 | 不需要。想用 Codecov 就添加 secret `CODECOV_TOKEN`；没有它时上传步骤不会运行。 |
| `pypi.yml` | 推送到 `main`、pull request、`v*.*.*` tag | 构建软件包；推送版本 tag 时发布到 PyPI | 新建名为 `pypi` 的 [environment](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)，并配置 [Trusted Publishing](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/#configuring-trusted-publishing)。 |
| `gh-pages.yml` | 推送到 `main` | 把文档部署到 GitHub Pages | 把仓库变量 `DOCS_DEPLOY_TARGET` 设为 `github-pages`；在 **Settings > Pages** 里把 **Source** 设为 **GitHub Actions**。 |
| `cloudflare.yml` | 推送到 `main` | 把文档部署到 Cloudflare | 把仓库变量 `DOCS_DEPLOY_TARGET` 设为 `cloudflare`；添加 secret `CLOUDFLARE_API_TOKEN` 和 `CLOUDFLARE_ACCOUNT_ID`；在 `docs/wrangler.jsonc` 里填好 Worker 的名字。 |

两个部署 workflow 只用一个，另一个删掉。
仓库被标记为模板（template）时，`pypi.yml` 里的发布 job 不会运行。

## 目录结构

```plaintext
python_package_template/
├── .devcontainer/          # 开发容器配置
├── .github/workflows/      # CI、发布、文档部署
├── docs/
│   ├── en/                 # 英文文档：user/、developer/、agents/
│   ├── zh/                 # 中文文档，结构与英文相同
│   ├── conf.py             # 两种语言共用的 Sphinx 配置
│   └── build_docs.py       # 构建站点、llms.txt 和 llms-full.txt
├── src/
│   └── python_package_template/  # 包的源码
│       ├── docs_index.py   # 列出、读取、搜索文档
│       └── mcp_server.py   # 提供文档的 MCP 服务器
├── tests/                  # 测试
├── .gitattributes          # 行尾和二进制文件
├── .gitignore              # 常见的 Python 忽略规则
├── .pre-commit-config.yaml # pre-commit 配置
├── AGENTS.md               # 写给编码 agent 的入口
├── init_package.sh         # 初始化脚本
├── LICENSE                 # 许可证
├── pyproject.toml          # 项目元数据和依赖
├── README.md               # 英文 README
└── README.zh-CN.md         # 本文件
```

### devcontainer

仓库带有 `.devcontainer` 目录，可以在 Visual Studio Code 里直接起一个开发容器：

1. 在 Visual Studio Code 里安装 [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) 扩展。
2. 用 Visual Studio Code 打开仓库。
3. 按 `F1`，在命令面板里选 "Dev Containers: Reopen in Container"。
4. 等容器构建并启动。第一次会花几分钟。
5. 容器起来之后，就可以在统一的环境里开发了。

## 相关资料

- [Python Packaging User Guide](https://packaging.python.org)
