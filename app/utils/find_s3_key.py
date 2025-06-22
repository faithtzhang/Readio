import boto3
from botocore.client import Config

def find_latest_video_key(bucket: str, prefix: str = "") -> str | None:
    """
    Search for the latest modified MP4 under the given prefix.
    """
    s3 = boto3.client('s3', region_name=settings.AWS_REGION)
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

    latest = {"Key": None, "LastModified": None}
    for page in page_iterator:
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('.mp4'):
                if latest['LastModified'] is None or obj['LastModified'] > latest['LastModified']:
                    latest = obj

    return latest["Key"]
