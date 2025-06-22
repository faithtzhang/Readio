from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from app.services.book_service import generate_video_script
from app.services.audio_service import generate_audio
from app.services.video_service import VideoService
import os
import shutil

router = APIRouter()

# Pydantic models for request bodies
class GenerateVideoRequest(BaseModel):
    labels: List[str]

class DownloadVideoRequest(BaseModel):
    s3_key: str
    local_path: str = None

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
    # return {"script": script}

@router.post("/video/download")
async def download_video(request: DownloadVideoRequest):
    """Download video from S3 to local storage."""
    if not video_service:
        raise HTTPException(status_code=500, detail="Video service not available")
    
    local_path = video_service.download_video_from_s3(request.s3_key, request.local_path)
    if local_path:
        return {"success": True, "local_path": local_path}
    else:
        raise HTTPException(status_code=500, detail="Failed to download video")

@router.post("/video/get-url")
async def get_video_url(request: DownloadVideoRequest):
    """Get a pre-signed URL for video download."""
    if not video_service:
        raise HTTPException(status_code=500, detail="Video service not available")
    
    url = video_service.get_video_url(request.s3_key)
    if url:
        return {"success": True, "download_url": url}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate download URL")

@router.post("/video/analyze")
async def analyze_video(video: UploadFile = File(...), perspective: str = "professional"):
    if not video_service:
        raise HTTPException(status_code=500, detail="Video service not available")
    
    result = video_service.process_video_to_audio(video.file, perspective)
    # result["filename"] = video.filename
    
    return result

@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Readio API is running"}
