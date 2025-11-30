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
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="1600" height="1200"
     viewBox="0 0 1600 1200">
  <g fill="rgb(0,0,0)" stroke="rgb(0,0,0)" stroke-width="0">
    <path d="M0 6000 l0 -6000 8000 0 8000 0 0 6000 0 6000 -8000 0 -8000 0 0
-6000z m9720 5110 c791 -28 1117 -73 1520 -212 417 -144 723 -333 1024 -634
351 -351 573 -748 707 -1264 130 -499 149 -888 149 -3000 0 -2112 -19 -2501
-149 -3000 -134 -516 -356 -913 -707 -1264 -351 -351 -748 -573 -1264 -707
-500 -130 -887 -149 -3000 -149 -2113 0 -2500 19 -3000 149 -516 134 -913 356
-1264 707 -351 351 -573 748 -707 1264 -130 499 -149 888 -149 3000 0 2112 19
2501 149 3000 134 516 356 913 707 1264 301 301 607 490 1024 634 393 135 740
185 1475 211 330 12 3156 13 3485 1z"/>
  </g>
  <g fill="rgb(0,0,0)" stroke="rgb(0,0,0)" stroke-width="0">
    <path d="M6490 10189 c-923 -22 -1268 -76 -1647 -259 -182 -87 -287 -163 -449
-325 -208 -207 -328 -404 -423 -690 -144 -437 -171 -883 -171 -2915 0 -1747
22 -2302 106 -2680 56 -252 156 -495 281 -685 87 -130 309 -354 441 -443 181
-123 440 -230 692 -286 379 -84 927 -106 2680 -106 1753 0 2301 22 2680 106
252 56 511 163 692 286 132 89 354 313 441 443 125 190 225 433 281 685 84
378 106 933 106 2680 0 1747 -22 2302 -106 2680 -56 252 -156 495 -281 685
-87 130 -309 354 -441 443 -181 123 -440 230 -692 286 -385 85 -946 106 -2750
104 -624 -1 -1272 -5 -1440 -9z m4390 -861 c95 -22 209 -88 286 -165 120 -119
178 -264 177 -438 0 -171 -58 -311 -178 -431 -115 -115 -238 -171 -400 -181
-186 -11 -337 47 -471 181 -134 134 -192 285 -181 471 10 154 62 277 167 389
150 159 377 226 600 174z m-2585 -713 c784 -91 1462 -505 1900 -1160 581 -870
581 -2040 0 -2910 -180 -268 -400 -498 -655 -681 -916 -660 -2164 -660 -3080
0 -979 704 -1351 1989 -903 3116 355 893 1171 1518 2133 1634 157 19 446 19
605 1z"/>
  </g>
  <g fill="rgb(0,0,0)" stroke="rgb(0,0,0)" stroke-width="0">
    <path d="M7840 7698 c-730 -68 -1345 -612 -1504 -1328 -85 -387 -37 -779 140
-1133 269 -535 787 -883 1396 -937 404 -36 842 96 1173 355 381 297 612 726
655 1218 36 404 -96 840 -356 1173 -292 375 -724 610 -1204 653 -129 12 -165
12 -300 -1z"/>
  </g>
  <g fill="rgb(171,57,155)" stroke="rgb(171,57,155)" stroke-width="0">
    <path d="M6235 11109 c-735 -26 -1082 -76 -1475 -211 -417 -144 -723 -333
