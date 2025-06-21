from fastapi import APIRouter
from app.services.recommender import recommend_by_labels
from app.services.llama4_service import generate_summary
from app.services.tts_service import synthesize

router = APIRouter()

@router.post("/recommend/")
def recommend(payload: dict):
    labels = payload.get("labels", [])
    if not labels:
        return {"error": "Provide at least one label"}
    recs = recommend_by_labels(labels, top_n=5)
    return {"recommendations": recs}

@router.post("/summarize/")
def summarize(book: dict):
    script = generate_summary(book["summary"], book.get("voice_style", "Neutral"))
    return {"script": script}

@router.post("/tts/")
def text_to_audio(req: dict):
    return {"audio_url": synthesize(req["script"], req["voice_id"])}
