import cv2
import numpy as np
import os

def get_unique_filename(directory, base_filename, extension):
    """ Generate a unique filename if a file with the same name exists. """
    count = 1
    new_filename = f"{base_filename}{extension}"
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base_filename}_{count}{extension}"
        count += 1
    return os.path.join(directory, new_filename)

def pencil_sketch(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print("❌ Error: Could not load image. Please check the file path.")
        return

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Enhance edges using Laplacian filter (for sharp contours)
    edges = cv2.Laplacian(gray_img, cv2.CV_8U, ksize=5)
    edges = 255 - edges  # Invert to get white strokes on black

    # Apply edge-preserving filter for details
    detail_enhanced = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.2)
    gray_detailed = cv2.cvtColor(detail_enhanced, cv2.COLOR_BGR2GRAY)

    # Invert grayscale for pencil effect
    inverted_gray = 255 - gray_detailed

    # Apply Gaussian Blur for shading
    blurred = cv2.GaussianBlur(inverted_gray, (25, 25), 0)

    # Invert the blurred image
    inverted_blurred = 255 - blurred

    # Create final pencil sketch with sharper edges
    sketch = cv2.divide(gray_detailed, inverted_blurred, scale=256.0)

    # Blend edges with the sketch
    final_sketch = cv2.addWeighted(sketch, 0.8, edges, 0.2, 0)

    # Improve contrast & sharpness
    final_sketch = cv2.convertScaleAbs(final_sketch, alpha=1.5, beta=10)

    # Ensure media directory exists
    media_dir = "media"
    os.makedirs(media_dir, exist_ok=True)

    # Generate a unique filename
    output_filename = get_unique_filename(media_dir, "realistic_pencil_sketch", ".png")

    # Save the final sketch
    cv2.imwrite(output_filename, final_sketch)

    print(f"✅ Final realistic sketch saved at: {output_filename}")

# Example usage
if __name__ == "__main__":
    image_path = input("Enter image path: ").strip()
    pencil_sketch(image_path)
