# looger_config.py

"""
This module sets up the advanced logging configuration for the application.
It includes both console and file logging, with options for formatting and log rotation.
"""

import logging
import logging.handlers
import os

# Create a 'logger' directory if it doesn't exist
log_directory = 'logger'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure the format for logging
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

# Determine log level from environment variable (default to INFO if not set)
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

# Create a logger instance
logger = logging.getLogger(__name__)

# Check if handlers are already configured (to avoid adding multiple handlers)
if not logger.handlers:
    # Basic configuration for console logging
    logging.basicConfig(level=getattr(logging, log_level), format=log_format)

    # File handler - logs messages to a file with rotation, within the 'logger' directory
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_directory, 'application.log'), maxBytes=10000000, backupCount=5
    )
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(logging.Formatter(log_format))

    # Add the file handler to the logger
    logger.addHandler(file_handler)
