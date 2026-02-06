"""
2-D Discrete Fourier Transform (DFT) implementation without using ready-made FFT functions
"""
import numpy as np
import matplotlib.pyplot as plt


def dft_2d(image):
    """
    Compute the 2-D DFT of an image without using ready-made DFT/FFT functions.
    
    Parameters:
    - image: 2D numpy array (MxN image)
    
    Returns:
    - dft_result: Complex 2D array containing the DFT coefficients
    """
    M, N = image.shape
    dft_result = np.zeros((M, N), dtype=complex)
    
    # Compute 2-D DFT using the formula:
    # F(u,v) = sum_{x=0}^{M-1} sum_{y=0}^{N-1} f(x,y) * exp(-j*2*pi*(ux/M + vy/N))
    for u in range(M):
        for v in range(N):
            sum_val = 0.0 + 0.0j
            for x in range(M):
                for y in range(N):
                    angle = -2 * np.pi * ((u * x / M) + (v * y / N))
                    sum_val += image[x, y] * (np.cos(angle) + 1j * np.sin(angle))
            dft_result[u, v] = sum_val
    
    return dft_result


def idft_2d(dft_result):
    """
    Compute the inverse 2-D DFT.
    
    Parameters:
    - dft_result: Complex 2D array containing the DFT coefficients
    
    Returns:
    - image: Reconstructed 2D array
    """
    M, N = dft_result.shape
    image = np.zeros((M, N), dtype=complex)
    
    # Compute inverse 2-D DFT using the formula:
    # f(x,y) = (1/MN) * sum_{u=0}^{M-1} sum_{v=0}^{N-1} F(u,v) * exp(j*2*pi*(ux/M + vy/N))
    for x in range(M):
        for y in range(N):
            sum_val = 0.0 + 0.0j
            for u in range(M):
                for v in range(N):
                    angle = 2 * np.pi * ((u * x / M) + (v * y / N))
                    sum_val += dft_result[u, v] * (np.cos(angle) + 1j * np.sin(angle))
            image[x, y] = sum_val / (M * N)
    
    return image.real


def compute_magnitude_spectrum(dft_result):
    """
    Compute the magnitude spectrum of the DFT result.
    
    Parameters:
    - dft_result: Complex 2D array containing the DFT coefficients
    
    Returns:
    - magnitude: 2D array containing the magnitude values
    """
    magnitude = np.abs(dft_result)
    return magnitude


def compute_phase_spectrum(dft_result):
    """
    Compute the phase spectrum of the DFT result.
    
    Parameters:
    - dft_result: Complex 2D array containing the DFT coefficients
    
    Returns:
    - phase: 2D array containing the phase values
    """
    phase = np.angle(dft_result)
    return phase


def plot_dft_results(image, dft_result, title_prefix="", save_path=None):
    """
    Plot the original image, magnitude spectrum, and phase spectrum.
    
    Parameters:
    - image: Original 2D image
    - dft_result: Complex 2D array containing the DFT coefficients
    - title_prefix: Prefix for plot titles
    - save_path: Path to save the plot
    """
    magnitude = compute_magnitude_spectrum(dft_result)
    phase = compute_phase_spectrum(dft_result)
    
    # Log scale for better visualization
    magnitude_log = np.log(1 + magnitude)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Original image
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title(f'{title_prefix}Original Image')
    axes[0].axis('off')
    
    # Magnitude spectrum (log scale)
    im1 = axes[1].imshow(magnitude_log, cmap='jet')
    axes[1].set_title(f'{title_prefix}Magnitude Spectrum (Log Scale)')
    axes[1].axis('off')
    plt.colorbar(im1, ax=axes[1], fraction=0.046)
    
    # Phase spectrum
    im2 = axes[2].imshow(phase, cmap='hsv')
    axes[2].set_title(f'{title_prefix}Phase Spectrum')
    axes[2].axis('off')
    plt.colorbar(im2, ax=axes[2], fraction=0.046)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"DFT results saved to {save_path}")
    
    plt.show()


def center_image(image):
    """
    Center the image by multiplying with (-1)^(x+y).
    This shifts the zero-frequency component to the center of the spectrum.
    
    Parameters:
    - image: 2D numpy array
    
    Returns:
    - centered_image: Centered 2D array
    """
    M, N = image.shape
    centered_image = np.zeros((M, N))
    
    for x in range(M):
        for y in range(N):
            centered_image[x, y] = image[x, y] * ((-1) ** (x + y))
    
    return centered_image


if __name__ == "__main__":
    # Test with a simple 8x8 image
    test_image = np.zeros((8, 8))
    test_image[2:6, 2:6] = 1  # Create a small square
    
    print("Computing 2-D DFT...")
    dft_result = dft_2d(test_image)
    
    print("Plotting results...")
    plot_dft_results(test_image, dft_result, title_prefix="Test - ", 
                    save_path='Result/test_dft.png')
    
    print("\nDFT computation completed!")
