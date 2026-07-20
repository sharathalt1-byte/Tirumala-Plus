import time

from tirumala_pulse.api.ttd_api import TTDNewsAPI
from tirumala_pulse.models.checkpoint_status import CheckpointStatus
from tirumala_pulse.parsers.statistics_parser import StatisticsParser
from tirumala_pulse.repositories.checkpoint_repository import (
    CheckpointRepository,
)
from tirumala_pulse.services.process_post_service import (
    ProcessPostService,
)
from tirumala_pulse.utils.logger import get_logger

logger = get_logger(__name__)

PROCESS_NAME = "historical_backfill"


class BackfillService:

    def __init__(self):

        self.api = TTDNewsAPI()

        self.process_service = ProcessPostService()

        self.checkpoint_repository = CheckpointRepository()

    def run(self, max_pages=None, reset_checkpoint=False):

        start_time = time.perf_counter()

        if reset_checkpoint:
            logger.info("Resetting checkpoint...")
            self.checkpoint_repository.reset(PROCESS_NAME)

        checkpoint = self.checkpoint_repository.resume(PROCESS_NAME)

        if checkpoint.status == CheckpointStatus.NOT_STARTED:

            logger.info("No checkpoint found.")
            logger.info("Starting historical backfill.")

        else:

            logger.info("=" * 60)
            logger.info("Resuming Historical Backfill")
            logger.info("=" * 60)
            logger.info("Status              : %s", checkpoint.status.value)
            logger.info("Resume Page         : %s", checkpoint.last_page)
            logger.info("Posts Scanned       : %s", checkpoint.posts_scanned)
            logger.info(
                "Statistics Processed: %s",
                checkpoint.statistics_processed,
            )

        self.checkpoint_repository.start(checkpoint)

        pages_processed = 0

        for page, posts in self.api.iter_pages(checkpoint.last_page):
            logger.info("Posts received on page %s: %s", page, len(posts))

            logger.info("=" * 60)
            logger.info("Processing Page %s", page)
            logger.info("=" * 60)

            processed_this_page = 0

            last_statistics_date = checkpoint.last_post_date

            for post in posts:

                checkpoint.posts_scanned += 1

                if not StatisticsParser.is_statistics_post(post):
                    continue

                result = self.process_service.process(post)

                if result.success:

                    checkpoint.statistics_processed += result.records_processed

                    processed_this_page += 1

                    last_statistics_date = result.report_date

            checkpoint.last_page = page + 1

            checkpoint.last_post_date = last_statistics_date

            self.checkpoint_repository.update_progress(checkpoint)

            pages_processed += 1

            logger.info("Checkpoint saved. Next page: %s", checkpoint.last_page)

            if max_pages is not None and pages_processed >= max_pages:

                logger.info("Reached max_pages=%s", max_pages)

                execution_time = int((time.perf_counter() - start_time) * 1000)

                logger.info("Execution Time : %sms", execution_time)

                return

        self.checkpoint_repository.complete(checkpoint)

        execution_time = int((time.perf_counter() - start_time) * 1000)

        logger.info("=" * 60)
        logger.info("Historical Backfill Completed")
        logger.info("=" * 60)
        logger.info("Posts Scanned       : %s", checkpoint.posts_scanned)
        logger.info(
            "Statistics Processed: %s",
            checkpoint.statistics_processed,
        )
        logger.info("Execution Time      : %sms", execution_time)
