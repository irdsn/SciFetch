from openai import api_key

from agents.scientific_fetcher import run_agent, extract_relevant_articles
from pathlib import Path
import pytest
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

API_KEY = os.getenv("OPENAI_API_KEY")

@pytest.mark.skipif("OPENAI_API_KEY" not in os.environ, reason="Missing OpenAI API Key in .env")
def test_run_agent_real_integration(monkeypatch):
    """
    Integration test for run_agent using a real prompt and real API key.
    """

    monkeypatch.setenv("OPENAI_API_KEY", API_KEY)

    prompt = "Quantum computing and cryptography"
    result = run_agent(prompt)

    assert isinstance(result, dict)
    assert "summary" in result
    assert "articles" in result
    assert "markdown" in result
    assert "output_file" in result

    output_path = Path(result["output_file"])
    assert output_path.exists()
    assert output_path.suffix == ".md"
    assert len(result["summary"]) > 20
    assert len(result["articles"]) > 0

def test_extract_relevant_articles():
    """
    Unit test for extract_relevant_articles with mock summary and articles.
    """
    summary = "The paper titled 'ABC Quantum' and 'XYZ Cryptography' are particularly relevant."
    articles = [
        {"title": "ABC Quantum", "abstract": "Quantum stuff", "doi": "abc/123", "url": "http://example.com/abc"},
        {"title": "XYZ Cryptography", "abstract": "Crypto stuff", "doi": "xyz/456", "url": "http://example.com/xyz"},
        {"title": "Unrelated Article", "abstract": "No relevance", "doi": "none/000", "url": "http://example.com/none"},
    ]

    relevant = extract_relevant_articles(summary, articles)

    assert len(relevant) == 2
    assert any(a["title"] == "ABC Quantum" for a in relevant)
    assert any(a["title"] == "XYZ Cryptography" for a in relevant)
