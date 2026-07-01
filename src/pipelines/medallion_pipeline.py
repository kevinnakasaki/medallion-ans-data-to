import sys

from prefect import flow
from prefect.logging import get_run_logger

from src.flows.bronze import download_to_bronze
from src.flows.gold import silver_to_gold
from src.flows.silver import bronze_to_silver
from src.utils.config import get_data_url


@flow()
def medallion_pipeline(url: str | None = None):
    """
    Orchestrates the medallion pipeline, including downloading data to bronze,
    transforming it to silver, and then to gold, with logging and error handling.

    """
    logger = get_run_logger()
    url = url or get_data_url()
    if not url:
        raise ValueError("DATA_SAMPLE_URL not set and no custom URL provided")

    bronze = download_to_bronze(url)
    logger.info(f"Bronze: {bronze['rows']} rows, {bronze['columns']}")

    silver = bronze_to_silver()
    logger.info(f"Silver: {silver['rows']} rows, {silver['columns']}")

    gold = silver_to_gold()
    logger.info(f"Gold: {gold['rows']} rows")


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else None
    medallion_pipeline(url=url)
