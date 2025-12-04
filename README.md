# EK Tools Image Backend

A FastAPI backend service for image processing operations: vectorization, rasterization, and background removal.

## Features

- **POST /vectorize**: Convert PNG images to SVG with configurable color quantization (2-20 colors)
- **POST /rasterize**: Convert SVG files to PNG images
- **POST /remove-background**: Remove background from JPEG or PNG images

## Requirements

- Python 3.13+
- `uv` package manager
- Potrace (optional, for better vectorization quality)

## Installation

### 1. Install uv

If you don't have `uv` installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on macOS with Homebrew:

```bash
brew install uv
```

### 2. Install Dependencies

```bash
uv sync
```

This will install all project dependencies including dev dependencies.

### 3. Install Potrace (Optional but Recommended)

For better vectorization quality, install Potrace:

**macOS:**
```bash
brew install potrace
```

**Ubuntu/Debian:**
```bash
sudo apt-get install potrace
```

**Note:** If Potrace is not available, the service will fall back to a Python-based marching squares algorithm.

## Running the Service

### Development Mode

```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**Note:** Make sure to run these commands from the project root directory. The `src` directory will be automatically added to the Python path when using `uvicorn src.main:app`.

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. POST /vectorize

Vectorizes a PNG image into an SVG with configurable color quantization.

**Rate Limit:** 100 requests per minute.

**Request:**
- `multipart/form-data`
  - `file`: PNG image file (required)
  - `colors`: Integer between 2 and 20 (required)

**Response:**
- `200 OK`: SVG content as `text/plain`
- `400 Bad Request`: Invalid file type, size, or colors parameter
- `429 Too Many Requests`: Rate limit exceeded

**Example:**
```bash
curl -X POST "http://localhost:8000/vectorize" \
  -F "file=@image.png" \
  -F "colors=5" \
  -o output.svg
```

### 2. POST /rasterize

Converts an SVG file to PNG.

**Rate Limit:** 100 requests per minute.

**Request:**
- `multipart/form-data`
  - `file`: SVG file (required)

**Response:**
- `200 OK`: PNG image as `image/png`
- `400 Bad Request`: Invalid file type or size
- `429 Too Many Requests`: Rate limit exceeded

**Example:**
```bash
curl -X POST "http://localhost:8000/rasterize" \
  -F "file=@image.svg" \
  -o output.png
```

### 3. POST /remove-background

Removes background from a JPEG or PNG image.

**Rate Limit:** 100 requests per minute.

**Request:**
- `multipart/form-data`
  - `file`: JPEG or PNG image file (required)

**Response:**
- `200 OK`: PNG image with alpha channel as `image/png`
- `400 Bad Request`: Invalid file type
- `429 Too Many Requests`: Rate limit exceeded

**Example:**
```bash
curl -X POST "http://localhost:8000/remove-background" \
  -F "file=@image.jpg" \
  -o no_background.png
```

## Testing

Run tests with pytest:

```bash
uv run pytest
```

Run tests with verbose output:

```bash
uv run pytest -v
```

## Project Structure

```
project/
├── pyproject.toml          # Project configuration and dependencies
├── README.md              # This file
├── src/
│   ├── main.py            # FastAPI application entry point
│   ├── api/
│   │   ├── vectorize.py   # /vectorize endpoint
│   │   ├── rasterize.py   # /rasterize endpoint
│   │   └── remove_bg.py   # /remove-background endpoint
│   ├── core/
│   │   ├── quantize.py    # K-means color quantization
│   │   ├── trace.py       # Mask to SVG path tracing
│   │   ├── svg_builder.py # SVG document builder
│   │   ├── rasterizer.py  # SVG to PNG conversion
│   │   ├── background.py  # Background removal algorithms
│   │   └── limiter.py     # Rate limiter instance
│   └── utils/
│       ├── validators.py   # File validation utilities
│       ├── image_io.py     # Image loading/saving utilities
│       └── mask_ops.py    # Mask operations
└── tests/
    ├── test_vectorize.py
    ├── test_rasterize.py
    └── test_remove_bg.py
```

## Implementation Details

### Vectorization Pipeline

1. Validates PNG file type and size (max 100 MB)
2. Validates colors parameter (2-20)
3. Loads image using OpenCV and PIL
4. Performs K-means color quantization
5. Generates binary masks for each color cluster
6. Traces each mask to SVG paths (using Potrace if available, otherwise marching squares)
7. Builds multi-layer SVG document
8. Returns SVG as text/plain

### Rasterization Pipeline

1. Validates SVG file type and size (max 10 MB)
2. Converts SVG to PNG using CairoSVG
3. Returns PNG as image/png

### Background Removal Pipeline

1. Validates image file type (PNG or JPEG)
2. Loads image
3. Performs K-means color segmentation (3 clusters)
4. Identifies largest cluster as background
5. Creates mask and applies morphological operations
6. Outputs PNG with alpha channel
7. Returns PNG as image/png

## Limitations

- Vectorization: Only accepts PNG files
- Rasterization: Only accepts SVG files
- Background removal: Works best with images that have clear foreground/background separation
- File size limits: 100 MB for vectorization, 10 MB for rasterization

## License

This project is provided as-is for development purposes.
