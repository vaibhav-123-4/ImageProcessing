# Lab 02: Affine Transformations on Digital Images

## Objective
To understand and implement affine transformations on digital images by applying scaling, rotation, translation, and shearing operations without using built-in or library functions for image processing.

## Problem Statement
Design and implement a program to perform affine transformations on a given input image. The program allows users to specify transformation parameters and generates the transformed output image.

## Features
- **Scaling**: Resize image by horizontal and vertical scaling factors
- **Rotation**: Rotate image by a specified angle (in degrees)
- **Translation**: Move image horizontally and vertically
- **Shearing**: Apply horizontal and vertical shear transformations
- **Combined Transformations**: Apply multiple transformations using matrix composition
- **No Built-in Libraries**: All transformations implemented from scratch

## Implementation Details

### File Structure
```
lab02/
├── main.py              # Main program entry point
├── image_reader.py      # BMP file reading functionality
├── image_writer.py      # BMP file writing functionality
├── affine_matrix.py     # Matrix operations for transformations
├── scale.py             # Scaling transformation
├── rotate.py            # Rotation transformation
├── translate.py         # Translation transformation
├── shear.py             # Shearing transformation
├── input.bmp            # Sample input image
├── result/              # Output directory
│   └── output.bmp       # Transformed image
└── README.md            # This file
```

### Transformation Matrices

#### 1. Scaling Matrix
```
[sx   0   0]
[0   sy   0]
[0    0   1]
```
- `sx`: horizontal scaling factor
- `sy`: vertical scaling factor

#### 2. Rotation Matrix
```
[cos(θ)  -sin(θ)  0]
[sin(θ)   cos(θ)  0]
[  0        0     1]
```
- `θ`: rotation angle in radians (counter-clockwise)

#### 3. Translation Matrix
```
[1  0  tx]
[0  1  ty]
[0  0   1]
```
- `tx`: horizontal translation
- `ty`: vertical translation

#### 4. Shear Matrix
```
[1   shx  0]
[shy  1   0]
[0    0   1]
```
- `shx`: horizontal shear factor
- `shy`: vertical shear factor

### Algorithms Used

#### Backward Mapping (Inverse Transformation)
- Used for rotation, scaling, and shearing
- For each pixel in output image, finds corresponding source pixel
- Prevents holes in output image

#### Bilinear Interpolation
- Used to get smooth pixel values from non-integer coordinates
- Interpolates between 4 neighboring pixels
- Formula: `f(x,y) = f(0,0)(1-x)(1-y) + f(1,0)x(1-y) + f(0,1)(1-x)y + f(1,1)xy`

#### Matrix Composition
- Multiple transformations combined using matrix multiplication
- Order of transformations: Scale → Shear → Rotate → Translate
- Enables efficient application of complex transformations

## Usage

### Running the Program

1. **Ensure you have Python installed** (Python 3.6 or higher)

2. **Navigate to lab02 directory**:
   ```bash
   cd lab02
   ```

3. **Run the main program**:
   ```bash
   python main.py
   ```

4. **Follow the prompts**:
   - Enter input BMP file path (or press Enter for default `input.bmp`)
   - Enter transformation parameters:
     1. Horizontal scaling factor
     2. Vertical scaling factor
     3. Rotation angle (degrees)
     4. Horizontal translation
     5. Vertical translation
     6. Horizontal shear factor
     7. Vertical shear factor
   - Press Enter to use default value (identity transformation)

5. **Output**:
   - Transformed image saved to `result/output.bmp`
   - Transformation matrices displayed in console

### Example Usage

```
AFFINE TRANSFORMATION PROGRAM
============================================================

Enter input BMP file path (default: input.bmp): input.bmp

Reading image: input.bmp
Image size: 400 x 300 pixels

------------------------------------------------------------
TRANSFORMATION PARAMETERS
------------------------------------------------------------

1. Horizontal scaling factor (default: 1.0): 1.5
2. Vertical scaling factor (default: 1.0): 1.5
3. Rotation angle in degrees (default: 0.0): 45
4. Horizontal translation (default: 0.0): 50
5. Vertical translation (default: 0.0): 50
6. Horizontal shear factor (default: 0.0): 0.2
7. Vertical shear factor (default: 0.0): 0.0

Applying affine transformation...
Output image size: 800 x 750 pixels

Writing output image: result/output.bmp

TRANSFORMATION COMPLETED SUCCESSFULLY!
```

## Input Requirements

- **Image Format**: 24-bit BMP (Bitmap) files
- **File Extension**: `.bmp`
- **Color Format**: BGR (Blue, Green, Red)

## Key Implementation Notes

1. **No External Libraries**: 
   - No NumPy, PIL, OpenCV, or similar libraries used
   - Only standard Python libraries (math, os)
   - All algorithms implemented from scratch

2. **BMP File Handling**:
   - Manual parsing of BMP headers
   - Handling of row padding (BMP rows are 4-byte aligned)
   - Bottom-to-top pixel storage order

3. **Transformation Quality**:
   - Bilinear interpolation for smooth results
   - Backward mapping to avoid holes
   - Dynamic canvas sizing to fit transformed image

4. **Edge Cases Handled**:
   - Out-of-bounds pixel access returns black [0,0,0]
   - Singular matrix detection for shear inverse
   - Division by zero protection

## Testing

Test the program with various parameters:

1. **Identity Test**: All parameters at default (should produce identical image)
2. **Scaling Test**: `sx=2.0, sy=2.0` (doubles image size)
3. **Rotation Test**: `angle=90` (rotates 90 degrees)
4. **Translation Test**: `tx=100, ty=100` (moves image)
5. **Shear Test**: `shx=0.5` (horizontal shear)
6. **Combined Test**: Multiple transformations together

## Limitations

- Only supports 24-bit BMP files
- Large transformations may require significant memory
- Processing time increases with image size and transformation complexity

## Mathematical Background

Affine transformations preserve:
- Parallelism of lines
- Ratios of distances along lines
- Collinearity of points

General affine transformation in homogeneous coordinates:
```
[x']   [a  b  c] [x]
[y'] = [d  e  f] [y]
[1 ]   [0  0  1] [1]
```

Where transformation can decompose into:
- Linear transformation: rotation, scaling, shearing
- Translation: moving image position

## Author
Lab 02 - Image Processing Course

## Date
January 2026
