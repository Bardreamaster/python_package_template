# Python Package Template

[简体中文](README.zh-CN.md)

A template for a Python package with a `src` layout. It uses uv, ruff and pytest.
It includes Sphinx documentation in English and Chinese, guides for AI agents, and GitHub Actions workflows.

## Quick Start

1. Click the "Use this template" button on GitHub to create a new repository. Then clone your repository.

2. Initialize the package with the desired name, author, and email:

    ```bash
    bash init_package.sh --name your-package-name --author "Your Name" --email "your.email@example.com"
    ```

    | Option | Meaning |
    | --- | --- |
    | `--description TEXT` | The one-line description in `pyproject.toml` and the README. |
    | `--repo OWNER/NAME` | The GitHub repository. The default is the `origin` remote. |
    | `--docs-url URL` | The address of the documentation site. The default is `https://OWNER.github.io/NAME/`. |

    The script changes the package name, the author, the copyright line in `LICENSE`, the project URLs, and both README files.
    It runs on Linux and macOS. It does not rename the repository directory.

3. Delete the `init_package.sh` script.

4. Install the dependencies and run the checks:

    ```bash
    uv sync
    uv run ruff check
    uv run pytest
    uv run python docs/build_docs.py
    ```

5. Write the documentation. Search `docs/` for "Template placeholder" and "模板占位" to find the pages that need your content.

6. (Optional) Change the license. The default license is MIT. Change the `LICENSE` file and the `license` field in `pyproject.toml` together.

## GitHub Actions

The workflows are in `.github/workflows`. Their triggers are active.
The steps that publish or deploy do nothing until you complete the setup in this table.

| Workflow | Runs on | Purpose | Setup |
| --- | --- | --- | --- |
| `tests.yml` | push to `main`, pull request | Lint, tests, documentation build | None. To use Codecov, add the secret `CODECOV_TOKEN`. Without it, the upload steps do not run. |
| `pypi.yml` | push to `main`, pull request, tag `v*.*.*` | Build the package. Publish it to PyPI when you push a version tag. | Create the [environment](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) `pypi` and configure [Trusted Publishing](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/#configuring-trusted-publishing). |
| `gh-pages.yml` | push to `main` | Deploy the documentation to GitHub Pages | Set the repository variable `DOCS_DEPLOY_TARGET` to `github-pages`. In **Settings > Pages**, set **Source** to **GitHub Actions**. |
| `cloudflare.yml` | push to `main` | Deploy the documentation to Cloudflare | Set the repository variable `DOCS_DEPLOY_TARGET` to `cloudflare`. Add the secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. Set the Worker name in `docs/wrangler.jsonc`. |
| `template-selftest.yml` | push to `main`, pull request | Test `init_package.sh` in the template repository | None. `init_package.sh` deletes this workflow. |

Use one of the two deployment workflows and delete the other.
The publish job in `pypi.yml` does not run in a repository that is marked as a template.

## Directory Structure

```plaintext
python_package_template/
├── .devcontainer/          # Development container configuration
├── .github/workflows/      # CI, release and documentation deployment
├── docs/
│   ├── en/                 # English documentation: user/, developer/, agents/
│   ├── zh/                 # Chinese documentation with the same structure
│   ├── conf.py             # Sphinx configuration for both languages
│   └── build_docs.py       # Builds the site, llms.txt and llms-full.txt
├── src/
│   └── python_package_template/  # Source code for the package
├── tests/                  # Test files
├── .gitattributes          # Line endings and binary files
├── .gitignore              # Git ignore file with common python patterns
├── .pre-commit-config.yaml # Pre-commit configuration file
├── AGENTS.md               # Entry point for coding agents
├── init_package.sh         # Script to initialize the package
├── LICENSE                 # License file
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # This file, the README
└── README.zh-CN.md         # The README in Chinese
```

### devcontainer

This repository includes a `.devcontainer` folder for setting up a development container using Visual Studio Code. To use it, follow these steps:
1. Install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension in Visual Studio Code.
2. Open the repository in Visual Studio Code.
3. Press `F1` and select "Dev Containers: Reopen in Container" from the command palette.
4. Wait for the container to build and start. This may take a few minutes, especially the first time.
5. Once the container is running, you can start developing your Python package in a consistent environment.

## Related Sources

- [Python Packaging User Guide](https://packaging.python.org)
