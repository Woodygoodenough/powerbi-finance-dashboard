import csv
import logging
from alphavantage import AlphaVantageError, create_client
from constants import DATA_DIR, FILE_NAME

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logger.info("Starting to fetch data from Alpha Vantage")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / FILE_NAME

    with create_client() as client:
        try:
            payload = client.time_series_daily(symbol="AAPL")
        except AlphaVantageError as e:
            logger.error(f"Error: {e}")
            raise
        else:
            logger.info(f"Data fetched successfully")

    with open(file_path, "w", encoding="utf-8") as f:
        logger.info(f"Writing data to {file_path}")

        writer = csv.writer(f)
        writer.writerow(["date", "open", "high", "low", "close", "volume"])

        # Alpha Vantage returns a mapping of date -> {metric -> value}; flatten it
        for date, metrics in sorted(payload.items(), reverse=True):
            writer.writerow(
                [
                    date,
                    metrics.get("1. open"),
                    metrics.get("2. high"),
                    metrics.get("3. low"),
                    metrics.get("4. close"),
                    metrics.get("5. volume"),
                ]
            )

        logger.info(f"Data written successfully to {file_path}")


if __name__ == "__main__":
    main()
