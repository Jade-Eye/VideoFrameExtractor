from dataclasses import dataclass, field

from .extraction_stats import ExtractionStats

@dataclass(slots=True)
class AppState:
    """
    Stores the current application state.

    Shared between the GUI and background worker.
    """

    is_processing: bool = False

    cancel_requested: bool = False

    current_video: str = ""

    current_frame: int = 0

    stats: ExtractionStats = field(default_factory=ExtractionStats)