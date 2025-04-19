"""
Fix for OpenAI client initialization with 'proxies' error.
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

# Check for environment variables that might be causing the 'proxies' error
print("\nChecking environment variables:")
proxy_vars = ["http_proxy", "https_proxy", "all_proxy", "ALL_PROXY", "HTTPS_PROXY", "HTTP_PROXY"]
for var in proxy_vars:
    value = os.getenv(var)
    if value:
        print(f"Found {var}={value}")
    else:
        print(f"{var} not set")

# Try to fix the 'proxies' error by creating a custom client
print("\n=== Testing Custom Client Initialization ===")
try:
    # Create a custom client without proxies
    client = openai.OpenAI(
        api_key=api_key,
        # Explicitly set proxies to None to avoid the error
        http_client=None
    )
    print("Custom client initialized successfully")
    
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
    print("Making API call with custom client")
    print("Using model: gpt-4.1-mini")
    
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
    print(f"Error with custom client: {e}")

# Try with a different approach - using the OpenAI API directly
print("\n=== Testing Direct API Call ===")
try:
    # Set the API key directly
    openai.api_key = api_key
    
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
    
    # Make API call using the direct approach
    print("Making API call with direct approach")
    print("Using model: gpt-4.1-mini")
    
    # Use the _client attribute to access the underlying client
    response = openai._client.OpenAI(api_key=api_key).chat.completions.create(
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
    print(f"Error with direct API call: {e}")

print("\nDebug tests completed.") 