"""
Shear Transformation Module
Implements image shearing without using built-in libraries
"""

from affine_matrix import create_shear_matrix, matrix_multiply_point
from image_reader import get_pixel
from image_writer import create_empty_image


def apply_shear(pixel_data, width, height, shx, shy):
    """
    Apply shear transformation to an image
    
    Args:
        pixel_data: 2D list of [B, G, R] pixel values
        width: original image width
        height: original image height
        shx: horizontal shear factor (shears along x-axis)
        shy: vertical shear factor (shears along y-axis)
    
    Returns:
        (new_width, new_height, new_pixel_data)
    """
    # Calculate new dimensions to fit sheared image
    # For horizontal shear: width increases by height * |shx|
    # For vertical shear: height increases by width * |shy|
    new_width = int(width + height * abs(shx))
    new_height = int(height + width * abs(shy))
    
    # Create empty output image
    output = create_empty_image(new_width, new_height)
    
    # Get centers
    center_x = width / 2.0
    center_y = height / 2.0
    new_center_x = new_width / 2.0
    new_center_y = new_height / 2.0
    
    # Create inverse shear matrix
    # Inverse of shear matrix [1, shx, 0; shy, 1, 0; 0, 0, 1]
    # is [1, -shx, 0; -shy, 1 + shx*shy, 0; 0, 0, 1]
    det = 1 - shx * shy
    if abs(det) < 0.0001:
        # Matrix is nearly singular, use identity
        inv_shx = 0
        inv_shy = 0
    else:
        inv_shx = -shx / det
        inv_shy = -shy / det
    
    inverse_shear_matrix = [
        [1, inv_shx, 0],
        [inv_shy, 1 - inv_shx * inv_shy, 0],
        [0, 0, 1]
    ]
    
    # Apply inverse transformation (backward mapping)
    for y in range(new_height):
        for x in range(new_width):
            # Translate to center of output image
            out_x = x - new_center_x
            out_y = y - new_center_y
            
            # Apply inverse shear
            src_x, src_y = matrix_multiply_point(inverse_shear_matrix, out_x, out_y)
            
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
