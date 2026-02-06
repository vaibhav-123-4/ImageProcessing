"""
Generate and display the basis of an 8x8 2-D DFT
"""
import numpy as np
import matplotlib.pyplot as plt


def generate_dft_basis_2d(N=8):
    """
    Generate the basis functions of an NxN 2-D DFT.
    
    Parameters:
    - N: Size of the DFT (default 8)
    
    Returns:
    - basis_real: Real parts of basis functions (N*N, N, N)
    - basis_imag: Imaginary parts of basis functions (N*N, N, N)
    """
    basis_real = np.zeros((N * N, N, N))
    basis_imag = np.zeros((N * N, N, N))
    
    idx = 0
    for u in range(N):
        for v in range(N):
            for x in range(N):
                for y in range(N):
                    angle = -2 * np.pi * ((u * x / N) + (v * y / N))
                    basis_real[idx, x, y] = np.cos(angle)
                    basis_imag[idx, x, y] = np.sin(angle)
            idx += 1
    
    return basis_real, basis_imag


def display_dft_basis(N=8, save_path='Result/dft_basis.png'):
    """
    Display the 2-D DFT basis functions as a grid image.
    
    Parameters:
    - N: Size of the DFT (default 8)
    - save_path: Path to save the output image
    """
    basis_real, basis_imag = generate_dft_basis_2d(N)
    
    # Compute magnitude of basis functions
    basis_magnitude = np.sqrt(basis_real**2 + basis_imag**2)
    
    # Create a grid to display all basis functions
    grid_size = N
    img_size = N
    result_img = np.zeros((grid_size * img_size, grid_size * img_size))
    
    idx = 0
    for i in range(grid_size):
        for j in range(grid_size):
            # Normalize the basis function for display
            basis_func = basis_magnitude[idx]
            basis_func_norm = (basis_func - basis_func.min()) / (basis_func.max() - basis_func.min() + 1e-10)
            
            # Place in the grid
            result_img[i*img_size:(i+1)*img_size, j*img_size:(j+1)*img_size] = basis_func_norm
            idx += 1
    
    # Display the result
    plt.figure(figsize=(10, 10))
    plt.imshow(result_img, cmap='gray')
    plt.title(f'{N}x{N} 2-D DFT Basis Functions (displayed as {grid_size*img_size}x{grid_size*img_size} image)')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    
    print(f"DFT basis saved to {save_path}")
    print(f"Total basis functions: {N*N}")
    print(f"Output image size: {grid_size*img_size}x{grid_size*img_size}")
    
    return result_img


if __name__ == "__main__":
    # Generate and display 8x8 DFT basis as 64x64 image
    display_dft_basis(N=8, save_path='Result/dft_basis.png')
