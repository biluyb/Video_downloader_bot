"""Temporary file and directory cleanup service."""

import shutil
from pathlib import Path
from typing import Union

from app.utils.logger import get_logger

logger = get_logger(__name__)


def cleanup_job_directory(job_dir: Union[str, Path]) -> None:
    """Safely remove a job directory and all its contents.

    Args:
        job_dir: Path to directory to remove.
    """
    path = Path(job_dir).resolve()
    if path.exists() and path.is_dir():
        try:
            shutil.rmtree(path)
            logger.info("Cleaned job directory: %s", path)
        except Exception as e:
            logger.error("Failed to clean job directory %s: %s", path, e)
