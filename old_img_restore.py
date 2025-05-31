import cv2
import numpy as np

def restore_old_image(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found.")
        return
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    kernel_sharpening = np.array([[0, -1, 0],
                                  [-1, 5,-1],
                                  [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel_sharpening)
    equalized = cv2.equalizeHist(sharpened)
    cv2.imwrite(output_path, equalized)
    print(f"Restored image saved to {output_path}")

if __name__ == "__main__":
    restore_old_image("old_photo.jpg", "restored_photo.jpg")
