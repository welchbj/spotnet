"""Utilities for logging."""

import sys
import logging

from logging import Formatter, getLogger, StreamHandler


def get_configured_logger(logger_name):
    """Get a configured Logger instance.

    Args:
        logger_name (str): The name to pass to ``logging.getLogger`` to
            retrieve the logger instance.

    Returns:
        logging.Logger: The configured Logger instance.

    """
    handler = StreamHandler(stream=sys.stdout)
    formatter = Formatter('[%(asctime)s|%(name)s|%(levelname)s] - %(message)s')

    logger = getLogger(logger_name)
    logger.setLevel(logging.INFO)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
