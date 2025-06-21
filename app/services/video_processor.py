import os
import json
from typing import Dict, List, Optional
from app.services.video_analyzer import VideoAnalyzer
from app.services.audio_dubber import AudioDubber


class VideoProcessor:
    """Main service for processing videos with Llama analysis and AWS Polly dubbing."""
    
    def __init__(self):
        self.video_analyzer = VideoAnalyzer()
        self.audio_dubber = AudioDubber()
    
    def process_video_complete(self, video_path: str, output_dir: str, perspectives: Optional[List[str]] = None) -> Dict:
        """Complete video processing pipeline: analyze → generate scripts → create dubs."""
        try:
            # Step 1: Analyze video content
            print("Step 1: Analyzing video content...")
            video_insights = self.video_analyzer.extract_visual_insights(video_path)
            
            if "error" in video_insights:
                return {"success": False, "error": video_insights["error"]}
            
            # Step 2: Generate scripts for different perspectives
            print("Step 2: Generating narrative scripts...")
            if perspectives:
                scripts = {}
                for perspective in perspectives:
                    scripts[perspective] = self.video_analyzer.generate_narrative_script(
                        video_insights, perspective
                    )
            else:
                scripts = self.video_analyzer.generate_multiple_perspectives(video_insights)
            
            # Step 3: Generate audio for each script
            print("Step 3: Generating audio dubs...")
            audio_versions = {}
            for perspective, script in scripts.items():
                audio_versions[perspective] = self.audio_dubber.generate_audio_for_script(
                    script, perspective
                )
            
            # Step 4: Create final videos with dubs
            print("Step 4: Creating final videos...")
            final_videos = self.audio_dubber.create_final_video(
                video_path, audio_versions, output_dir
            )
            
            return {
                "success": True,
                "video_insights": video_insights,
                "scripts": scripts,
                "audio_versions": audio_versions,
                "final_videos": final_videos,
                "output_directory": output_dir
            }
            
        except Exception as e:
            return {"success": False, "error": f"Processing failed: {str(e)}"}
    
    def process_video_analysis_only(self, video_path: str) -> Dict:
        """Process video analysis only without audio generation."""
        try:
            video_insights = self.video_analyzer.extract_visual_insights(video_path)
            scripts = self.video_analyzer.generate_multiple_perspectives(video_insights)
            
            return {
                "success": True,
                "video_insights": video_insights,
                "scripts": scripts
            }
            
        except Exception as e:
            return {"success": False, "error": f"Analysis failed: {str(e)}"}
    
    def process_audio_only(self, script: str, video_path: str, output_dir: str, perspective: str = "professional") -> Dict:
        """Generate audio dub for existing script."""
        try:
            audio_data = self.audio_dubber.generate_audio_for_script(script, perspective)
            
            if audio_data["success"]:
                final_video = self.audio_dubber.sync_audio_with_video(
                    video_path, 
                    audio_data["audio_segments"],
                    os.path.join(output_dir, f"video_{perspective}.mp4")
                )
                
                return {
                    "success": True,
                    "audio_data": audio_data,
                    "final_video": final_video
                }
            else:
                return audio_data
                
        except Exception as e:
            return {"success": False, "error": f"Audio processing failed: {str(e)}"}
    
    def get_processing_status(self, video_path: str) -> Dict:
        """Get processing status and available options for a video."""
        try:
            # Check if video exists
            if not os.path.exists(video_path):
                return {"error": "Video file not found"}
            
            # Get available voices
            voices = self.audio_dubber.get_available_voices()
            
            return {
                "success": True,
                "video_path": video_path,
                "video_size": os.path.getsize(video_path),
                "available_voices": voices,
                "available_perspectives": list(self.audio_dubber.voice_mapping.keys())
            }
            
        except Exception as e:
            return {"success": False, "error": f"Status check failed: {str(e)}"}
    
    def batch_process_videos(self, video_paths: List[str], output_dir: str) -> Dict:
        """Process multiple videos in batch."""
        results = {}
        
        for video_path in video_paths:
            video_name = os.path.basename(video_path)
            print(f"Processing {video_name}...")
            
            video_output_dir = os.path.join(output_dir, video_name.replace('.', '_'))
            os.makedirs(video_output_dir, exist_ok=True)
            
            results[video_name] = self.process_video_complete(video_path, video_output_dir)
        
        return {
            "success": True,
            "total_videos": len(video_paths),
            "processed_videos": len([r for r in results.values() if r["success"]]),
            "results": results
        }
    
    def export_processing_report(self, processing_result: Dict, output_path: str) -> Dict:
        """Export processing results to a JSON report."""
        try:
            with open(output_path, 'w') as f:
                json.dump(processing_result, f, indent=2)
            
            return {
                "success": True,
                "report_path": output_path,
                "report_size": os.path.getsize(output_path)
            }
            
        except Exception as e:
            return {"success": False, "error": f"Failed to export report: {str(e)}"} 