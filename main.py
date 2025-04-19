import os
from pathlib import Path
from typing import Optional, Literal
import platform

# Import our modules
from ai import process_image, save_poem
from capture import capture_image
from helpers.print_functions import ThermalPrinter

def run_pipeline(
    demo_mode: bool = False,
    poem_type: Literal["sonnet", "haiku"] = "sonnet",
    code_version: str = "v0.1",
    demo_image: str = "data/cdmx.jpg"
) -> None:
    """
    Run the complete pipeline:
    1. Capture image (or use demo image)
    2. Generate poem from image
    3. Print poem
    
    Args:
        demo_mode: If True, use the demo image instead of capturing a new one
        poem_type: Type of poem to generate ("sonnet" or "haiku")
        code_version: Version of the code to display in the footer
        demo_image: Path to the image to use in demo mode
    """
    try:
        # Step 1: Capture image
        if demo_mode:
            print(f"Using demo image: {demo_image}")
            image_path = Path(demo_image)
        else:
            print("Capturing new image...")
            image_path = capture_image()
        
        # Step 2: Generate poem
        print(f"\nGenerating {poem_type}...")
        poem = process_image(demo_mode=demo_mode, poem_type=poem_type, demo_image=str(image_path))
        
        # Save the poem
        saved_path = save_poem(poem, image_path)
        
        # Step 3: Print poem
        printer = ThermalPrinter()
        printer.initialize()
        
        # Get poem count for the header
        poem_number = get_poem_count()
        
        # Print the poem
        printer.print_custom_header(poem_number, image_path.name, saved_path.name)
        printer.print_main(poem)
        printer.print_footer(code_version)
        
        print("\nPoem generated successfully!")
        print("-" * 40)
        print(poem)
        print("-" * 40)
        print("            a poem by berlin            ")
        print("             @notnotjohnnie             ")
        print(f"\nPoem saved to: {saved_path}")
        
    except Exception as e:
        print(f"Error in pipeline: {e}")

def get_poem_count():
    """Get the count of existing poems in the poems directory."""
    poems_dir = Path("poems")
    if not poems_dir.exists():
        return 1
    return len(list(poems_dir.glob("*.txt"))) + 1

if __name__ == "__main__":
    # Set to True to use demo image, False to use camera
    DEMO_MODE = False
    
    # Set poem type: "sonnet" or "haiku"
    POEM_TYPE = "haiku"  # Change this to "sonnet" for sonnets
    
    # Set code version
    CODE_VERSION = "v0.1"
    
    # Set demo image path
    DEMO_IMAGE = "data/cdmx.jpg"
    
    print("Starting Berlin...")
    run_pipeline(
        demo_mode=DEMO_MODE,
        poem_type=POEM_TYPE,
        code_version=CODE_VERSION,
        demo_image=DEMO_IMAGE
    )
