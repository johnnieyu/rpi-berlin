"""
Script to print Sonnet 18 using the thermal printer.
"""

import os
from pathlib import Path
from helpers.print_functions import ThermalPrinter
from escpos.printer import Usb

def get_poem_count():
    """Get the count of existing poems in the poems directory."""
    poems_dir = Path("poems")
    if not poems_dir.exists():
        return 1
    return len(list(poems_dir.glob("*.txt"))) + 1

def print_poem(image_name="debug.jpg", poem_name="aworldofdew.txt"):
    # Initialize the printer
    printer = ThermalPrinter()
    printer.initialize()
    
    # Get poem count
    poem_number = get_poem_count()
    
    # Print custom header
    printer.print_custom_header(
        poem_number=poem_number,
        image_name=image_name,
        poem_name=poem_name
    )
    
    # Haiku by Kobayashi Issa
    haiku = """I write, erase, rewrite
Erase again, and then
A poppy blooms."""
    
    # Print the haiku (left-aligned)
    printer.print_main(haiku, center=False)
    
    # Print footer
    printer.print_footer()

if __name__ == "__main__":
    print_poem()