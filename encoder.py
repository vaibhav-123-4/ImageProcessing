import cv2
import numpy as np
import struct
import os

# Configuration mappings for resolution and bit depth
RESOLUTION_MAP = {0: 100, 1: 200, 2: 400, 3: 800}
BITDEPTH_MAP = {0: 1, 1: 2, 2: 4, 3: 8}


def prepare_square_grayscale(filepath):
    """Read image and convert to center-cropped grayscale square."""
    grayscale_img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    height, width = grayscale_img.shape
    
    # Calculate square dimensions from shorter side
    crop_size = min(height, width)
    y_offset = (height - crop_size) // 2
    x_offset = (width - crop_size) // 2
    
    cropped = grayscale_img[y_offset:y_offset+crop_size, x_offset:x_offset+crop_size]
    return cropped


def apply_quantization(image_array, bit_depth):
    """Reduce intensity levels based on bit depth."""
    num_levels = 2 ** bit_depth
    normalized = image_array.astype(np.float32) / 255.0
    quantized = np.round(normalized * (num_levels - 1)).astype(np.uint8)
    return quantized


def encode_image(source_path, res_idx, depth_idx, target_file):
    """
    Compress and encode image to binary format.
    
    Parameters:
    - source_path: Path to input image
    - res_idx: Resolution index (0-3)
    - depth_idx: Bit depth index (0-3)
    - target_file: Output binary file path
    """
    processed_img = prepare_square_grayscale(source_path)
    
    # Resize to target resolution
    target_res = RESOLUTION_MAP[res_idx]
    scaled_img = cv2.resize(processed_img, (target_res, target_res), 
                           interpolation=cv2.INTER_AREA)
    
    # Apply bit depth quantization
    bit_depth = BITDEPTH_MAP[depth_idx]
    quantized_data = apply_quantization(scaled_img, bit_depth)
    
    # Create header byte (4 bits total: 2 for resolution + 2 for bit depth)
    header_byte = (res_idx << 2) | depth_idx
    
    # Write binary file
    with open(target_file, "wb") as output:
        output.write(struct.pack('B', header_byte))
        output.write(quantized_data.tobytes())
    
    print(f"[ENCODE] Output written to → {target_file}")
    return True


def get_encoder_inputs():
    """Get user inputs for encoding parameters."""
    print("=" * 60)
    print("IMAGE ENCODER")
    print("=" * 60)
    
    # Get image path
    input_image = input("\nEnter the image file path (e.g., image.png): ").strip()
    
    if not os.path.exists(input_image):
        print(f"Error: File '{input_image}' not found!")
        return None, None, None
    
    # Display spatial resolution options
    print("\n" + "-" * 60)
    print("SPATIAL RESOLUTION SELECTION (Sampling)")
    print("-" * 60)
    print("Select one of the following spatial resolutions:")
    print("  [0] 100 × 100 pixels")
    print("  [1] 200 × 200 pixels")
    print("  [2] 400 × 400 pixels")
    print("  [3] 800 × 800 pixels")
    
    while True:
        try:
            resolution_idx = int(input("\nEnter your choice (0-3): ").strip())
            if resolution_idx in RESOLUTION_MAP:
                break
            else:
                print("Invalid choice! Please enter a number between 0 and 3.")
        except ValueError:
            print("Invalid input! Please enter a number.")
    
    # Display intensity depth options
    print("\n" + "-" * 60)
    print("INTENSITY RESOLUTION SELECTION (Quantization)")
    print("-" * 60)
    print("Select the pixel intensity depth:")
    print("  [0] 1 bit  (2 gray levels)")
    print("  [1] 2 bits (4 gray levels)")
    print("  [2] 4 bits (16 gray levels)")
    print("  [3] 8 bits (256 gray levels)")
    
    while True:
        try:
            bitdepth_idx = int(input("\nEnter your choice (0-3): ").strip())
            if bitdepth_idx in BITDEPTH_MAP:
                break
            else:
                print("Invalid choice! Please enter a number between 0 and 3.")
        except ValueError:
            print("Invalid input! Please enter a number.")
    
    print("\n" + "=" * 60)
    print(f"Configuration Summary:")
    print(f"  Image: {input_image}")
    print(f"  Resolution: {RESOLUTION_MAP[resolution_idx]} × {RESOLUTION_MAP[resolution_idx]} pixels")
    print(f"  Bit Depth: {BITDEPTH_MAP[bitdepth_idx]} bits ({2**BITDEPTH_MAP[bitdepth_idx]} gray levels)")
    print("=" * 60 + "\n")
    
    return input_image, resolution_idx, bitdepth_idx


if __name__ == "__main__":
    # Get user inputs
    input_image, resolution_idx, bitdepth_idx = get_encoder_inputs()
    
    if input_image is None:
        exit(1)
    
    # Encoding phase
    print("\n[ENCODING] Processing...")
    print(f"  - Loading and preprocessing: {input_image}")
    print(f"  - Cropping to center square")
    print(f"  - Resizing to {RESOLUTION_MAP[resolution_idx]}×{RESOLUTION_MAP[resolution_idx]}")
    print(f"  - Quantizing to {BITDEPTH_MAP[bitdepth_idx]}-bit depth")
    
    encode_image(input_image, resolution_idx, bitdepth_idx, "encoded_image.bin")
    
    print("\n" + "=" * 60)
    print("Encoding Complete!")
    print("=" * 60)
