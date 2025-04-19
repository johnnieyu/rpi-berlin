"""
Test script for OpenAI API with proxy fix.
"""

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

# Test image path
image_path = "data/cdmx.jpg"
if not os.path.exists(image_path):
    print(f"Error: Test image not found at {image_path}")
    print("Please provide a valid image path or create the data directory with a demo image.")
    exit(1)

# Encode image
def encode_image(image_path):
    """Convert image to base64 string for OpenAI API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(image_path)
print(f"Image encoded successfully: {base64_image[:20]}...")

print("\n=== Testing with http_client=None Fix ===")
try:
    # Initialize with http_client=None to fix the proxies issue
    client = openai.OpenAI(
        api_key=api_key,
        http_client=None
    )
    print("Client initialized successfully")
    
    # Create messages
    messages = [
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
    ]
    
    # Make API call
    print("Making API call with model: gpt-4.1-mini")
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        max_tokens=300
    )
    print("API call successful!")
    
    # Extract and print the poem
    poem = response.choices[0].message.content
    print("\nGenerated poem:")
    print("-" * 40)
    print(poem)
    print("-" * 40)
    
except Exception as e:
    print(f"Error: {e}")

print("\nTest completed.") 