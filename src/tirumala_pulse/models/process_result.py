from dataclasses import dataclass
from datetime import date
from typing import Optional

from tirumala_pulse.models.process_status import ProcessStatus


@dataclass
class ProcessResult:

    success: bool

    report_date: Optional[date] = None

    status: ProcessStatus = ProcessStatus.SUCCESS

    records_processed: int = 0

    error_message: Optional[str] = None
