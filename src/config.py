import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# S3 Configuration
BUCKET_NAME = os.getenv('BUCKET_NAME', 'default-bucket-name')
BUCKET_DIR = os.getenv('BUCKET_DIR', 'default/dir/')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# SSH Tunnel Configuration (Optional)
SSH_HOST=os.getenv('SSH_HOST')
SSH_PORT=int(os.getenv('SSH_PORT')) if os.getenv('SSH_PORT') else None
SSH_USER=os.getenv('SSH_USER')
SSH_KEY_PATH=os.getenv('SSH_KEY_PATH')

# MySQL Database Configuration
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT')) if os.getenv('DB_PORT') else None
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

if not all([DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME]):
    raise ValueError("Database configuration is incomplete. Please set all required environment variables.")


def shoud_use_ssh_tunnel() -> bool:
    return all([SSH_HOST, SSH_PORT, SSH_USER])