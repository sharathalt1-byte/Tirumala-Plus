from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from tirumala_pulse.models.checkpoint_status import (
    CheckpointStatus,
)


@dataclass
class Checkpoint:

    process_name: str

    status: CheckpointStatus

    last_page: int

    posts_scanned: int

    statistics_processed: int

    version: str = "1.0"

    last_post_date: Optional[date] = None

    started_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None
