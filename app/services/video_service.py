import boto3Add
import time
from app.config import settings
import os
import tempfile
from typing import Dict, Optional
from app.services.llama4_service import get_client
from app.services.audio_service import generate_audio

class VideoService:
    """Service for extracting text from video using Llama API and generating audio."""
    
    def __init__(self):
        self.perspectives = {
            "educational": "Academic and informative tone",
            "entertaining": "Engaging and conversational tone", 
            "professional": "Business and formal tone",
            "casual": "Relaxed and friendly tone",
            "technical": "Detailed and technical explanations"
        }

    def generate_video_content(script: str) -> str:
        bedrock_client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

        try:
            response = bedrock_client.start_async_invoke(
                modelId=settings.BEDROCK_MODEL_ID,
                modelInput={
                    "prompt": script,
                    "aspect_ratio": "16:9",
                    "loop": False,
                    "duration": "9s",
                    "resolution": "720p"
                },
                outputDataConfig={
                    's3OutputDataConfig': {
                        's3Uri': f"s3://{settings.S3_BUCKET_NAME}/"
                    }
                }
            )

            invocation_arn = response['invocationArn']

            while True:
                async_invoke = bedrock_client.get_async_invoke(
                    invocationArn=invocation_arn
                )
                if async_invoke.get('status') != 'InProgress':
                    break
                time.sleep(5)

            video_url = async_invoke.get('outputDataConfig', {}).get('s3OutputDataConfig', {}).get('s3Uri')
            if video_url:
                return video_url
            else:
                return "Error: No video URL returned."
        except Exception as e:
            return f"Error generating video: {str(e)}"

    def process_video_to_audio(self, video_file, perspective: Optional[str] = None) -> Dict:
        """Extract text from video file and generate audio."""
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                temp_file.write(video_file.read())
                temp_path = temp_file.name
            
            client = get_client()
            
            # Analyze video
            analysis_prompt = f"""
            Analyze this video at {temp_path} and provide insights on:
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
            
            # Generate audio from script
            audio_url = generate_audio(script)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            return  audio_url
            # return {
            #     "success": True,
            #     "text": script,
            #     "audio_url": audio_url,
            #     "perspective": perspective or "neutral"
            # }
            
        except Exception as e:
            # Clean up temp file on error
            if 'temp_path' in locals():
                try:
                    os.unlink(temp_path)
                except:
                    pass
            return {"success": False, "error": str(e)}
        
