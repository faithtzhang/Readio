import os
from typing import Dict, Optional
from app.services.llama4_service import get_client


class VideoService:
    """Service for extracting text from video using Llama API."""
    
    def __init__(self):
        self.perspectives = {
            "educational": "Academic and informative tone",
            "entertaining": "Engaging and conversational tone", 
            "professional": "Business and formal tone",
            "casual": "Relaxed and friendly tone",
            "technical": "Detailed and technical explanations"
        }
    
    def process_video_to_text(self, video_path: str, perspective: Optional[str] = None) -> Dict:
        """Extract text from video using Llama API."""
        try:
            client = get_client()
            
            # Analyze video
            analysis_prompt = f"""
            Analyze this video at {video_path} and provide insights on:
            1. Visual content and scenes
            2. Charts, graphs, or data visualizations
            3. Text overlays or captions
            4. Key themes and topics
            5. Recommended narrative structure
            """
            
            analysis_response = client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[{"role": "user", "content": analysis_prompt}]
            )
            
            video_insights = analysis_response.choices[0].message.content
            
            # Generate script
            script_prompt = f"""
            Based on the video analysis, create a comprehensive narrative script.
            Perspective: {perspective or 'neutral'}
            Video insights: {video_insights}
            
            Generate a script that:
            1. Introduces the main topics
            2. Explains visual elements and charts
            3. Provides context and insights
            4. Maintains engaging flow
            5. Adapts to the specified perspective
            """
            
            script_response = client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[{"role": "user", "content": script_prompt}]
            )
            
            script = script_response.choices[0].message.content or ""
            
            return {
                "success": True,
                "video_path": video_path,
                "text": script,
                "perspective": perspective or "neutral"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
