import os
from pathlib import Path
from typing import Optional
import RPi.GPIO as GPIO

# Import our modules
from ai import process_image, save_poem
from capture import capture_image

# TODO: Import this when it is implemented
# from print import print_poem

def run_pipeline(demo_mode: bool = False) -> None:
    """
    Run the complete pipeline:
    1. Capture image (or use demo image)
    2. Generate poem from image
    3. Print poem
    
    Args:
        demo_mode: If True, use the demo image instead of capturing a new one
    """
    try:
        # Step 1: Capture image
        if demo_mode:
            print("Using demo image: data/cdmx.jpg")
            image_path = Path("data/cdmx.jpg")
        else:
            print("Capturing new image...")
            image_path = capture_image()
        
        # Step 2: Generate poem
        print("\nGenerating poem...")
        poem = process_image(demo_mode=demo_mode)
        
        # Save the poem
        saved_path = save_poem(poem, image_path)
        
        # Step 3: Print poem
        # TODO: Implement actual printing
        # print_poem(poem)
        print("\nPoem generated successfully!")
        print("-" * 40)
        print(poem)
        print("-" * 40)
        print("            a poem by berlin            ")
        print("             @notnotjohnnie             ")
        print(f"\nPoem saved to: {saved_path}")
        
    except Exception as e:
        print(f"Error in pipeline: {e}")
    finally:
        # Clean up GPIO
        if not demo_mode:
            GPIO.cleanup()

if __name__ == "__main__":
    # Set to True to use demo image, False to use camera
    DEMO_MODE = True
    
    print("Starting Berlin Poetry Camera...")
    run_pipeline(demo_mode=DEMO_MODE)
