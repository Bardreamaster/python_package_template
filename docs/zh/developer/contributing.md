# 参与开发

## 准备环境

先安装 [uv](https://docs.astral.sh/uv/)，然后在仓库根目录运行：

```bash
uv sync
uv run pre-commit install
```

`uv sync` 把这个包和 `dev` 依赖组装进 `.venv/`。

## 检查改动

```bash
uv run ruff check
uv run ruff format --check
uv run pytest
```

三条命令全部通过后再提 pull request。格式不对时，用 `uv run ruff format` 自动整理。

## 发布

1. 修改 `pyproject.toml` 里的 `version`。版本号只写在这一处。
2. 把改动合并进 `main`。
3. 在这个提交上打 `v<版本号>` 的 tag 并推送。

`pypi.yml` 会构建软件包并发布到 PyPI，用的是 [Trusted Publishing](https://docs.pypi.org/trusted-publishers/)。
第一次发布前，先在 PyPI 上配置 publisher，并在 GitHub 仓库里建好名为 `pypi` 的 environment。

:::{admonition} 模板占位
补充项目自己的约定：分支命名、提交信息、评审流程。
:::
