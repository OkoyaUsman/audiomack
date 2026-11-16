# Audiomack Music Downloader

A Python command-line tool to download music from Audiomack using simple HTTP requests. This script authenticates with the Audiomack API and downloads high-quality audio files to your local machine.

## Features

- 🎵 Download music from Audiomack
- 🔐 OAuth 1.0 authentication with HMAC-SHA1 signature
- ✅ URL validation to ensure only valid Audiomack URLs are processed
- 📁 Automatic file organization in a `downloads` directory
- 🎧 High-quality audio downloads (HQ enabled)
- 🚀 Simple command-line interface

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/OkoyaUsman/audiomack.git
cd audiomack
```

2. Navigate to the project directory:
```bash
cd audiomack
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install requests
```

## Usage

Run the script with an Audiomack URL set inside main.py:

```bash
python main.py
```


### Output

The downloaded audio file will be saved in the `downloads` directory with a filename based on the song path. For example:
- URL: `https://audiomack.com/artist/song-name`
- Output: `downloads/artist_song-name.m4a` (or appropriate extension)

## How It Works

1. **OAuth Authentication**: 
   - Generates a random nonce for each request
   - Creates an OAuth timestamp
   - Builds OAuth parameters including consumer key, signature method, and version
   - Generates an HMAC-SHA1 signature using the consumer secret

3. **API Request**: 
   - Sends an authenticated GET request to the Audiomack API
   - Receives a signed URL for the audio file

4. **Download**: 
   - Downloads the audio file from the signed URL
   - Saves it to the `downloads` directory with an appropriate filename and extension

## Project Structure

```
audiomack/
├── main.py              # Main script file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── downloads/          # Directory where downloaded files are saved (created automatically)
```

## Code Overview

### Main Functions

- `main()`: Entry point that handles argument parsing, API authentication, and file download
- `generate_nonce(length: int)`: Generates a random nonce for OAuth authentication
- `generate_signature(params: dict)`: Creates HMAC-SHA1 OAuth signature from parameters

### Key Components

- **OAuth 1.0 Authentication**: Implements the OAuth 1.0 protocol with HMAC-SHA1 signature method
- **URL Parsing**: Uses `urllib.parse` to extract and validate URL components
- **File Handling**: Uses `pathlib.Path` for cross-platform file path management


## Requirements

- `requests`: For making HTTP requests to the Audiomack API

All other dependencies (os, hmac, time, base64, random, string, hashlib, argparse, urllib.parse, pathlib) are part of Python's standard library.

## Notes

- The script uses a hardcoded consumer secret for OAuth authentication
- Downloads are saved in high quality (HQ) format
- The `downloads` directory is created automatically if it doesn't exist
- File extensions are automatically detected from the API response

## License

This project is provided as-is for educational purposes. Please respect Audiomack's terms of service and copyright policies when using this tool.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational purposes only. Users are responsible for ensuring they have the right to download content from Audiomack and must comply with all applicable laws and terms of service.