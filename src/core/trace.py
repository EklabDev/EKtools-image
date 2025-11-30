"""Tracing binary masks to SVG paths using Potrace or marching squares."""

import os
import re
import subprocess
import tempfile
from typing import List, Optional

try:  # pragma: no cover - handled at runtime
    from skimage import measure  # type: ignore[import-not-found]
except ImportError as exc:  # pragma: no cover
    measure = None  # type: ignore[assignment]
    _MEASURE_IMPORT_ERROR = exc
else:
    _MEASURE_IMPORT_ERROR = None

import numpy as np


def trace_mask_potrace(mask: np.ndarray) -> Optional[List[str]]:
    """
    Trace a binary mask to SVG path using Potrace.

    Args:
        mask: Binary mask (0 or 255)

    Returns:
        SVG path string or None if Potrace is not available
    """
    try:
        # Create temporary PBM file
        with tempfile.NamedTemporaryFile(suffix=".pbm", delete=False) as tmp_pbm:
            pbm_path = tmp_pbm.name
            # Write PBM format
            height, width = mask.shape
            with open(pbm_path, "wb") as f:
                f.write(f"P4\n{width} {height}\n".encode())
                # Convert mask to PBM format (1 bit per pixel)
                # PBM P4 format: packed binary
                for y in range(height):
                    row = mask[y]
                    byte_row = bytearray()
                    for x in range(0, width, 8):
                        byte_val = 0
                        for bit in range(8):
                            if x + bit < width:
                                # Potrace treats bits set to 1 as foreground (black)
                                if row[x + bit] > 0:
                                    byte_val |= 1 << (7 - bit)
                        byte_row.append(byte_val)
                    f.write(bytes(byte_row))

        # Create temporary SVG file
        with tempfile.NamedTemporaryFile(
            suffix=".svg", delete=False, mode="w"
        ) as tmp_svg:
            svg_path = tmp_svg.name

        # Run Potrace
        try:
            subprocess.run(
                ["potrace", "-s", "-o", svg_path, pbm_path],
                check=True,
                capture_output=True,
                timeout=30,
            )

            # Read SVG content
            with open(svg_path, "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Extract all <path> elements
            paths = re.findall(r'<path[^>]*d="([^"]+)"', svg_content)
            return paths or None

        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            # Potrace not available or failed
            return None
        finally:
            # Cleanup
            if os.path.exists(pbm_path):
                os.unlink(pbm_path)
            if os.path.exists(svg_path):
                os.unlink(svg_path)

    except (OSError, ValueError, RuntimeError):
        return None


def trace_mask_marching_squares(
    mask: np.ndarray, tolerance: float = 1.25, level: float = 0.5
) -> List[str]:
    """
    Trace a binary mask to SVG path using marching squares algorithm.

    This is a Python implementation that doesn't require Potrace.

    Args:
        mask: Binary mask (0 or 255)

    Returns:
        SVG path string
    """
    if measure is None:
        raise RuntimeError(
            "scikit-image is required for marching squares tracing"
        ) from _MEASURE_IMPORT_ERROR

    # Normalize mask to [0, 1] floats for skimage
    normalized = (mask.astype(np.float32) / 255.0).clip(0.0, 1.0)

    contours = measure.find_contours(normalized, level=level)

    paths: List[str] = []
    for contour in contours:
        if contour.shape[0] < 2:
            continue

        if tolerance > 0:
            contour = measure.approximate_polygon(contour, tolerance)
            if contour.shape[0] < 3:
                continue

        # Skimage returns points as (row, col); convert to (x, y)
        points = contour[:, ::-1]
        commands = []
        x0, y0 = points[0]
        commands.append(f"M {x0:.2f} {y0:.2f}")
        for x, y in points[1:]:
            commands.append(f"L {x:.2f} {y:.2f}")
        commands.append("Z")
        paths.append(" ".join(commands))

    return paths


def trace_mask(mask: np.ndarray, prefer_potrace: bool = True) -> List[str]:
    """
    Trace a binary mask to SVG path.

    Tries Potrace first if available, falls back to marching squares.

    Args:
        mask: Binary mask (0 or 255)
        prefer_potrace: Whether to try Potrace first

    Returns:
        SVG path string
    """
    if prefer_potrace:
        paths = trace_mask_potrace(mask)
        if paths:
            return paths

    # Fallback to marching squares
    return trace_mask_marching_squares(mask)
