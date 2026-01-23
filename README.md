# Image Encoder/Decoder

A Python application for image encoding and decoding with customizable spatial and intensity resolution.

## Features

- **Image Preprocessing**: Converts images to grayscale and crops to center square
- **Spatial Resolution Control**: Choose from 100×100, 200×200, 400×400, or 800×800 pixels
- **Intensity Quantization**: Select 1-bit, 2-bit, 4-bit, or 8-bit depth
- **Custom Binary Format**: 4-bit header + quantized pixel data
- **Image Reconstruction**: Decode and display compressed images

## File Structure

```
ImageProcessing/
├── encoder.py           # Image encoding module
├── decoder.py           # Image decoding module
├── demo.py              # Complete demo pipeline
├── image.png            # Sample input image
├── encoded_image.bin    # Encoded binary output
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Run Complete Demo
```bash
python demo.py
```
This runs the complete encoding/decoding pipeline with preset configurations.

### Option 2: Manual Encoding and Decoding

#### Encode an Image
```bash
python encoder.py
```
Follow the prompts to:
1. Enter image file path
2. Select spatial resolution (0-3)
3. Select bit depth (0-3)

Output: `encoded_image.bin`

#### Decode an Image
```bash
python decoder.py
```
Follow the prompts to:
1. Enter encoded file path

Output: `results/reconstructed.png`

## How It Works

### Encoding Process
1. **Load & Preprocess**: Read image, convert to grayscale, crop to center square
2. **Spatial Sampling**: Resize to selected resolution (100/200/400/800 pixels)
3. **Intensity Quantization**: Reduce to selected bit depth (1/2/4/8 bits)
4. **Create Header**: 4-bit header (2 bits resolution + 2 bits depth)
5. **Write Binary**: Save header + quantized pixel data

### Custom File Format
```
[Header Byte] [Pixel Data...]
     |              |
     |              └── Quantized image pixels
     |
     └── First 2 bits: Spatial resolution index (0-3)
         Next 2 bits: Bit depth index (0-3)
```

### Decoding Process
1. **Read Header**: Extract resolution and bit depth from 4-bit header
2. **Read Pixels**: Load quantized pixel data
3. **Reconstruct**: Dequantize to 8-bit grayscale
4. **Display**: Show reconstructed image

## Configuration Options

### Spatial Resolution
- **0**: 100 × 100 pixels
- **1**: 200 × 200 pixels
- **2**: 400 × 400 pixels
- **3**: 800 × 800 pixels

### Intensity Depth
- **0**: 1 bit (2 gray levels)
- **1**: 2 bits (4 gray levels)
- **2**: 4 bits (16 gray levels)
- **3**: 8 bits (256 gray levels)

## Example

```python
from encoder import encode_image
from decoder import decode_image

# Encode image with 400×400 resolution and 4-bit depth
encode_image("image.png", res_idx=2, depth_idx=2, target_file="encoded_image.bin")

# Decode and display
reconstructed = decode_image("encoded_image.bin")
```

## Output

- **encoded_image.bin**: Compressed binary file
- **results/reconstructed.png**: Decoded image
- **Compression info**: File size comparison and compression ratio

## Notes

- Images are automatically converted to grayscale
- Center cropping ensures square images
- Higher resolution and bit depth = larger file size, better quality
- Lower resolution and bit depth = smaller file size, lower quality

## Author

Image Processing Project
