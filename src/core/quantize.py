"""
Color quantization using K-means clustering.
"""
import numpy as np
from sklearn.cluster import KMeans
from typing import Tuple, List


def quantize_colors(image: np.ndarray, n_colors: int) -> Tuple[np.ndarray, np.ndarray, List[Tuple[int, int, int]]]:
    """
    Quantize image colors using K-means clustering.
    
    Args:
        image: Input image in BGR format (H, W, 3)
        n_colors: Number of color clusters (2-20)
        
    Returns:
        Tuple of:
        - Quantized image (same shape as input)
        - Label image (H, W) with cluster indices
        - List of RGB color tuples (centroids)
    """
    # Reshape image to (N, 3) where N = H * W
    h, w, c = image.shape
    pixels = image.reshape(-1, 3)
    
    # Convert BGR to RGB for better color representation
    pixels_rgb = pixels[:, ::-1]
    
    # Apply K-means
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixels_rgb)
    
    # Get cluster centers (RGB)
    centers_rgb = kmeans.cluster_centers_.astype(np.uint8)
    
    # Convert centers back to BGR for image reconstruction
    centers_bgr = centers_rgb[:, ::-1]
    
    # Reconstruct quantized image
    quantized_pixels = centers_bgr[labels]
    quantized_image = quantized_pixels.reshape(h, w, c)
    
    # Reshape labels to image shape
    label_image = labels.reshape(h, w)
    
    # Convert centers to list of RGB tuples
    color_list = [tuple(center) for center in centers_rgb]
    
    return quantized_image, label_image, color_list


def get_color_masks(label_image: np.ndarray, n_colors: int) -> List[np.ndarray]:
    """
    Generate binary masks for each color cluster.
    
    Args:
        label_image: Image with cluster labels (H, W)
        n_colors: Number of clusters
        
    Returns:
        List of binary masks, one per color
    """
    masks = []
    for i in range(n_colors):
        mask = (label_image == i).astype(np.uint8) * 255
        masks.append(mask)
    return masks

