import os

from dotenv import load_dotenv

load_dotenv()


def get_minio_config() -> dict:
    return {
        "endpoint": os.getenv("MINIO_ENDPOINT", "minio:9000"),
        "access_key": os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        "secret_key": os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        "region": os.getenv("MINIO_REGION", "us-east-1"),
        "use_ssl": os.getenv("MINIO_USE_SSL", "false").lower() == "true",
    }


def get_data_url() -> str | None:
    return os.getenv("DATA_SAMPLE_URL")
