from dataclasses import dataclass
from pathlib import Path
import re
@dataclass(slots=True)
class VideoMetadata:
    sequence: int
    path: Path
    filename: str
    extension: str

    total_frames: int
    fps: float
    duration: float

    width: int
    height: int

    extracted_frames: int = 0

    @property
    def resolution(self) -> str:
        """
        Return the resolution in a user-friendly format.

        Example:
            1920 × 1080
        """
        return f"{self.width} × {self.height}"

    @property
    def duration_text(self) -> str:
        """
        Return the duration in HH:MM:SS format.
        """
        total_seconds = int(self.duration)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    @property
    def aspect_ratio(self) -> float:
        """
        Return the aspect ratio.

        Example:
            1.777777777 (16:9)
        """
        if self.height == 0:
            return 0.0

        return self.width / self.height

    @property
    def file_stem(self) -> str:
        """
        Filename without extension.

        Example:
            camera01.mp4 -> camera01
        """
        return self.path.stem
    @property
    

    @property
    def safe_name(self) -> str:
        """
        Return a filesystem-safe version of the filename
        without its extension.
        """
        return re.sub(r"[^\w\-]", "_", self.path.stem)