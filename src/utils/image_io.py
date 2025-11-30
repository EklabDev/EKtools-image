"""
Image I/O utilities for loading and saving images.
"""
import io
from typing import Tuple
import numpy as np
from PIL import Image
import cv2


def load_image_from_bytes(image_bytes: bytes) -> Tuple[np.ndarray, Image.Image]:
    """
    Load image from bytes into both OpenCV and PIL formats.
    
    Args:
        image_bytes: Image file bytes
        
    Returns:
        Tuple of (opencv_image, pil_image)
    """
    # Load with PIL
    pil_image = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB if needed
    if pil_image.mode != "RGB":
        pil_image = pil_image.convert("RGB")
    
    # Convert to OpenCV format (BGR)
    opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    return opencv_image, pil_image


def image_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
    """
    Convert PIL Image to bytes.
    
    Args:
        image: PIL Image object
        format: Image format (PNG, JPEG, etc.)
        
    Returns:
        Image bytes
    """
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()


def numpy_to_pil(image: np.ndarray) -> Image.Image:
    """
    Convert numpy array (OpenCV format) to PIL Image.
    
    Args:
        image: numpy array in BGR format
        
    Returns:
        PIL Image in RGB format
    """
    # Convert BGR to RGB
    if len(image.shape) == 3:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image_rgb = image
    
    return Image.fromarray(image_rgb)

