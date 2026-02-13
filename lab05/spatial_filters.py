import cv2

def apply_spatial_filter(img, noise_type):

    if noise_type == "salt_pepper":
        return cv2.medianBlur(img, 3)

    elif noise_type == "gaussian":
        return cv2.GaussianBlur(img, (5, 5), 1.0)

    elif noise_type == "speckle":
        return cv2.bilateralFilter(img, 9, 75, 75)

    return img
