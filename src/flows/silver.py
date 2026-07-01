from deltalake import write_deltalake
from prefect import task
from prefect.logging import get_run_logger

from src.utils.config import get_minio_config
from src.utils.constants import STORAGE_OPTIONS
from src.utils.duckdb_helpers import get_connection


@task
def bronze_to_silver() -> dict:
    """
    Reads the data from the bronze layer and transforms it into the silver layer,
    removing duplicates and converting the DT_CARGA column to DATE.

    The `CAST` is done only for the DT_CARGA column to avoid type compatibility issues
    in the future with the other columns. This can be adjusted as needed whenever
    more context about the data becomes available.

    """
    logger = get_run_logger()
    config = get_minio_config()
    conn = get_connection(config)

    logger.info("Reading bronze data from S3 and casting DT_CARGA to DATE...")
    df = conn.execute("""
        SELECT DISTINCT
            * EXCLUDE (DT_CARGA),
            CAST(DT_CARGA AS DATE) AS DT_CARGA
        FROM read_csv_auto('s3://bronze/ans_data.csv')
    """).df()
    conn.register("bronze_df", df)

    logger.info("Creating the silver table in DuckDB...")
    conn.execute("""
        CREATE OR REPLACE TABLE silver AS
        SELECT DISTINCT * FROM bronze_df
    """)

    logger.info("Getting the silver table data...")
    result = conn.execute("SELECT * FROM silver").df()
    conn.close()

    logger.info("Writing silver data to Delta Lake...")
    write_deltalake(
        "s3://silver/ans_data",
        result,
        storage_options=STORAGE_OPTIONS,
        mode="overwrite",
    )

    return {"rows": len(result), "columns": len(result.columns)}
