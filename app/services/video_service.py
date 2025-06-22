import boto3
import time
from app.config import settings

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
