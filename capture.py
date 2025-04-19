"""
Step 1 along the pipeline.
Capture an image from the camera and save it to the SD card.

Steps:
1. Initialize the camera
2. Wait for button press
3. Capture image
4. Save image to SD card
5. Clean up
"""

import os
import time
from pathlib import Path
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from datetime import datetime

# Configure GPIO
BUTTON_PIN = 21  # GPIO21 (Physical pin 40)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_button():
    """
    Wait for button press on GPIO21.
    Returns True when button is pressed.
    """
    print("Waiting for button press...")
    GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
    # Debounce
    time.sleep(0.3)
    return True

def capture_image() -> Path:
    """
    Capture an image using the Raspberry Pi camera and save it to /images.
    
    Returns:
        Path: Path to the saved image
    """
    # Initialize camera
    picam2 = Picamera2()
    
    # Configure camera
    config = picam2.create_still_configuration()
    picam2.configure(config)
    
    # Create images directory if it doesn't exist
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = images_dir / f"{timestamp}.jpg"
    
    try:
        # Start camera
        picam2.start()
        
        # Wait for button press
        wait_for_button()
        
        # Capture image
        print("Capturing image...")
        picam2.capture_file(str(image_path))
        print(f"Image saved to: {image_path}")
        
        return image_path
        
    finally:
        # Clean up
        picam2.stop()
        picam2.close()

if __name__ == "__main__":
    # Test the capture function
    try:
        image_path = capture_image()
        print(f"Successfully captured image: {image_path}")
    except Exception as e:
        print(f"Error capturing image: {e}")
    finally:
        GPIO.cleanup()
