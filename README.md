# Video Frame Extractor

A modern Python desktop application for extracting frames from videos and automatically organizing them into **Train**, **Test**, and **Validation** datasets for computer vision projects such as **YOLO**, **TensorFlow**, **PyTorch**, and **EthicEye**.

---

## Features

* Modern desktop GUI built with **Tkinter**
* Process one or multiple videos
* Select any output folder (no files are saved to the C: drive unless you choose it)
* Automatic creation of:

  ```
  train/
  test/
  val/
  ```
* Extract frames at a user-defined FPS
* Configurable Train/Test/Validation split (e.g., 70:15:15)
* Random frame distribution to reduce dataset bias
* Live progress bar
* Live processing statistics
* Processing log
* CSV dataset report
* Automatically remembers:

  * Output folder
  * FPS
  * Dataset split ratios
  * Last opened video folder
* Responsive GUI (background processing)
* Compatible with Windows, Linux, and macOS

---

## Project Structure

```
VideoFrameExtractor/
│
├── app.py
├── gui.py
├── extractor.py
├── config.py
├── utils.py
│
├── config.json          # Auto-created
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets/
│     └── icon.ico
│
└── output/
      ├── train/
      ├── test/
      └── val/
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/<YOUR_USERNAME>/VideoFrameExtractor.git
cd VideoFrameExtractor
```

---

### Create a Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python app.py
```

---

## How It Works

1. Launch the application.
2. Add one or more video files.
3. Choose an output folder.
4. Enter the desired extraction FPS.
5. Configure the Train/Test/Validation ratio.
6. Click **Start Processing**.

The application will automatically:

* Extract frames from each video.
* Randomly distribute frames according to the specified ratios.
* Save the frames into:

  ```
  train/
  test/
  val/
  ```
* Generate a processing log.
* Generate a CSV report.

---

## Example Output

```
Dataset/

├── train/
│      frm_0001_camera01_000001.png
│      frm_0001_camera01_000002.png
│
├── test/
│      frm_0001_camera01_000350.png
│
├── val/
│      frm_0001_camera01_000520.png
│
├── dataset_report.csv
└── processing_log.txt
```

---

## Frame Naming Convention

```
frm_<video_sequence>_<video_name>_<frame_number>.png
```

Example:

```
frm_0001_camera01_000001.png
frm_0001_camera01_000002.png
frm_0002_highway05_000001.png
```

This naming convention helps identify the source video of every extracted frame.

---

## Saved Configuration

The application automatically creates a `config.json` file to remember your settings.

Example:

```json
{
    "output_folder": "D:\\YOLO_Dataset",
    "fps": 5,
    "train_ratio": 70,
    "test_ratio": 15,
    "val_ratio": 15,
    "last_video_folder": "D:\\Videos"
}
```

---

## Dataset Report

After processing, a CSV report is generated.

Example:

```
Video,Frames,Train,Test,Val

camera01.mp4,4215,2950,632,633
camera02.mp4,3560,2492,534,534
```

---

## Requirements

* Python 3.10 or newer
* OpenCV
* Pillow
* Tkinter (included with Python)

---

## Future Enhancements

* Drag-and-drop video support
* Folder processing
* Pause/Resume processing
* Cancel processing
* ETA estimation
* Dark mode
* Live frame preview
* Export statistics to Excel
* Multi-threaded processing
* Build as a standalone Windows executable

---

## License

This project is released under the MIT License.

---

## Contributing

Contributions, feature requests, bug reports, and suggestions are welcome.

If you discover a bug or have an idea for improvement, please open an issue or submit a pull request.

---

## Acknowledgements

This project was developed to simplify the preparation of image datasets for computer vision applications, including object detection and surveillance projects such as **EthicEye**.
