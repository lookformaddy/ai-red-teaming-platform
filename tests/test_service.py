import pytest
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from red_teaming.service import app

def test_health_and_attacks():
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    attacks = client.get("/attacks").json()
    assert len(attacks) == 21

def test_evaluate_endpoint():
    client = TestClient(app)
    body = client.post("/evaluate", json={"mode": "strict"}).json()
    assert body["total"] == 21 and body["successes"] == 4
