from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_recommend_without_labels():
    res = client.post("/recommend/", json={})
    assert res.status_code == 200
    assert res.json() == {"error": "Provide at least one label"}

def test_recommend_with_labels():
    # Use common labels present in Open Library
    payload = {"labels": ["science_fiction", "adventure"]}
    res = client.post("/recommend/", json=payload)
    assert res.status_code == 200
    data = res.json().get("recommendations", [])
    assert isinstance(data, list)
    if data:
        assert "title" in data[0]
        assert "authors" in data[0]
        assert "score" in data[0]

def test_summarize_missing_keys():
    res = client.post("/summarize/", json={})
    assert res.status_code == 500 or res.status_code == 422

def test_tts_missing_keys():
    res = client.post("/tts/", json={})
    assert res.status_code == 500 or res.status_code == 422
