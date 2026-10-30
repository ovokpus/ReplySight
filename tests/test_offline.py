"""Offline checks used by CI: no OpenAI/Tavily key, no network calls to model providers."""
import os
import sys

# The API modules import each other as top-level packages (config, models, services), as in the Docker image.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "api"))
os.environ.pop("OPENAI_API_KEY", None)
os.environ.pop("TAVILY_API_KEY", None)

from fastapi.testclient import TestClient  # noqa: E402

from app import app  # noqa: E402

client = TestClient(app)


def test_health_reports_missing_keys():
    body = client.get("/health").json()
    assert body["dependencies"]["openai"] is False
    assert body["dependencies"]["tavily"] is False
    assert body["workflow"]["graph_compilation"] == "ok"


def test_workflow_graph_is_served_without_keys():
    r = client.get("/workflow/graph")
    assert r.status_code == 200
    assert "mermaid" in r.text.lower() or "graph" in r.text.lower()


def test_respond_validates_input():
    assert client.post("/respond", json={}).status_code == 422
