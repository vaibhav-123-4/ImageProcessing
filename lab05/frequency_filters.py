import numpy as np
from utils import fft2, ifft2, normalize

def gaussian_low_pass(shape, cutoff=60):
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2

    mask = np.zeros((rows, cols))

    for i in range(rows):
        for j in range(cols):
            d2 = (i - crow) ** 2 + (j - ccol) ** 2
            mask[i, j] = np.exp(-d2 / (2 * cutoff ** 2))

    return mask

def apply_frequency_filter(img):

    fshift = fft2(img)
    mask = gaussian_low_pass(img.shape, 60)

    filtered = fshift * mask
    result = ifft2(filtered)

    return normalize(result)
