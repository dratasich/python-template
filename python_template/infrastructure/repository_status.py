from enum import Enum


class RepositoryStatus(str, Enum):
    UNKNOWN = "unknown"
    CONNECTED = "connected"
