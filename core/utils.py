"""
===============================================================================
File        : utils.py
Project     : Video Frame Extractor

Description
-----------
Reusable helper functions shared across the application.

Guidelines
----------
✓ No GUI code
✓ No OpenCV VideoCapture
✓ No logging
✓ Pure helper functions
===============================================================================
"""

from __future__ import annotations

import re
from datetime import timedelta
from pathlib import Path


# =============================================================================
# Directory Helpers
# =============================================================================

def create_directory(path: Path) -> Path:
    """
    Create a directory if it does not already exist.

    Parameters
    ----------
    path : Path

    Returns
    -------
    Path
        The created (or existing) directory.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_output_structure(output_folder: Path) -> dict[str, Path]:
    """
    Ensure the standard dataset directory structure exists.

    Returns
    -------
    dict
        {
            "train": Path,
            "test": Path,
            "val": Path
        }
    """

    train = create_directory(output_folder / "train")
    test = create_directory(output_folder / "test")
    val = create_directory(output_folder / "val")

    return {
        "train": train,
        "test": test,
        "val": val,
    }


# =============================================================================
# Validation
# =============================================================================

def validate_ratios(train: int, test: int, val: int) -> bool:
    """
    Validate dataset split ratios.

    Returns
    -------
    bool
    """
    return (train + test + val) == 100


# =============================================================================
# File Helpers
# =============================================================================

def sanitize_filename(name: str) -> str:
    """
    Remove invalid filename characters.

    Example
    -------
    camera 01?.mp4

    becomes

    camera_01
    """

    name = Path(name).stem

    name = re.sub(r"[^\w\-]", "_", name)

    return name


def generate_frame_name(
    sequence: int,
    video_name: str,
    frame_number: int,
    extension: str = "png",
) -> str:
    """
    Generate a standardized frame filename.

    Example
    -------
    frm_0001_camera01_000123.png
    """

    video_name = sanitize_filename(video_name)

    return (
        f"frm_{sequence:04d}_"
        f"{video_name}_"
        f"{frame_number:06d}."
        f"{extension}"
    )


# =============================================================================
# Formatting
# =============================================================================

def format_duration(seconds: float) -> str:
    """
    Convert seconds into HH:MM:SS format.
    """
    return str(timedelta(seconds=int(seconds)))


def human_readable_size(size: int) -> str:
    """
    Convert bytes into KB, MB, GB...
    """

    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:

        if value < 1024:
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


# =============================================================================
# Time
# =============================================================================

def timestamp() -> str:
    """
    Return current timestamp.

    Example
    -------
    20260625_143530
    """

    from datetime import datetime

    return datetime.now().strftime("%Y%m%d_%H%M%S")