import logging
from pathlib import Path


def get_logger() -> logging.Logger:
    logger = logging.getLogger("backend.scoring")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s request_id=%(request_id)s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def ensure_log_directory() -> None:
    Path("logs").mkdir(exist_ok=True)
