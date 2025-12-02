import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.core.config import settings


def setup_logging():
    # Create directory for logs if it doesn't exist
    log_path = Path(settings.LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Log format
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Main logger
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    # 1. Console Output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 2. File Output with Rotation (10MB, 5 backups)
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    logging.info("Logging setup complete.")
