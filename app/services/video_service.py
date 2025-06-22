import boto3
import time
from app.config import settings
import os
import tempfile
from typing import Dict, Optional
from app.services.llama4_service import client
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
        # Initialize S3 client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

    def download_video_from_s3(self, s3_key: str, local_path: str = None) -> str:
        """Download video from S3 bucket."""
        try:
            if not local_path:
                local_path = f"downloaded_video_{int(time.time())}.mp4"
            
            self.s3_client.download_file(
                settings.S3_BUCKET_NAME,
                s3_key,
                local_path
            )
            return local_path
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None

    def get_video_url(self, s3_key: str, expires_in: int = 3600) -> str:
        """Generate a pre-signed URL for video download."""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.S3_BUCKET_NAME, 'Key': s3_key},
                ExpiresIn=expires_in
            )
            return url
        except Exception as e:
            print(f"Error generating URL: {e}")
            return None

    def generate_video_content(self, script: str) -> str:
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
        
