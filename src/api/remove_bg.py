"""
POST /remove-background endpoint: Remove background from JPEG or PNG.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import Response
import numpy as np
import cv2
from PIL import Image

from src.core.limiter import limiter
from src.utils.validators import validate_image_file
from src.utils.image_io import load_image_from_bytes, numpy_to_pil, image_to_bytes
from src.core.background import remove_background

router = APIRouter()


@router.post("", response_class=Response)
@limiter.limit("100/minute")
async def remove_background_endpoint(request: Request, file: UploadFile = File(...)):
    """
    Remove background from a JPEG or PNG image.
    
    Args:
        file: JPEG or PNG image file
        
    Returns:
        PNG image with alpha channel as image/png
    """
    # Validate file type
    validate_image_file(file)
    
    # Read file content
    file_content = await file.read()
    
    try:
        # Load image
        opencv_image, pil_image = load_image_from_bytes(file_content)
        
        # Remove background (returns BGRA image)
        result_bgra = remove_background(opencv_image, method="kmeans")
        
        # Convert to PIL Image (RGBA)
        result_rgba = cv2.cvtColor(result_bgra, cv2.COLOR_BGRA2RGBA)
        result_pil = Image.fromarray(result_rgba)
        
        # Convert to PNG bytes
        png_bytes = image_to_bytes(result_pil, format="PNG")
        
        # Return PNG as image/png
        return Response(
            content=png_bytes,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=no_background.png"}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error removing background: {str(e)}"
        )
