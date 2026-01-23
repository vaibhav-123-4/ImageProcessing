"""
Scaling Transformation Module
Implements image scaling without using built-in libraries
"""

from affine_matrix import create_scaling_matrix, matrix_multiply_point
from image_reader import get_pixel
from image_writer import create_empty_image


def apply_scaling(pixel_data, width, height, sx, sy):
    """
    Apply scaling transformation to an image
    
    Args:
        pixel_data: 2D list of [B, G, R] pixel values
        width: original image width
        height: original image height
        sx: horizontal scaling factor
        sy: vertical scaling factor
    
    Returns:
        (new_width, new_height, new_pixel_data)
    """
    # Calculate new dimensions
    new_width = int(width * abs(sx))
    new_height = int(height * abs(sy))
    
    # Create empty output image
    output = create_empty_image(new_width, new_height)
    
    # Create scaling matrix
    scale_matrix = create_scaling_matrix(sx, sy)
    
    # Get center of original image
    center_x = width / 2.0
    center_y = height / 2.0
    
    # Apply inverse transformation (backward mapping)
    for y in range(new_height):
        for x in range(new_width):
            # Map output coordinate to input coordinate
            # Center around origin, apply inverse transform, then translate back
            out_x = x - new_width / 2.0
            out_y = y - new_height / 2.0
            
            # Apply inverse scaling (divide by scale factors)
            if sx != 0:
                src_x = out_x / sx + center_x
            else:
                src_x = center_x
                
            if sy != 0:
                src_y = out_y / sy + center_y
            else:
                src_y = center_y
            
            # Use bilinear interpolation for better quality
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
