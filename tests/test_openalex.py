import pytest
from apis.OpenAlex import OpenAlexClient, OpenAlexTool

def test_openalex_client_returns_results():
    """
    Test that OpenAlexClient returns structured results for a valid query.
    """
    client = OpenAlexClient()
    results = client.search("neural networks", max_results=3)

    assert isinstance(results, list)
    assert len(results) > 0
    for item in results:
        assert "title" in item
        assert "abstract" in item
        assert "doi" in item
        assert "source" in item and item["source"] == "OpenAlex"
        assert "url" in item
        assert "publication_date" in item


def test_openalex_tool_call_consistency():
    """
    Ensure the OpenAlexTool __call__ returns expected data format.
    """
    tool = OpenAlexTool()
    results = tool("machine learning")

    assert isinstance(results, list)
    assert len(results) > 0
    assert all("title" in r and r["source"] == "OpenAlex" for r in results)


def test_decode_abstract_logic():
    """
    Verifies correct decoding of an abstract from OpenAlex inverted index format.
    """
    client = OpenAlexClient()
    mock_item = {
        "abstract_inverted_index": {
            "deep": [0],
            "learning": [1],
            "models": [2],
            "are": [3],
            "powerful": [4]
        }
    }

    decoded = client.decode_abstract(mock_item)
    assert decoded == "deep learning models are powerful"
