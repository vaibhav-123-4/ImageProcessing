import cv2
import os
from encoder import encode_image, RESOLUTION_MAP, BITDEPTH_MAP
from decoder import decode_image, save_decoded_image


def run_demo():
    """
    Demo script showing the complete encoding and decoding pipeline.
    Interactive mode - asks user for all parameters.
    """
    print("=" * 60)
    print("IMAGE ENCODER/DECODER DEMO")
    print("=" * 60)
    
    # Step 1: Get image path from user
    print("\n[STEP 1] IMAGE INPUT AND PREPROCESSING")
    input_image = input("\nEnter the image file path (e.g., image.png): ").strip()
    
    if not os.path.exists(input_image):
        print(f"Error: File '{input_image}' not found!")
        return
    
    print(f"✓ Image loaded: {input_image}")
    print("✓ Will convert to grayscale and crop to center square")
    
    # Step 2: Spatial Resolution Selection
    print("\n[STEP 2] SPATIAL RESOLUTION SELECTION (Sampling)")
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
    
    print(f"✓ Selected resolution: {RESOLUTION_MAP[resolution_idx]} × {RESOLUTION_MAP[resolution_idx]} pixels")
    
    # Step 3: Intensity Resolution Selection
    print("\n[STEP 3] INTENSITY RESOLUTION SELECTION (Quantization)")
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
    
    print(f"✓ Selected bit depth: {BITDEPTH_MAP[bitdepth_idx]} bits ({2**BITDEPTH_MAP[bitdepth_idx]} gray levels)")
    
    print("\n" + "=" * 60)
    print("Configuration Summary:")
    print(f"  Image: {input_image}")
    print(f"  Resolution: {RESOLUTION_MAP[resolution_idx]} × {RESOLUTION_MAP[resolution_idx]} pixels")
    print(f"  Bit Depth: {BITDEPTH_MAP[bitdepth_idx]} bits ({2**BITDEPTH_MAP[bitdepth_idx]} gray levels)")
    print("=" * 60)
    
    # Step 4: Image Encoding Algorithm
    print("\n[STEP 4] IMAGE ENCODING ALGORITHM")
    print("Applying spatial sampling and intensity quantization...")
    print(f"  - Loading and preprocessing: {input_image}")
    print(f"  - Converting to grayscale and cropping to center square")
    print(f"  - Applying spatial sampling: Resizing to {RESOLUTION_MAP[resolution_idx]}×{RESOLUTION_MAP[resolution_idx]}")
    print(f"  - Applying intensity quantization: {BITDEPTH_MAP[bitdepth_idx]}-bit depth")
    
    # Step 5: Custom File Format Design & Step 6: Save encoded file
    print("\n[STEP 5] CUSTOM FILE FORMAT DESIGN")
    print("Creating 4-bit header:")
    print(f"  - First 2 bits: Spatial resolution index = {resolution_idx}")
    print(f"  - Next 2 bits: Bit depth index = {bitdepth_idx}")
    print("  - Remaining data: Quantized image pixels")
    
    print("\n[STEP 6] SAVING ENCODED FILE")
    encode_image(input_image, resolution_idx, bitdepth_idx, "encoded_image.bin")
    
    # Step 7: Image Decoding Algorithm
    print("\n[STEP 7] IMAGE DECODING ALGORITHM")
    print("Reading custom binary file...")
    print("  - Extracting spatial resolution and intensity depth from header")
    reconstructed_image = decode_image("encoded_image.bin")
    
    print("\n[SAVING] Saving reconstructed image...")
    save_decoded_image("reconstructed", reconstructed_image)
    
    print("\n[DISPLAY] Displaying reconstructed image...")
    print("Press any key in the image window to close.")
    cv2.imshow("Reconstructed Image", reconstructed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Display file size info
    original_size = os.path.getsize(input_image)
    encoded_size = os.path.getsize("encoded_image.bin")
    compression_ratio = (1 - encoded_size / original_size) * 100
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("-" * 60)
    print(f"Original File Size:   {original_size:,} bytes")
    print(f"Encoded File Size:    {encoded_size:,} bytes")
    print(f"Compression Ratio:    {compression_ratio:.2f}%")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
