import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_run_endpoint_with_mock(monkeypatch):
    # Patch run_agent to return a fixed response
    def mock_run_agent(prompt):
        return {
            "summary": "mock summary",
            "articles": [{}] * 3,
            "markdown": "# Mock Markdown",
            "output_file": "mock_path.md"
        }

    monkeypatch.setattr("app.run_agent", mock_run_agent)

    response = client.post("/run", json={
        "prompt": "cancer prevention",
        "api_key": "sk-test-key"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["message"].startswith("✅")
    assert "output_file" in data
