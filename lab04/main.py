
import numpy as np
import matplotlib.pyplot as plt
from basis import display_dft_basis
from dft2d import dft_2d, plot_dft_results, center_image


def create_rectangle_image(size=64):
    """
    Create a binary image containing a rectangle based on user input.
    
    Parameters:
    - size: Size of the square image (default 64x64)
    
    Returns:
    - image: Binary image with rectangle
    - params: Dictionary containing rectangle parameters
    """
    image = np.zeros((size, size))
    
    print(f"\nCreating a {size}x{size} binary image with a rectangle")
    print("=" * 60)
    
    # Get user input for rectangle parameters
    while True:
        try:
            top = int(input(f"Enter the top-left corner row position (0-{size-1}): "))
            left = int(input(f"Enter the top-left corner column position (0-{size-1}): "))
            width = int(input(f"Enter the width of the rectangle (pixels): "))
            height = int(input(f"Enter the height of the rectangle (pixels): "))
            
            # Validate inputs
            if top < 0 or left < 0 or top >= size or left >= size:
                print(f"Error: Top-left corner must be within (0-{size-1})")
                continue
            
            if width <= 0 or height <= 0:
                print("Error: Width and height must be positive")
                continue
            
            if top + height > size or left + width > size:
                print(f"Error: Rectangle exceeds image boundaries")
                print(f"Maximum width: {size - left}, Maximum height: {size - top}")
                continue
            
            break
        except ValueError:
            print("Error: Please enter valid integers")
    
    # Create the rectangle
    image[top:top+height, left:left+width] = 1
    
    params = {
        'top': top,
        'left': left,
        'width': width,
        'height': height
    }
    
    print(f"\nRectangle created:")
    print(f"  Position: ({top}, {left})")
    print(f"  Size: {width}x{height} pixels")
    print(f"  Bottom-right corner: ({top+height-1}, {left+width-1})")
    
    return image, params


def save_image(image, filename):
    """
    Save an image to a file.
    
    Parameters:
    - image: 2D numpy array
    - filename: Output filename
    """
    plt.figure(figsize=(6, 6))
    plt.imshow(image, cmap='gray')
    plt.title('Binary Image with Rectangle')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Image saved to {filename}")


def main():
    """
    Main function to execute all tasks.
    """
    print("=" * 60)
    print("LAB 04: 2-D Discrete Fourier Transform (DFT)")
    print("=" * 60)
    
    # Task 1: Generate and display 8x8 DFT basis
    print("\n" + "=" * 60)
    print("TASK 1: Generate 8x8 2-D DFT Basis")
    print("=" * 60)
    display_dft_basis(N=8, save_path='Result/dft_basis.png')
    
    # Task 2: Create binary image with rectangle
    print("\n" + "=" * 60)
    print("TASK 2: Create Binary Image with Rectangle")
    print("=" * 60)
    rect_image, params = create_rectangle_image(size=64)
    save_image(rect_image, 'Result/rectangle_image.png')
    
    # Task 3: Compute and plot 2-D DFT for the rectangle image
    print("\n" + "=" * 60)
    print("TASK 3: Compute 2-D DFT for Rectangle Image")
    print("=" * 60)
    print("Computing 2-D DFT (this may take a moment for 64x64 image)...")
    dft_result = dft_2d(rect_image)
    print("DFT computation completed!")
    print("Plotting results...")
    plot_dft_results(rect_image, dft_result, 
                    title_prefix="",
                    save_path='Result/rectangle_dft.png')
    
    # Task 4: Compute and plot 2-D DFT for centered image
    print("\n" + "=" * 60)
    print("TASK 4: Compute 2-D DFT for Centered Image")
    print("=" * 60)
    print("Centering image by multiplying with (-1)^(x+y)...")
    centered_image = center_image(rect_image)
    save_image(centered_image, 'Result/centered_image.png')
    
    print("Computing 2-D DFT for centered image...")
    dft_centered = dft_2d(centered_image)
    print("DFT computation completed!")
    print("Plotting results...")
    plot_dft_results(centered_image, dft_centered, 
                    title_prefix="Centered - ",
                    save_path='Result/centered_dft.png')
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("All tasks completed successfully!")
    print("\nGenerated files:")
    print("  1. Result/dft_basis.png - 8x8 DFT basis displayed as 64x64 image")
    print("  2. Result/rectangle_image.png - Binary image with rectangle")
    print("  3. Result/rectangle_dft.png - DFT of rectangle image")
    print("  4. Result/centered_image.png - Centered image")
    print("  5. Result/centered_dft.png - DFT of centered image")
    print("\nNote: The centering operation multiplies the image by (-1)^(x+y),")
    print("      which shifts the zero-frequency component to the center of")
    print("      the frequency spectrum, making it easier to analyze.")
    print("=" * 60)


if __name__ == "__main__":
    main()
