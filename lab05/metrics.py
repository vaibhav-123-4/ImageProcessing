import numpy as np

def mse(img1, img2):
    return np.mean((img1.astype(np.float32) - img2.astype(np.float32)) ** 2)

def psnr(img1, img2):
    m = mse(img1, img2)
    if m == 0:
        return float("inf")
    return 20 * np.log10(255.0 / np.sqrt(m))

def compute_ssim(img1, img2):
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    mu1 = img1.mean()
    mu2 = img2.mean()

    var1 = img1.var()
    var2 = img2.var()
    cov = ((img1 - mu1) * (img2 - mu2)).mean()

    return ((2 * mu1 * mu2 + C1) * (2 * cov + C2)) / \
           ((mu1**2 + mu2**2 + C1) * (var1 + var2 + C2))
