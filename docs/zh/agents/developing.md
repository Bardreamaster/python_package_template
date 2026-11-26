# 修改本仓库

这一页写给修改本仓库代码或文档的 agent。

## 规则

- 注释和 docstring 一律用英文。
- 新代码要写类型标注。
- 改了 `docs/en/` 里的页面，就同步修改 `docs/zh/` 里对应的页面；反过来也一样。
- 中文直接用中文写，不要逐句翻译英文。
- 不要编辑 `docs/<语言>/apidocs/`，这些文件由构建生成。
- 不要提交 `docs/internal/` 里的文件。
- 版本号只在 `pyproject.toml` 里改。

:::{admonition} 模板占位
补充项目自己的规则。
:::

## 代码地图

| 路径 | 内容 |
| --- | --- |
| `src/python_package_template/` | 包的源码。 |
| `tests/` | 测试，每个模块对应一个测试文件。 |
| `docs/en/`、`docs/zh/` | 文档，两边结构相同。 |
| `docs/conf.py` | 两种语言共用的 Sphinx 配置。 |
| `docs/build_docs.py` | 构建站点的脚本。 |
| `.github/workflows/` | CI、发布和部署。 |

## 检查命令

结束工作前运行下面的命令，必须全部通过。

```bash
uv run ruff check
uv run ruff format --check
uv run pytest
uv run python docs/build_docs.py --strict
```

## 常见任务

### 添加功能

1. 在 `src/python_package_template/` 里写代码。
2. 在 `tests/` 里补测试。
3. 在 `docs/en/user/usage.md` 和 `docs/zh/user/usage.md` 里说明这项功能。
4. 运行检查命令。

### 添加文档页面

1. 在 `docs/en/` 和 `docs/zh/` 里用同一个文件名各建一页。
2. 把新页面加进两种语言里对应章节 index 的 `toctree`。
3. 运行 `uv run python docs/build_docs.py --strict`。

### 发布版本

1. 修改 `pyproject.toml` 里的 `version`。
2. 运行检查命令。
3. 让用户推送 `v<版本号>` 的 tag。不要自己推送 tag。
