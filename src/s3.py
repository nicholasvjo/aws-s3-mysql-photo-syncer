import boto3
from functools import lru_cache
from pathlib import Path
from config import BUCKET_NAME
from boto3.s3.transfer import S3UploadFailedError

@lru_cache(maxsize=1)
def get_s3_client():
    return boto3.client('s3')


def upload_file_to_s3(s3_key: str, file_path: Path):
    s3 = get_s3_client()

    try:
        s3.upload_file(file_path.as_posix(),
                    BUCKET_NAME,
                    s3_key,
                    ExtraArgs={"ContentType": "image/png", "ACL": "public-read"},
                )
        print(f"[Successfully uploaded {file_path} to s3://{BUCKET_NAME}/{s3_key}")
    except S3UploadFailedError as e:
        print(f"[FAILURE] Failed to upload {file_path} to s3://{BUCKET_NAME}/{s3_key}: {e}")