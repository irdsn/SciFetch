import pytest
from apis.arXiv import ArxivClient, ArxivTool


@pytest.mark.parametrize("query", ["quantum", "machine learning"])
def test_arxiv_client_returns_results(query):
    """
    Test that ArxivClient returns a non-empty list of results
    with expected keys when given a valid query.
    """
    client = ArxivClient()
    results = client.search(query=query, max_results=3)

    assert isinstance(results, list)
    assert len(results) > 0
    for article in results:
        assert "title" in article
        assert "abstract" in article
        assert "url" in article
        assert "source" in article
        assert article["source"] == "arXiv"


def test_arxiv_tool_call_matches_client():
    """
    Test that ArxivTool.__call__ and _run return results
    similar to those from the client directly.
    """
    tool = ArxivTool()
    query = "neural networks"

    results_call = tool(query)
    results_run = tool._run(query)

    assert isinstance(results_call, list)
    assert isinstance(results_run, list)
    assert results_call == results_run
    assert len(results_call) > 0
    assert all("title" in art for art in results_call)


def test_arxiv_tool_arun_not_implemented():
    """
    Ensure that async interface raises NotImplementedError.
    """
    tool = ArxivTool()
    with pytest.raises(NotImplementedError):
        tool._arun("any query")
