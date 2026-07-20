from dataclasses import dataclass
from typing import Optional


@dataclass
class ETLRun:

    status: str

    records_processed: int

    execution_time_ms: int

    error_message: Optional[str] = None

    def to_dict(self):

        return {
            "status": self.status,
            "records_processed": self.records_processed,
            "execution_time_ms": self.execution_time_ms,
            "error_message": self.error_message,
        }

    def __str__(self):

        return (
            f"ETLRun("
            f"status={self.status}, "
            f"records={self.records_processed}, "
            f"time={self.execution_time_ms}ms)"
        )
