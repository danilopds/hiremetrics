"""
Centralized logging configuration for ETL scripts
Ensures all logging output is properly captured by Prefect
"""

import logging
import sys
import os


def configure_logging(level=logging.INFO, script_name="ETL"):
    """
    Configure logging to ensure output is captured by Prefect

    Args:
        level: Logging level (default: INFO)
        script_name: Name of the script for log identification
    """
    # Create formatter
    formatter = logging.Formatter(
        f"%(asctime)s - {script_name} - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler that writes to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Create stderr handler for errors
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(formatter)

    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(stderr_handler)

    # Ensure subprocesses inherit the logging configuration
    os.environ["PYTHONUNBUFFERED"] = "1"
    # os.environ['PYTHONIOENCODING'] = 'utf-8'

    return root_logger


def get_logger(name, level=logging.INFO):
    """
    Get a logger with the specified name and level

    Args:
        name: Logger name
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # If no handlers are configured, configure them
    if not logger.handlers:
        configure_logging(level, name)

    return logger
