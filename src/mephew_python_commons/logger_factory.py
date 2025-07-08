"""A utility module for creating and configuring standard loggers.

This module provides a LoggerFactory class to simplify the process of
setting up a consistent logging structure across an application. It includes
support for console logging and general/error-specific rotated log files.
"""

import logging
import logging.handlers

class LoggerFactory:
    """A factory for creating and configuring standardized logger instances."""

    # Default formatter for log messages written to files.
    # Format: <LoggerName> <ThreadName>; <YYYY-MM-DD HH:MM:SS>; <LogLevel>; <Message>
    DEFAULT_FILE_LOG_FORMATTER = logging.Formatter(
        "%(name)s %(threadName)s; %(asctime)s; %(levelname)s; %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    # Default formatter for log messages written to the console (stream).
    # Format: <LoggerName> <ThreadName>; <HH:MM:SS>; <LogLevel>; <Message>
    DEFAULT_STREAM_LOG_FORMATTER = logging.Formatter(
        "%(name)s %(threadName)s; %(asctime)s; %(levelname)s; %(message)s",
        "%H:%M:%S",
    )

    def __init__(
        self,
        *,
        log_file_prefix: str,
        error_log_file_prefix: str,
        backup_count: int = 7,
        encoding: str = "utf-8",
    ):
        """Initializes the factory with a common logging configuration.

        Args:
            log_file_prefix (str): The file prefix for general logs
            error_log_file_prefix (str): The file prefix for error logs
            backup_count (int, optional): The number of backup log files to keep
                Defaults to 7
            encoding (str, optional): The encoding for log files
                Defaults to "utf-8"
        """
        self.log_file_prefix = log_file_prefix
        self.error_log_file_prefix = error_log_file_prefix
        self.backup_count = backup_count
        self.encoding = encoding

    def get_logger(
        self,
        name: str,
        *,
        level: int,
        file_log_formatter: logging.Formatter = DEFAULT_FILE_LOG_FORMATTER,
        stream_log_formatter: logging.Formatter = DEFAULT_STREAM_LOG_FORMATTER,
    ) -> logging.Logger:
        """Sets up and returns a custom logger using the factory's configuration.

        Args:
            name (str): The name of the logger, typically `__name__`
            level (int): The minimum logging level for the logger (e.g., logging.INFO)
            file_log_formatter (logging.Formatter, optional): Formatter for
                file logs. Defaults to `DEFAULT_FILE_LOG_FORMATTER`
            stream_log_formatter (logging.Formatter, optional): Formatter for
                stream logs. Defaults to `DEFAULT_STREAM_LOG_FORMATTER`

        Returns:
            logging.Logger: A configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Add handlers only if they haven't been added before to prevent duplicate logs.
        if logger.handlers:
            return logger

        # Handler for writing ERROR level logs to a separate, rotated file.
        error_log_file_handler = logging.handlers.TimedRotatingFileHandler(
            f"{self.error_log_file_prefix}.error.log",
            when="midnight",
            backupCount=self.backup_count,
            encoding=self.encoding,
        )
        error_log_file_handler.setFormatter(file_log_formatter)
        error_log_file_handler.setLevel(logging.ERROR)

        # Handler for writing all logs to a general, rotated file.
        general_log_file_handler = logging.handlers.TimedRotatingFileHandler(
            f"{self.log_file_prefix}.log",
            when="midnight",
            backupCount=self.backup_count,
            encoding=self.encoding,
        )
        general_log_file_handler.setFormatter(file_log_formatter)

        # Handler for writing logs to the console/stream (e.g., stdout).
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(stream_log_formatter)

        logger.addHandler(general_log_file_handler)
        logger.addHandler(error_log_file_handler)
        logger.addHandler(stream_handler)

        return logger
