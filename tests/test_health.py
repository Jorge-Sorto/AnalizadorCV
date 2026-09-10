def test_health_returns_version(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["version"] == "1.0.0"


def test_docs_available(client):
    assert client.get("/docs").status_code == 200
