"""
HoneyPy application logger.
"""

import logging
from pathlib import Path

from honeypy.config import LOG_PATH


def setup_logger():
    Path(LOG_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger("honeypy")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
