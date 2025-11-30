"""
File validation utilities for image processing endpoints.
"""
import os
from typing import Optional
from fastapi import UploadFile, HTTPException


def validate_png_file(file: UploadFile) -> None:
    """
    Validate that the uploaded file is a PNG.
    
    Args:
        file: UploadFile object
        
    Raises:
        HTTPException: If file is not PNG or invalid
    """
    # Check content type
    if file.content_type not in ["image/png", "application/octet-stream"]:
        # Also check extension as fallback
        if not file.filename or not file.filename.lower().endswith(".png"):
            raise HTTPException(
                status_code=400,
                detail="File must be a PNG image. JPEG, GIF, WebP, SVG, and PDF are not accepted."
            )
    
    # Check extension
    if file.filename and not file.filename.lower().endswith(".png"):
        raise HTTPException(
            status_code=400,
            detail="File must have .png extension"
        )


def validate_svg_file(file: UploadFile) -> None:
    """
    Validate that the uploaded file is an SVG.
    
    Args:
        file: UploadFile object
        
    Raises:
        HTTPException: If file is not SVG or invalid
    """
    # Check content type
    valid_types = ["image/svg+xml", "text/xml", "application/xml", "application/octet-stream"]
    if file.content_type not in valid_types:
        # Check extension as fallback
        if not file.filename or not file.filename.lower().endswith(".svg"):
            raise HTTPException(
                status_code=400,
                detail="File must be an SVG image"
            )
    
    # Check extension
    if file.filename and not file.filename.lower().endswith(".svg"):
        raise HTTPException(
            status_code=400,
            detail="File must have .svg extension"
        )


def validate_image_file(file: UploadFile) -> None:
    """
    Validate that the uploaded file is a PNG or JPEG.
    
    Args:
        file: UploadFile object
        
    Raises:
        HTTPException: If file is not PNG/JPEG or invalid
    """
    valid_types = ["image/png", "image/jpeg", "image/jpg", "application/octet-stream"]
    if file.content_type not in valid_types:
        # Check extension as fallback
        if file.filename:
            ext = file.filename.lower().split(".")[-1]
            if ext not in ["png", "jpg", "jpeg"]:
                raise HTTPException(
                    status_code=400,
                    detail="File must be a PNG or JPEG image"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="File must be a PNG or JPEG image"
            )


def validate_file_size(file_size: int, max_size_mb: int) -> None:
    """
    Validate file size is within limit.
    
    Args:
        file_size: File size in bytes
        max_size_mb: Maximum size in MB
        
    Raises:
        HTTPException: If file size exceeds limit
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum of {max_size_mb} MB"
        )


async def get_file_size(file: UploadFile) -> int:
    """
    Get the size of an uploaded file.
    
    Args:
        file: UploadFile object
        
    Returns:
        File size in bytes
    """
    # Read file to get size
    content = await file.read()
    await file.seek(0)  # Reset file pointer
    return len(content)

