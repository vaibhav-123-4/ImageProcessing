import numpy as np

def global_hist_eq(img):
    """
    Manual implementation of global histogram equalization.
    Does not use built-in histogram equalization functions.
    """
    M, N = img.shape
    hist = np.zeros(256, dtype=int)
    
    # Compute histogram
    for i in range(M):
        for j in range(N):
            hist[img[i, j]] += 1
    
    # Compute probability density function (PDF)
    pdf = hist / (M * N)
    
    # Compute cumulative distribution function (CDF)
    cdf = np.zeros(256)
    cdf[0] = pdf[0]
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + pdf[i]
    
    # Apply histogram equalization transformation
    out = np.zeros_like(img)
    for i in range(M):
        for j in range(N):
            out[i, j] = round(255 * cdf[img[i, j]])
    
    return out.astype(np.uint8)


def local_hist_eq(img):
    """
    Manual implementation of local histogram equalization using a 3×3 window.
    Does not use built-in histogram equalization functions.
    """
    M, N = img.shape
    out = np.zeros_like(img)
    
    # Pad image with edge values to handle borders
    padded = np.pad(img, 1, mode='edge')
    
    for i in range(M):
        for j in range(N):
            # Extract 3x3 window
            window = padded[i:i+3, j:j+3]
            
            # Compute histogram for the window
            hist = np.zeros(256, dtype=int)
            for x in range(3):
                for y in range(3):
                    hist[window[x, y]] += 1
            
            # Compute PDF
            pdf = hist / 9.0
            
            # Compute CDF
            cdf = np.zeros(256)
            cdf[0] = pdf[0]
            for k in range(1, 256):
                cdf[k] = cdf[k - 1] + pdf[k]
            
            # Apply transformation to center pixel
            out[i, j] = round(255 * cdf[img[i, j]])
    
    return out.astype(np.uint8)
