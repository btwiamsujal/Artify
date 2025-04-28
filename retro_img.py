from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np

def make_retro_oldmoney():
    # Take input from user
    image_path = input("Upload an image (Enter the path): ")
    output_path = input("Enter output filename (e.g., output_retro.jpg): ")
    
    # Load image
    img = Image.open(image_path).convert('RGB')
    
    # 1. Reduce Saturation
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.5)  # 0.5 means 50% saturation
    
    # 2. Warm Filter (yellowish tone)
    r, g, b = img.split()
    r = r.point(lambda i: min(255, i * 1.1))  # boost red
    g = g.point(lambda i: min(255, i * 1.05)) # boost green slightly
    img = Image.merge('RGB', (r, g, b))
    
    # 3. Add slight blur to soften image
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Convert to numpy for further edits
    img_cv = np.array(img)

    # 4. Add grain (noise) safely
    noise = np.random.normal(0, 10, img_cv.shape).astype(np.int16)
    img_cv = np.clip(img_cv + noise, 0, 255).astype(np.uint8)

    # 5. Add vignette properly
    rows, cols = img_cv.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, cols/3)  # /3 gives lighter vignette
    kernel_y = cv2.getGaussianKernel(rows, rows/3)
    kernel = kernel_y * kernel_x.T
    mask = kernel / np.max(kernel)  # normalize mask between 0 and 1

    vignette = np.empty_like(img_cv)
    for i in range(3):  # for each channel
        vignette[:,:,i] = img_cv[:,:,i] * mask

    # Convert back to PIL
    final_img = Image.fromarray(np.uint8(vignette))

    # Save the output
    final_img.save(output_path)
    print(f"Retro/Old-money image saved at {output_path}")

# Call the function
make_retro_oldmoney()
