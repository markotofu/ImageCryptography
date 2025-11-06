# ImageCryptography Project Guide

## Overview
A Python project that converts text into images and decrypts images back to text using a custom character-to-RGB mapping system.

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd ImageCryptography
   ```

2. **Create a virtual environment (recommended):**
   ```sh
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - **Windows PowerShell:**
     ```powershell
     . .\.venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux:**
     ```sh
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

5. **Run the code:**
   ```sh
   python MainCode/main.py
   ```

## Features
- Convert text to an image using character-to-RGB encoding
- Decrypt images back to text using the same mapping
- Supports lowercase letters (a-z), digits (0-9), basic punctuation (.,!? ), space, and newline

## Usage Guide

### Running the Program
When you run `main.py`, you'll see a menu:
- **Option 1:** Text to Image Generation
- **Option 2:** Image Decryption

### Text to Image Mode
1. Select option `1`
2. Choose input method:
   - `1` for direct text input
   - `2` to read from `MainCode/testText` file
3. The program generates `output_image.png` in the project root

### Image to Text Mode
1. Select option `2`
2. The program reads `output_image.png` and prints the decrypted text

## How It Works
- Each pixel in the image encodes up to 3 characters
- Characters are mapped to indices in the `numToLetter` array
- Indices are stored directly as RGB values (0-255)
- Image dimensions: width = (text_length / 3), height = 1 pixel

## Limitations
- **Character set:** Only supports characters in the `numToLetter` list:
  - Lowercase letters: a-z
  - Digits: 0-9
  - Punctuation: . , ! ? (space and newline)
- **Unsupported characters:** Any character not in the list (uppercase letters, special symbols, etc.) will be replaced with `'a'`
- **Maximum characters per color channel:** 255 (current alphabet size is 42, so plenty of room)
- **Image format:** Single-row PNG image; width depends on text length

## Troubleshooting
- **Unexpected characters in output?** Your input contains unsupported characters (e.g., uppercase, symbols). They are converted to `'a'`.
- **Import errors?** Run `pip install -r requirements.txt` in your activated virtual environment.
- **File not found?** Ensure you're running from the project root directory.

## Customization
- **Add more characters:** Update the `numToLetter` list in both `encryption.py` and `decryption.py`
- **Change input file:** Modify the `file_path` variable in `main.py`
- **Change output filename:** Update the filename in `encryption.py`'s `img.save()` call

## Project Structure
```
ImageCryptography/
├── MainCode/
│   ├── main.py          # Main program entry point
│   ├── encryption.py    # Text-to-image conversion
│   ├── decryption.py    # Image-to-text conversion
│   └── testText         # Sample text file for testing
├── .venv/               # Virtual environment (not in git)
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Notes
- **Python version:** Tested on Python 3.14
- **Git:** Do NOT commit `.venv` to git (it's in `.gitignore`)
- **Dependencies:** If you add new packages, run `pip freeze > requirements.txt`
- **Beginner project:** This is a learning project; bugs and improvements are expected!

## Future Improvements
- Add support for all ASCII/Unicode characters
- Implement compression for large texts
- Add GUI for easier interaction
- Support multi-row images for better aspect ratios
- Add encryption/password protection 




## How it works
    - Main

## Encryption

# Decryption