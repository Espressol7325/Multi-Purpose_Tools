# Multi-Purpose_Tools
Some tools that help with personal uses

This repository contains a collection of Python scripts for various personal utility tasks, including downloading media, compressing files, and performing OCR on clipboard images.

## Tools Included

1.  [Media Downloader](#media-downloader)
2.  [Media Compressor](#media-compressor)
3.  [Clipboard OCR](#clipboard-ocr)

---

## Media Downloader

A command-line tool ([mediaDownloader.py](mediaDownloader.py)) to download video and audio from various websites using `yt_dlp`.

### Features
- Download the best quality video or audio.
- List all available formats for a given URL.
- Download a specific format by its ID.
- Saves files to the `Media_Downloader/` directory with a timestamp.

### Usage
Run the script from your terminal and follow the on-screen prompts.
```sh
python mediaDownloader.py
```

### Dependencies
- `yt-dlp`

Install dependencies using pip:
```sh
pip install yt-dlp
```

---

## Media Compressor

A GUI application ([mediaCompressor.py](mediaCompressor.py)) for compressing image and video files to reduce their size.

### Features
- Simple graphical user interface built with Tkinter and ttkbootstrap.
- Supports common image formats (JPG, PNG) and video formats (MP4, AVI, MKV).
- Adjustable compression levels (low, medium, high).
- Shows original file size and compression progress.

### Usage
Run the script to launch the GUI:
```sh
python mediaCompressor.py
```

### Dependencies
- `ttkbootstrap`
- `Pillow`
- **FFmpeg**: Must be installed and accessible in your system's PATH for video compression.

Install Python dependencies using pip:
```sh
pip install ttkbootstrap Pillow
```

---

## Clipboard OCR

A Jupyter Notebook ([JPOCR.ipynb](JPOCR.ipynb)) to perform Optical Character Recognition (OCR) on an image copied to the clipboard. It's configured for extracting Japanese and English text.

### Features
- Extracts text directly from a clipboard image.
- Provides two OCR engine options:
    - `easyocr`: A user-friendly OCR library.
    - `pytesseract`: A wrapper for Google's Tesseract-OCR Engine.

### Usage
1. Open [JPOCR.ipynb](JPOCR.ipynb) in a Jupyter environment.
2. Copy an image containing text to your clipboard.
3. Run the cells in the notebook to extract and print the text.

### Dependencies
- `easyocr`
- `pytesseract`
- `Pillow`
- **Tesseract-OCR Engine**: For the `pytesseract` option, you need to install Tesseract OCR and the required language data (e.g., `jpn`, `eng`).

Install Python dependencies using pip:
```sh
pip install easyocr pytesseract Pillow opencv
```
