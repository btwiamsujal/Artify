import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance

def get_unique_filename(directory, base_filename, extension):
    """ Generate a unique filename if a file with the same name exists. """
    count = 1
    new_filename = f"{base_filename}{extension}"
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base_filename}_{count}{extension}"
        count += 1
    return os.path.join(directory, new_filename)

def enhance_image(image_path):
    """ Enhance image using OpenCV and PIL (local processing). """
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            print("❌ Error: Could not load image. Please check the file path.")
            return
        
        # Convert to grayscale and apply CLAHE for contrast enhancement
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        lab = cv2.merge((l, a, b))
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Apply bilateral filter for noise reduction
        img = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
        
        # Convert to PIL for sharpness and brightness enhancement
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Sharpness(pil_img)
        pil_img = enhancer.enhance(2.0)  # Increase sharpness
        
        enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = enhancer.enhance(1.2)  # Slightly increase brightness
        
        # Convert back to OpenCV format
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        
        # Ensure output directory exists
        output_dir = "enhanced_images"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate a unique filename and save
        output_filename = get_unique_filename(output_dir, "enhanced_image", ".jpg")
        cv2.imwrite(output_filename, img)
        
        print(f"✅ Enhanced image saved at: {output_filename}")
    except Exception as e:
        print(f"❌ Exception: {e}")

# Example usage
if __name__ == "__main__":
    image_path = input("Enter image path: ").strip()
    enhance_image(image_path)
