"""
SQLite database layer for HoneyPy.
"""

import sqlite3
from pathlib import Path

from honeypy.config import DATABASE_PATH
from honeypy.models.attack import AttackEvent


class Database:
    def __init__(self, database_path: str = DATABASE_PATH):
        self.database_path = database_path

        Path(database_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            database_path,
            check_same_thread=False
        )

        self._create_tables()

    def _create_tables(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS attacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_ip TEXT NOT NULL,
                event_type TEXT NOT NULL,
                username TEXT,
                password TEXT,
                command TEXT,
                timestamp TEXT NOT NULL
            )
            """
        )

        self.connection.commit()

    def record_attack(self, event: AttackEvent):
        self.connection.execute(
            """
            INSERT INTO attacks (
                source_ip,
                event_type,
                username,
                password,
                command,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                event.source_ip,
                event.event_type,
                event.username,
                event.password,
                event.command,
                event.timestamp,
            ),
        )

        self.connection.commit()

    def get_recent_attacks(self, limit: int = 20):
        cursor = self.connection.execute(
            """
            SELECT
                id,
                source_ip,
                event_type,
                username,
                password,
                command,
                timestamp
            FROM attacks
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        return cursor.fetchall()

    def close(self):
        self.connection.close()
