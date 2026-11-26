# Documentation

## Structure

The English documentation is in `docs/en/`. The Chinese documentation is in `docs/zh/`.
The two directories are independent source trees with the same files and the same sections.
Each tree has three parts: `user/`, `developer/` and `agents/`.

The API reference comes from the docstrings.
Sphinx writes it to `docs/<language>/apidocs/` during the build. Git ignores these directories.

## Write

- Make each change in both languages. The two versions must give the same information.
- Write the English pages in Simplified Technical English: short sentences, active voice, one word for one meaning.
- Write the Chinese pages as original Chinese text. Do not translate sentence by sentence.
- Add new terms to the glossary in both languages.

## Build

```bash
uv run python docs/build_docs.py
```

The script builds both languages and writes the site to `docs/build/html/`:

| Path | Content |
| --- | --- |
| `index.html` | Redirect to `en/`. |
| `en/`, `zh/` | The two languages. |
| `llms.txt`, `llms-full.txt` | The page index and the full text for agents. `zh/` has its own two files. |

Add `--strict` to stop the build when Sphinx gives a warning. The CI uses this option.

To see the result, run:

```bash
uv run python -m http.server 8000 -d docs/build/html
```

Then open <http://localhost:8000>.

To build one language again after each change, run:

```bash
uv run sphinx-autobuild -c docs docs/en docs/build/html/en
uv run sphinx-autobuild -c docs -t zh docs/zh docs/build/html/zh
```

## Deploy

The repository has one deployment workflow for GitHub Pages and one for Cloudflare.
The repository variable `DOCS_DEPLOY_TARGET` selects the workflow. Without the variable, no workflow deploys.

| `DOCS_DEPLOY_TARGET` | Workflow | Setup |
| --- | --- | --- |
| `github-pages` | `gh-pages.yml` | In **Settings > Pages**, set **Source** to **GitHub Actions**. |
| `cloudflare` | `cloudflare.yml` | Add the secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. Set the Worker name in `docs/wrangler.jsonc`. |

For Cloudflare, also set the repository variable `DOCS_BASE_URL` to the address of the site.
The build uses this address for the links in `llms.txt`.
