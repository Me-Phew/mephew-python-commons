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

The `logger_factory` module provides a `LoggerFactory` class to configure and create robust loggers for your application. This pattern allows you to set up default logging behavior (like file paths, formatters, and rotation) once and then easily get standardized logger instances anywhere in your code.

**Features:**

-   **Centralized Defaults:** Instantiate the factory once with your application's default settings using a single `log_files_prefix`.
-   **Per-Logger Overrides:** Flexibly override the default file names or formatters for specific loggers when needed, giving you fine-grained control.
-   **Console Logging:** Logs messages to the standard console (stream).
-   **General File Logging:** Logs all messages (from the specified level up) to a general log file (e.g., `app.log`).
-   **Dedicated Error Logging:** Logs only `ERROR` level messages and higher to a separate error log file (e.g., `app.error.log`), making it easy to isolate critical issues.
-   **Log Rotation:** Automatically rotates log files daily at midnight.
-   **Idempotent:** Prevents duplicate handlers if `get_logger` is called multiple times for the same logger name.

## Usage Example

The best practice is to create a single `LoggerFactory` instance in a central configuration module and import it wherever you need a logger.

#### 1. Configure the Factory (e.g., in `config.py`)

Create the factory instance that your entire application will share. This is where you define the default behavior for all loggers.

```python
# config.py
from mephew_python_commons.logger_factory import LoggerFactory

# Create and configure the factory once.
# The `log_files_prefix` will be used to create `logs/app.log` and `logs/app.error.log`.
logger_factory = LoggerFactory(
    log_files_prefix="logs/app"
)
```

#### 2. Use the Factory in Your Application

Import the factory instance and use its `get_logger` method. You can either use the defaults or provide specific overrides.

```python
# main.py
import logging
from config import logger_factory # Import the pre-configured factory

# --- Example 1: Get a logger using factory defaults ---
# The name is typically __name__, which helps in tracking log origins.
main_logger = logger_factory.get_logger(__name__, level=logging.INFO)

main_logger.info("Application has started successfully.")
main_logger.error("Failed to connect to the database.")


# --- Example 2: Get a logger with custom overrides for a specific task ---
# This logger will write to different files than the default.
worker_logger = logger_factory.get_logger(
    "worker_process",
    level=logging.DEBUG,
    log_file_name="logs/worker.log",
    error_log_file_name="logs/worker.error.log"
)

worker_logger.debug("Starting a long-running task...")
try:
    result = 1 / 0
except ZeroDivisionError:
    worker_logger.exception("A critical error occurred in the worker!")

print("\nCheck your console output and the log files in the 'logs/' directory.")
```

### What Happens:

-   **Console Output:** All messages from `INFO` level and up will be printed to your console.
-   **`logs/app.log`:** This file will contain the `INFO` and `ERROR` messages from `main_logger`.
    -   `Application has started successfully.`
    -   `Failed to connect to the database.`
-   **`logs/app.error.log`:** This file will *only* contain the `ERROR` message from `main_logger`.
    -   `Failed to connect to the database.`
-   **`logs/worker.log`:** This file contains all messages from `worker_logger`.
    -   `Starting a long-running task...`
    -   `A critical error occurred in the worker!` (with stack trace)
-   **`logs/worker.error.log`:** This file *only* contains the `EXCEPTION` message from `worker_logger`.
    -   `A critical error occurred in the worker!` (with stack trace)
