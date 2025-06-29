import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from app.services.book_service import generate_video_script
from app.services.audio_service import generate_audio
from app.services.video_service import VideoService

router = APIRouter()

# Pydantic models for request bodies
class GenerateVideoRequest(BaseModel):
    labels: List[str]

class VideoPathRequest(BaseModel):
    path: str
    perspective: str = "professional"

# Initialize video service
try:
    video_service = VideoService()
except Exception as e:
    print(f"Warning: Could not initialize VideoService: {e}")
    video_service = None

@router.post("/generate_video/")
async def generate_video(request: GenerateVideoRequest):
    script = generate_video_script(request.labels)
    video_url = video_service.generate_video_content(script)
    audio_url = generate_audio(script)
    return {"video_url": video_url, "audio_url": audio_url}

@router.post("/video/analyze")
async def analyze_video(request: VideoPathRequest):
    if not video_service:
        raise HTTPException(status_code=500, detail="Video service not available")
    
    if not os.path.isfile(request.path):
        raise HTTPException(status_code=400, detail=f"Video file not found at {request.path}")

    try:
        result = video_service.process_video_to_audio(request.path, request.perspective)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return result


@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Readio API is running"}
