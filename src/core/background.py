"""
Background removal using K-means or GrabCut.
"""
import numpy as np
import cv2
from typing import Tuple
from src.utils.mask_ops import get_bounding_box, apply_mask


def remove_background_kmeans(image: np.ndarray, n_clusters: int = 3) -> np.ndarray:
    """
    Remove background using K-means color segmentation.
    
    Identifies the largest cluster as background and masks it out.
    
    Args:
        image: Input image in BGR format
        n_clusters: Number of K-means clusters (default: 3)
        
    Returns:
        Image with alpha channel (BGRA)
    """
    # Reshape to pixels
    h, w, c = image.shape
    pixels = image.reshape(-1, 3)
    
    # Convert to float for K-means
    pixels_float = pixels.astype(np.float32)
    
    # Apply K-means
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixels_float)
    
    # Reshape labels
    label_image = labels.reshape(h, w)
    
    # Find largest cluster (assumed to be background)
    cluster_sizes = [np.sum(label_image == i) for i in range(n_clusters)]
    background_cluster = np.argmax(cluster_sizes)
    
    # Create mask (1 for foreground, 0 for background)
    mask = (label_image != background_cluster).astype(np.uint8) * 255
    
    # Apply morphological operations to clean up mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Apply mask to image
    result = apply_mask(image, mask)
    
    return result


def remove_background_grabcut(image: np.ndarray) -> np.ndarray:
    """
    Remove background using OpenCV GrabCut algorithm.
    
    Args:
        image: Input image in BGR format
        
    Returns:
        Image with alpha channel (BGRA)
    """
    h, w = image.shape[:2]
    
    # Initialize mask
    mask = np.zeros((h, w), np.uint8)
    
    # Initialize background and foreground models
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    # Define rectangle (use entire image with small margin)
    margin = 10
    rect = (margin, margin, w - 2 * margin, h - 2 * margin)
    
    # Run GrabCut
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    
    # Create binary mask (0 = background, 255 = foreground)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 255).astype(np.uint8)
    
    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel)
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)
    
    # Apply mask
    result = apply_mask(image, mask2)
    
    return result


def remove_background(image: np.ndarray, method: str = "kmeans") -> np.ndarray:
    """
    Remove background from image.
    
    Args:
        image: Input image in BGR format
        method: Method to use ("kmeans" or "grabcut")
        
    Returns:
        Image with alpha channel (BGRA)
    """
    if method == "grabcut":
        return remove_background_grabcut(image)
    else:
        return remove_background_kmeans(image)

