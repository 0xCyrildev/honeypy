"""
HoneyPy event processing.
"""

from honeypy.core.database import Database
from honeypy.models.attack import AttackEvent
from honeypy.utils.logger import setup_logger


class EventProcessor:
    def __init__(self, database: Database):
        self.database = database
        self.logger = setup_logger()

    def process(self, event: AttackEvent):
        self.database.record_attack(event)

        self.logger.info(
            "ATTACK | type=%s | ip=%s | username=%s | command=%s",
            event.event_type,
            event.source_ip,
            event.username,
            event.command,
        )
