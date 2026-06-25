from dataclasses import dataclass

@dataclass(slots=True)
class ExtractionStats:
    """
    Live statistics displayed in the GUI.
    """

    videos_total: int = 0

    videos_processed: int = 0

    total_frames: int = 0

    extracted_frames: int = 0

    train_frames: int = 0

    test_frames: int = 0

    val_frames: int = 0

    skipped_frames: int = 0

    failed_frames: int = 0

    progress: float = 0.0