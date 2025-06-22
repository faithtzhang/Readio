from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from botocore.client import Config
from contextlib import closing
from app.config import settings
import uuid

def generate_audio(script: str, voice_id: str = "Joanna") -> str:
    # Initialize session and clients
    session = Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    polly = session.client("polly")
    s3 = session.client("s3", config=Config(signature_version='s3v4'))

    try:
        response = polly.synthesize_speech(
            Text=script,
            OutputFormat="mp3",
            VoiceId=voice_id,
            Engine="neural"
        )
    except (BotoCoreError, ClientError) as error:
        return f"Error generating speech: {error}"

    if "AudioStream" not in response:
        return "Error: No audio stream returned."

    # Save to a temp file and then upload to S3
    temp_file = "/tmp/audio.mp3"
    try:
        with closing(response["AudioStream"]) as stream:
            with open(temp_file, "wb") as f:
                f.write(stream.read())
        s3_key = f"polly-audio/{uuid.uuid4().hex}.mp3"
        s3.upload_file(temp_file, settings.S3_BUCKET_NAME, s3_key)
    except Exception as e:
        return f"Error uploading audio file: {e}"

    # Generate a pre-signed URL valid for 1 hour
    try:
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': settings.S3_BUCKET_NAME, 'Key': s3_key},
            ExpiresIn=3600
        )
        return url
    except Exception as e:
        return f"Error generating URL: {e}"
