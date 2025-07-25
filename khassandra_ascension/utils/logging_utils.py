"""
Logging utilities for the Khassandra Ascension package.

This module centralises logging configuration.  It sets up a root
logger that writes to both the console and to a log file in the
specified output directory.  A typical usage pattern is to call
``setup_logging`` early in your application and then use
``logging.getLogger(__name__)`` throughout your code.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(output_dir: str, level: int = logging.INFO) -> logging.Logger:
    """Configure the root logger to log to console and to a file.

    Parameters
    ----------
    output_dir:
        Directory in which to place the log file.  The directory will be
        created if it does not already exist.
    level:
        The logging level to set on the root logger.  Defaults to
        :data:`logging.INFO`.

    Returns
    -------
    logging.Logger
        The configured root logger.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    log_file = out_path / "ascension.log"

    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove any existing handlers to avoid duplicate logs when setup is
    # called multiple times.
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler writes logs to disk
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console handler outputs logs to stdout
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.debug("Logging has been configured. Logs will be written to %s", log_file)
    return logger
