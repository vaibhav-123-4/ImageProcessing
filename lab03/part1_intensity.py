import numpy as np
import cv2

def log_transform(img):
    """
    Apply logarithmic transformation to enhance dark regions.
    Formula: s = c * log(1 + r)
    """
    r = img.astype(np.float32)
    s = np.log(1 + r)
    s = 255 * s / np.max(s)
    return s.astype(np.uint8)


def gamma_correction(img, gamma):
    """
    Apply gamma correction for contrast adjustment.
    Formula: s = c * r^gamma
    gamma < 1: brightens image
    gamma > 1: darkens image
    """
    r = img.astype(np.float32) / 255.0
    s = np.power(r, gamma) * 255.0
    return np.clip(s, 0, 255).astype(np.uint8)


def bit_planes(img):
    """
    Extract all 8 bit planes from the image.
    Each bit plane shows the contribution of that bit to the image.
    """
    planes = []
    for k in range(8):
        # Extract k-th bit plane
        p = ((img >> k) & 1) * 255
        planes.append(p.astype(np.uint8))
    return planes
