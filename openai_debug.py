"""
Debug script for OpenAI API calls.
This script tests different configurations for the OpenAI API to identify a working setup.
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

# Test different OpenAI configurations
def test_openai_config(config_num, client_init_func, api_call_func, model="gpt-4.1-mini"):
    """Test a specific OpenAI configuration."""
    print(f"\n=== Testing Configuration {config_num} ===")
    
    try:
        # Initialize client
        print(f"Initializing client with: {client_init_func.__name__}")
        client = client_init_func(api_key)
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
        print(f"Making API call with: {api_call_func.__name__}")
        print(f"Using model: {model}")
        
        response = api_call_func(client, model, messages)
        print("API call successful!")
        
        # Extract and print the poem
        poem = response.choices[0].message.content
        print("\nGenerated poem:")
        print("-" * 40)
        print(poem)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

# Configuration 1: Latest API style with OpenAI client
def init_latest(api_key):
    return openai.OpenAI(api_key=api_key)

def call_latest(client, model, messages):
    return client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=300
    )

# Configuration 2: Latest API style with direct initialization
def init_direct(api_key):
    openai.api_key = api_key
    return openai

def call_direct(client, model, messages):
    return client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=300
    )

# Configuration 3: Older API style
def init_old(api_key):
    openai.api_key = api_key
    return openai

def call_old(client, model, messages):
    return client.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=300
    )

# Run tests
print("\nTesting OpenAI API configurations...")

# Test with gpt-4.1-mini
print("\n=== Testing with gpt-4.1-mini model ===")
test_openai_config(1, init_latest, call_latest, "gpt-4.1-mini")
test_openai_config(2, init_direct, call_direct, "gpt-4.1-mini")
test_openai_config(3, init_old, call_old, "gpt-4.1-mini")

# Test with gpt-4-vision-preview
print("\n=== Testing with gpt-4-vision-preview model ===")
test_openai_config(4, init_latest, call_latest, "gpt-4-vision-preview")
test_openai_config(5, init_direct, call_direct, "gpt-4-vision-preview")
test_openai_config(6, init_old, call_old, "gpt-4-vision-preview")

print("\nDebug tests completed.") 