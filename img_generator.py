import requests
import json
import os
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_image(prompt, model='runwayml/stable-diffusion-v1-5'):
    api_key = os.getenv("RunwayAPI")
    if not api_key:
        print("Error: Runway API key not found in .env file.")
        return
    
    url = f"https://api.runwayml.com/v1/models/{model}/generate"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"prompt": prompt}
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        os.makedirs("media", exist_ok=True)  # Ensure the media folder exists
        filename = f"media/{uuid.uuid4()}.png"  # Generate a unique filename
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Image saved as {filename}")
    else:
        print("Error:", response.json())

# Usage
prompt = input("Enter a prompt: ")
generate_image(prompt)