# Lab 04: 2-D Discrete Fourier Transform (DFT)

## Overview
This lab implements 2-D Discrete Fourier Transform operations from scratch without using ready-made DFT/FFT functions.

## Tasks Implemented

### Task 1: Generate 8×8 2-D DFT Basis
- Generates the basis functions of an 8×8 2-D DFT
- Displays all 64 basis functions as a 64×64 image grid
- Output: `Result/dft_basis.png`

### Task 2: Create Binary Rectangle Image
- Creates a 64×64 binary image containing a rectangle
- Takes user input for:
  - Top-left corner position (row, column)
  - Width and height of the rectangle in pixels
- Output: `Result/rectangle_image.png`

### Task 3: Compute 2-D DFT for Rectangle Image
- Computes the 2-D DFT without using ready-made DFT/FFT functions
- Displays the magnitude and phase spectrum
- Output: `Result/rectangle_dft.png`

### Task 4: Compute 2-D DFT for Centered Image
- Centers the image by multiplying with (-1)^(x+y)
- Computes the 2-D DFT for the centered image
- This operation shifts the zero-frequency component to the center
- Outputs: `Result/centered_image.png`, `Result/centered_dft.png`

## Files Structure
```
lab04/
├── basis.py          # DFT basis generation functions
├── dft2d.py          # 2-D DFT implementation
├── main.py           # Main program
├── README.md         # This file
├── requirements.txt  # Required Python packages
└── Result/           # Output directory for generated images
```

## Usage

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Complete Program
```bash
python main.py
```

This will execute all four tasks sequentially:
1. Generate and save the 8×8 DFT basis
2. Prompt for rectangle parameters and create the binary image
3. Compute and display the DFT of the rectangle image
4. Compute and display the DFT of the centered image

### Run Individual Modules

#### Generate DFT Basis Only
```bash
python basis.py
```

#### Test DFT Implementation
```bash
python dft2d.py
```

## Example Input
When running the program, you'll be prompted to enter rectangle parameters:
```
Enter the top-left corner row position (0-63): 20
Enter the top-left corner column position (0-63): 20
Enter the width of the rectangle (pixels): 24
Enter the height of the rectangle (pixels): 24
```

## Implementation Details

### 2-D DFT Formula
The 2-D DFT is computed using:
```
F(u,v) = Σ Σ f(x,y) * exp(-j*2π*(ux/M + vy/N))
         x y
```

Where:
- f(x,y) is the input image
- F(u,v) is the DFT coefficient
- M, N are the dimensions of the image

### Centering Operation
The centering operation multiplies the image by (-1)^(x+y):
```
f_centered(x,y) = f(x,y) * (-1)^(x+y)
```

This shifts the zero-frequency component to the center of the spectrum.

## Output Files
All generated images are saved in the `Result/` directory:
- `dft_basis.png` - 8×8 DFT basis visualization
- `rectangle_image.png` - Binary rectangle image
- `rectangle_dft.png` - DFT analysis of rectangle image
- `centered_image.png` - Centered rectangle image
- `centered_dft.png` - DFT analysis of centered image

## Notes
- The DFT computation is implemented from scratch without using NumPy's FFT functions
- For a 64×64 image, the computation may take a few moments due to the O(N^4) complexity
- The magnitude spectrum is displayed in log scale for better visualization
- All angles are in radians
