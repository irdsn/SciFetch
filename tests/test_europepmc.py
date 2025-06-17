import pytest
from apis.EuropePMC import EuropePMCClient, EuropePMCTool

@pytest.mark.parametrize("query", ["machine learning", "cancer genomics"])
def test_europepmc_client_returns_results(query):
    """
    Test that EuropePMCClient returns a list of structured results for valid queries.
    """
    client = EuropePMCClient()
    results = client.search(query=query, max_results=3)

    assert isinstance(results, list)
    assert len(results) > 0
    for item in results:
        assert "title" in item
        assert "abstract" in item
        assert "doi" in item
        assert "url" in item
        assert item["source"] == "EuropePMC"


def test_europepmc_tool_call_consistency():
    """
    Ensure the EuropePMCTool __call__ returns a valid list of articles.
    """
    tool = EuropePMCTool()
    results = tool("bioinformatics")

    assert isinstance(results, list)
    assert len(results) > 0
    assert all("title" in r for r in results)
    assert all(r["source"] == "EuropePMC" for r in results)
