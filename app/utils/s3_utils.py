import os
import boto3
from botocore.client import Config
from typing import Optional
from app.config import settings

def find_latest_video_key(bucket: str, prefix: str = "") -> Optional[str]:
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

def upload_and_get_url(local_paths: list[str], bucket: str, region: str) -> list[str]:
    """
    Upload each file in local_paths to S3 under 'frames/' prefix,
    delete it locally, and return a list of pre-signed URLs.
    """
    s3 = boto3.client("s3", region_name=region, config=Config(signature_version="s3v4"))
    urls = []

    for path in local_paths:
        filename = os.path.basename(path)
        key = f"frames/{filename}"

        try:
            s3.upload_file(path, bucket, key)
        except Exception as e:
            print(f"Error uploading {path}: {e}")
            continue  # skip cleanup/presign for failed uploads

        # clean up local file
        try:
            os.remove(path)
        except OSError as e:
            print(f"Warning deleting temp file {path}: {e}")

        try:
            url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=3600,
            )
            urls.append(url)
        except Exception as e:
            print(f"Error generating URL for key {key}: {e}")

    return urls
