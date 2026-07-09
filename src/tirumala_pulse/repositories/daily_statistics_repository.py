from pprint import pprint

from tirumala_pulse.database.connection import supabase
from tirumala_pulse.models.daily_statistics import DailyStatistics


class DailyStatisticsRepository:

    def exists(self, report_date):

        response = (
            supabase
            .table("daily_statistics")
            .select("id")
            .eq("report_date", report_date.strftime("%Y-%m-%d"))
            .limit(1)
            .execute()
        )

        return len(response.data) > 0

    def insert(self, statistics: DailyStatistics):

        payload = statistics.to_dict()

        print("\n================ PAYLOAD ================\n")
        pprint(payload)
        print("\nType of report_date:", type(payload["report_date"]))
        print("\n=========================================\n")

        if self.exists(statistics.report_date):

            print(
                f"⏭ Report for {statistics.report_date} already exists. Skipping."
            )

            return None

        response = (
            supabase
            .table("daily_statistics")
            .insert(payload)
            .execute()
        )

        print(
            f"✅ Inserted report for {statistics.report_date}"
        )

        return response