from tirumala_pulse.api.ttd_api import TTDNewsAPI
from tirumala_pulse.parsers.statistics_parser import StatisticsParser
from tirumala_pulse.repositories.daily_statistics_repository import (
    DailyStatisticsRepository,
)
from tirumala_pulse.utils.logger import get_logger


logger = get_logger(__name__)


class ETLService:

    def __init__(self):

        self.api = TTDNewsAPI()
        self.repository = DailyStatisticsRepository()

    def run(self):

        logger.info("Starting ETL process")

        logger.info("Fetching latest posts from TTD")

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

            statistics = StatisticsParser.parse(post)

            logger.info(
                "Processing report for %s",
                statistics.report_date
            )

            self.repository.insert(statistics)

        logger.info("ETL completed successfully")