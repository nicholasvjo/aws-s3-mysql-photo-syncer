from pathlib import Path
from s3 import upload_file_to_s3

def get_s3_key(file_name: str) -> str:
    # Example S3 key generation logic
    return f"uploads/{file_name}"    

def main(directory: Path, tenant_id: str):
    if not directory.exists() or not directory.is_dir():
        print(f"Directory {directory} does not exist or is not a directory.")
        return
    
    for file_path in directory.iterdir():
        if not file_path.is_file():
            print(f"Skipping {file_path}, not a file.")
            continue

        s3_key : str = get_s3_key(file_path.name)
        upload_file_to_s3(s3_key, file_path)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Upload files from a local directory to an S3 bucket.")
    parser.add_argument("directory", type=Path, help="Path to the local directory containing files to upload.")
    parser.add_argument("tenant_id", type=str, help="Tenant ID to use in S3 key generation.")

    args = parser.parse_args()
    main(args.directory, args.tenant_id)


    



