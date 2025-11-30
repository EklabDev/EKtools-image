"""
Tests for /vectorize endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from PIL import Image
import io

from src.main import app

client = TestClient(app)


def create_test_png(width: int = 100, height: int = 100) -> bytes:
    """Create a simple test PNG image."""
    img = Image.new("RGB", (width, height), color="red")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


def test_vectorize_success():
    """Test successful vectorization."""
    png_bytes = create_test_png(50, 50)
    
    response = client.post(
        "/vectorize",
        files={"file": ("test.png", png_bytes, "image/png")},
        data={"colors": "5"}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    
    # Check that response contains SVG
    svg_content = response.text
    assert "<svg" in svg_content.lower()
    assert "xmlns" in svg_content.lower()
    assert "viewBox" in svg_content.lower()


def test_vectorize_invalid_file_type():
    """Test rejection of non-PNG files."""
    # Create a fake JPEG
    img = Image.new("RGB", (50, 50), color="blue")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    jpeg_bytes = buffer.getvalue()
    
    response = client.post(
        "/vectorize",
        files={"file": ("test.jpg", jpeg_bytes, "image/jpeg")},
        data={"colors": "5"}
    )
    
    assert response.status_code == 400


def test_vectorize_invalid_colors():
    """Test rejection of invalid colors parameter."""
    png_bytes = create_test_png()
    
    # Test colors < 2
    response = client.post(
        "/vectorize",
        files={"file": ("test.png", png_bytes, "image/png")},
        data={"colors": "1"}
    )
    assert response.status_code == 400
    
    # Test colors > 20
    response = client.post(
        "/vectorize",
        files={"file": ("test.png", png_bytes, "image/png")},
        data={"colors": "21"}
    )
    assert response.status_code == 400


def test_vectorize_missing_file():
    """Test rejection when file is missing."""
    response = client.post(
        "/vectorize",
        data={"colors": "5"}
    )
    
    assert response.status_code == 422  # FastAPI validation error


def test_vectorize_missing_colors():
    """Test rejection when colors parameter is missing."""
    png_bytes = create_test_png()
    
    response = client.post(
        "/vectorize",
        files={"file": ("test.png", png_bytes, "image/png")}
    )
    
    assert response.status_code == 422  # FastAPI validation error

