"""A utility module for creating and configuring standard loggers.

This module provides a LoggerFactory class to simplify the process of
setting up a consistent logging structure across an application. It includes
support for console logging and general/error-specific rotated log files.
"""

import logging
import threading

from concurrent_log_handler import ConcurrentTimedRotatingFileHandler


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
        log_files_prefix: str,
        backup_count: int = 7,
        encoding: str = "utf-8",
        file_log_formatter: logging.Formatter = DEFAULT_FILE_LOG_FORMATTER,
        stream_log_formatter: logging.Formatter = DEFAULT_STREAM_LOG_FORMATTER,
    ):
        """Initializes the factory with a common logging configuration.

        This configuration acts as the default for all loggers created by this factory.

        Args:
            log_files_prefix (str): The base prefix for log file names. This will be
                used to generate `{log_files_prefix}.log` and `{log_files_prefix}.error.log`
                by default
            backup_count (int, optional): The number of backup log files to keep.
                Defaults to 7
            encoding (str, optional): The encoding for log files
                Defaults to "utf-8"
            file_log_formatter (logging.Formatter, optional): The default formatter
                for file-based logs. Defaults to `DEFAULT_FILE_LOG_FORMATTER`
            stream_log_formatter (logging.Formatter, optional): The default formatter
                for console-based logs. Defaults to `DEFAULT_STREAM_LOG_FORMATTER`
        """
        self._log_files_prefix = log_files_prefix
        self._backup_count = backup_count
        self._encoding = encoding
        self._file_log_formatter = file_log_formatter
        self._stream_log_formatter = stream_log_formatter

        self._lock = threading.Lock()

    def get_logger(
        self,
        name: str,
        *,
        level: int,
        log_file_name: str | None = None,
        error_log_file_name: str | None = None,
        file_log_formatter: logging.Formatter | None = None,
        stream_log_formatter: logging.Formatter | None = None,
    ) -> logging.Logger:
        """Sets up and returns a custom logger, with options to override factory settings.

        If an override argument (e.g., `log_file_name`) is not provided, this method
        will use the default configuration from the factory instance.

        Args:
            name (str): The name of the logger, typically `__name__`
            level (int): The minimum logging level for the logger (e.g., logging.INFO)
            log_file_name (str | None, optional): Overrides the default general log
                file name. If None, uses the factory's default: `{log_files_prefix}.log`
            error_log_file_name (str | None, optional): Overrides the default error log
                file name. If None, uses the factory's default: `{log_files_prefix}.error.log`
            file_log_formatter (logging.Formatter | None, optional): Overrides the
                factory's default file formatter
            stream_log_formatter (logging.Formatter | None, optional): Overrides the
                factory's default stream formatter

        Returns:
            logging.Logger: A configured logger instance.
        """
        with self._lock:
            # Determine the final configuration, using overrides if provided, otherwise factory defaults.
            final_log_file_name = log_file_name or f"{self._log_files_prefix}.log"
            final_error_log_file_name = error_log_file_name or f"{self._log_files_prefix}.error.log"
            final_file_formatter = file_log_formatter or self._file_log_formatter
            final_stream_formatter = stream_log_formatter or self._stream_log_formatter

            logger = logging.getLogger(name)

            if logger.handlers:
                if logger.level > level:
                    logger.setLevel(level)

                # Skip the rest of the configuration if the logger already has handlers to avoid duplicate handlers.
                return logger

            logger.setLevel(level)
            logger.propagate = False

            # Handler for writing ERROR level logs to a separate, rotated file.
            error_log_file_handler = ConcurrentTimedRotatingFileHandler(
                final_error_log_file_name,
                when="midnight",
                backupCount=self._backup_count,
                encoding=self._encoding,
            )
            error_log_file_handler.setFormatter(final_file_formatter)
            error_log_file_handler.setLevel(logging.ERROR)

            # Handler for writing all logs to a general, rotated file.
            general_log_file_handler = ConcurrentTimedRotatingFileHandler(
                final_log_file_name,
                when="midnight",
                backupCount=self._backup_count,
                encoding=self._encoding,
            )
            general_log_file_handler.setFormatter(final_file_formatter)

            # Handler for writing logs to the console/stream (e.g., stdout).
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(final_stream_formatter)

            logger.addHandler(general_log_file_handler)
            logger.addHandler(error_log_file_handler)
            logger.addHandler(stream_handler)

            return logger
