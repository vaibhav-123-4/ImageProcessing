import os
import warnings

from utils import read_gray, save_image
from noise_estimation import estimate_noise_type
from spatial_filters import apply_spatial_filter
from frequency_filters import apply_frequency_filter
from metrics import mse, psnr, compute_ssim

# hide TIFF metadata warnings
warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images")
RESULT_DIR = os.path.join(BASE_DIR, "results")

# ----- reference image -----
REF_PATH = os.path.join(IMAGE_DIR, "0.tif")
ref_img = read_gray(REF_PATH)

if ref_img is None:
    print("0.tif not found!")
    exit()


def process_image(idx):

    path = os.path.join(IMAGE_DIR, f"{idx}.tif")
    noisy = read_gray(path)

    if noisy is None:
        print(f"Image {idx} not found.")
        return

    print(f"\nProcessing Image {idx}")

    # ----- Check reference availability -----
    use_reference = (noisy.shape == ref_img.shape)

    if use_reference:
        noise_type = estimate_noise_type(ref_img, noisy)
    else:
        noise_type = "gaussian"   # fallback

    print("Estimated Noise:", noise_type)

    # ----- Apply filters -----
    spatial_out = apply_spatial_filter(noisy, noise_type)
    freq_out = apply_frequency_filter(noisy)

    # ----- Metrics -----
    if use_reference:

        psnr_sp = psnr(ref_img, spatial_out)
        psnr_fr = psnr(ref_img, freq_out)

        print("Spatial Filter Metrics:")
        print("MSE :", mse(ref_img, spatial_out))
        print("PSNR:", psnr_sp)
        print("SSIM:", compute_ssim(ref_img, spatial_out))

        print("Frequency Filter Metrics:")
        print("MSE :", mse(ref_img, freq_out))
        print("PSNR:", psnr_fr)
        print("SSIM:", compute_ssim(ref_img, freq_out))

        # best filter
        best = "Spatial" if psnr_sp > psnr_fr else "Frequency"
        print("Best Filter:", best)

    else:
        print("⚠ No reference image (different size).")
        print("PSNR/SSIM skipped for this image.")

    # ----- Save outputs -----
    save_image(os.path.join(RESULT_DIR, f"{idx}_spatial.tif"), spatial_out)
    save_image(os.path.join(RESULT_DIR, f"{idx}_frequency.tif"), freq_out)

    print(f"Saved results for {idx}")


def main():
    for i in range(1, 8):
        process_image(i)


if __name__ == "__main__":
    main()
