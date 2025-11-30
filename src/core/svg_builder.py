"""SVG builder for creating multi-layer SVG files."""

from typing import List, Tuple


def build_svg(
    width: int,
    height: int,
    paths: List[Tuple[str, Tuple[int, int, int]]],
    scale_factor: float = 1.0,
) -> str:
    """
    Build a complete SVG document from paths and colors.

    Args:
        width: Image width
        height: Image height
        paths: List of (path_string, rgb_color) tuples
        scale_factor: Multiplier for width/height/viewBox to match path coordinates

    Returns:
        Complete SVG document as string
    """
    scaled_width = max(int(round(width * scale_factor)), 1)
    scaled_height = max(int(round(height * scale_factor)), 1)

    svg_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg"',
        f'     width="{width}" height="{height}"',
        f'     viewBox="0 0 {scaled_width} {scaled_height}">',
    ]

    # Add each path as a group with its color
    for path_str, rgb_color in paths:
        if not path_str:  # Skip empty paths
            continue

        r, g, b = rgb_color
        svg_parts.append(
            f'  <g fill="rgb({r},{g},{b})" stroke="rgb({r},{g},{b})" stroke-width="0">'
        )
        svg_parts.append(f'    <path d="{path_str}"/>')
        svg_parts.append("  </g>")

    svg_parts.append("</svg>")

    return "\n".join(svg_parts)
