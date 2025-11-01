def get_file_s3_key(tenant_id: str, file_name: str) -> str:
    return f"databases/{tenant_id}/users/{file_name}"