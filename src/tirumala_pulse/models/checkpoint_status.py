from enum import Enum


class CheckpointStatus(str, Enum):

    NOT_STARTED = "NOT_STARTED"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"
