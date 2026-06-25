"""
===============================================================================
File        : video_service.py
Project     : Video Frame Extractor

Description
-----------
Provides helper functions for reading and validating video files.

Responsibilities
----------------
✓ Validate video files
✓ Open videos
✓ Read metadata
✓ Calculate extraction interval

This module DOES NOT extract frames.
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import cv2

from core.constants import SUPPORTED_VIDEO_EXTENSIONS
from core.exceptions import (
    InvalidVideoError,
    UnsupportedVideoFormatError,
)
from core.models import VideoMetadata


# =============================================================================
# Validation
# =============================================================================

def validate_video(video_path: Path) -> None:
    """
    Validate a video before opening it.

    Raises
    ------
    FileNotFoundError
    UnsupportedVideoFormatError
    """

    if not video_path.exists():
        raise FileNotFoundError(video_path)

    if video_path.suffix.lower() not in SUPPORTED_VIDEO_EXTENSIONS:
        raise UnsupportedVideoFormatError(video_path.suffix)


# =============================================================================
# Video Capture
# =============================================================================

def open_capture(video_path: Path) -> cv2.VideoCapture:
    """
    Open a video using OpenCV.

    Returns
    -------
    cv2.VideoCapture
    """

    validate_video(video_path)

    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        raise InvalidVideoError(
            f"Unable to open video:\n{video_path}"
        )

    return capture


def close_capture(capture: cv2.VideoCapture) -> None:
    """
    Release an OpenCV VideoCapture object.
    """

    if capture is not None:
        capture.release()


# =============================================================================
# Metadata
# =============================================================================

def get_video_metadata(
    sequence: int,
    video_path: Path,
) -> VideoMetadata:
    """
    Read metadata from a video.

    Parameters
    ----------
    sequence
        Sequential number assigned by the application.

    video_path
        Video path.

    Returns
    -------
    VideoMetadata
    """

    capture = open_capture(video_path)

    try:

        fps = capture.get(cv2.CAP_PROP_FPS)

        total_frames = int(
            capture.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        width = int(
            capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        duration = 0.0

        if fps > 0:
            duration = total_frames / fps

        return VideoMetadata(
            sequence=sequence,
            path=video_path,
            filename=video_path.name,
            extension=video_path.suffix.lower(),
            fps=fps,
            total_frames=total_frames,
            duration=duration,
            width=width,
            height=height,
        )

    finally:
        close_capture(capture)


# =============================================================================
# Frame Extraction Helpers
# =============================================================================

def calculate_frame_interval(
    original_fps: float,
    target_fps: float,
) -> int:
    """
    Calculate the frame interval.

    Example
    -------

    Original FPS : 30

    Target FPS : 5

    Interval = 6

    Every 6th frame is extracted.
    """

    if target_fps <= 0:
        raise ValueError("Target FPS must be greater than zero.")

    if original_fps <= target_fps:
        return 1

    return max(
        1,
        round(original_fps / target_fps)
    )