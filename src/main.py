from pathlib import Path
from s3 import upload_file_to_s3
from my_sql import execute_update_query, get_update_query, test_connection
import config
import re
import time

def get_s3_key(file_name: str) -> str:
    return f"{config.BUCKET_DIR}{file_name}" 


def extract_user_id(filename: str, pattern: str) -> int:
    """
    Extract the user ID from the filename based on the given pattern.
    """
    # Transforma o padrão em uma regex com grupo nomeado
    regex_pattern = re.escape(pattern)
    regex_pattern = re.sub(r'\\{user_id\\}', r'(?P<user_id>.+?)', regex_pattern)
    regex_pattern = f"^{regex_pattern}$"
    
    match = re.match(regex_pattern, filename)

    if not match:
        return None
    
    try:
        user_id = int(match.group('user_id'))
        return user_id
    except ValueError:
        print(f"Could not convert extracted user_id to int for file {filename}.")
        return None
        
def get_user_confirmation(ids_lenght : int) -> bool:
    continue_prompt = input(f"About to update photo URLs for {ids_lenght} users in the database. Proceed? (y/n): ")

    return continue_prompt.lower() == 'y'


def main(directory: Path, pattern: str, no_confirm: bool = False):
    start = time.perf_counter()
    if not directory.exists() or not directory.is_dir():
        print(f"Directory {directory} does not exist or is not a directory.")
        return
    ids = set()
    for file_path in directory.iterdir():
        if not file_path.is_file():
            print(f"Skipping {file_path}, not a file.")
            continue

        user_id = extract_user_id(file_path.name, pattern)
        if user_id is None:
            print(f"Skipping {file_path}, could not extract user ID.")
            continue

        s3_key : str = get_s3_key(str(user_id) + ".jpg")
        upload_file_to_s3(s3_key, file_path)
        ids.add(user_id)
    
    if not ids:
        print("No valid user IDs found. Exiting.")
        return
    
    print(f"Uploading and processing completed in {time.perf_counter() - start:.2f} seconds.")
    
    query = get_update_query(len(ids))
    print("Generated SQL Query:", query)

    if not no_confirm and not get_user_confirmation(len(ids)):
        print("Operation cancelled by user.")
        return
    
    execute_update_query(ids)

    print(f"Total operation completed in {time.perf_counter() - start:.2f} seconds.")
    


if __name__ == "__main__":
    import argparse


    parser = argparse.ArgumentParser(description="Upload files from a local directory to an S3 bucket.")
    parser.add_argument("directory", type=Path, help="Path to the local directory containing files to upload.")
    parser.add_argument("--pattern", type=str, help="Filename pattern with {user_id} placeholder, e.g., 'user_{user_id}_photo.jpg'.", default="{user_id}.jpg")
    parser.add_argument("--no-confirm", action='store_true', help="If set, skips the confirmation prompt before updating the database." )
    parser.add_argument("--test-connection", action='store_true', help="If set, tests the MySQL connection and exits." )
    args = parser.parse_args()

    if args.test_connection:
        test_connection()
        exit(0)


    main(args.directory, args.pattern, args.no_confirm)




    



