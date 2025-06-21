from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.recommender import recommend_by_labels
from app.services.llama4_service import generate_summary
from app.services.tts_service import synthesize
from app.services.video_processor import VideoProcessor
import os
import shutil
from typing import List, Optional

router = APIRouter()

# Initialize services
video_processor = VideoProcessor()

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

# Video Processing Endpoints

@router.post("/video/upload")
async def upload_video(video: UploadFile = File(...)):
    """Upload a video file for processing."""
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save uploaded video
        if video.filename is None:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        video_path = os.path.join(upload_dir, video.filename)
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        return {
            "success": True,
            "video_path": video_path,
            "filename": video.filename,
            "size": os.path.getsize(video_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/video/process")
def process_video(request: dict):
    """Process video with complete analysis and dubbing pipeline."""
    try:
        video_path = request.get("video_path")
        output_dir = request.get("output_dir", "output")
        perspectives = request.get("perspectives")  # Optional list of specific perspectives
        
        if not video_path:
            raise HTTPException(status_code=400, detail="Video path is required")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Convert perspectives to proper type if provided
        perspectives_list: Optional[List[str]] = None
        if perspectives is not None:
            if isinstance(perspectives, list):
                perspectives_list = perspectives
            else:
                raise HTTPException(status_code=400, detail="Perspectives must be a list")
        
        result = video_processor.process_video_complete(video_path, output_dir, perspectives_list)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@router.post("/video/analyze")
def analyze_video(request: dict):
    """Analyze video content only without audio generation."""
    try:
        video_path = request.get("video_path")
        
        if not video_path:
            raise HTTPException(status_code=400, detail="Video path is required")
        
        result = video_processor.process_video_analysis_only(video_path)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/video/dub")
def dub_video(request: dict):
    """Generate audio dub for existing script."""
    try:
        script = request.get("script")
        video_path = request.get("video_path")
        output_dir = request.get("output_dir", "output")
        perspective = request.get("perspective", "professional")
        
        if not script or not video_path:
            raise HTTPException(status_code=400, detail="Script and video path are required")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        result = video_processor.process_audio_only(str(script), str(video_path), output_dir, str(perspective))
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dubbing failed: {str(e)}")

@router.get("/video/status/{video_path:path}")
def get_video_status(video_path: str):
    """Get processing status and available options for a video."""
    try:
        result = video_processor.get_processing_status(video_path)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.post("/video/batch")
def batch_process_videos(request: dict):
    """Process multiple videos in batch."""
    try:
        video_paths = request.get("video_paths", [])
        output_dir = request.get("output_dir", "batch_output")
        
        if not video_paths:
            raise HTTPException(status_code=400, detail="Video paths are required")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        result = video_processor.batch_process_videos(video_paths, output_dir)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")

@router.get("/video/perspectives")
def get_available_perspectives():
    """Get available voice perspectives for dubbing."""
    try:
        return {
            "success": True,
            "perspectives": {
                "educational": "Academic and informative tone",
                "entertaining": "Engaging and conversational tone",
                "professional": "Business and formal tone",
                "casual": "Relaxed and friendly tone",
                "technical": "Detailed and technical explanations"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get perspectives: {str(e)}")

@router.get("/video/voices")
def get_available_voices():
    """Get available AWS Polly voices."""
    try:
        voices = video_processor.audio_dubber.get_available_voices()
        return voices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get voices: {str(e)}")
