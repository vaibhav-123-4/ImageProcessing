"""
Image Reader Module
Reads BMP image files without using built-in image processing libraries
"""

def read_bmp(filename):
    """
    Reads a BMP file and returns image data
    Returns: (width, height, pixel_data)
    pixel_data is a 2D list where each element is [B, G, R]
    """
    with open(filename, 'rb') as f:
        # Read BMP Header (14 bytes)
        bmp_header = f.read(14)
        
        # Check if file is BMP
        if bmp_header[0:2] != b'BM':
            raise ValueError("Not a valid BMP file")
        
        # Get pixel data offset
        pixel_data_offset = int.from_bytes(bmp_header[10:14], byteorder='little')
        
        # Read DIB Header (40 bytes for BITMAPINFOHEADER)
        dib_header = f.read(40)
        
        # Extract image dimensions
        width = int.from_bytes(dib_header[4:8], byteorder='little')
        height = int.from_bytes(dib_header[8:12], byteorder='little')
        bits_per_pixel = int.from_bytes(dib_header[14:16], byteorder='little')
        
        # Only support 24-bit BMP
        if bits_per_pixel != 24:
            raise ValueError(f"Only 24-bit BMP supported, got {bits_per_pixel}-bit")
        
        # Move to pixel data
        f.seek(pixel_data_offset)
        
        # Calculate row size (must be multiple of 4 bytes)
        row_size = ((width * 3 + 3) // 4) * 4
        padding = row_size - (width * 3)
        
        # Read pixel data (BMP stores bottom to top)
        pixel_data = []
        for y in range(height):
            row = []
            for x in range(width):
                # Read BGR values
                b = int.from_bytes(f.read(1), byteorder='little')
                g = int.from_bytes(f.read(1), byteorder='little')
                r = int.from_bytes(f.read(1), byteorder='little')
                row.append([b, g, r])
            
            # Skip padding bytes
            f.read(padding)
            
            # Insert at beginning to reverse bottom-to-top storage
            pixel_data.insert(0, row)
        
        return width, height, pixel_data


def get_pixel(pixel_data, x, y, width, height):
    """
    Get pixel value at (x, y) with boundary checking
    Returns [B, G, R] or [0, 0, 0] if out of bounds
    """
    if x < 0 or x >= width or y < 0 or y >= height:
        return [0, 0, 0]
    return pixel_data[y][x]
