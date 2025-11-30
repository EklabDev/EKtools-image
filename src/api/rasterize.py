"""
POST /rasterize endpoint: Convert SVG to PNG.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response

from src.utils.validators import validate_svg_file, validate_file_size, get_file_size
from src.core.rasterizer import svg_to_png

router = APIRouter()


@router.post("", response_class=Response)
async def rasterize(file: UploadFile = File(...)):
    """
    Convert an SVG file to PNG.
    
    Args:
        file: SVG file
        
    Returns:
        PNG image as image/png
    """
    # Validate file type
    validate_svg_file(file)
    
    # Read file content
    file_content = await file.read()
    
    # Validate file size (10 MB)
    file_size = len(file_content)
    validate_file_size(file_size, 10)
    
    try:
        # Convert SVG to PNG
        png_bytes = svg_to_png(file_content)
        
        # Return PNG as image/png
        return Response(
            content=png_bytes,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=rasterized.png"}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error converting SVG to PNG: {str(e)}"
        )

