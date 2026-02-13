import numpy as np

def estimate_noise_type(ref, noisy):
    """
    Estimate noise using reference image.
    """

    diff = noisy.astype(np.int16) - ref.astype(np.int16)

    # salt & pepper detection
    extreme = np.sum((noisy <= 5) | (noisy >= 250))
    ratio = extreme / noisy.size

    if ratio > 0.03:
        return "salt_pepper"

    # gaussian detection
    if np.std(diff) > 15:
        return "gaussian"

    return "speckle"
