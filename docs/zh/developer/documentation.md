# 文档

## 结构

英文文档在 `docs/en/`，中文文档在 `docs/zh/`。
两个目录是各自独立的源文件树，文件和章节一一对应。
每棵树分三部分：`user/`、`developer/`、`agents/`。

API 参考从 docstring 生成。
构建时 Sphinx 把它写进 `docs/<语言>/apidocs/`，Git 会忽略这些目录。

## 写作

- 每次改动两种语言都要改，两边的信息保持一致。
- 英文按 Simplified Technical English 来写：句子短，用主动语态，一个词只表示一个意思。
- 中文直接用中文写，不要对着英文逐句翻译。
- 新术语加进术语表，两种语言都加。

## 构建

```bash
uv run python docs/build_docs.py
```

脚本会构建两种语言，站点输出到 `docs/build/html/`：

| 路径 | 内容 |
| --- | --- |
| `index.html` | 跳转到 `en/`。 |
| `en/`、`zh/` | 两种语言的文档。 |
| `llms.txt`、`llms-full.txt` | 给 agent 用的页面索引和全文。`zh/` 下另有一份中文的。 |

加上 `--strict`，Sphinx 一有警告构建就失败。CI 用的就是这个选项。

本地预览：

```bash
uv run python -m http.server 8000 -d docs/build/html
```

然后打开 <http://localhost:8000>。

想在改动后自动重建某一种语言，运行：

```bash
uv run sphinx-autobuild -c docs docs/en docs/build/html/en
uv run sphinx-autobuild -c docs -t zh docs/zh docs/build/html/zh
```

## 部署

仓库里有两个部署 workflow，一个发布到 GitHub Pages，一个发布到 Cloudflare。
用哪一个由仓库变量 `DOCS_DEPLOY_TARGET` 决定；没有设这个变量时，两个都不部署。

| `DOCS_DEPLOY_TARGET` | Workflow | 需要的设置 |
| --- | --- | --- |
| `github-pages` | `gh-pages.yml` | 在 **Settings > Pages** 里把 **Source** 设为 **GitHub Actions**。 |
| `cloudflare` | `cloudflare.yml` | 添加 secret `CLOUDFLARE_API_TOKEN` 和 `CLOUDFLARE_ACCOUNT_ID`，并在 `docs/wrangler.jsonc` 里填好 Worker 的名字。 |

部署到 Cloudflare 时，还要把仓库变量 `DOCS_BASE_URL` 设为站点地址，`llms.txt` 里的链接用的是它。
