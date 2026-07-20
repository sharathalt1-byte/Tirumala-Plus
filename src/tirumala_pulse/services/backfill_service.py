from datetime import datetime

from tirumala_pulse.api.ttd_api import TTDNewsAPI
from tirumala_pulse.models.raw_report import RawReport
from tirumala_pulse.parsers.statistics_parser import StatisticsParser
from tirumala_pulse.repositories.daily_statistics_repository import (
    DailyStatisticsRepository,
)
from tirumala_pulse.repositories.raw_report_repository import (
    RawReportRepository,
)
from tirumala_pulse.utils.logger import get_logger


logger = get_logger(__name__)


class BackfillService:

    def __init__(self):

        self.api = TTDNewsAPI()

        self.raw_repository = RawReportRepository()

        self.statistics_repository = DailyStatisticsRepository()

    def run(self):

        logger.info("=" * 60)
        logger.info("Starting Historical Backfill")
        logger.info("=" * 60)

        statistics_found = 0

        statistics_saved = 0

        for post in self.api.iter_posts():

            if not StatisticsParser.is_statistics_post(post):
                continue

            statistics_found += 1

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

            self.statistics_repository.insert(statistics)

            statistics_saved += 1

            logger.info(
                "Historical Reports Saved : %s",
                statistics_saved
            )

        logger.info("=" * 60)
        logger.info("Historical Backfill Finished")
        logger.info("Statistics Found : %s", statistics_found)
        logger.info("Statistics Saved : %s", statistics_saved)
        logger.info("=" * 60)