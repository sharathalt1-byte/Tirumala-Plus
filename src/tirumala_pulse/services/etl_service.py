from datetime import datetime
import time

from tirumala_pulse.api.ttd_api import TTDNewsAPI
from tirumala_pulse.models.raw_report import RawReport
from tirumala_pulse.models.etl_run import ETLRun
from tirumala_pulse.parsers.statistics_parser import StatisticsParser
from tirumala_pulse.repositories.daily_statistics_repository import (
    DailyStatisticsRepository,
)
from tirumala_pulse.repositories.raw_report_repository import (
    RawReportRepository,
)
from tirumala_pulse.repositories.etl_run_repository import (
    ETLRunRepository,
)
from tirumala_pulse.utils.logger import get_logger


logger = get_logger(__name__)


class ETLService:

    def __init__(self):

        self.api = TTDNewsAPI()

        self.statistics_repository = DailyStatisticsRepository()

        self.raw_repository = RawReportRepository()

        self.etl_run_repository = ETLRunRepository()

    def run(self):

        start_time = time.perf_counter()

        records_processed = 0

        try:

            logger.info("Starting ETL process")

            posts = self.api.get_posts()

            logger.info("Fetched %s posts", len(posts))

            statistics_posts = [
                post
                for post in posts
                if StatisticsParser.is_statistics_post(post)
            ]

            logger.info(
                "Found %s statistics post(s)",
                len(statistics_posts)
            )

            for post in statistics_posts:

                report_date = datetime.strptime(
                    post["date"],
                    "%Y-%m-%dT%H:%M:%S"
                ).date()

                raw_report = RawReport(
                    report_date=report_date,
                    source_url=post["link"],
                    raw_content=post["content"]["rendered"]
                )

                self.raw_repository.insert(raw_report)

                statistics = StatisticsParser.parse(post)

                logger.info(
                    "Processing statistics for %s",
                    statistics.report_date
                )

                self.statistics_repository.insert(statistics)

                records_processed += 1

            execution_time = int(
                (time.perf_counter() - start_time) * 1000
            )

            etl_run = ETLRun(
                status="SUCCESS",
                records_processed=records_processed,
                execution_time_ms=execution_time
            )

            self.etl_run_repository.insert(etl_run)

            logger.info(
                "ETL completed successfully in %sms",
                execution_time
            )

        except Exception as ex:

            execution_time = int(
                (time.perf_counter() - start_time) * 1000
            )

            logger.exception("ETL failed")

            etl_run = ETLRun(
                status="FAILED",
                records_processed=records_processed,
                execution_time_ms=execution_time,
                error_message=str(ex)
            )

            self.etl_run_repository.insert(etl_run)

            raise