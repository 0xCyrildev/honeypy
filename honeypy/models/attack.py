"""
Data models for HoneyPy attack events.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AttackEvent:
    source_ip: str
    event_type: str
    username: str | None = None
    password: str | None = None
    command: str | None = None
    timestamp: str | None = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
