"""Build the documentation site.

The script builds the English and the Chinese source tree with Sphinx and
writes the files of the site root:

    docs/build/html/index.html       redirect to the English documentation
    docs/build/html/llms.txt         page index for agents (English)
    docs/build/html/llms-full.txt    all English pages in one file
    docs/build/html/en/              English documentation
    docs/build/html/zh/              Chinese documentation, with its own
                                     llms.txt and llms-full.txt

Run it from the repository root: `uv run python docs/build_docs.py`.
Set the environment variable `DOCS_BASE_URL` to the public address of the
site to get absolute links in `llms.txt`.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from python_package_template import docs_index

DOCS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = DOCS_DIR / "build" / "html"
DOCTREE_DIR = DOCS_DIR / "build" / "doctrees"

# The site root sends the reader to this language.
DEFAULT_LANGUAGE = "en"

REDIRECT_PAGE = """\
<!DOCTYPE html>
<html lang="{language}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url={language}/">
    <link rel="canonical" href="{language}/">
    <title>Redirecting</title>
  </head>
  <body>
    <p><a href="{language}/">Open the documentation.</a></p>
  </body>
</html>
"""


def build_language(language: str, sphinx_options: list[str]) -> None:
    """Build the source tree of one language with Sphinx."""
    command = [sys.executable, "-m", "sphinx", "-b", "html", "-c", str(DOCS_DIR)]
    command += ["-d", str(DOCTREE_DIR / language)]
    if language != DEFAULT_LANGUAGE:
        command += ["-t", language]
    command += sphinx_options
    command += [str(DOCS_DIR / language), str(OUTPUT_DIR / language)]
    subprocess.run(command, check=True)


def write_llms_files(language: str, directory: Path, base_url: str) -> None:
    """Write `llms.txt` and `llms-full.txt` for one language.

    Args:
        language: Language of the pages.
        directory: Directory that receives the two files.
        base_url: Address of the site root. Empty for relative links.
    """
    pages = docs_index.list_pages(language)
    titles = {page.path: page.title for page in pages}

    def link(page: docs_index.DocPage) -> str:
        if base_url:
            return f"{base_url}/{page.path}.html"
        target = OUTPUT_DIR / f"{page.path}.html"
        return Path(os.path.relpath(target, directory)).as_posix()

    # Group the pages by subdirectory. Top-level pages go into "Docs".
    sections: dict[str, list[str]] = {}
    for page in pages:
        parts = page.path.split("/")
        name = parts[1] if len(parts) > 2 else ""
        heading = titles.get(f"{language}/{name}/index", name) if name else "Docs"
        sections.setdefault(heading, []).append(f"- [{page.title}]({link(page)})")

    index = [f"# {titles[f'{language}/index']}"]
    for heading, links in sections.items():
        index += ["", f"## {heading}", "", *links]
    (directory / "llms.txt").write_text("\n".join(index) + "\n", encoding="utf-8")

    full = []
    for page in pages:
        text = docs_index.read_page(page.path).strip()
        full.append(f"<!-- {page.path} -->\n\n{text}\n")
    (directory / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--strict", action="store_true", help="Stop when Sphinx gives a warning."
    )
    arguments = parser.parse_args()
    sphinx_options = ["-W", "--keep-going"] if arguments.strict else []
    base_url = os.environ.get("DOCS_BASE_URL", "").rstrip("/")

    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    for language in docs_index.LANGUAGES:
        build_language(language, sphinx_options)

    redirect = REDIRECT_PAGE.format(language=DEFAULT_LANGUAGE)
    (OUTPUT_DIR / "index.html").write_text(redirect, encoding="utf-8")

    for language in docs_index.LANGUAGES:
        is_default = language == DEFAULT_LANGUAGE
        directory = OUTPUT_DIR if is_default else OUTPUT_DIR / language
        write_llms_files(language, directory, base_url)

    print(f"The site is in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
