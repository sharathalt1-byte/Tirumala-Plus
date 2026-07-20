import time

from tirumala_pulse.api.ttd_api import TTDNewsAPI
from tirumala_pulse.models.etl_run import ETLRun
from tirumala_pulse.parsers.statistics_parser import StatisticsParser
from tirumala_pulse.repositories.etl_run_repository import (
    ETLRunRepository,
)
from tirumala_pulse.services.process_post_service import (
    ProcessPostService,
)
from tirumala_pulse.utils.logger import get_logger

logger = get_logger(__name__)


class ETLService:

    def __init__(self):

        self.api = TTDNewsAPI()

        self.process_service = ProcessPostService()

        self.etl_run_repository = ETLRunRepository()

    def run(self):

        start_time = time.perf_counter()

        records_processed = 0

        try:

            logger.info("=" * 60)
            logger.info("Starting ETL process")
            logger.info("=" * 60)

            posts = self.api.get_posts()

            logger.info("Fetched %s posts", len(posts))

            statistics_posts = [
                post for post in posts if StatisticsParser.is_statistics_post(post)
            ]

            logger.info("Found %s statistics post(s)", len(statistics_posts))

            for post in statistics_posts:

                result = self.process_service.process(post)

                if result.success:
                    records_processed += result.records_processed

            execution_time = int((time.perf_counter() - start_time) * 1000)

            etl_run = ETLRun(
                status="SUCCESS",
                records_processed=records_processed,
                execution_time_ms=execution_time,
            )

            self.etl_run_repository.insert(etl_run)

            logger.info("=" * 60)
            logger.info("ETL completed successfully")
            logger.info("Records Processed : %s", records_processed)
            logger.info("Execution Time    : %sms", execution_time)
            logger.info("=" * 60)

        except Exception as ex:

            execution_time = int((time.perf_counter() - start_time) * 1000)

            logger.exception("ETL failed")

            etl_run = ETLRun(
                status="FAILED",
                records_processed=records_processed,
                execution_time_ms=execution_time,
                error_message=str(ex),
            )

            self.etl_run_repository.insert(etl_run)

            raise
