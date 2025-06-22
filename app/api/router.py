from fastapi import APIRouter
from app.services.book_service import generate_video_script
from app.services.video_service import generate_video_content
from app.services.audio_service import generate_audio

router = APIRouter()

@router.post("/generate_video/")
async def generate_video(labels: list):
    script = generate_video_script(labels)
    video_url = generate_video_content(script)
    audio_url = generate_audio(script)
    return {"video_url": video_url, "audio_url": audio_url}

# @router.post("/summarize/")
# def summarize(book: dict):
#     script = generate_summary(book["summary"], book.get("voice_style", "Neutral"))
#     return {"script": script}

# @router.post("/tts/")
# def text_to_audio(req: dict):
#     return {"audio_url": synthesize(req["script"], req["voice_id"])}
