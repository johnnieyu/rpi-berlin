"""
Debug version for Mac testing without RPi dependencies.
Focuses on testing poem generation and formatting.
"""

import os
from pathlib import Path
from typing import Literal

# Import only the modules we need for testing
from ai import process_image, save_poem
from helpers.print_functions import ThermalPrinter

def debug_pipeline(
    poem_type: Literal["sonnet", "haiku"] = "haiku",
    code_version: str = "v0.1",
    demo_image: str = "data/cdmx.jpg"
) -> None:
    """
    Debug pipeline that skips RPi-specific functionality:
    1. Use demo image
    2. Generate poem
    3. Save poem
    4. Print using thermal printer
    
    Args:
        poem_type: Type of poem to generate ("sonnet" or "haiku")
        code_version: Version string to display
        demo_image: Path to the demo image to use
    """
    try:
        # Step 1: Use demo image
        print(f"Using demo image: {demo_image}")
        image_path = Path(demo_image)
        
        # Step 2: Generate poem
        print(f"\nGenerating {poem_type}...")
        poem = process_image(demo_mode=True, poem_type=poem_type, demo_image=demo_image)
        
        # Step 3: Save poem
        saved_path = save_poem(poem, image_path, poem_type=poem_type)
        
        # Step 4: Print using thermal printer
        print("\nPrinting poem...")
        printer = ThermalPrinter()
        printer.initialize()
        
        # Print header
        printer.print_custom_header(1, image_path.name, saved_path.name)
        
        # Print poem
        printer.print_main(poem)
        
        # Print footer
        printer.print_footer(code_version)
        
        print("Printing complete!")
        print(f"\nPoem saved to: {saved_path}")
        
    except Exception as e:
        print(f"Error in debug pipeline: {e}")

if __name__ == "__main__":
    # Configuration
    POEM_TYPE = "haiku"  # or "sonnet"
    CODE_VERSION = "v0.1"
    DEMO_IMAGE = "data/aubrey-alinea.jpg"
    
    print("Starting Berlin Poetry Camera (Mac Debug Mode)...")
    debug_pipeline(
        poem_type=POEM_TYPE,
        code_version=CODE_VERSION,
        demo_image=DEMO_IMAGE
    ) 