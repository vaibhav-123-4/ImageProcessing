"""
Rotation Transformation Module
Implements image rotation without using built-in libraries
"""

from affine_matrix import create_rotation_matrix, matrix_multiply_point
from image_reader import get_pixel
from image_writer import create_empty_image
import math


def apply_rotation(pixel_data, width, height, angle_degrees):
    """
    Apply rotation transformation to an image
    
    Args:
        pixel_data: 2D list of [B, G, R] pixel values
        width: original image width
        height: original image height
        angle_degrees: rotation angle in degrees (counter-clockwise)
    
    Returns:
        (new_width, new_height, new_pixel_data)
    """
    # Convert angle to radians
    angle_rad = angle_degrees * math.pi / 180.0
    
    # Calculate new dimensions to fit rotated image
    cos_angle = abs(math.cos(angle_rad))
    sin_angle = abs(math.sin(angle_rad))
    
    new_width = int(width * cos_angle + height * sin_angle)
    new_height = int(width * sin_angle + height * cos_angle)
    
    # Create empty output image
    output = create_empty_image(new_width, new_height)
    
    # Get centers
    center_x = width / 2.0
    center_y = height / 2.0
    new_center_x = new_width / 2.0
    new_center_y = new_height / 2.0
    
    # Create rotation matrix (for inverse transformation)
    rotation_matrix = create_rotation_matrix(-angle_degrees)  # Negative for inverse
    
    # Apply inverse transformation (backward mapping)
    for y in range(new_height):
        for x in range(new_width):
            # Translate to center of output image
            out_x = x - new_center_x
            out_y = y - new_center_y
            
            # Apply inverse rotation
            src_x, src_y = matrix_multiply_point(rotation_matrix, out_x, out_y)
            
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
