import boto3
from botocore.exceptions import NoCredentialsError
from app.config import settings

def generate_audio(script: str, voice_id: str = "Joanna") -> str:
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    try:
        response = polly_client.synthesize_speech(
            Text=script,
            OutputFormat="mp3",
            VoiceId=voice_id,  # Choose appropriate voice
        )

        audio_stream = response.get("AudioStream")
        if audio_stream:
            audio_path = "audio.mp3"
            with open(audio_path, "wb") as file:
                file.write(audio_stream.read())
            return audio_path
        else:
            return "Error: No audio stream returned."
    except NoCredentialsError:
        return "Error: AWS credentials not found."
    except Exception as e:
        return f"Error generating audio: {str(e)}"
