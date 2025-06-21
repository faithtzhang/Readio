import boto3
import json
import os
from typing import Dict, List, Optional
from app.core.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION


class AudioDubber:
    """Service for generating and syncing audio dubs with video using AWS Polly."""
    
    def __init__(self):
        self.polly_client = boto3.client(
            'polly',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        
        # Available voices for different perspectives
        self.voice_mapping = {
            "educational": {
                "voice_id": "Joanna",
                "engine": "neural",
                "language_code": "en-US"
            },
            "entertaining": {
                "voice_id": "Matthew", 
                "engine": "neural",
                "language_code": "en-US"
            },
            "professional": {
                "voice_id": "Salli",
                "engine": "neural", 
                "language_code": "en-US"
            },
            "casual": {
                "voice_id": "Justin",
                "engine": "neural",
                "language_code": "en-US"
            },
            "technical": {
                "voice_id": "Ivy",
                "engine": "neural",
                "language_code": "en-US"
            }
        }
    
    def generate_audio_for_script(self, script: str, perspective: str = "professional") -> Dict:
        """Generate audio narration for a script using AWS Polly."""
        try:
            voice_config = self.voice_mapping.get(perspective, self.voice_mapping["professional"])
            
            # Split script into manageable chunks
            script_chunks = self._split_script(script)
            audio_segments = []
            
            for i, chunk in enumerate(script_chunks):
                audio_data = self._synthesize_chunk(chunk, voice_config)
                audio_segments.append({
                    "chunk_index": i,
                    "text": chunk,
                    "audio_data": audio_data,
                    "duration": self._estimate_duration(chunk)
                })
            
            return {
                "success": True,
                "perspective": perspective,
                "voice_used": voice_config["voice_id"],
                "audio_segments": audio_segments,
                "total_duration": sum(seg["duration"] for seg in audio_segments)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate audio: {str(e)}"
            }
    
    def generate_multiple_voice_versions(self, script: str) -> Dict[str, Dict]:
        """Generate audio versions for all available perspectives."""
        versions = {}
        
        for perspective in self.voice_mapping.keys():
            versions[perspective] = self.generate_audio_for_script(script, perspective)
        
        return versions
    
    def sync_audio_with_video(self, video_path: str, audio_segments: List[Dict], output_path: str) -> Dict:
        """Sync generated audio with original video."""
        try:
            # This would use ffmpeg or similar for video processing
            # For now, returning mock sync result
            
            sync_result = self._process_video_audio_sync(video_path, audio_segments, output_path)
            
            return {
                "success": True,
                "output_path": output_path,
                "sync_details": sync_result,
                "total_segments": len(audio_segments)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to sync audio with video: {str(e)}"
            }
    
    def create_final_video(self, video_path: str, audio_versions: Dict[str, Dict], output_dir: str) -> Dict:
        """Create final videos with different audio dubs."""
        results = {}
        
        for perspective, audio_data in audio_versions.items():
            if audio_data["success"]:
                output_path = os.path.join(output_dir, f"video_{perspective}.mp4")
                result = self.sync_audio_with_video(
                    video_path, 
                    audio_data["audio_segments"], 
                    output_path
                )
                results[perspective] = result
        
        return results
    
    def _split_script(self, script: str, max_chunk_length: int = 150) -> List[str]:
        """Split long script into manageable chunks for TTS."""
        sentences = script.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chunk_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _synthesize_chunk(self, text: str, voice_config: Dict) -> bytes:
        """Synthesize audio for a text chunk using AWS Polly."""
        response = self.polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_config["voice_id"],
            Engine=voice_config["engine"],
            LanguageCode=voice_config["language_code"]
        )
        
        return response['AudioStream'].read()
    
    def _estimate_duration(self, text: str) -> float:
        """Estimate audio duration based on text length."""
        # Rough estimate: 150 words per minute
        words = len(text.split())
        return (words / 150) * 60  # Duration in seconds
    
    def _process_video_audio_sync(self, video_path: str, audio_segments: List[Dict], output_path: str) -> Dict:
        """Process video-audio synchronization using ffmpeg."""
        # This would implement actual video processing
        # For now, returning mock processing details
        
        return {
            "video_duration": 120.0,  # Mock video duration
            "audio_duration": sum(seg["duration"] for seg in audio_segments),
            "sync_method": "ffmpeg",
            "processing_time": 5.2  # Mock processing time
        }
    
    def get_available_voices(self) -> Dict:
        """Get list of available AWS Polly voices."""
        try:
            response = self.polly_client.describe_voices(
                LanguageCode='en-US',
                Engine='neural'
            )
            
            return {
                "success": True,
                "voices": response.get("Voices", []),
                "total_count": len(response.get("Voices", []))
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get voices: {str(e)}"
            } 