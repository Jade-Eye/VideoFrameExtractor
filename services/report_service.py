"""
===============================================================================
File        : report_service.py
Project     : Video Frame Extractor

Description
-----------
Generates processing reports.

Responsibilities
----------------
✓ CSV report
✓ Dataset summary
✓ Future JSON export
✓ Future Excel export

===============================================================================
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from core.managers import logger
from core.models import (
    ExtractionStats,
    ProcessingResult,
)


# =============================================================================
# Public Functions
# =============================================================================

def generate_csv(
    results: list[ProcessingResult],
    stats: ExtractionStats,
    output_folder: Path,
) -> Path:
    """
    Generate dataset_report.csv.

    Parameters
    ----------
    results
        Processing results.

    stats
        Final extraction statistics.

    output_folder
        Root output directory.

    Returns
    -------
    Path
        Path to generated report.
    """

    reports_dir = output_folder / "reports"
    reports_dir.mkdir(exist_ok=True)
    report = reports_dir / "dataset_report.csv"

    logger.info(f"Writing report: {report}")

    with report.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.writer(csv_file)

        # -----------------------------------------------------------------
        # Header
        # -----------------------------------------------------------------

        writer.writerow([
            "Video",
            "Extracted",
            "Train",
            "Test",
            "Validation",
            "Elapsed (s)",
            "Status",
        ])

        # -----------------------------------------------------------------
        # Videos
        # -----------------------------------------------------------------

        for result in results:

            writer.writerow([
                result.video_name,
                result.extracted,
                result.train,
                result.test,
                result.val,
                f"{result.elapsed_seconds:.2f}",
                "Success" if result.success else "Failed",
            ])

        # -----------------------------------------------------------------
        # Empty Line
        # -----------------------------------------------------------------

        writer.writerow([])

        # -----------------------------------------------------------------
        # Summary
        # -----------------------------------------------------------------

        writer.writerow(["Summary"])

        writer.writerow([
            "Videos Processed",
            stats.videos_processed,
        ])

        writer.writerow([
            "Frames Extracted",
            stats.extracted_frames,
        ])

        writer.writerow([
            "Train Frames",
            stats.train_frames,
        ])

        writer.writerow([
            "Test Frames",
            stats.test_frames,
        ])

        writer.writerow([
            "Validation Frames",
            stats.val_frames,
        ])

        writer.writerow([
            "Skipped Frames",
            stats.skipped_frames,
        ])

        writer.writerow([
            "Failed Frames",
            stats.failed_frames,
        ])

        writer.writerow([])

        writer.writerow([
            "Generated",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ])

    logger.info("Report generated successfully.")

    return report


# =============================================================================
# Future
# =============================================================================

def generate_json(*args, **kwargs):
    """
    Reserved for future implementation.
    """
    raise NotImplementedError()


def generate_excel(*args, **kwargs):
    """
    Reserved for future implementation.
    """
    raise NotImplementedError()