from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"


def pages(language: str) -> list[str]:
    """Return the Markdown pages of one language, without the generated API pages."""
    root = DOCS_DIR / language
    files = (file.relative_to(root) for file in root.rglob("*.md"))
    return sorted(file.as_posix() for file in files if file.parts[0] != "apidocs")


def test_languages_have_the_same_pages():
    assert pages("en") == pages("zh")
    assert "index.md" in pages("en")
