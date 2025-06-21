import requests
from app.config import settings

def generate_video_content(script):
    headers = {"Authorization": f"Bearer {settings.AI4CHAT_API_KEY}"}
    data = {"prompt": script, "duration": 30, "shape": "rectangle"}
    response = requests.post(settings.AI4CHAT_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("video_url")
    else:
        return "Error generating video"
