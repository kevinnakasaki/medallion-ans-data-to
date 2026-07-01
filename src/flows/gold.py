from deltalake import write_deltalake
from prefect import task
from prefect.logging import get_run_logger

from src.utils.config import get_minio_config
from src.utils.constants import STORAGE_OPTIONS
from src.utils.duckdb_helpers import get_connection


@task
def silver_to_gold() -> dict:
    """
    Transforms silver data into gold data by reading from the silver layer,
    processing with DuckDB, and writing to the gold layer, partitioning by DT_CARGA.

    """
    logger = get_run_logger()
    config = get_minio_config()
    conn = get_connection(config)

    logger.info("Reading silver data from Delta Lake...")
    df = conn.execute("SELECT * FROM delta_scan('s3://silver/ans_data')").df()
    conn.close()

    logger.info("Writing gold data to Delta Lake...")
    write_deltalake(
        "s3://gold/ans_data",
        df,
        storage_options=STORAGE_OPTIONS,
        mode="overwrite",
        partition_by=["DT_CARGA"],
    )
    return {"rows": len(df)}
