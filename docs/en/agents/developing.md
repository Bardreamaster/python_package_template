# Change the repository

This page is for an agent that changes the code or the documentation in this repository.

## Rules

- Write all comments and docstrings in English.
- Use type hints in new code.
- When you change a page in `docs/en/`, make the same change in `docs/zh/`. Do the same in the other direction.
- Write the Chinese text as original Chinese. Do not translate sentence by sentence.
- Do not edit `docs/<language>/apidocs/`. The build generates these files.
- Do not commit files from `docs/internal/`.
- Change the version only in `pyproject.toml`.

:::{admonition} Template placeholder
Add the rules of your project.
:::

## Code map

| Path | Content |
| --- | --- |
| `src/python_package_template/` | The package. |
| `tests/` | The tests. One test file for each module. |
| `docs/en/`, `docs/zh/` | The documentation. Same structure in both. |
| `docs/conf.py` | The Sphinx configuration for both languages. |
| `docs/build_docs.py` | The script that builds the site. |
| `.github/workflows/` | CI, release and deployment. |

## Checks

Run these commands before you finish. All of them must pass.

```bash
uv run ruff check
uv run ruff format --check
uv run pytest
uv run python docs/build_docs.py --strict
```

## Common tasks

### Add a feature

1. Add the code in `src/python_package_template/`.
2. Add tests in `tests/`.
3. Describe the feature in `docs/en/user/usage.md` and `docs/zh/user/usage.md`.
4. Run the checks.

### Add a documentation page

1. Create the page with the same file name in `docs/en/` and `docs/zh/`.
2. Add the page to the `toctree` of the section index in both languages.
3. Run `uv run python docs/build_docs.py --strict`.

### Release a version

1. Change `version` in `pyproject.toml`.
2. Run the checks.
3. Tell the user to push the tag `v<version>`. Do not push tags yourself.
