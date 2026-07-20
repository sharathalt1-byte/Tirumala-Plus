from tirumala_pulse.database.connection import supabase
from tirumala_pulse.models.raw_report import RawReport
from tirumala_pulse.utils.logger import get_logger

logger = get_logger(__name__)


class RawReportRepository:

    def exists(self, report_date) -> bool:
        """
        Check whether a raw report already exists for the given date.
        """

        response = (
            supabase.table("raw_reports")
            .select("id")
            .eq("report_date", report_date.strftime("%Y-%m-%d"))
            .limit(1)
            .execute()
        )

        return len(response.data) > 0

    def insert(self, report: RawReport):

        if self.exists(report.report_date):

            logger.info(
                "Raw report for %s already exists. Skipping.",
                report.report_date,
            )

            return None

        logger.info(
            "Saving raw report for %s.",
            report.report_date,
        )

        response = supabase.table("raw_reports").insert(report.to_dict()).execute()

        logger.info(
            "Successfully saved raw report for %s.",
            report.report_date,
        )

        return response
