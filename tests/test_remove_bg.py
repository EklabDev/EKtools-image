"""
Tests for /remove-background endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from PIL import Image
import io

from src.main import app

client = TestClient(app)


def create_test_image(format: str = "PNG") -> bytes:
    """Create a simple test image."""
    img = Image.new("RGB", (100, 100), color="red")
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    return buffer.getvalue()


def test_remove_background_png_success():
    """Test successful background removal with PNG."""
    png_bytes = create_test_image("PNG")
    
    response = client.post(
        "/remove-background",
        files={"file": ("test.png", png_bytes, "image/png")}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Check that response is PNG bytes
    assert len(response.content) > 0
    # PNG files start with PNG signature
    assert response.content[:8] == b"\x89PNG\r\n\x1a\n"
    
    # Verify it's a valid PNG with alpha channel
    result_img = Image.open(io.BytesIO(response.content))
    assert result_img.mode in ["RGBA", "LA", "P"]  # Should have alpha


def test_remove_background_jpeg_success():
    """Test successful background removal with JPEG."""
    jpeg_bytes = create_test_image("JPEG")
    
    response = client.post(
        "/remove-background",
        files={"file": ("test.jpg", jpeg_bytes, "image/jpeg")}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Check that response is PNG bytes (always returns PNG)
    assert len(response.content) > 0
    assert response.content[:8] == b"\x89PNG\r\n\x1a\n"


def test_remove_background_invalid_file_type():
    """Test rejection of invalid file types."""
    # Create a fake SVG
    fake_svg = b"<svg></svg>"
    
    response = client.post(
        "/remove-background",
        files={"file": ("test.svg", fake_svg, "image/svg+xml")}
    )
    
    assert response.status_code == 400


def test_remove_background_missing_file():
    """Test rejection when file is missing."""
    response = client.post("/remove-background")
    
    assert response.status_code == 422  # FastAPI validation error

