"""
===============================================================================
File        : __init__.py
Project     : Video Frame Extractor

Description
-----------
Exports all data models used throughout the application.

Example
-------
from core.models import (
    VideoInfo,
    ExtractionStats,
    ProcessingResult,
    DatasetSplit,
)
===============================================================================
"""

from .video_metadata import VideoMetadata
from .extraction_stats import ExtractionStats
from .processing_result import ProcessingResult
from .dataset_split import DatasetSplit
from .app_state import AppState
from .frame_distribution import FrameDistribution

__all__ = [
    "VideoMetadata",
    "ExtractionStats",
    "ProcessingResult",
    "DatasetSplit",
    "AppState",
    "FrameDistribution",
]