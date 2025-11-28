"""Health check responses.

Usually we have one class per file, but these are small enough to keep together.
"""

from enum import Enum

from pydantic import BaseModel


class SimpleStatus(str, Enum):
    up = "UP"
    down = "DOWN"


class Status(BaseModel):
    status: SimpleStatus
    details: dict


class Readiness(BaseModel):
    db: Status

    def is_down(self) -> bool:
        return self.db.status == SimpleStatus.down


class Liveness(BaseModel):
    webserver: SimpleStatus
