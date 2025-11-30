"""
Tests for /rasterize endpoint.
"""
import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def create_test_svg() -> bytes:
    """Create a simple test SVG."""
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <rect x="10" y="10" width="80" height="80" fill="red"/>
</svg>"""
    return svg_content.encode("utf-8")


def test_rasterize_success():
    """Test successful rasterization."""
    svg_bytes = create_test_svg()
    
    response = client.post(
        "/rasterize",
        files={"file": ("test.svg", svg_bytes, "image/svg+xml")}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Check that response is PNG bytes
    assert len(response.content) > 0
    # PNG files start with PNG signature
    assert response.content[:8] == b"\x89PNG\r\n\x1a\n"


def test_rasterize_invalid_file_type():
    """Test rejection of non-SVG files."""
    # Create a fake PNG
    fake_png = b"\x89PNG\r\n\x1a\n" + b"fake" * 100
    
    response = client.post(
        "/rasterize",
        files={"file": ("test.png", fake_png, "image/png")}
    )
    
    assert response.status_code == 400


def test_rasterize_missing_file():
    """Test rejection when file is missing."""
    response = client.post("/rasterize")
    
    assert response.status_code == 422  # FastAPI validation error


def test_rasterize_invalid_svg():
    """Test handling of invalid SVG content."""
    invalid_svg = b"<not>a valid svg</not>"
    
    response = client.post(
        "/rasterize",
        files={"file": ("test.svg", invalid_svg, "image/svg+xml")}
    )
    
    # Should either succeed (if CairoSVG is lenient) or return 500
    assert response.status_code in [200, 500]

