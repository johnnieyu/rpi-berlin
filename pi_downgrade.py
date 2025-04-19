"""
Script to downgrade OpenAI package and test the older API version.
Run this to fix the OpenAI API issues on Raspberry Pi.
"""

import os
import subprocess
import sys

print("Downgrading OpenAI package to version 0.28.0...")
try:
    # Downgrade OpenAI package
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai==0.28.0"])
    print("Downgrade successful!")
    
    # Create test script with older API style
    test_script = """
import os
import base64
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables")
    exit(1)

print(f"API Key found: {api_key[:5]}...{api_key[-5:]}")

# Set the API key directly (old style)
openai.api_key = api_key

# Test image path
image_path = "data/cdmx.jpg"
if not os.path.exists(image_path):
    print(f"Error: Test image not found at {image_path}")
    print("Please provide a valid image path or create the data directory with a demo image.")
    exit(1)

# Encode image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(image_path)
print(f"Image encoded successfully: {base64_image[:20]}...")

print("\\n=== Testing with older OpenAI API (v0.28.0) ===")
try:
    # Use the old API style for ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",  # This model works with image input in v0.28
        messages=[
            {
                "role": "system",
                "content": "Write a haiku based on the image given."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please write a poem inspired by this image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    print("API call successful!")
    
    # Extract and print the poem
    poem = response['choices'][0]['message']['content']
    print("\\nGenerated poem:")
    print("-" * 40)
    print(poem)
    print("-" * 40)
    
except Exception as e:
    print(f"Error: {e}")

print("\\nTest completed.")
"""
    
    # Save the test script
    with open("old_api_test.py", "w") as f:
        f.write(test_script)
    
    print("Test script created: old_api_test.py")
    print("Run it with: python old_api_test.py")
    
except Exception as e:
    print(f"Error: {e}") 