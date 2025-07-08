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

The `logger_factory` module provides a `LoggerFactory` class to configure and create robust loggers for your application. This pattern allows you to set up your logging configuration (like file paths and rotation settings) once and then easily get standardized logger instances anywhere in your code.

**Features:**

-   **Centralized Configuration:** Instantiate the factory once with your desired settings (file prefixes, backup count) and reuse it.
-   **Console Logging:** Logs messages to the standard console (stream).
-   **General File Logging:** Logs all messages (from the specified level and up) to a general log file (e.g., `my_app.log`).
-   **Dedicated Error Logging:** Logs only `ERROR` level messages and higher to a separate error log file (e.g., `my_app.error.log`), making it easy to isolate critical issues.
-   **Log Rotation:** Automatically rotates log files daily at midnight, preventing them from growing indefinitely.
-   **Customizable:** Easily change log levels, formatters, and backup counts.
-   **Idempotent:** Prevents duplicate handlers if `get_logger` is called multiple times for the same logger name.

## Usage Example

Here's how to use the `LoggerFactory` in your project. The best practice is to create the factory instance in a central configuration module.

#### 1. Configure the Factory (e.g., in `config.py`)

Create a single factory instance that your entire application can share. This is where you define the log file locations.

```python
# config.py
from mephew_python_commons.logger_factory import LoggerFactory

# Create and configure the factory once for your application.
# This instance will be imported by other modules.
logger_factory = LoggerFactory(
    log_file_prefix="logs/my_app",
    error_log_file_prefix="logs/my_app_errors"
)
```

#### 2. Use the Factory in Your Application (e.g., in `main.py`)

Import the factory instance and use it to get a logger specific to the current module.

```python
# main.py
import logging
from config import logger_factory # Import the pre-configured factory

# Get a logger for this specific module.
# The name is typically __name__, which helps in tracking log origins.
logger = logger_factory.get_logger(__name__, level=logging.INFO)

# Use the logger to record events
logger.debug("This is a debug message. It won't be shown because level is INFO.")
logger.info("Application has started successfully.")
logger.warning("The disk space is running low.")
logger.error("Failed to connect to the database. This will go to all logs.")

try:
    result = 1 / 0
except ZeroDivisionError:
    # exc_info=True adds the full stack trace to the log message.
    logger.exception("An unhandled exception occurred!")

print("\nCheck your console output, 'logs/my_app.log', and 'logs/my_app_errors.error.log' files.")

```

### What Happens:

-   **Console Output:** All messages from `INFO` level and up will be printed to your console with a simple timestamp.
-   **`logs/my_app.log`:** This file will contain the `INFO`, `WARNING`, `ERROR`, and `EXCEPTION` messages, with detailed timestamps.
-   **`logs/my_app_errors.error.log`:** This file will *only* contain the `ERROR` and `EXCEPTION` messages, making it easy to find critical failures.
