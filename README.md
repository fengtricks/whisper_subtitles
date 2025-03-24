# Video Subtitle Generator

A command-line tool that automatically transcribes videos and generates subtitles using OpenAI's Whisper. It can transcribe audio in various languages and translate it to English.

## Prerequisites

- Python 3.7 or higher
- FFmpeg installed on your system
- `uv` package installer (recommended) or `pip`

### Installing FFmpeg

- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`

### Installing uv (Recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

1. Clone this repository or download the files
2. Create and activate a virtual environment:
```bash
# Create virtual environment

uv venv 

# Or

python -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

3. Install dependencies using uv (recommended) or pip:
```bash
# Using uv (faster)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python main.py input_video.mp4
```

Options:
```bash
python main.py input_video.mp4 [options]

Options:
  -o, --output OUTPUT    Path to the output video file (default: input_video_with_subs.mp4)
  -m, --model MODEL     Whisper model size: small, medium, large (default: medium)
  -l, --language LANG   Source language code (optional, will auto-detect if not specified)
  -t, --temp-dir DIR    Directory for temporary files (default: temp)
```

Examples:
```bash
# Specify output file
python main.py input_video.mp4 -o output.mp4

# Use a larger model for better accuracy
python main.py input_video.mp4 -m large

# Process French audio
python main.py input_video.mp4 -l fr

# Specify custom temp directory
python main.py input_video.mp4 -t /path/to/temp
```

## Models

Available Whisper models:
- `small`: Good balance of speed and accuracy
- `medium`: Better accuracy, slower 
- `large`: Best accuracy, slowest 

