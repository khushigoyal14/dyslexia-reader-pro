# Dyslexia Assistive Reader Pro

A desktop accessibility application built with Python and Tkinter designed to assist individuals with dyslexia by providing customizable typography tools, contrast-balanced visual themes, and an asynchronous text-to-speech tracking engine.

## Core Features
* **Asynchronous Audio Pipeline:** Utilizes Python's `threading` module to isolate text-to-speech processing loops on background worker threads, keeping the desktop graphical user interface completely fluid and responsive during continuous speech execution.
* **Real-Time Word Tracking:** Synchronizes visual highlight maps to the active spoken word block by calculating character-level position indices directly from native speech driver event callbacks.
* **Adjustable Speech Engine:** Integrated words-per-minute (WPM) calibration tools allowing users to dynamically modify playback rate parameters between 100 WPM and 300 WPM to match cognitive comfort.
* **Visual Accommodation Controls:** Real-time modification of text font families and scaling factors alongside a choice of research-backed pastel background palettes (Cream, Pastel Blue, Sage Green) to mitigate high-contrast visual strain.
* **Document Ingestion (OCR):** Integrates the Tesseract OCR engine architecture to cleanly parse, extract, and format text strings out of digital image files (.png, .jpg, .jpeg, .bmp).

## Tech Stack
* **Language:** Python 3
* **GUI Framework:** Tkinter
* **Speech Integration:** Pyttsx3
* **Image Processing & OCR:** PyTesseract, Pillow (PIL)
* **Version Control:** Git & GitHub

## Installation & Setup
1. Ensure the **Tesseract OCR Engine** binary is installed on your local operating system and configured correctly within the project's companion `config.py` script.
2. Install the necessary library requirements:
   ```bash
   pip install -r requirements.txt

## Application Walkthrough
* See the features of the application in action below:
https://github.com/user-attachments/assets/6dd4c8f7-91ed-437b-bbff-cc2547872162

