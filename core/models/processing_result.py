from dataclasses import dataclass

@dataclass(slots=True)
class ProcessingResult:
    """
    Returned after one video has been processed.
    """

    success: bool

    video_name: str

    extracted: int

    train: int

    test: int

    val: int

    elapsed_seconds: float

    error_message: str = ""