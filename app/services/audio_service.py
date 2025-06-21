import requests
from app.core.config import PLAYHT_API_KEY

def synthesize(text: str, voice_id: str) -> str:
    headers = {"Authorization": f"Bearer {PLAYHT_API_KEY}"}
    payload = {"voice": voice_id, "content": text}
    response = requests.post("https://api.play.ht/convert", json=payload, headers=headers)
    return response.json().get("audio_url")