-1024 -634 -302 -303 -490 -607 -636 -1029 -138 -400 -182 -720 -210 -1515 -9
-260 -12 -2743 -3 -2641 5 51 29 83 45 60 7 -11 11 -11 15 -1 2 6 13 12 24 12
10 0 19 7 19 15 0 18 68 90 77 81 3 -3 -9 -19 -27 -36 -18 -17 -30 -33 -27
-36 3 -4 13 1 22 10 9 9 21 16 26 16 5 0 9 7 9 15 0 8 5 15 10 15 6 0 10 9 10
20 0 16 7 20 30 20 17 0 30 5 30 10 0 6 9 10 20 10 11 0 20 5 20 10 0 6 9 10
20 10 12 0 20 7 20 16 0 19 28 49 38 40 3 -4 0 -11 -8 -16 -8 -5 -11 -13 -6
-17 5 -4 11 -2 13 5 3 6 11 12 20 12 19 0 43 24 43 44 0 11 9 16 28 16 16 0
34 8 42 20 8 11 22 20 32 20 10 0 18 4 18 8 0 5 23 15 50 22 35 9 50 19 50 30
0 13 12 19 42 23 23 3 47 13 54 21 6 9 19 16 28 16 9 0 16 5 16 10 0 6 14 10
30 10 17 0 30 5 30 10 0 6 -4 10 -10 10 -5 0 -10 5 -10 10 0 6 9 10 19 10 11
0 21 6 24 13 2 7 8 8 13 3 5 -5 4 -11 -3 -13 -18 -6 -16 -23 2 -23 13 0 15 88
15 728 0 1083 20 1749 61 2072 49 385 155 696 326 955 87 130 309 354 441 443
181 123 440 230 692 286 378 84 933 106 2680 106 1747 0 2302 -22 2680 -106
252 -56 511 -163 692 -286 132 -89 354 -313 441 -443 125 -190 225 -433 281
-685 84 -378 106 -933 106 -2680 0 -1747 -22 -2302 -106 -2680 -56 -252 -156
-495 -281 -685 -49 -73 -110 -144 -226 -260 l-160 -160 2 -70 c1 -38 7 -71 12
-73 5 -2 9 -17 9 -33 0 -16 5 -29 10 -29 6 0 10 -16 10 -35 0 -19 5 -35 10
-35 6 0 10 -20 10 -45 0 -25 5 -45 10 -45 6 0 10 -22 10 -49 0 -27 4 -51 10
-53 5 -1 12 -46 16 -98 5 -62 12 -100 22 -109 10 -10 11 -16 3 -19 -14 -5 -15
-52 0 -52 6 0 8 -9 4 -20 -5 -14 -2 -20 9 -20 13 0 16 -14 16 -80 0 -79 0 -80
25 -80 30 0 102 39 239 128 278 182 564 468 748 748 243 369 402 840 462 1364
45 397 56 878 56 2490 0 2112 -19 2501 -149 3000 -134 516 -356 913 -707 1264
-301 301 -607 490 -1024 634 -403 139 -729 184 -1520 212 -329 12 -3155 11
-3485 -1z"/>
  </g>
  <g fill="rgb(171,57,155)" stroke="rgb(171,57,155)" stroke-width="0">
    <path d="M10630 9339 c-175 -27 -351 -147 -438 -300 -101 -179 -107 -402 -16
-589 51 -104 170 -223 274 -274 187 -91 409 -85 590 17 128 72 248 231 286
378 21 77 23 224 5 299 -41 175 -165 331 -322 407 -46 22 -104 46 -129 51 -72
17 -180 21 -250 11z"/>
  </g>
  <g fill="rgb(171,57,155)" stroke="rgb(171,57,155)" stroke-width="0">
    <path d="M7690 8614 c-811 -98 -1522 -556 -1944 -1253 -195 -321 -316 -680
