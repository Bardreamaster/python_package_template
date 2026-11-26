# Contributing

## Set up

Install [uv](https://docs.astral.sh/uv/). Then run these commands in the repository root:

```bash
uv sync
uv run pre-commit install
```

`uv sync` installs the package and the `dev` dependency group into `.venv/`.

## Check your change

```bash
uv run ruff check
uv run ruff format --check
uv run pytest
```

All three commands must pass before you open a pull request.
`uv run ruff format` formats the code.

## Release

1. Change `version` in `pyproject.toml`. This is the only place that contains the version.
2. Merge the change into `main`.
3. Create the tag `v<version>` on that commit and push the tag.

The workflow `pypi.yml` builds the package and publishes it to PyPI.
The workflow uses [Trusted Publishing](https://docs.pypi.org/trusted-publishers/).
Configure the publisher on PyPI and create the GitHub environment `pypi` before the first release.

:::{admonition} Template placeholder
Add the rules of your project: branch names, commit messages, review.
:::
