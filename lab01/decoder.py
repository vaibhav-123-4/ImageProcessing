import cv2
import numpy as np
import struct
import os

# Configuration mappings for resolution and bit depth
RESOLUTION_MAP = {0: 100, 1: 200, 2: 400, 3: 800}
BITDEPTH_MAP = {0: 1, 1: 2, 2: 4, 3: 8}


def decode_image(binary_file):
    """
    Decode binary file and reconstruct image.
    
    Parameters:
    - binary_file: Path to encoded binary file
    
    Returns:
    - restored_img: Reconstructed image as numpy array
    """
    with open(binary_file, "rb") as input_stream:
        # Read and parse header
        header_byte = struct.unpack('B', input_stream.read(1))[0]
        res_idx = (header_byte >> 2) & 0b11
        depth_idx = header_byte & 0b11
        
        # Extract parameters
        resolution = RESOLUTION_MAP[res_idx]
        bit_depth = BITDEPTH_MAP[depth_idx]
        total_levels = 2 ** bit_depth
        
        # Read pixel data
        raw_pixels = np.frombuffer(input_stream.read(), dtype=np.uint8)
        quantized_img = raw_pixels.reshape((resolution, resolution))
    
    # Restore to 8-bit range
    restored_img = (quantized_img.astype(np.float32) / (total_levels - 1)) * 255
    restored_img = restored_img.astype(np.uint8)
    
    print("[DECODE] Parameters extracted:")
    print(f" Resolution   = {resolution}×{resolution}")
    print(f" Bit Depth    = {bit_depth} bits")
    print(f" Gray Levels  = {total_levels}")
    
    return restored_img


def save_decoded_image(filename, image_data, output_dir="results"):
    """Save decoded image to specified directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, f"{filename}.png")
    cv2.imwrite(output_path, image_data)
    print(f"[SAVE] Image saved to {output_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("IMAGE DECODER")
    print("=" * 60)
    
    # Get encoded file path
    encoded_file = input("\nEnter the encoded file path (e.g., encoded_image.bin): ").strip()
    
    if not os.path.exists(encoded_file):
        print(f"Error: File '{encoded_file}' not found!")
        exit(1)
    
    print("\n[DECODING] Processing...")
    
    # Decode image
    reconstructed_image = decode_image(encoded_file)
    
    # Save reconstructed image
    print("\n[SAVING] Saving reconstructed image...")
    save_decoded_image("reconstructed", reconstructed_image)
    
    # Display result
    print("\n[DISPLAY] Showing reconstructed image...")
    print("Press any key in the image window to close.")
    cv2.imshow("Reconstructed Image", reconstructed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n" + "=" * 60)
    print("Decoding Complete!")
    print("=" * 60)
