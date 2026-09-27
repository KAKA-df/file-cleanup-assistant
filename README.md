# File Cleanup Assistant

A small Python tool that scans folders and helps you find and clean up unnecessary files.

## Features

- Recursively scans folders
- Detects large and old files
- Lets you choose size and age thresholds
- Displays human-readable file sizes
- Detects duplicate files using SHA-256 hashes
- Sorts flagged files by size
- Shows a cleanup summary
- Lets you select multiple files for cleanup
- Moves selected files to the Recycle Bin instead of permanently deleting them

## Requirements

- Python 3
- `Send2Trash`
```bash
python -m pip install -r requirements.txt
```
## Installation and Usage

Clone the repository:

```bash
git clone https://github.com/KAKA-df/file-cleanup-assistant.git
cd file-cleanup-assistant
python cleanup.py
```
