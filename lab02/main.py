"""
Main Program for Affine Transformations
Applies user-specified affine transformations to input images
"""

from image_reader import read_bmp
from image_writer import write_bmp
from scale import apply_scaling
from rotate import apply_rotation
from translate import apply_translation
from shear import apply_shear
from affine_matrix import (
    create_identity_matrix, 
    create_scaling_matrix, 
    create_rotation_matrix,
    create_translation_matrix,
    create_shear_matrix,
    combine_transformations,
    matrix_multiply_point,
    print_matrix
)
from image_writer import create_empty_image
from image_reader import get_pixel
import os


def apply_combined_affine_transformation(pixel_data, width, height, 
                                        sx, sy, angle, tx, ty, shx, shy):
    """
    Apply combined affine transformation using matrix composition
    
    Args:
        pixel_data: 2D list of [B, G, R] pixel values
        width, height: original image dimensions
        sx, sy: scaling factors
        angle: rotation angle in degrees
        tx, ty: translation values
        shx, shy: shear factors
    
    Returns:
        (new_width, new_height, new_pixel_data)
    """
    import math
    
    # Create individual transformation matrices
    scale_mat = create_scaling_matrix(sx, sy)
    rotation_mat = create_rotation_matrix(angle)
    shear_mat = create_shear_matrix(shx, shy)
    
    # Combine transformations (order matters!)
    # First scale, then shear, then rotate
    combined_matrix = combine_transformations([scale_mat, shear_mat, rotation_mat])
    
    # Print the combined transformation matrix
    print("\n" + "="*60)
    print("TRANSFORMATION MATRICES")
    print("="*60)
    print_matrix(scale_mat, "Scaling Matrix")
    print_matrix(rotation_mat, "Rotation Matrix")
    print_matrix(shear_mat, "Shear Matrix")
    print_matrix(combined_matrix, "Combined Transformation Matrix")
    print("="*60)
    
    # Calculate bounds of transformed image
    corners = [
        (0, 0),
        (width, 0),
        (0, height),
        (width, height)
    ]
    
    # Get center for rotation
    center_x = width / 2.0
    center_y = height / 2.0
    
    # Transform corners to find bounding box
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    
    for cx, cy in corners:
        # Center coordinate
        x_centered = cx - center_x
        y_centered = cy - center_y
        
        # Apply transformation
        tx_corner, ty_corner = matrix_multiply_point(combined_matrix, x_centered, y_centered)
        
        min_x = min(min_x, tx_corner)
        max_x = max(max_x, tx_corner)
        min_y = min(min_y, ty_corner)
        max_y = max(max_y, ty_corner)
    
    # Calculate new dimensions
    new_width = int(max_x - min_x) + 1
    new_height = int(max_y - min_y) + 1
    
    # Add translation to dimensions
    new_width += abs(int(tx))
    new_height += abs(int(ty))
    
    # Create output image
    output = create_empty_image(new_width, new_height)
    
    # Create inverse transformation matrix
    # For inverse: reverse order and invert each matrix
    inv_rotation_mat = create_rotation_matrix(-angle)
    
    # Inverse shear matrix
    det = 1 - shx * shy
    if abs(det) < 0.0001:
        inv_shx = 0
        inv_shy = 0
    else:
        inv_shx = -shx / det
        inv_shy = -shy / det
    inv_shear_mat = create_shear_matrix(inv_shx, inv_shy)
    
    # Inverse scale matrix
    if sx != 0 and sy != 0:
        inv_scale_mat = create_scaling_matrix(1/sx, 1/sy)
    else:
        inv_scale_mat = create_identity_matrix()
    
    # Combine inverse matrices (reverse order)
    inverse_matrix = combine_transformations([inv_rotation_mat, inv_shear_mat, inv_scale_mat])
    
    # Calculate output center
    new_center_x = new_width / 2.0
    new_center_y = new_height / 2.0
    
    # Apply inverse transformation (backward mapping)
    for y in range(new_height):
        for x in range(new_width):
            # Account for translation
            out_x = x - tx - new_center_x + (max_x + min_x) / 2
            out_y = y - ty - new_center_y + (max_y + min_y) / 2
            
            # Apply inverse transformation
            src_x, src_y = matrix_multiply_point(inverse_matrix, out_x, out_y)
            
            # Translate back to original image coordinates
            src_x += center_x
            src_y += center_y
            
            # Use bilinear interpolation
            src_x_int = int(src_x)
            src_y_int = int(src_y)
            
            # Get the fractional parts
            dx = src_x - src_x_int
            dy = src_y - src_y_int
            
            # Get the four neighboring pixels
            p00 = get_pixel(pixel_data, src_x_int, src_y_int, width, height)
            p10 = get_pixel(pixel_data, src_x_int + 1, src_y_int, width, height)
            p01 = get_pixel(pixel_data, src_x_int, src_y_int + 1, width, height)
            p11 = get_pixel(pixel_data, src_x_int + 1, src_y_int + 1, width, height)
            
            # Bilinear interpolation for each channel
            for c in range(3):
                val = (p00[c] * (1 - dx) * (1 - dy) +
                       p10[c] * dx * (1 - dy) +
                       p01[c] * (1 - dx) * dy +
                       p11[c] * dx * dy)
                output[y][x][c] = int(val)
    
    return new_width, new_height, output


