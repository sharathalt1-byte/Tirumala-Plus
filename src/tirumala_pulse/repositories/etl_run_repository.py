from tirumala_pulse.database.connection import supabase
from tirumala_pulse.models.etl_run import ETLRun
from tirumala_pulse.utils.logger import get_logger


logger = get_logger(__name__)


class ETLRunRepository:

    def insert(self, etl_run: ETLRun):

        response = (
            supabase
            .table("etl_runs")
            .insert(etl_run.to_dict())
            .execute()
        )

        logger.info(
            "Saved ETL run (%s)",
            etl_run.status
        )

        return response