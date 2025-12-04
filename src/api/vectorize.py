"""
POST /vectorize endpoint: Convert PNG to SVG with color quantization.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import Response
import math
import re
from typing import List, Tuple
import numpy as np

from src.core.limiter import limiter
from src.utils.validators import validate_png_file, validate_file_size
from src.utils.image_io import load_image_from_bytes
from src.core.quantize import quantize_colors, get_color_masks
from src.core.trace import trace_mask
from src.core.svg_builder import build_svg

router = APIRouter()


@router.post("", response_class=Response)
@limiter.limit("100/minute")
async def vectorize(
    request: Request, file: UploadFile = File(...), colors: int = Form(...)
):
    """
    Vectorize a PNG image into an SVG with configurable color quantization.

    Args:
        file: PNG image file
        colors: Number of colors (2-20)

    Returns:
        SVG content as text/plain
    """
    # Validate file type
    validate_png_file(file)

    # Validate colors parameter
    if colors < 2 or colors > 20:
        raise HTTPException(
            status_code=400, detail="colors parameter must be between 2 and 20"
        )

    # Read file content
    file_content = await file.read()

    # Validate file size (100 MB)
    file_size = len(file_content)
    validate_file_size(file_size, 100)

    try:
        # Load image
        opencv_image, pil_image = load_image_from_bytes(file_content)

        # Get image dimensions
        width, height = pil_image.size

        # Quantize colors
        _, label_image, color_list = quantize_colors(opencv_image, colors)

        # Get masks for each color
        masks = get_color_masks(label_image, colors)

        total_pixels = width * height
        cluster_data = []
        for i, mask in enumerate(masks):
            area = int(np.count_nonzero(mask))
            brightness = sum(color_list[i]) / (3 * 255)
            cluster_data.append(
                {
                    "index": i,
                    "mask": mask,
                    "color": color_list[i],
                    "area": area,
                    "is_background": (area / total_pixels) >= 0.4 and brightness >= 0.9,
                }
            )

        # Sort largest areas first so backgrounds are drawn before details
        cluster_data.sort(key=lambda item: item["area"], reverse=True)

        render_clusters = [c for c in cluster_data if not c["is_background"]]
        if not render_clusters:
            render_clusters = cluster_data

        # Trace each mask to SVG paths
        paths = []
        for cluster in render_clusters:
            path_list = trace_mask(cluster["mask"], prefer_potrace=True)

            for path_str in path_list:
                if path_str:
                    paths.append((path_str, cluster["color"]))

        scale_factor = _determine_scale_factor(paths, width, height)

        # Build SVG
        svg_content = build_svg(width, height, paths, scale_factor=scale_factor)

        # Return SVG as text/plain
        return Response(
            content=svg_content,
            media_type="text/plain",
            headers={"Content-Disposition": "attachment; filename=vectorized.svg"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing image: {str(e)}"
        ) from e


def _determine_scale_factor(
    paths: List[Tuple[str, Tuple[int, int, int]]], width: int, height: int
) -> float:
    """
    Infer a scale factor for the SVG viewport based on path coordinates.
    """
    if not paths:
        return 1.0

    number_pattern = re.compile(r"-?\d+(?:\.\d+)?")
    max_coord = 0.0
    for path_str, _ in paths:
        for match in number_pattern.findall(path_str):
            try:
                value = abs(float(match))
            except ValueError:
                continue
            max_coord = max(max_coord, value)

    expected = max(width, height, 1)
    ratio = max_coord / expected
    if ratio <= 1.2:
        return 1.0

    return 10.0
