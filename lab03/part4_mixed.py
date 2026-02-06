import cv2
import numpy as np
from part1_intensity import gamma_correction

def mixed_enhancement(img):
    """
    Apply mixed spatial enhancement combining:
    - Laplacian operator
    - Sobel gradient magnitude
    - Gamma correction
    """
    # Apply Laplacian
    lap = cv2.Laplacian(img, cv2.CV_32F)
    
    # Apply Sobel gradients
    sx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
    sy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)
    
    # Compute gradient magnitude
    grad = np.abs(sx) + np.abs(sy)
    
    # Combine with original image
    temp = img.astype(np.float32) + lap + grad
    temp = np.clip(temp, 0, 255).astype(np.uint8)
    
    # Apply gamma correction for final enhancement
    return gamma_correction(temp, 0.8)
