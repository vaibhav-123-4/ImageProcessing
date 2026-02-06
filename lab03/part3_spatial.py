import cv2
import numpy as np

def box_filter(img, k):
    """
    Apply box (mean) filter with kernel size k×k.
    """
    kernel = np.ones((k, k), np.float32) / (k * k)
    return cv2.filter2D(img, -1, kernel)


def gaussian_filter(img, k, sigma):
    """
    Apply Gaussian filter with kernel size k×k and standard deviation sigma.
    """
    return cv2.GaussianBlur(img, (k, k), sigma)


def laplacian_sharpen(img, c=1.0):
    """
    Apply Laplacian sharpening.
    Formula: g(x,y) = f(x,y) + c * ∇²f(x,y)
    """
    lap = cv2.Laplacian(img, cv2.CV_32F)
    res = img.astype(np.float32) + c * lap
    return np.clip(res, 0, 255).astype(np.uint8)


def unsharp_mask(img, k=1.5):
    """
    Apply unsharp masking for edge enhancement.
    Formula: g(x,y) = f(x,y) + k * (f(x,y) - f_blur(x,y))
    """
    blur = cv2.GaussianBlur(img, (5, 5), 1.0)
    mask = img.astype(np.float32) - blur.astype(np.float32)
    res = img.astype(np.float32) + k * mask
    return np.clip(res, 0, 255).astype(np.uint8)
