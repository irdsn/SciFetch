import pytest
from apis.CrossRef import CrossRefClient, CrossRefTool

@pytest.mark.parametrize("query", ["quantum computing", "natural language processing"])
def test_crossref_client_returns_results(query):
    """
    Test that CrossRefClient returns a non-empty list of results
    with expected fields for a valid query.
    """
    client = CrossRefClient()
    results = client.search(query=query, max_results=3)

    assert isinstance(results, list)
    assert len(results) > 0
    for item in results:
        assert "title" in item
        assert "abstract" in item
        assert "doi" in item
        assert "url" in item
        assert item["source"] == "CrossRef"


def test_crossref_tool_call_and_run_consistency():
    """
    Ensure CrossRefTool __call__ and _run behave identically and return expected structure.
    """
    tool = CrossRefTool()
    query = "deep learning"

    results_call = tool(query)
    results_run = tool._run(query)

    assert isinstance(results_call, list)
    assert isinstance(results_run, list)
    assert results_call == results_run
    assert len(results_call) > 0
    assert all("title" in pub for pub in results_call)


def test_crossref_tool_arun_not_implemented():
    """
    Verify that asynchronous execution raises NotImplementedError.
    """
    tool = CrossRefTool()
    with pytest.raises(NotImplementedError):
        tool._arun("any query")
