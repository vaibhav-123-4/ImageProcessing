"""
Image Writer Module
Writes BMP image files without using built-in image processing libraries
"""

def write_bmp(filename, width, height, pixel_data):
    """
    Writes a BMP file from pixel data
    pixel_data: 2D list where each element is [B, G, R]
    """
    # Calculate row size (must be multiple of 4 bytes)
    row_size = ((width * 3 + 3) // 4) * 4
    padding = row_size - (width * 3)
    
    # Calculate file size
    pixel_data_size = row_size * height
    file_size = 54 + pixel_data_size  # 14 (BMP header) + 40 (DIB header) + pixel data
    
    with open(filename, 'wb') as f:
        # BMP Header (14 bytes)
        f.write(b'BM')  # Signature
        f.write(file_size.to_bytes(4, byteorder='little'))  # File size
        f.write((0).to_bytes(2, byteorder='little'))  # Reserved
        f.write((0).to_bytes(2, byteorder='little'))  # Reserved
        f.write((54).to_bytes(4, byteorder='little'))  # Pixel data offset
        
        # DIB Header (40 bytes - BITMAPINFOHEADER)
        f.write((40).to_bytes(4, byteorder='little'))  # DIB header size
        f.write(width.to_bytes(4, byteorder='little'))  # Width
        f.write(height.to_bytes(4, byteorder='little'))  # Height
        f.write((1).to_bytes(2, byteorder='little'))  # Color planes
        f.write((24).to_bytes(2, byteorder='little'))  # Bits per pixel
        f.write((0).to_bytes(4, byteorder='little'))  # Compression (none)
        f.write(pixel_data_size.to_bytes(4, byteorder='little'))  # Image size
        f.write((2835).to_bytes(4, byteorder='little'))  # Horizontal resolution (72 DPI)
        f.write((2835).to_bytes(4, byteorder='little'))  # Vertical resolution (72 DPI)
        f.write((0).to_bytes(4, byteorder='little'))  # Colors in palette
        f.write((0).to_bytes(4, byteorder='little'))  # Important colors
        
        # Write pixel data (bottom to top)
        for y in range(height - 1, -1, -1):
            for x in range(width):
                # Get pixel, clamp values to 0-255
                pixel = pixel_data[y][x]
                b = max(0, min(255, int(pixel[0])))
                g = max(0, min(255, int(pixel[1])))
                r = max(0, min(255, int(pixel[2])))
                
                # Write BGR
                f.write(b.to_bytes(1, byteorder='little'))
                f.write(g.to_bytes(1, byteorder='little'))
                f.write(r.to_bytes(1, byteorder='little'))
            
            # Write padding
            for _ in range(padding):
                f.write((0).to_bytes(1, byteorder='little'))


def create_empty_image(width, height):
    """
    Creates an empty image with black pixels
    Returns: 2D list of [B, G, R] values
    """
    return [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
