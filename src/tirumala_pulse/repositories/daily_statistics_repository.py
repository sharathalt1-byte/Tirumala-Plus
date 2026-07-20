from tirumala_pulse.database.connection import supabase
from tirumala_pulse.models.daily_statistics import DailyStatistics
from tirumala_pulse.utils.logger import get_logger

logger = get_logger(__name__)


class DailyStatisticsRepository:

    def exists(self, report_date) -> bool:
        """
        Check whether a report for the given date already exists.
        """

        response = (
            supabase.table("daily_statistics")
            .select("id")
            .eq("report_date", report_date.strftime("%Y-%m-%d"))
            .limit(1)
            .execute()
        )

        return len(response.data) > 0

    def insert(self, statistics: DailyStatistics):
        """
        Insert a statistics record if it does not already exist.
        """

        if self.exists(statistics.report_date):

            logger.info(
                "Report for %s already exists. Skipping.",
                statistics.report_date,
            )

            return None

        payload = statistics.to_dict()

        logger.info(
            "Saving report for %s to Supabase.",
            statistics.report_date,
        )

        response = supabase.table("daily_statistics").insert(payload).execute()

        logger.info(
            "Successfully inserted report for %s.",
            statistics.report_date,
        )

        return response

    def insert_many(self, statistics_list: list[DailyStatistics]):
        """
        Bulk insert multiple statistics records.
        """

        rows = [statistics.to_dict() for statistics in statistics_list]

        response = supabase.table("daily_statistics").insert(rows).execute()

        logger.info(
            "Inserted %s reports into Supabase.",
            len(rows),
        )

        return response
