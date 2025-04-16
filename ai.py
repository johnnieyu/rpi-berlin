import os
import base64
from pathlib import Path
from typing import Optional
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

def generate_poem_from_image(
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
    
    response = client.chat.completions.create(
        model=model,
        messages=[
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
        ],
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content

def get_system_prompt() -> str:
    prompt_path = Path("data/system_prompt.txt")
    
    # Default prompt if file doesn't exist or is empty
    default_prompt = "Write a poem based on the image given."
    
    try:
        if prompt_path.exists():
            with open(prompt_path, "r") as f:
                prompt = f.read().strip()
                if prompt:  # Only use file content if it's not empty
                    return prompt
    except Exception as e:
        print(f"Warning: Could not read system prompt file: {e}")
    
    return default_prompt

def process_image(
    demo_mode: bool = False,
    system_prompt: Optional[str] = None
) -> str:
    """
    Process an image and generate a poem.
    
    Args:
        demo_mode: If True, use the demo image from /data/cdmx.jpg
        system_prompt: Custom system prompt for poem generation
    
    Returns:
        str: The generated poem
    """
    # Get system prompt from file if none provided
    if system_prompt is None:
        system_prompt = get_system_prompt()
    
    # Determine image path based on demo mode
    if demo_mode:
        image_path = Path("data/cdmx.jpg")
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
    return generate_poem_from_image(str(image_path), system_prompt)

def get_next_serial_number(poems_dir: Path) -> int:
    """
    Get the next available serial number for poem files.
    
    Args:
        poems_dir: Path to the poems directory
    
    Returns:
        int: Next available serial number
    """
    # Get all existing poem files
    existing_files = list(poems_dir.glob("*.txt"))
    
    if not existing_files:
        return 1
    
    # Extract serial numbers from existing filenames
    serial_numbers = []
    for file in existing_files:
        try:
            # Split filename and extract the serial number
            parts = file.stem.split('-')
            if len(parts) >= 2:
                serial = int(parts[1])
                serial_numbers.append(serial)
        except (ValueError, IndexError):
            continue
    
    return max(serial_numbers, default=0) + 1

def save_poem(poem: str, image_path: Path) -> Path:
    """
    Save the generated poem to a text file in the poems directory.
    
    Args:
        poem: The poem text to save
        image_path: Path to the source image (used for filename generation)
    
    Returns:
        Path: Path to the saved poem file
    """
    # Create poems directory if it doesn't exist
    poems_dir = Path("poems")
    poems_dir.mkdir(exist_ok=True)
    
    # Get current date and next serial number
    date_str = datetime.now().strftime("%Y%m%d")
    serial_number = get_next_serial_number(poems_dir)
    
    # Generate filename with date, serial number, and image name
    image_name = image_path.stem
    poem_filename = f"{date_str}-{serial_number:03d}-{image_name}.txt"
    poem_path = poems_dir / poem_filename
    
    # Save the poem
    with open(poem_path, "w") as f:
        f.write(poem)
    
    return poem_path

if __name__ == "__main__":
    # Example usage
    try:
        # Set demo mode
        demo_mode = True  # Set to False to use images from /images directory
        
        # Generate poem and get the image path used
        poem = process_image(demo_mode=demo_mode)
        
        # Get the image path that was used
        image_path = Path("data/cdmx.jpg") if demo_mode else max(Path("images").glob("*.jpg"), key=lambda x: x.stat().st_mtime)
        
        # Save poem to file
        saved_path = save_poem(poem, image_path)
        
        print("Generated Poem:")
        print("-" * 40)
        print(poem)
        print("-" * 40)
        print("            a poem by berlin            ")
        print("             @notnotjohnnie             ")
        print(f"\nPoem saved to: {saved_path}")
    except Exception as e:
        print(f"Error: {e}")