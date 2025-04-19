"""
Step 2 along the pipeline.
AI module for generating poems from images.

Steps:
1. Encode the image
2. Generate a poem
3. Save the poem to a file
"""

import os
import base64
from pathlib import Path
from typing import Literal
import openai
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_path: str) -> str:
    """Convert image to base64 string for OpenAI API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_poem(
    image_path: str,
    system_prompt: str,
    model: str = "gpt-4.1-mini",
    max_tokens: int = 300
) -> str:
    """
    Generate a poem from an image using OpenAI's API.
    
    Args:
        image_path: Path to the image file
        system_prompt: The system prompt to guide the poem generation
        model: The OpenAI model to use
        max_tokens: Maximum number of tokens in the response
    
    Returns:
        str: The generated poem
    """
    base64_image = encode_image(image_path)
    
    # Create the messages array with the correct structure for the latest OpenAI API
    messages = [
        {
            "role": "system",
            "content": system_prompt
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
    
    # Use the latest API style
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content

def get_prompt(poem_type: Literal["sonnet", "haiku"]) -> str:
    """
    Get the appropriate prompt based on poem type.
    
    Args:
        poem_type: Type of poem to generate ("sonnet" or "haiku")
    
    Returns:
        str: The prompt text
    """
    # Map poem types to prompt files
    prompt_files = {
        "sonnet": "data/sonnet_prompt.txt",
        "haiku": "data/haiku_prompt.txt"
    }
    
    prompt_path = Path(prompt_files[poem_type])
    
    # Default prompts if files don't exist or are empty
    default_prompts = {
        "sonnet": "Write a sonnet based on the image given.",
        "haiku": "Write a haiku based on the image given."
    }
    
    try:
        if prompt_path.exists():
            with open(prompt_path, "r") as f:
                prompt = f.read().strip()
                if prompt:  # Only use file content if it's not empty
                    return prompt
    except Exception as e:
        print(f"Warning: Could not read {poem_type} prompt file: {e}")
    
    return default_prompts[poem_type]

def process_image(
    demo_mode: bool = False,
    poem_type: Literal["sonnet", "haiku"] = "sonnet",
    demo_image: str = "data/cdmx.jpg"
) -> str:
    """
    Process an image and generate a poem.
    
    Args:
        demo_mode: If True, use the demo image
        poem_type: Type of poem to generate ("sonnet" or "haiku")
        demo_image: Path to the image to use in demo mode
    
    Returns:
        str: The generated poem
    """
    # Get appropriate prompt based on poem type
    system_prompt = get_prompt(poem_type)
    
    # Determine image path based on demo mode
    if demo_mode:
        image_path = Path(demo_image)
    else:
        # In production mode, use the most recent image from the images directory
        images_dir = Path("images")
        if not images_dir.exists():
            raise FileNotFoundError("Images directory not found")
        
        # Get the most recent image file
        image_files = list(images_dir.glob("*.jpg"))
        if not image_files:
            raise FileNotFoundError("No images found in the images directory")
        
        image_path = max(image_files, key=lambda x: x.stat().st_mtime)
    
    # Generate and return the poem
    return generate_poem(str(image_path), system_prompt)

def get_serial(poems_dir: Path) -> int:
    """
    Get the next available serial number for poem files.
    
    Args:
        poems_dir: Path to the poems directory
    
    Returns:
        int: Next available serial number
    """
    existing_files = list(poems_dir.glob("*.txt"))
    if not existing_files:
        return 1
    
    serial_numbers = []
    for file in existing_files:
        try:
            serial = int(file.stem.split('-')[1])
            serial_numbers.append(serial)
        except (ValueError, IndexError):
            continue
    
    return max(serial_numbers, default=0) + 1

def save_poem(
    poem: str,
    image_path: Path
) -> Path:
    """
    Save the generated poem to a text file in the poems directory.
    
    Args:
        poem: The poem text to save
        image_path: Path to the source image
    
    Returns:
        Path: Path to the saved poem file
    """
    # Create poems directory if it doesn't exist
    poems_dir = Path("poems")
    poems_dir.mkdir(exist_ok=True)
    
    # Get current date and next serial number
    date_str = datetime.now().strftime("%Y%m%d")  # Changed back to YYYYMMDD format
    serial_number = get_serial(poems_dir)
    
    # Generate filename with date and serial number
    poem_filename = f"{date_str}-{serial_number:03d}.txt"
    poem_path = poems_dir / poem_filename
    
    # Save the poem
    with open(poem_path, "w") as f:
        f.write(poem)
    
    return poem_path