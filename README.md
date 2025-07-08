# MePhew Python Commons

![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)

Common utilities for Python projects.

This repository contains a collection of reusable, high-quality Python modules designed to simplify common development tasks.

## Table of Contents

- [Installation](#installation)
- [Utilities](#utilities)
  - [Custom Logger](#custom-logger)
- [Usage Example](#usage-example)
- [Contributing](#contributing)
- [License](#license)

## Utilities

This library aims to provide a collection of useful, standalone utilities.

### Custom Logger

The `custom_logger` module provides a factory function `get_custom_logger` to quickly configure a robust logger for your application.

**Features:**

-   **Easy Setup:** Get a pre-configured logger with a single function call.
-   **Console Logging:** Logs messages to the standard console (stream).
-   **General File Logging:** Logs all messages (from the specified level and up) to a general log file (e.g., `simple485.log`).
-   **Dedicated Error Logging:** Logs only `ERROR` level messages and higher to a separate error log file (e.g., `simple485.error.log`), making it easy to isolate critical issues.
-   **Log Rotation:** Automatically rotates log files daily at midnight, preventing them from growing indefinitely.
-   **Customizable:** Easily change log levels, file names, formatters, and backup counts.
-   **Idempotent:** Prevents duplicate handlers if called multiple times for the same logger name.

## Usage Example

Here's how to use the `get_custom_logger` function in your project.

```python
import logging
from mephew_python_commons.custom_logger import get_custom_logger

# 1. Get a configured logger instance using default settings.
# The name is typically the module name, which helps in tracking log origins.
logger = get_custom_logger(__name__, level=logging.INFO)

# You can also customize the file names and other settings:
# logger = get_custom_logger(
#     __name__,
#     level=logging.DEBUG,
#     log_file_name="my_app.log",
#     error_log_file_name="my_app.error.log"
# )

# 2. Use the logger to record events
logger.debug("This is a debug message. It won't be shown because level is INFO.")
logger.info("Application has started successfully.")
logger.warning("The disk space is running low.")
logger.error("Failed to connect to the database. This will go to all logs.")

try:
    result = 1 / 0
except ZeroDivisionError:
    logger.exception("An unhandled exception occurred! This will also go to the error log.")

print("\nCheck your console output, 'simple485.log', and 'simple485.error.log' files.")

```

### What Happens:

-   **Console Output:** All messages from `INFO` level and up will be printed to your console with a simple timestamp.
-   **`simple485.log`:** This file will contain the `INFO`, `WARNING`, `ERROR`, and `EXCEPTION` messages, with detailed timestamps.
-   **`simple485.error.log`:** This file will *only* contain the `ERROR` and `EXCEPTION` messages, making it easy to find critical failures.
