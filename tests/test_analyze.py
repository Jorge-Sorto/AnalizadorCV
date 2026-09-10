import json
from pathlib import Path

from app.services.llm_client import LLMError, LLMTimeoutError

CASES = json.loads((Path(__file__).parent / "fixtures/examples.json").read_text())


def test_analyze_returns_structured_result(client):
    case = CASES[0]
    payload = {"cv_text": case["cv_text"], "job_profile_text": case["job_profile_text"]}
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    assert 0 <= response.json()["compatibility_score"] <= 100
    assert len(response.json()["recommendations"]) >= 3


def test_short_input_returns_422(client):
    response = client.post("/api/v1/analyze", json={"cv_text": "corto", "job_profile_text": "corto"})
    assert response.status_code == 422


def test_examples_have_three_levels(client):
    response = client.get("/api/v1/examples")
    assert response.status_code == 200
    assert {item["level"] for item in response.json()} == {"alta", "media", "baja"}


def test_timeout_returns_503(client):
    def fail(*_):
        raise LLMTimeoutError("timeout")

    client.app.state.analyzer.llm.extract = fail
    case = CASES[0]
    payload = {"cv_text": case["cv_text"], "job_profile_text": case["job_profile_text"]}
    assert client.post("/api/v1/analyze", json=payload).status_code == 503


def test_invalid_provider_response_returns_502(client):
    def fail(*_):
        raise LLMError("json inválido")

    client.app.state.analyzer.llm.extract = fail
    case = CASES[0]
    payload = {"cv_text": case["cv_text"], "job_profile_text": case["job_profile_text"]}
    assert client.post("/api/v1/analyze", json=payload).status_code == 502
