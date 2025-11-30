"""
Mask operations for image processing.
"""
from typing import Tuple
import numpy as np
import cv2


def create_binary_mask(mask: np.ndarray) -> np.ndarray:
    """
    Create a binary mask from a mask array.
    
    Args:
        mask: Mask array (can be boolean or integer)
        
    Returns:
        Binary mask (0 or 255)
    """
    binary = (mask > 0).astype(np.uint8) * 255
    return binary


def get_largest_contour(mask: np.ndarray) -> np.ndarray:
    """
    Get the largest contour from a binary mask.
    
    Args:
        mask: Binary mask
        
    Returns:
        Largest contour or None
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    return max(contours, key=cv2.contourArea)


def get_bounding_box(mask: np.ndarray) -> Tuple[int, int, int, int]:
    """
    Get bounding box of a mask.
    
    Args:
        mask: Binary mask
        
    Returns:
        Tuple of (x, y, width, height)
    """
    coords = np.column_stack(np.where(mask > 0))
    if len(coords) == 0:
        return (0, 0, 0, 0)
    
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)
    
    return (x_min, y_min, x_max - x_min + 1, y_max - y_min + 1)


def apply_mask(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Apply a mask to an image, setting background to transparent.
    
    Args:
        image: Input image (BGR)
        mask: Binary mask (0 or 255)
        
    Returns:
        Image with alpha channel
    """
    # Convert to RGBA
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    
    # Apply mask to alpha channel
    rgba[:, :, 3] = mask
    
    return rgba