-361 -1066 -14 -119 -19 -264 -8 -222 3 13 15 17 48 17 25 0 45 5 48 13 4 9 8
8 16 -3 9 -12 13 -12 19 -3 5 8 40 14 95 15 48 2 87 6 87 11 0 4 23 7 50 7 28
0 50 5 50 10 0 6 14 10 30 10 17 0 30 -3 30 -7 0 -5 63 -9 140 -10 81 -1 140
2 140 8 0 5 38 9 84 9 l85 0 6 48 c49 385 225 743 496 1012 353 348 852 533
1327 490 613 -54 1127 -402 1401 -947 132 -265 197 -595 171 -881 -21 -240
-75 -427 -191 -665 -32 -67 -59 -127 -59 -135 0 -19 73 -89 78 -74 6 18 22 15
22 -4 0 -17 36 -54 52 -54 4 0 8 -7 8 -15 0 -10 10 -15 30 -15 20 0 30 -5 30
-15 0 -27 127 -145 155 -145 16 0 25 -6 25 -15 0 -8 60 -76 134 -149 l135
-135 27 37 c15 20 33 42 40 47 19 16 116 179 166 280 422 841 360 1864 -157
2640 -438 655 -1116 1069 -1900 1160 -159 18 -448 18 -605 -1z"/>
  </g>
  <g fill="rgb(171,57,155)" stroke="rgb(171,57,155)" stroke-width="0">
    <path d="M5810 6120 c0 -5 5 -10 10 -10 6 0 10 5 10 10 0 6 -4 10 -10 10 -5 0
-10 -4 -10 -10z"/>
  </g>
  <g fill="rgb(171,57,155)" stroke="rgb(171,57,155)" stroke-width="0">
    <path d="M11550 1400 c0 -5 5 -10 10 -10 6 0 10 5 10 10 0 6 -4 10 -10 10 -5
0 -10 -4 -10 -10z"/>
  </g>
  <g fill="rgb(243,135,79)" stroke="rgb(243,135,79)" stroke-width="0">
    <path d="M5790 6140 c0 -5 -22 -10 -50 -10 -27 0 -50 -3 -50 -7 0 -5 -39 -9
-87 -11 -55 -1 -90 -7 -95 -15 -6 -9 -10 -9 -19 3 -8 11 -12 12 -16 3 -3 -8
-23 -13 -48 -13 -36 0 -44 -4 -49 -22 -11 -42 -6 -232 9 -363 95 -821 551
-1534 1254 -1959 828 -502 1894 -502 2722 0 239 144 449 322 628 529 92 106
210 265 198 265 -2 0 -18 -20 -36 -45 l-32 -44 -134 134 c-74 74 -135 142
-135 150 0 9 -9 15 -25 15 -28 0 -155 118 -155 145 0 10 -10 15 -30 15 -20 0
-30 5 -30 15 0 8 -4 15 -8 15 -16 0 -52 37 -52 54 0 19 -16 22 -22 4 -6 -17
-78 57 -78 79 0 10 7 27 15 37 8 11 15 25 15 30 0 6 -16 -16 -36 -49 -118
-196 -342 -419 -546 -544 -561 -342 -1235 -342 -1796 0 -381 233 -668 638
-766 1079 -31 144 -50 341 -41 443 l7 77 -86 0 c-47 0 -86 -4 -86 -9 0 -6 -59
-9 -140 -8 -77 1 -140 5 -140 10 0 4 -13 7 -30 7 -16 0 -30 -4 -30 -10z m40
-20 c0 -5 -4 -10 -10 -10 -5 0 -10 5 -10 10 0 6 5 10 10 10 6 0 10 -4 10 -10z"/>
  </g>
  <g fill="rgb(243,135,79)" stroke="rgb(243,135,79)" stroke-width="0">
    <path d="M3770 5640 c0 -5 -9 -10 -20 -10 -11 0 -20 -4 -20 -10 0 -5 5 -10 10
