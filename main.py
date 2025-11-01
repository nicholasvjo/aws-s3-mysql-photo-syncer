import boto3
from functools import lru_cache
from pathlib import Path
from src.constants import BUCKET_NAME
from src.utils import get_file_s3_key
from boto3.s3.transfer import S3UploadFailedError
@lru_cache(maxsize=1)
def get_s3_client():
    return boto3.client('s3')

# def bucket_exists(bucket_name):
#     s3 = get_s3_client()
#     try:
#         s3.head_bucket(Bucket=bucket_name)
#         return True
#     except s3.exceptions.NoSuchBucket:
#         return False
    
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


def main(directory: Path, tenant_id: str):
    if not directory.exists() or not directory.is_dir():
        print(f"Directory {directory} does not exist or is not a directory.")
        return
    
    for file_path in directory.iterdir():
        if not file_path.is_file():
            print(f"Skipping {file_path}, not a file.")
            continue

        s3_key : str = get_file_s3_key(tenant_id, file_path.name)
        upload_file_to_s3(s3_key, file_path)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Upload files from a local directory to an S3 bucket.")
    parser.add_argument("directory", type=Path, help="Path to the local directory containing files to upload.")
    parser.add_argument("tenant_id", type=str, help="Tenant ID to use in S3 key generation.")

    args = parser.parse_args()
    main(args.directory, args.tenant_id)


    



