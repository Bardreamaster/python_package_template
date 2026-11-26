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
import re
import shutil
import subprocess
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = DOCS_DIR / "build" / "html"
DOCTREE_DIR = DOCS_DIR / "build" / "doctrees"

# Each language is one source tree in DOCS_DIR.
LANGUAGES = ("en", "zh")
# The site root sends the reader to this language.
DEFAULT_LANGUAGE = "en"

# Directories that Sphinx extensions generate inside a source tree.
GENERATED_DIRS = frozenset({"apidocs"})

TOCTREE_RE = re.compile(r"^```\{toctree\}[^\n]*\n(.*?)^```", re.DOTALL | re.MULTILINE)
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)

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


def list_pages(language: str) -> list[Path]:
    """Return the Markdown pages of one language in reading order.

    The order follows the `toctree` directives, starting at `index.md`.
    Pages that no `toctree` contains come last, in alphabetical order.
    """
    root = DOCS_DIR / language
    pages: list[Path] = []

    def is_generated(file: Path) -> bool:
        return bool(GENERATED_DIRS.intersection(file.relative_to(root).parts))

    def walk(file: Path) -> None:
        if not file.is_file() or file in pages or is_generated(file):
            return
        pages.append(file)
        for block in TOCTREE_RE.findall(file.read_text(encoding="utf-8")):
            for line in block.splitlines():
                entry = line.strip()
                if not entry or entry.startswith(":"):
                    continue
                # An entry is "target" or "Title <target>".
                target = entry.rsplit("<", 1)[-1].rstrip(">").strip()
                target = target.removesuffix(".md")
                base = root if target.startswith("/") else file.parent
                walk(base / f"{target.lstrip('/')}.md")

    walk(root / "index.md")
    for file in sorted(root.rglob("*.md")):
        if file not in pages and not is_generated(file):
            pages.append(file)
    return pages


def page_title(file: Path) -> str:
    """Return the text of the first level-one heading of a page."""
    match = TITLE_RE.search(file.read_text(encoding="utf-8"))
    return match.group(1) if match else file.stem


def write_llms_files(language: str, directory: Path, base_url: str) -> None:
    """Write `llms.txt` and `llms-full.txt` for one language.

    Args:
        language: Language of the pages.
        directory: Directory that receives the two files.
        base_url: Address of the site root. Empty for relative links.
    """
    root = DOCS_DIR / language
    pages = list_pages(language)

    def link(file: Path) -> str:
        page = file.relative_to(DOCS_DIR).with_suffix(".html")
        if base_url:
            return f"{base_url}/{page.as_posix()}"
        return Path(os.path.relpath(OUTPUT_DIR / page, directory)).as_posix()

    # Group the pages by subdirectory. Top-level pages go into "Docs".
    sections: dict[str, list[str]] = {}
    for file in pages:
        parts = file.relative_to(root).parts
        heading = "Docs"
        if len(parts) > 1:
            index = root / parts[0] / "index.md"
            heading = page_title(index) if index.is_file() else parts[0]
        entry = f"- [{page_title(file)}]({link(file)})"
        sections.setdefault(heading, []).append(entry)

    lines = [f"# {page_title(root / 'index.md')}"]
    for heading, entries in sections.items():
        lines += ["", f"## {heading}", "", *entries]
    (directory / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    full = []
    for file in pages:
        name = file.relative_to(DOCS_DIR).with_suffix("").as_posix()
        text = file.read_text(encoding="utf-8").strip()
        full.append(f"<!-- {name} -->\n\n{text}\n")
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
    for language in LANGUAGES:
        build_language(language, sphinx_options)

    redirect = REDIRECT_PAGE.format(language=DEFAULT_LANGUAGE)
    (OUTPUT_DIR / "index.html").write_text(redirect, encoding="utf-8")

    for language in LANGUAGES:
        is_default = language == DEFAULT_LANGUAGE
        directory = OUTPUT_DIR if is_default else OUTPUT_DIR / language
        write_llms_files(language, directory, base_url)

    print(f"The site is in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
