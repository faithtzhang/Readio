import boto3
from app.config import settings

def generate_video_content(script: str) -> str:
    bedrock_client = boto3.client(
        "bedrock",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    try:
        response = bedrock_client.invoke_model(
            ModelId=settings.BEDROCK_MODEL_ID,
            Body=script.encode("utf-8"),
            ContentType="application/json",
        )

        video_url = response.get("VideoUrl")
        if video_url:
            return video_url
        else:
            return "Error: No video URL returned."
    except Exception as e:
        return f"Error generating video: {str(e)}"
