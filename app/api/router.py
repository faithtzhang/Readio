from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.book_service import generate_video_script
from app.services.audio_service import generate_audio
from app.services.video_service import VideoService
import os
import shutil

router = APIRouter()

# Initialize video service
try:
    video_service = VideoService()
except Exception as e:
    print(f"Warning: Could not initialize VideoService: {e}")
    video_service = None

@router.post("/generate_video/")
async def generate_video(labels: list):
    script = generate_video_script(labels)
    audio_url = generate_audio(script)
    return {"script": script, "audio_url": audio_url}

@router.post("/video/analyze")
def analyze_video(request: dict):
    if not video_service:
        raise HTTPException(status_code=500, detail="Video service not available")
    
    video_path = request.get("video_path")
    if not video_path:
        raise HTTPException(status_code=400, detail="Video path required")
    return video_service.process_video_to_text(video_path, request.get("perspective"))

@router.post("/video/upload")
async def upload_video(video: UploadFile = File(...)):
    if not video.filename:
        raise HTTPException(status_code=400, detail="Filename required")
    
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    video_path = os.path.join(upload_dir, video.filename)
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    
    return {"video_path": video_path, "filename": video.filename}
