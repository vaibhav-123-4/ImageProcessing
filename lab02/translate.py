"""
Translation Transformation Module
Implements image translation without using built-in libraries
"""

from affine_matrix import create_translation_matrix, matrix_multiply_point
from image_reader import get_pixel
from image_writer import create_empty_image


def apply_translation(pixel_data, width, height, tx, ty):
    """
    Apply translation transformation to an image
    
    Args:
        pixel_data: 2D list of [B, G, R] pixel values
        width: original image width
        height: original image height
        tx: horizontal translation (positive = right, negative = left)
        ty: vertical translation (positive = down, negative = up)
    
    Returns:
        (new_width, new_height, new_pixel_data)
    """
    # Calculate new dimensions to fit translated image
    new_width = width + abs(int(tx))
    new_height = height + abs(int(ty))
    
    # Create empty output image
    output = create_empty_image(new_width, new_height)
    
    # Determine offset for placing the image
    offset_x = max(0, int(tx))
    offset_y = max(0, int(ty))
    
    # If translation is negative, we need to adjust source offset
    src_offset_x = max(0, -int(tx))
    src_offset_y = max(0, -int(ty))
    
    # Apply translation (forward mapping)
    for y in range(height):
        for x in range(width):
            # Calculate destination coordinates
            dst_x = x + offset_x
            dst_y = y + offset_y
            
            # Check if destination is within bounds
            if 0 <= dst_x < new_width and 0 <= dst_y < new_height:
                # Copy pixel from source to destination
                output[dst_y][dst_x] = pixel_data[y][x][:]
    
    return new_width, new_height, output