def get_float_input(prompt, default=None):
    """Get a float input from user with validation"""
    while True:
        try:
            user_input = input(prompt)
            if user_input.strip() == "" and default is not None:
                return default
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    print("\n" + "="*60)
    print("AFFINE TRANSFORMATION PROGRAM")
    print("="*60)
    print("\nThis program applies affine transformations to BMP images.")
    print("No built-in image processing libraries are used.\n")
    
    # Input file
    input_file = input("Enter input BMP file path (default: input.bmp): ").strip()
    if not input_file:
        input_file = "input.bmp"
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"\nError: File '{input_file}' not found!")
        return
    
    try:
        # Read input image
        print(f"\nReading image: {input_file}")
        width, height, pixel_data = read_bmp(input_file)
        print(f"Image size: {width} x {height} pixels")
        
        # Get transformation parameters from user
        print("\n" + "-"*60)
        print("TRANSFORMATION PARAMETERS")
        print("-"*60)
        print("\nEnter the following transformation parameters:")
        print("(Press Enter to use default value)\n")
        
        sx = get_float_input("1. Horizontal scaling factor (default: 1.0): ", 1.0)
        sy = get_float_input("2. Vertical scaling factor (default: 1.0): ", 1.0)
        angle = get_float_input("3. Rotation angle in degrees (default: 0.0): ", 0.0)
        tx = get_float_input("4. Horizontal translation (default: 0.0): ", 0.0)
        ty = get_float_input("5. Vertical translation (default: 0.0): ", 0.0)
        shx = get_float_input("6. Horizontal shear factor (default: 0.0): ", 0.0)
        shy = get_float_input("7. Vertical shear factor (default: 0.0): ", 0.0)
        
        # Display parameters
        print("\n" + "-"*60)
        print("TRANSFORMATION PARAMETERS SUMMARY")
        print("-"*60)
        print(f"Scaling (Horizontal, Vertical): ({sx}, {sy})")
        print(f"Rotation Angle: {angle} degrees")
        print(f"Translation (Horizontal, Vertical): ({tx}, {ty})")
        print(f"Shear (Horizontal, Vertical): ({shx}, {shy})")
        print("-"*60)
        
        # Apply combined transformation
        print("\nApplying affine transformation...")
        new_width, new_height, output = apply_combined_affine_transformation(
            pixel_data, width, height, sx, sy, angle, tx, ty, shx, shy
        )
        
        print(f"Output image size: {new_width} x {new_height} pixels")
        
        # Create result directory if it doesn't exist
        if not os.path.exists("lab02/result"):
            os.makedirs("result")
        
        # Output file
        output_file = "lab02/result/output.bmp"
        print(f"\nWriting output image: {output_file}")
        write_bmp(output_file, new_width, new_height, output)
        
        print("\n" + "="*60)
        print("TRANSFORMATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Output saved to: {output_file}\n")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
