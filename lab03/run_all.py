import os
import cv2

from part1_intensity import log_transform, gamma_correction, bit_planes
from part2_histogram import global_hist_eq, local_hist_eq
from part3_spatial import box_filter, gaussian_filter, laplacian_sharpen, unsharp_mask
from part4_mixed import mixed_enhancement


INPUT_FOLDER = "DIP3E_Original_Images_CH03"
OUTPUT_FOLDER = "result"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("=" * 60)
print("LAB03: INTENSITY TRANSFORMATIONS AND SPATIAL FILTERING")
print("=" * 60)

# Get list of image files
image_files = [f for f in os.listdir(INPUT_FOLDER) 
               if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"))]

if not image_files:
    print(f"\nError: No image files found in '{INPUT_FOLDER}' folder!")
    print("Please add some images to the folder and try again.")
    exit(1)

print(f"\nFound {len(image_files)} image(s) to process")
print(f"Input folder: {INPUT_FOLDER}")
print(f"Output folder: {OUTPUT_FOLDER}")
print("\nProcessing images...\n")

processed_count = 0

for fname in image_files:
    path = os.path.join(INPUT_FOLDER, fname)
    
    # Read image in grayscale
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"⚠ Skipping {fname} (could not read)")
        continue
    
    name, _ = os.path.splitext(fname)
    print(f"Processing: {fname}")
    
    # ---------- Part 1: Intensity Transformations ----------
    # Log transformation
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{name}_log.png"),
                log_transform(img))
    
    # Gamma corrections (6 different gamma values)
    for g in [0.6, 0.4, 0.3, 3.0, 4.0, 5.0]:
        cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{name}_gamma_{g}.png"),
                    gamma_correction(img, g))
    
    # Bit-plane slicing (8 planes)
    planes = bit_planes(img)
    for i, p in enumerate(planes):
        cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{name}_bit_{i}.png"), p)
    
    # ---------- Part 2: Histogram Processing ----------
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{name}_hist_eq.png"),
                global_hist_eq(img))
    
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{name}_local_hist_eq.png"),
                local_hist_eq(img))
    
    # ---------- Part 3: Spatial Filtering ----------
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{name}_box3.png"),
                box_filter(img, 3))
    
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{name}_box5.png"),
                box_filter(img, 5))
    
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{name}_gauss5.png"),
                gaussian_filter(img, 5, 1.0))
    
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{name}_laplacian.png"),
                laplacian_sharpen(img))
    
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{name}_unsharp.png"),
                unsharp_mask(img))
    
    # ---------- Part 4: Mixed Spatial Enhancement ----------
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"{name}_mixed.png"),
                mixed_enhancement(img))
    
    processed_count += 1
    print(f"  ✓ Completed ({processed_count}/{len(image_files)})")

print("\n" + "=" * 60)
print(f"PROCESSING COMPLETE!")
print(f"Total images processed: {processed_count}")
print(f"Results saved in: {OUTPUT_FOLDER}/")
print("=" * 60)
