import pytest
from apis.PubMed import PubMedClient, PubMedTool

def test_pubmed_search_returns_ids():
    """
    Test that PubMedClient.search returns a list of article IDs for a valid query.
    """
    client = PubMedClient()
    ids = client.search("cancer", max_results=3)

    assert isinstance(ids, list)
    assert len(ids) > 0
    assert all(isinstance(i, str) for i in ids)


def test_pubmed_fetch_details_returns_articles():
    """
    Test that fetch_details returns structured metadata for given article IDs.
    """
    client = PubMedClient()
    ids = client.search("genomics", max_results=2)
    if not ids:
        pytest.skip("PubMed returned no IDs; skipping fetch_details test.")

    articles = client.fetch_details(ids)

    assert isinstance(articles, list)
    assert len(articles) > 0
    for article in articles:
        assert "title" in article
        assert "abstract" in article
        assert "doi" in article
        assert "source" in article and article["source"] == "PubMed"
        assert "url" in article
        assert "publication_date" in article


def test_pubmed_tool_call_returns_valid_data():
    """
    Test that PubMedTool returns a valid metadata list using __call__.
    """
    tool = PubMedTool()
    results = tool("machine learning")

    assert isinstance(results, list)
    assert len(results) > 0
    assert all("title" in r and r["source"] == "PubMed" for r in results)
