from src.utils.config import get_minio_config

MINIO_CONFIG = get_minio_config()
STORAGE_OPTIONS = {
    "AWS_ENDPOINT_URL": f"http://{MINIO_CONFIG['endpoint']}",
    "AWS_ACCESS_KEY_ID": MINIO_CONFIG["access_key"],
    "AWS_SECRET_ACCESS_KEY": MINIO_CONFIG["secret_key"],
    "AWS_REGION": MINIO_CONFIG["region"],
    "AWS_ALLOW_HTTP": "true",
    "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
}
