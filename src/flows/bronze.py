import io
from zipfile import ZipFile

import httpx
import pandas as pd
from prefect import task
from prefect.logging import get_run_logger

from src.utils.config import get_minio_config
from src.utils.duckdb_helpers import get_connection


@task
def download_to_bronze(url: str) -> dict:
    """
    Download the ZIP file from the given URL, extract the CSV,
    and load it into the bronze layer in MinIO.

    As the idea is to replicate the original data "as-is", and as the
    bronze layer is not a consumable layer, the data is loaded
    with the original format, preserving as much of its characteristics
    as possible.

    """
    logger = get_run_logger()
    config = get_minio_config()
    conn = get_connection(config)

    logger.info(f"Downloading from {url}")
    response = httpx.get(url, follow_redirects=True, timeout=300)
    response.raise_for_status()

    logger.info("Extracting CSV from ZIP and reading into DataFrame")
    with ZipFile(io.BytesIO(response.content)) as zipf:
        csv_name = next(file for file in zipf.namelist() if file.endswith(".csv"))
        df = pd.read_csv(zipf.open(csv_name), sep=";")

    logger.info("Writing DataFrame to bronze layer in MinIO")
    conn.register("bronze_df", df)
    conn.execute("COPY bronze_df TO 's3://bronze/ans_data.csv' (HEADER, DELIMITER ',')")
    conn.close()

    return {"rows": len(df), "columns": list(df.columns)}
