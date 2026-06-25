"""
===============================================================================
File        : frame_extractor.py
Project     : Video Frame Extractor

Description
-----------
Core engine responsible for extracting frames from videos.

Responsibilities
----------------
✓ Process one or more videos
✓ Generate randomized Train/Test/Val distribution
✓ Update application statistics
✓ Support cancellation
✓ Notify GUI through callbacks

NOTE:
Actual frame extraction is implemented in Part 2.
===============================================================================
"""

from __future__ import annotations
from core.utils import generate_frame_name
import cv2
import random
from pathlib import Path
from typing import Callable
from core.types import DatasetType,ImageFormat

from core.managers import config, logger
from core.models import (
    AppState,
    DatasetSplit,
    FrameDistribution,
    ProcessingResult,
    VideoMetadata,
)

from services.video_service import (
    get_video_metadata,
    calculate_frame_interval,
)

import time



from services.video_service import open_capture,close_capture
from core.utils import ensure_output_structure



class FrameExtractor:
    """
    Main frame extraction engine.

    This class performs all dataset extraction work while remaining
    independent from the GUI.

    Parameters
    ----------
    app_state
        Shared application state.

    progress_callback
        Optional callback used to update the GUI.

    status_callback
        Optional callback used to display status messages.
    """

    def __init__(
        self,
        app_state: AppState,
        progress_callback: Callable | None = None,
        status_callback: Callable | None = None,
    ) -> None:

        self.state = app_state

        self.progress_callback = progress_callback
        self.status_callback = status_callback

        logger.info("FrameExtractor initialized.")

    # ======================================================================
    # Public API
    # ======================================================================

    def cancel(self) -> None:
        """
        Request cancellation.

        The extraction loop checks this flag regularly and exits safely.
        """

        logger.warning("Cancellation requested.")

        self.state.cancel_requested = True

    # ----------------------------------------------------------------------

    def process_videos(
        self,
        videos: list[VideoMetadata],
    ) -> list[ProcessingResult]:
        """
        Process multiple videos.

        Parameters
        ----------
        videos
            List of videos selected by the user.

        Returns
        -------
        list[ProcessingResult]
        """

        logger.info(f"Processing {len(videos)} video(s).")

        self.state.is_processing = True
        self.state.cancel_requested = False

        self.state.stats.videos_total = len(videos)
        self.state.stats.videos_processed = 0

        results: list[ProcessingResult] = []

        for video in videos:

            if self.state.cancel_requested:

                logger.warning("Processing cancelled by user.")

                break

            self.state.current_video = video.filename

            self._notify_status(
                f"Processing {video.filename}"
            )

            result = self.process_video(video)

            results.append(result)

            self.state.stats.videos_processed += 1

            self._notify_progress()

        self.state.is_processing = False

        logger.info("All videos processed.")

        return results

    # ----------------------------------------------------------------------

    def process_video(
        self,
        video: VideoMetadata,
    ) -> ProcessingResult:
        """
        Process a single video.

        Implemented in Part 2.
        """

        raise NotImplementedError(
            "Implemented in Part 2."
        )

    # ======================================================================
    # Distribution
    # ======================================================================

    def generate_distribution(
        self,
        frame_count: int,
        split: DatasetSplit,
    ) -> FrameDistribution:
        """
        Generate randomized Train/Test/Validation assignments.

        Example
        -------

        T T T V T T T E T ...

        where

            T = Train
            E = Test
            V = Validation
        """

        train_count = round(
            frame_count * split.train / 100
        )

        test_count = round(
            frame_count * split.test / 100
        )

        val_count = (
            frame_count
            - train_count
            - test_count
        )

        assignments = (
            ["train"] * train_count
            + ["test"] * test_count
            + ["val"] * val_count
        )

        random.shuffle(assignments)

        distribution = FrameDistribution(
            train=[],
            test=[],
            val=[],
        )

        for index, destination in enumerate(assignments):

            if destination == DatasetType.TRAIN:

                distribution.train.add(index)

            elif destination == DatasetType.TEST:

                distribution.test.add(index)

            else:

                distribution.val.add(index)

        logger.info(
            "Generated random dataset distribution."
        )

        return distribution

    # ======================================================================
    # Callback Helpers
    # ======================================================================

    def _notify_progress(self) -> None:
        """
        Notify GUI that statistics have changed.
        """

        if self.progress_callback is not None:

            self.progress_callback(self.state)

    # ----------------------------------------------------------------------

    def _notify_status(
        self,
        message: str,
    ) -> None:
        """
        Notify GUI of status changes.
        """

        logger.info(message)

        if self.status_callback is not None:

            self.status_callback(message)

    # ======================================================================
    # Internal Helpers
    # ======================================================================

    def _is_cancelled(self) -> bool:
        """
        Check whether the user requested cancellation.
        """

        return self.state.cancel_requested

    # ----------------------------------------------------------------------

    @staticmethod
    def _frame_belongs_to(
        frame_number: int,
        distribution: FrameDistribution,
    ) -> str:
        """
        Determine the dataset folder for a frame.

        Returns
        -------
        str

            "train"
            "test"
            "val"
        """

        if frame_number in distribution.train:
            return "train"

        if frame_number in distribution.test:
            return "test"

        return "val"
    

        # ======================================================================
    # Video Processing
    # ======================================================================

    def process_video(
        self,
        video: VideoMetadata,
    ) -> ProcessingResult:
        """
        Process a single video.

        This method is responsible for:

            • Opening the video
            • Reading frames
            • Extracting frames at the configured FPS
            • Updating statistics
            • Delegating frame saving

        Returns
        -------
        ProcessingResult
        """

        

        logger.info(f"Starting video: {video.filename}")

        start_time = time.perf_counter()

        capture = None

        extracted = 0
        train = 0
        test = 0
        val = 0

        try:

            capture = open_capture(video.path)

            interval = calculate_frame_interval(
                video.fps,
                config.fps,
            )

            estimated_frames = max(
                1,
                video.total_frames // interval,
            )

            split = DatasetSplit(
                train=config.train_ratio,
                test=config.test_ratio,
                val=config.val_ratio,
            )

            distribution = self.generate_distribution(
                estimated_frames,
                split,
            )

            output_dirs = ensure_output_structure(
                Path(config.output_folder)
            )

            extracted_index = 0
            frame_index = 0

            while True:

                if self._is_cancelled():

                    logger.warning(
                        "Extraction cancelled."
                    )

                    break

                success, frame = capture.read()

                if not success:
                    break

                frame_index += 1

                # Skip frames according to extraction interval.
                if frame_index % interval != 0:
                    continue

                extracted_index += 1

                destination = self._frame_belongs_to(
                    extracted_index - 1,
                    distribution,
                )

                saved = self._save_frame(
                    frame=frame,
                    video=video,
                    frame_number=extracted_index,
                    destination=destination,
                    output_dirs=output_dirs,
                )

                if not saved:
                    self.state.stats.failed_frames += 1
                    continue

                extracted += 1

                video.extracted_frames = extracted

                if destination == "train":
                    train += 1
                elif destination == "test":
                    test += 1
                else:
                    val += 1

                self._update_statistics(destination)

                self._update_progress(
                    frame_index,
                    video.total_frames,
                )

            elapsed = time.perf_counter() - start_time

            logger.info(
                f"{video.filename} finished "
                f"({extracted} frames)"
            )

            return ProcessingResult(
                success=True,
                video_name=video.filename,
                extracted=extracted,
                train=train,
                test=test,
                val=val,
                elapsed_seconds=elapsed,
            )

        except Exception as exc:

            logger.exception(
                f"Error processing {video.filename}"
            )

            elapsed = time.perf_counter() - start_time

            return ProcessingResult(
                success=False,
                video_name=video.filename,
                extracted=0,
                train=0,
                test=0,
                val=0,
                elapsed_seconds=elapsed,
                error_message=str(exc),
            )

        finally:

            if capture is not None:
                close_capture(capture=capture)

    
    # ======================================================================
    # Frame Saving
    # ======================================================================

    def _save_frame(
        self,
        *,
        frame,
        video: VideoMetadata,
        frame_number: int,
        destination: str,
        output_dirs: dict[str, Path],
    ) -> bool:
        """
        Save an extracted frame.

        Parameters
        ----------
        frame
            OpenCV image.

        video
            Source video metadata.

        frame_number
            Sequential extracted frame number.

        destination
            train | test | val

        output_dirs
            Output folder dictionary.

        Returns
        -------
        bool

            True  -> Saved successfully

            False -> Failed / Skipped
        """

        from core.utils import generate_frame_name

        folder = output_dirs[destination]

        filename = generate_frame_name(
            sequence=video.sequence,
            video_name=video.safe_name,
            frame_number=frame_number,
            extension=config.image_format,
        )

        output_file = folder / filename

        # --------------------------------------------------------------
        # Existing File
        # --------------------------------------------------------------

        if output_file.exists():

            if not config.overwrite_existing:

                self.state.stats.skipped_frames += 1

                return False

        # --------------------------------------------------------------
        # PNG
        # --------------------------------------------------------------

        if config.image_format.lower() == ImageFormat.PNG:

            success = cv2.imwrite(
                str(output_file),
                frame,
            )

        # --------------------------------------------------------------
        # JPG
        # --------------------------------------------------------------

        else:

            success = cv2.imwrite(
                str(output_file),
                frame,
                [
                    cv2.IMWRITE_JPEG_QUALITY,
                    config.jpeg_quality,
                ],
            )

        if success:

            logger.debug(f"Saved: {filename}")

        else:

            logger.error(f"Unable to save: {filename}")

        return success

    # ======================================================================
    # Statistics
    # ======================================================================

    def _update_statistics(
        self,
        destination: str,
    ) -> None:
        """
        Update application statistics.
        """

        self.state.stats.extracted_frames += 1

        if destination == "train":

            self.state.stats.train_frames += 1

        elif destination == "test":

            self.state.stats.test_frames += 1

        else:

            self.state.stats.val_frames += 1

    # ----------------------------------------------------------------------

    def _update_progress(
        self,
        frame_index: int,
        total_frames: int,
    ) -> None:
        """
        Update extraction progress.
        """

        if total_frames <= 0:

            self.state.stats.progress = 0.0

        else:

            self.state.stats.progress = (
                frame_index / total_frames
            ) * 100.0

        self.state.current_frame = frame_index

        self._notify_progress()

    # ======================================================================
    # Helpers
    # ======================================================================

    @staticmethod
    def _save_destination(
        destination: str,
        output_dirs: dict[str, Path],
    ) -> Path:
        """
        Return destination directory.
        """

        return output_dirs[destination]

    # ----------------------------------------------------------------------

    @staticmethod
    def _is_supported_image_format(
        extension: str,
    ) -> bool:
        """
        Validate image format.
        """

        return extension.lower() in (
            "png",
            "jpg",
            "jpeg",
        )
    



        # ======================================================================
    # Cleanup
    # ======================================================================

    def _reset_state(self) -> None:
        """
        Reset runtime processing state.

        This method is called before a new extraction session starts.
        """

        self.state.cancel_requested = False
        self.state.is_processing = False

        self.state.current_video = ""
        self.state.current_frame = 0

    # ----------------------------------------------------------------------

    def _finish_processing(self) -> None:
        """
        Called when all videos have finished processing.
        """

        self.state.is_processing = False

        self._notify_status("Processing completed.")

        self._notify_progress()

        logger.info("Frame extraction completed.")

    # ======================================================================
    # Session Helpers
    # ======================================================================

    def start(self) -> None:
        """
        Prepare extractor for a new session.
        """

        logger.info("Starting extraction session.")

        self._reset_state()

        self.state.is_processing = True

    # ----------------------------------------------------------------------

    def stop(self) -> None:
        """
        Stop current extraction session.
        """

        logger.info("Stopping extraction session.")

        self._finish_processing()

    # ======================================================================
    # Utility
    # ======================================================================

    @staticmethod
    def _safe_percentage(
        value: int,
        total: int,
    ) -> float:
        """
        Calculate percentage safely.

        Returns
        -------
        float
        """

        if total == 0:
            return 0.0

        return round((value / total) * 100.0, 2)

    # ----------------------------------------------------------------------

    def summary(self) -> dict:
        """
        Return extraction statistics.

        Useful for reports and GUI.
        """

        stats = self.state.stats

        return {
            "videos_total": stats.videos_total,
            "videos_processed": stats.videos_processed,
            "frames_total": stats.total_frames,
            "frames_extracted": stats.extracted_frames,
            "train_frames": stats.train_frames,
            "test_frames": stats.test_frames,
            "val_frames": stats.val_frames,
            "skipped_frames": stats.skipped_frames,
            "failed_frames": stats.failed_frames,
            "progress": stats.progress,
            "train_percent": self._safe_percentage(
                stats.train_frames,
                stats.extracted_frames,
            ),
            "test_percent": self._safe_percentage(
                stats.test_frames,
                stats.extracted_frames,
            ),
            "val_percent": self._safe_percentage(
                stats.val_frames,
                stats.extracted_frames,
            ),
        }

    # ----------------------------------------------------------------------

    def __enter__(self):
        """
        Context manager support.

        Example
        -------
        with FrameExtractor(state) as extractor:
            ...
        """

        self.start()

        return self

    # ----------------------------------------------------------------------

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        """
        Ensure extractor is stopped.
        """

        self.stop()

        return False
    




