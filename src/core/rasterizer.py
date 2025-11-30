"""
SVG to PNG rasterization using CairoSVG.
"""
import io
import cairosvg
from typing import Optional


def svg_to_png(svg_content: bytes, width: Optional[int] = None, height: Optional[int] = None) -> bytes:
    """
    Convert SVG content to PNG bytes.
    
    Args:
        svg_content: SVG file content as bytes
        width: Optional output width (if None, uses SVG's natural size)
        height: Optional output height (if None, uses SVG's natural size)
        
    Returns:
        PNG image bytes
    """
    # Convert SVG to PNG
    png_bytes = cairosvg.svg2png(
        bytestring=svg_content,
        output_width=width,
        output_height=height
    )
    
    return png_bytes

