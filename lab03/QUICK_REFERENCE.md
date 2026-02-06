# Lab03 Quick Reference Guide

## File Descriptions

### Core Implementation Files

**part1_intensity.py**
- `log_transform(img)` - Logarithmic transformation
- `gamma_correction(img, gamma)` - Power-law transformation
- `bit_planes(img)` - Extracts all 8 bit planes

**part2_histogram.py**
- `global_hist_eq(img)` - Manual global histogram equalization
- `local_hist_eq(img)` - Manual local histogram equalization (3×3 window)

**part3_spatial.py**
- `box_filter(img, k)` - Box (mean) filter with kernel size k
- `gaussian_filter(img, k, sigma)` - Gaussian blur
- `laplacian_sharpen(img, c)` - Laplacian edge enhancement
- `unsharp_mask(img, k)` - Unsharp masking

**part4_mixed.py**
- `mixed_enhancement(img)` - Combined Laplacian + Sobel + Gamma

### Main Script

**run_all.py**
- Automatically finds all images in input folder
- Processes each image with all 23 transformations
- Saves results with descriptive filenames
- Shows progress during processing

## Usage Examples

### Process All Images
```bash
python run_all.py
```

### Use Individual Functions
```python
import cv2
from part1_intensity import log_transform, gamma_correction, bit_planes

# Read image
img = cv2.imread('image.tif', cv2.IMREAD_GRAYSCALE)

# Apply log transformation
log_img = log_transform(img)
cv2.imwrite('output_log.png', log_img)

# Apply gamma correction
gamma_img = gamma_correction(img, 0.5)  # Brighten
cv2.imwrite('output_gamma.png', gamma_img)

# Extract bit planes
planes = bit_planes(img)
for i, plane in enumerate(planes):
    cv2.imwrite(f'bit_plane_{i}.png', plane)
```

### Histogram Equalization
```python
from part2_histogram import global_hist_eq, local_hist_eq

# Global histogram equalization
eq_global = global_hist_eq(img)
cv2.imwrite('global_eq.png', eq_global)

# Local histogram equalization
eq_local = local_hist_eq(img)
cv2.imwrite('local_eq.png', eq_local)
```

### Spatial Filtering
```python
from part3_spatial import box_filter, gaussian_filter, laplacian_sharpen, unsharp_mask

# Smoothing filters
smooth_box = box_filter(img, 5)
smooth_gauss = gaussian_filter(img, 5, 1.0)

# Sharpening filters
sharp_lap = laplacian_sharpen(img, c=1.0)
sharp_unsharp = unsharp_mask(img, k=1.5)
```

## Output Statistics

**Total transformations per image:** 23
- 1 log transformation
- 6 gamma corrections (0.6, 0.4, 0.3, 3.0, 4.0, 5.0)
- 8 bit planes (0-7)
- 1 global histogram equalization
- 1 local histogram equalization
- 2 box filters (3×3, 5×5)
- 1 Gaussian filter
- 1 Laplacian sharpening
- 1 unsharp masking
- 1 mixed enhancement

**For your 28 images:** 28 × 23 = 644 output files ✓

## Key Features

✅ **Manual Histogram Equalization**
- No built-in cv2.equalizeHist() used
- Full implementation with histogram, PDF, CDF computation

✅ **Batch Processing**
- Automatically processes all images in folder
- Supports PNG, JPG, JPEG, BMP, TIF, TIFF formats

✅ **Descriptive Naming**
- Output files clearly indicate transformation applied
- Easy to identify and compare results

✅ **Progress Tracking**
- Shows which image is being processed
- Displays completion count

## Common Operations

### Gamma Values Guide
- **γ < 1** (e.g., 0.4, 0.6): Brightens image, expands dark regions
- **γ = 1**: No change (identity transformation)
- **γ > 1** (e.g., 3.0, 4.0, 5.0): Darkens image, compresses bright regions

### Bit Plane Information
- **Bit 7** (MSB): Most significant, major intensity variations
- **Bit 0** (LSB): Least significant, fine details/noise

### Filter Applications
- **Box filter**: Fast smoothing, removes noise
- **Gaussian filter**: Better edge preservation than box filter
- **Laplacian**: Edge detection and sharpening
- **Unsharp masking**: Professional sharpening technique

## Troubleshooting

**No images processed?**
- Check folder name: `DIP3E_Original_Images_CH03`
- Ensure images have valid extensions
- Verify read permissions

**Import errors?**
- Run: `pip install -r requirements.txt`
- Ensure Python 3.x is installed

**Output folder missing?**
- Created automatically by run_all.py
- Manual creation: `mkdir result`

## Mathematical Formulas

### Log Transform
```
s = c × log(1 + r)
```

### Gamma Correction
```
s = c × r^γ
```

### Histogram Equalization
```
s = T(r) = (L-1) × CDF(r)
where CDF(k) = Σ(i=0 to k) P(i)
```

### Laplacian Sharpening
```
g(x,y) = f(x,y) + c × ∇²f(x,y)
```

### Unsharp Masking
```
g(x,y) = f(x,y) + k × (f(x,y) - blur(x,y))
```

---

**Ready to process your images!** Just run `python run_all.py` 🚀
