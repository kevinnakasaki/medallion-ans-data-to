import boto3
from botocore.config import Config


def get_minio_client(config: dict):
    return boto3.client(
        "s3",
        endpoint_url=f"http://{config['endpoint']}",
        aws_access_key_id=config["access_key"],
        aws_secret_access_key=config["secret_key"],
        region_name=config["region"],
        use_ssl=config["use_ssl"],
        config=Config(),
    )
