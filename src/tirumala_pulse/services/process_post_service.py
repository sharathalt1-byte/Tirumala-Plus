from datetime import datetime

from tirumala_pulse.models.process_result import ProcessResult
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


class ProcessPostService:

    def __init__(self):

        self.statistics_repository = DailyStatisticsRepository()

        self.raw_repository = RawReportRepository()

    def process(self, post) -> ProcessResult:

        report_date = None

        try:

            report_date = datetime.strptime(post["date"], "%Y-%m-%dT%H:%M:%S").date()

            raw_report = RawReport(
                report_date=report_date,
                source_url=post["link"],
                raw_content=post["content"]["rendered"],
            )

            self.raw_repository.insert(raw_report)

            statistics = StatisticsParser.parse(post)

            logger.info("Processing statistics for %s", statistics.report_date)

            self.statistics_repository.insert(statistics)

            return ProcessResult(
                success=True,
                report_date=statistics.report_date,
                status="SUCCESS",
                records_processed=1,
            )

        except Exception as ex:

            logger.exception("Failed processing statistics post (%s)", report_date)

            return ProcessResult(
                success=False,
                report_date=report_date,
                status="FAILED",
                records_processed=0,
                error_message=str(ex),
            )
