"""
===============================================================================
File        : types.py
Project     : Video Frame Extractor

Description
-----------
Common enumerations used throughout the application.
===============================================================================
"""

from enum import Enum


class DatasetType(str, Enum):
    """
    Dataset split types.
    """

    TRAIN = "train"
    TEST = "test"
    VAL = "val"


class ImageFormat(str, Enum):
    """
    Supported image formats.
    """

    PNG = "png"
    JPG = "jpg"


class Theme(str, Enum):
    """
    Application themes.
    """

    LIGHT = "light"
    DARK = "dark"


class ProcessingStatus(str, Enum):
    """
    Processing status.
    """

    IDLE = "Idle"
    RUNNING = "Running"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    FAILED = "Failed"


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class VideoState(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"