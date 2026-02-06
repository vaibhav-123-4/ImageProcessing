# Lab03: Intensity Transformations and Spatial Filtering

**Digital Image Processing – Chapter 3 Assignment (Gonzalez & Woods)**

## Objective

Apply intensity transformations, histogram processing, and spatial filtering operations to all images in a folder.

All images inside the input folder are processed automatically and the results are stored in the "result" folder.

## Folder Structure

```
lab03/
│
├── DIP3E_Original_Images_CH03/  # Input images folder
├── result/                      # Output folder (created automatically)
│
├── part1_intensity.py           # Intensity transformations
├── part2_histogram.py           # Histogram processing
├── part3_spatial.py             # Spatial filtering
├── part4_mixed.py               # Mixed enhancement
├── run_all.py                   # Main script
└── readme.md                    # This file
```

## How to Run

```bash
python run_all.py
```

The script will automatically:
1. Find all images in `DIP3E_Original_Images_CH03/` folder
2. Process each image with all transformations
3. Save results to `result/` folder

## Part 1 – Intensity Transformations

- **Log transformation**: Enhances dark regions
- **Gamma correction**: 6 different gamma values (γ = 0.6, 0.4, 0.3, 3, 4, 5)
  - γ < 1: Brightens the image
  - γ > 1: Darkens the image
- **Bit-plane slicing**: Extracts all 8 bit planes (0 to 7)

## Part 2 – Histogram Processing

- **Global histogram equalization**: Manual implementation (no built-in functions)
  - Computes histogram, PDF, and CDF manually
  - Applies transformation for contrast enhancement
- **Local histogram equalization**: Manual implementation using a 3×3 window
  - Enhances local contrast
  - Better for images with varying illumination

## Part 3 – Spatial Filtering

- **Box (mean) filtering**: 3×3 and 5×5 kernels
  - Smooths the image
  - Reduces noise
- **Gaussian filtering**: 5×5 kernel with σ = 1.0
  - Weighted smoothing
  - Better edge preservation than box filter
- **Laplacian sharpening**: Enhances edges
  - Formula: g(x,y) = f(x,y) + c∇²f(x,y)
- **Unsharp masking**: Edge enhancement technique
  - Formula: g(x,y) = f(x,y) + k(f(x,y) - f_blur(x,y))

## Part 4 – Mixed Spatial Enhancement

Combination of multiple operations:
- Laplacian operator
- Sobel gradient magnitude
- Gamma correction (γ = 0.8)

This produces enhanced images with sharpened edges and improved contrast.

## Processing Details

- All images are read from the input folder automatically
- All processing is done in **grayscale**
- **No built-in histogram equalization functions** are used
- Global and local histogram equalization are **implemented manually**
- All output files overwrite automatically if they already exist

## Output

All results are saved in the `result/` folder with the following naming format:

```
<image>_log.png
<image>_gamma_0.6.png
<image>_gamma_0.4.png
<image>_gamma_0.3.png
<image>_gamma_3.0.png
<image>_gamma_4.0.png
<image>_gamma_5.0.png
<image>_bit_0.png
<image>_bit_1.png
...
<image>_bit_7.png
<image>_hist_eq.png
<image>_local_hist_eq.png
<image>_box3.png
<image>_box5.png
<image>_gauss5.png
<image>_laplacian.png
<image>_unsharp.png
<image>_mixed.png
```

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy

Install dependencies:
```bash
pip install opencv-python numpy
```

## Example Usage

1. Place your images in the `DIP3E_Original_Images_CH03/` folder
2. Run the script:
   ```bash
   python run_all.py
   ```
3. Check the `result/` folder for processed images

## Notes

- The script processes all image formats: PNG, JPG, JPEG, BMP, TIF, TIFF
- Images are automatically converted to grayscale
- Processing time depends on image size and number of images
- All output images are in PNG format for quality preservation

## Technical Details

### Histogram Equalization Algorithm

**Global Histogram Equalization:**
1. Compute histogram: `hist[k] = number of pixels with intensity k`
2. Compute PDF: `pdf[k] = hist[k] / (M × N)`
3. Compute CDF: `cdf[k] = sum(pdf[0] to pdf[k])`
4. Transform: `output[i,j] = round(255 × cdf[input[i,j]])`

**Local Histogram Equalization:**
- Same as global but applied to each 3×3 window independently
- Better for images with varying local contrast

### Spatial Filtering

- **Box filter**: Simple averaging with equal weights
- **Gaussian filter**: Weighted averaging (closer pixels have higher weights)
- **Laplacian**: Second-order derivative operator for edge detection
- **Unsharp masking**: Original + k × (Original - Blurred)

## Author

Lab03 - Image Processing Course
Indian Institute of Information Technology, Vadodara (IIITV)
