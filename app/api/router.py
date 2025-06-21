from fastapi import APIRouter
from app.services.book_service import generate_video_script

router = APIRouter()

@router.post("/generate_video/", response_model=BookRecommendationResponse)
async def generate_video(request: BookRecommendationRequest):
    books = fetch_books_by_labels(request.labels)
    script = generate_video_script(books)
    video_url = generate_video_content(script)
    audio_url = generate_audio(script)
    return BookRecommendationResponse(video_url=video_url, audio_url=audio_url)

# @router.post("/summarize/")
# def summarize(book: dict):
#     script = generate_summary(book["summary"], book.get("voice_style", "Neutral"))
#     return {"script": script}

# @router.post("/tts/")
# def text_to_audio(req: dict):
#     return {"audio_url": synthesize(req["script"], req["voice_id"])}
