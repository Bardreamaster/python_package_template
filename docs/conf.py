# Configuration file for the Sphinx documentation builder.
#
# The English and the Chinese documentation are two independent source trees:
# docs/en and docs/zh. Both trees use this file. Select the Chinese settings
# with the Sphinx tag "zh":
#
#   sphinx-build -c docs docs/en docs/build/html/en
#   sphinx-build -c docs -t zh docs/zh docs/build/html/zh
#
# docs/build_docs.py runs both builds and writes the files of the site root.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from importlib.metadata import version as package_version
from pathlib import Path

# Make docstring_parser.py importable.
sys.path.insert(0, str(Path(__file__).parent))

# Sphinx puts the "tags" object into the namespace of this file.
docs_language = "zh" if tags.has("zh") else "en"  # noqa: F821

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "python_package_template"
copyright = "2025, Wei Jinqi"
author = "Wei Jinqi"
# The version has one source: pyproject.toml. Install the package to read it.
release = package_version("python-package-template")
version = release
language = "zh_CN" if docs_language == "zh" else "en"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "autodoc2",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

# Options for autodoc2 extension. The path is relative to the source tree.
autodoc2_packages = [
    "../../src/python_package_template",
]
autodoc2_module_all_regexes = []
# Do not show names that start with an underscore.
autodoc2_hidden_objects = ["inherited", "private"]

# autodoc2_render_plugin = "myst"
autodoc2_docstring_parser_regexes = [
    # this will render all docstrings as Markdown
    (r".*", "docstring_parser"),
]
## ignore all warnings from this package
# nitpick_ignore_regex = [
#     ("py:.*", r"python_package_template\..*"),
# ]

# myst config
## enable md docstring
myst_enable_extensions = [
    "colon_fence",
    "fieldlist",
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"

# The deployment workflows set DOCS_BASE_URL to the public address of the site.
site_base_url = os.environ.get("DOCS_BASE_URL", "").rstrip("/")
if site_base_url:
    html_baseurl = f"{site_base_url}/{docs_language}/"

# The language link in the sidebar. See _templates/sidebar/language.html.
html_context = {
    "other_language": "en" if docs_language == "zh" else "zh",
    "other_language_name": "English" if docs_language == "zh" else "中文",
}
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/language.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
        "sidebar/variant-selector.html",
    ]
}

# Options for Furo theme
source_repository = "https://github.com/Bardreamaster/python_package_template"
source_branch = "main"
source_directory = f"docs/{docs_language}/"
html_theme_options = {
    "source_repository": source_repository,
    "source_branch": source_branch,
    "source_directory": source_directory,
    "top_of_page_buttons": ["view", "edit"],
}