-10 6 0 10 -4 10 -10 0 -5 -13 -10 -30 -10 -16 0 -30 -4 -30 -10 0 -5 -7 -10
-16 -10 -9 0 -22 -7 -28 -16 -7 -8 -31 -18 -54 -21 -30 -4 -42 -10 -42 -23 0
-11 -15 -21 -50 -30 -27 -7 -50 -17 -50 -22 0 -4 -8 -8 -18 -8 -10 0 -24 -9
-32 -20 -8 -12 -26 -20 -42 -20 -19 0 -28 -5 -28 -16 0 -33 -53 -60 -62 -32
-6 17 -38 -14 -38 -36 0 -9 -8 -16 -20 -16 -11 0 -20 -4 -20 -10 0 -5 -9 -10
-20 -10 -11 0 -20 -4 -20 -10 0 -5 -13 -10 -30 -10 -23 0 -30 -4 -30 -20 0
-11 -4 -20 -10 -20 -5 0 -10 -7 -10 -15 0 -8 -4 -15 -9 -15 -5 0 -17 -7 -26
-16 -9 -9 -19 -14 -22 -10 -3 3 9 19 27 36 18 17 30 33 27 36 -9 9 -77 -63
-77 -81 0 -8 -9 -15 -19 -15 -11 0 -22 -6 -24 -12 -4 -10 -8 -10 -15 1 -9 12
-13 11 -28 -4 -16 -15 -18 -44 -22 -245 -7 -368 21 -1083 54 -1375 59 -526
218 -999 462 -1369 184 -280 468 -564 748 -748 369 -243 840 -402 1364 -462
398 -45 875 -56 2490 -56 1359 0 1756 6 2180 30 513 31 897 113 1275 275 141
60 186 84 158 85 -22 0 -23 4 -23 80 0 66 -3 80 -16 80 -11 0 -14 6 -9 20 4
11 2 20 -4 20 -15 0 -14 47 0 52 8 3 7 9 -3 19 -10 9 -17 47 -22 109 -4 52
-11 96 -16 98 -6 2 -10 26 -10 53 0 27 -4 49 -10 49 -5 0 -10 20 -10 45 0 25
-4 45 -10 45 -5 0 -10 16 -10 35 0 19 -4 35 -10 35 -5 0 -10 13 -10 29 0 16
-4 31 -9 33 -5 2 -11 35 -12 75 -2 65 0 74 22 93 13 12 -19 -9 -73 -45 -185
-125 -444 -233 -698 -289 -379 -84 -927 -106 -2680 -106 -1753 0 -2301 22
-2680 106 -252 56 -511 163 -692 286 -132 89 -354 313 -441 443 -171 259 -277
570 -326 955 -35 275 -60 982 -61 1683 0 293 -2 337 -15 337 -8 0 -15 5 -15
10 0 6 5 10 10 10 6 0 10 5 10 10 0 6 -4 10 -10 10 -5 0 -10 -4 -10 -10z
m-500 -300 c0 -5 -4 -10 -10 -10 -5 0 -10 5 -10 10 0 6 5 10 10 10 6 0 10 -4
10 -10z m8300 -3940 c0 -5 -4 -10 -10 -10 -5 0 -10 5 -10 10 0 6 5 10 10 10 6
0 10 -4 10 -10z"/>
  </g>
</svg>
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**Note:** Make sure to run these commands from the project root directory. The `src` directory will be automatically added to the Python path when using `uvicorn src.main:app`.

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. POST /vectorize

Vectorizes a PNG image into an SVG with configurable color quantization.

**Request:**
- `multipart/form-data`
  - `file`: PNG image file (required)
  - `colors`: Integer between 2 and 20 (required)

**Response:**
- `200 OK`: SVG content as `text/plain`
- `400 Bad Request`: Invalid file type, size, or colors parameter

**Example:**
```bash
curl -X POST "http://localhost:8000/vectorize" \
  -F "file=@image.png" \
  -F "colors=5" \
  -o output.svg
```

### 2. POST /rasterize

Converts an SVG file to PNG.

**Request:**
- `multipart/form-data`
  - `file`: SVG file (required)

**Response:**
- `200 OK`: PNG image as `image/png`
- `400 Bad Request`: Invalid file type or size

**Example:**
```bash
curl -X POST "http://localhost:8000/rasterize" \
  -F "file=@image.svg" \
  -o output.png
```

### 3. POST /remove-background

Removes background from a JPEG or PNG image.

**Request:**
- `multipart/form-data`
  - `file`: JPEG or PNG image file (required)

**Response:**
- `200 OK`: PNG image with alpha channel as `image/png`
- `400 Bad Request`: Invalid file type

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
│   │   └── background.py  # Background removal algorithms
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

