# Video Frame Extractor

Python project for extracting video frames and organizing them into train, test, and validation folders for computer-vision datasets.

## Current status

The repository contains frame extraction, video, and report service modules under `services/`, plus shared helpers under `core/`. The top-level `app.py` and `gui.py` files and modules in `gui/` are currently empty, so the documented desktop application cannot be launched from the repository as it stands. Treat the GUI workflow as intended direction, not a verified working application. No execution or test results are claimed.

## Intended workflow

The project is structured toward selecting videos and an output folder, extracting frames at a configured rate, distributing frames across train/test/validation splits, and producing a dataset report. Verify the complete workflow after the application entry point and GUI are implemented.

The current requirements list NumPy, OpenCV, and Pillow.

## Repository layout

- `services/frame_extractor.py`: frame extraction service
- `services/video_service.py`: video handling helpers
- `services/report_service.py`: report generation
- `core/`: shared constants, types, and utilities
- `gui/`: planned GUI modules; currently empty
- `app.py` and `gui.py`: currently empty entry-point files

Portfolio category: Personal project.
