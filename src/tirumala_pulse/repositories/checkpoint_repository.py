from datetime import date, datetime

from tirumala_pulse.database.connection import supabase
from tirumala_pulse.models.checkpoint import Checkpoint
from tirumala_pulse.models.checkpoint_status import CheckpointStatus
from tirumala_pulse.utils.logger import get_logger

logger = get_logger(__name__)


class CheckpointRepository:

    TABLE_NAME = "etl_checkpoints"

    def resume(self, process_name: str) -> Checkpoint:
        """
        Resume an existing checkpoint.
        If one doesn't exist, create a new checkpoint.
        """

        response = (
            supabase.table(self.TABLE_NAME)
            .select("*")
            .eq("process_name", process_name)
            .limit(1)
            .execute()
        )

        if not response.data:

            logger.info(
                "No checkpoint found for '%s'. Creating one.",
                process_name,
            )

            checkpoint = Checkpoint(
                process_name=process_name,
                status=CheckpointStatus.NOT_STARTED,
                last_page=1,
                posts_scanned=0,
                statistics_processed=0,
            )

            self._upsert(checkpoint)

            return checkpoint

        return self._from_row(response.data[0])

    def start(self, checkpoint: Checkpoint):

        checkpoint.status = CheckpointStatus.RUNNING

        if checkpoint.started_at is None:
            checkpoint.started_at = datetime.utcnow()

        checkpoint.updated_at = datetime.utcnow()

        self._upsert(checkpoint)

        return checkpoint

    def update_progress(self, checkpoint: Checkpoint):

        checkpoint.updated_at = datetime.utcnow()

        self._upsert(checkpoint)

        return checkpoint

    def complete(self, checkpoint: Checkpoint):

        checkpoint.status = CheckpointStatus.COMPLETED
        checkpoint.completed_at = datetime.utcnow()
        checkpoint.updated_at = datetime.utcnow()

        self._upsert(checkpoint)

        return checkpoint

    def fail(self, checkpoint: Checkpoint):

        checkpoint.status = CheckpointStatus.FAILED
        checkpoint.updated_at = datetime.utcnow()

        self._upsert(checkpoint)

        return checkpoint

    def reset(self, process_name: str):

        logger.info(
            "Resetting checkpoint '%s'.",
            process_name,
        )

        checkpoint = Checkpoint(
            process_name=process_name,
            status=CheckpointStatus.NOT_STARTED,
            last_page=1,
            posts_scanned=0,
            statistics_processed=0,
        )

        self._upsert(checkpoint)

        return checkpoint

    def _upsert(self, checkpoint: Checkpoint):

        if checkpoint.updated_at is None:
            checkpoint.updated_at = datetime.utcnow()

        payload = self._to_payload(checkpoint)

        (
            supabase.table(self.TABLE_NAME)
            .upsert(
                payload,
                on_conflict="process_name",
            )
            .execute()
        )

    def _to_payload(
        self,
        checkpoint: Checkpoint,
    ) -> dict:

        return {
            "process_name": checkpoint.process_name,
            "status": checkpoint.status.value,
            "last_page": checkpoint.last_page,
            "posts_scanned": checkpoint.posts_scanned,
            "statistics_processed": checkpoint.statistics_processed,
            "version": checkpoint.version,
            "last_post_date": (
                checkpoint.last_post_date.isoformat()
                if checkpoint.last_post_date
                else None
            ),
            "started_at": (
                checkpoint.started_at.isoformat() if checkpoint.started_at else None
            ),
            "updated_at": (
                checkpoint.updated_at.isoformat() if checkpoint.updated_at else None
            ),
            "completed_at": (
                checkpoint.completed_at.isoformat() if checkpoint.completed_at else None
            ),
        }

    def _from_row(
        self,
        row: dict,
    ) -> Checkpoint:

        return Checkpoint(
            process_name=row["process_name"],
            status=CheckpointStatus(row["status"]),
            last_page=row["last_page"],
            posts_scanned=row["posts_scanned"],
            statistics_processed=row["statistics_processed"],
            version=row.get("version", "1.0"),
            last_post_date=self._parse_date(row.get("last_post_date")),
            started_at=self._parse_datetime(row.get("started_at")),
            updated_at=self._parse_datetime(row.get("updated_at")),
            completed_at=self._parse_datetime(row.get("completed_at")),
        )

    @staticmethod
    def _parse_datetime(value):

        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    @staticmethod
    def _parse_date(value):

        if value is None:
            return None

        if isinstance(value, date):
            return value

        return date.fromisoformat(value)
