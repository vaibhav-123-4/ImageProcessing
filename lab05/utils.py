import cv2
import numpy as np
import os

def read_gray(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

def save_image(path, img):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv2.imwrite(path, img)

def normalize(img):
    return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

def fft2(img):
    return np.fft.fftshift(np.fft.fft2(img))

def ifft2(fshift):
    return np.abs(np.fft.ifft2(np.fft.ifftshift(fshift)))
