from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_video():
    response = client.post("/api/v1/generate_video/", json={"labels": ["fiction", "adventure"]})
    assert response.status_code == 200
    assert "video_url" in response.json()
    assert "audio_url" in response.json()
