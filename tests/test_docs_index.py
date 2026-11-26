import asyncio

import pytest

from python_package_template import docs_index


def test_languages_have_the_same_pages():
    english = [page.path.removeprefix("en/") for page in docs_index.list_pages("en")]
    chinese = [page.path.removeprefix("zh/") for page in docs_index.list_pages("zh")]
    assert english == chinese
    assert english[0] == "index"


def test_read_page():
    assert docs_index.read_page("en/user/installation").startswith("# Installation")
    assert docs_index.read_page("zh/user/installation.md").startswith("# 安装")


@pytest.mark.parametrize("path", ["fr/index", "en/../../pyproject", "en/../conf"])
def test_read_page_rejects_paths_outside_the_docs(path):
    with pytest.raises((ValueError, FileNotFoundError)):
        docs_index.read_page(path)


def test_search_pages():
    hits = docs_index.search_pages("mcp server")
    assert hits[0].path == "en/agents/mcp"
    assert hits[0].snippets
    assert docs_index.search_pages("安装", language="zh")
    assert docs_index.search_pages("no-page-contains-this-term") == []


def test_mcp_server_tools():
    pytest.importorskip("mcp")
    from python_package_template.mcp_server import create_server

    tools = asyncio.run(create_server().list_tools())
    assert {tool.name for tool in tools} == {"list_docs", "read_doc", "search_docs"}
