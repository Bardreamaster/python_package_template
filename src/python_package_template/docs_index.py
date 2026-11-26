"""List, read and search the Markdown documentation that ships with the package.

The wheel contains the documentation sources in `_docs/<language>/`. In a
source checkout the functions read `docs/<language>/` instead.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

LANGUAGES = ("en", "zh")

# Directories that Sphinx extensions generate inside a source tree.
_GENERATED_DIRS = frozenset({"apidocs"})

_TOCTREE_RE = re.compile(r"^```\{toctree\}[^\n]*\n(.*?)^```", re.DOTALL | re.MULTILINE)
_TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class DocPage:
    """One documentation page."""

    path: str
    """Page identifier, for example `en/user/installation`."""
    title: str
    """Text of the first level-one heading."""


@dataclass(frozen=True)
class SearchHit:
    """One page that matches a search query."""

    path: str
    """Page identifier, for example `en/user/installation`."""
    title: str
    """Text of the first level-one heading."""
    score: int
    """Number of matches. A match in the title counts five times."""
    snippets: list[str]
    """The first lines of the page that contain a query term."""


def docs_root() -> Path:
    """Return the directory that contains one subdirectory for each language.

    Raises:
        FileNotFoundError: If the documentation is not installed.
    """
    bundled = Path(__file__).resolve().parent / "_docs"
    if bundled.is_dir():
        return bundled
    checkout = Path(__file__).resolve().parents[2] / "docs"
    if (checkout / LANGUAGES[0]).is_dir():
        return checkout
    raise FileNotFoundError("The documentation files are not installed.")


def list_pages(language: str = "en") -> list[DocPage]:
    """Return all pages of one language in reading order.

    The order follows the `toctree` directives, starting at `index.md`.
    Pages that no `toctree` contains come last, in alphabetical order.

    Args:
        language: Language code. One of `LANGUAGES`.

    Raises:
        ValueError: If the language is unknown.
    """
    root = _language_root(language)
    ordered: list[Path] = []
    _walk_toctree(root / "index.md", root, ordered)
    for file in sorted(root.rglob("*.md")):
        if file not in ordered and not _is_generated(file, root):
            ordered.append(file)
    return [_page(file, root, language) for file in ordered]


def read_page(path: str) -> str:
    """Return the Markdown source of one page.

    Args:
        path: Page identifier from `list_pages`. The `.md` suffix is
            optional.

    Raises:
        ValueError: If the path does not start with a known language or
            points outside the documentation.
        FileNotFoundError: If the page does not exist.
    """
    language, _, rest = path.strip("/").removesuffix(".md").partition("/")
    root = _language_root(language)
    file = (root / f"{rest or 'index'}.md").resolve()
    if not file.is_relative_to(root.resolve()):
        raise ValueError(f"Path is outside the documentation: {path!r}")
    if not file.is_file():
        raise FileNotFoundError(f"No such page: {path!r}")
    return file.read_text(encoding="utf-8")


def search_pages(query: str, language: str = "en", limit: int = 10) -> list[SearchHit]:
    """Search the pages of one language.

    The search ignores case. A page matches when it contains every
    whitespace-separated term of the query.

    Args:
        query: Search terms.
        language: Language code. One of `LANGUAGES`.
        limit: Maximum number of results.

    Returns:
        The matching pages, best match first.

    Raises:
        ValueError: If the language is unknown.
    """
    terms = query.lower().split()
    if not terms:
        return []
    hits: list[SearchHit] = []
    for page in list_pages(language):
        text = read_page(page.path)
        lowered = text.lower()
        if not all(term in lowered for term in terms):
            continue
        title = page.title.lower()
        score = sum(lowered.count(term) + 4 * title.count(term) for term in terms)
        snippets = [
            line.strip()
            for line in text.splitlines()
            if any(term in line.lower() for term in terms)
        ]
        hits.append(SearchHit(page.path, page.title, score, snippets[:3]))
    hits.sort(key=lambda hit: -hit.score)
    return hits[:limit]


def _language_root(language: str) -> Path:
    if language not in LANGUAGES:
        raise ValueError(f"Unknown language {language!r}. Use one of {LANGUAGES}.")
    return docs_root() / language


def _is_generated(file: Path, root: Path) -> bool:
    return bool(_GENERATED_DIRS.intersection(file.relative_to(root).parts))


def _page(file: Path, root: Path, language: str) -> DocPage:
    text = file.read_text(encoding="utf-8")
    match = _TITLE_RE.search(text)
    relative = file.relative_to(root).with_suffix("").as_posix()
    title = match.group(1) if match else relative
    return DocPage(f"{language}/{relative}", title)


def _walk_toctree(file: Path, root: Path, ordered: list[Path]) -> None:
    """Append `file` and the pages below it in `toctree` order."""
    if not file.is_file() or file in ordered or _is_generated(file, root):
        return
    ordered.append(file)
    text = file.read_text(encoding="utf-8")
    for block in _TOCTREE_RE.findall(text):
        for line in block.splitlines():
            entry = line.strip()
            if not entry or entry.startswith(":"):
                continue
            # An entry is "target" or "Title <target>".
            target = entry.rsplit("<", 1)[-1].rstrip(">").strip().removesuffix(".md")
            base = root if target.startswith("/") else file.parent
            _walk_toctree(base / f"{target.lstrip('/')}.md", root, ordered)
