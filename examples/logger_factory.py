import logging
import sys
from pathlib import Path

LIBRARY_PATH = Path(__file__).resolve().parents[1] / "src" / "mephew_python_commons"

sys.path.append(str(LIBRARY_PATH))

from mephew_python_commons.logger_factory import LoggerFactory

logger_factory = LoggerFactory(log_files_prefix="logger_factory_demo")

logger = logger_factory.get_logger(__name__, level=logging.DEBUG)

logger.debug("This is a debug message.")
logger.info("Hello world!")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")

try:
    1 / 0  # This will raise a ZeroDivisionError
except ZeroDivisionError as e:
    logger.exception("An exception occurred: %s", e)
