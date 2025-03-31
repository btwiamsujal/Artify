import requests
import os

def image_to_sketch(image_path, api_key):
    # Ensure the input path is valid
    image_path = image_path.strip("\"")

    # API endpoint (RapidAPI - Pencil Sketch Image Generation)
    url = "https://pencil-sketch-image-generation.p.rapidapi.com/api/v1/image"

    # Read image file
    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}

        headers = {
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': 'pencil-sketch-image-generation.p.rapidapi.com'
        }

        # Send image to API
        response = requests.post(url, files=files, headers=headers)

    # Parse response
    if response.status_code == 200:
        result = response.json()
        if 'output_url' in result:
            output_url = result['output_url']

            # Define output directory
            output_dir = "D:/Images/Sketches"
            os.makedirs(output_dir, exist_ok=True)

            # Define output file name
            output_path = os.path.join(output_dir, os.path.basename(image_path).replace('.jpg', '_sketch.jpg'))

            # Download and save the sketch
            sketch_image = requests.get(output_url).content
            with open(output_path, 'wb') as file:
                file.write(sketch_image)

            print(f"✅ Sketch saved successfully at: {output_path}")
        else:
            print("❌ Error: API response does not contain 'output_url'.", result)
    else:
        print(f"❌ API request failed with status code {response.status_code}: {response.text}")

# Example usage
if __name__ == "__main__":
    image_path = input("Upload an image (Enter the path): ").strip()
    api_key = "2660f99034msha63badb1394d9cdp1497c4jsn068088a15694"  # Replace with your actual RapidAPI key
    image_to_sketch(image_path, api_key)
