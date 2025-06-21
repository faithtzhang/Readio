import requests
import json
from typing import Dict, List, Optional
from app.core.config import LLAMA4_API_KEY, LLAMA4_API_BASE


class VideoAnalyzer:
    """Service for analyzing video content using Llama APIs."""
    
    def __init__(self):
        self.api_key = LLAMA4_API_KEY
        self.api_base = LLAMA4_API_BASE
    
    def analyze_video_frames(self, video_path: str, frame_interval: int = 30) -> List[Dict]:
        """Extract and analyze video frames at specified intervals."""
        # This would integrate with video processing libraries
        # For now, returning mock frame analysis
        frames = self._extract_frames(video_path, frame_interval)
        return [self._analyze_frame(frame) for frame in frames]
    
    def extract_visual_insights(self, video_path: str) -> Dict:
        """Extract comprehensive visual insights from video."""
        try:
            # Analyze video content using Llama Vision API
            analysis_prompt = """
            Analyze this video and provide insights on:
            1. Visual content and scenes
            2. Charts, graphs, or data visualizations
            3. Text overlays or captions
            4. Key themes and topics
            5. Recommended narrative structure
            """
            
            response = self._call_llama_vision_api(video_path, analysis_prompt)
            return self._parse_analysis_response(response)
            
        except Exception as e:
            return {"error": f"Failed to analyze video: {str(e)}"}
    
    def generate_narrative_script(self, video_insights: Dict, perspective: str = "neutral") -> str:
        """Generate narrative script based on video analysis."""
        try:
            script_prompt = f"""
            Based on the video analysis, create a comprehensive narrative script.
            Perspective: {perspective}
            
            Video insights: {json.dumps(video_insights, indent=2)}
            
            Generate a script that:
            1. Introduces the main topics
            2. Explains visual elements and charts
            3. Provides context and insights
            4. Maintains engaging flow
            5. Adapts to the specified perspective
            """
            
            response = self._call_llama_text_api(script_prompt)
            return response.get("text", "")
            
        except Exception as e:
            return f"Error generating script: {str(e)}"
    
    def generate_multiple_perspectives(self, video_insights: Dict) -> Dict[str, str]:
        """Generate scripts from multiple perspectives."""
        perspectives = {
            "educational": "Academic and informative tone",
            "entertaining": "Engaging and conversational tone", 
            "professional": "Business and formal tone",
            "casual": "Relaxed and friendly tone",
            "technical": "Detailed and technical explanations"
        }
        
        scripts = {}
        for perspective, description in perspectives.items():
            scripts[perspective] = self.generate_narrative_script(
                video_insights, f"{perspective}: {description}"
            )
        
        return scripts
    
    def _extract_frames(self, video_path: str, interval: int) -> List[str]:
        """Extract frames from video at specified intervals."""
        # This would use OpenCV or similar library
        # For now, returning mock frame paths
        return [f"frame_{i}.jpg" for i in range(0, 100, interval)]
    
    def _analyze_frame(self, frame_path: str) -> Dict:
        """Analyze individual video frame."""
        # Mock frame analysis
        return {
            "frame_path": frame_path,
            "content": "Sample frame content",
            "text_detected": "Sample text",
            "charts_detected": ["chart1", "chart2"]
        }
    
    def _call_llama_vision_api(self, video_path: str, prompt: str) -> Dict:
        """Call Llama Vision API for video analysis."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "video", "video": {"url": video_path}}
                    ]
                }
            ],
            "max_tokens": 2000
        }
        
        response = requests.post(
            f"{self.api_base}/chat/completions",
            json=payload,
            headers=headers
        )
        
        return response.json()
    
    def _call_llama_text_api(self, prompt: str) -> Dict:
        """Call Llama Text API for script generation."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 3000
        }
        
        response = requests.post(
            f"{self.api_base}/chat/completions",
            json=payload,
            headers=headers
        )
        
        return response.json()
    
    def _parse_analysis_response(self, response: Dict) -> Dict:
        """Parse Llama API response into structured insights."""
        try:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {
                "visual_content": content,
                "analysis_timestamp": response.get("created"),
                "model_used": response.get("model")
            }
        except Exception as e:
            return {"error": f"Failed to parse response: {str(e)}"} 