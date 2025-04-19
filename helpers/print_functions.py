#!/usr/bin/env python3
"""
Core printing functions for thermal printer output.
"""

import usb.core
import usb.util
import sys
import time
from datetime import datetime
import os
from escpos.printer import Usb

def print_format(input, max_length):
    """
    Format text to a specified line length, with indentation for wrapped lines.
    
    Args:
        input (str): The input text to format
        max_length (int): The maximum number of characters per line
        
    Returns:
        str: The formatted text with indentation for wrapped lines
    """
    # split input text into individual lines
    lines = input.split('\n')
    print_formatted = ''

    for x in lines:
        # split line into a list of words
        words = x.split()
        current = ''

        for x in words:
            # if length of current + length of next word is within max line length
            if len(current) + len(x) <= max_length:
                # then keep adding current to this line
                current += x + ' '
            else:
                # finish current, add it to our output print_formatted
                # also adds extra spaces for next line's indent
                print_formatted += current.strip() + '\n   '
                
                # start new current
                current = x + ' '

        # add last line to our output
        print_formatted += current.strip() + '\n'

    return print_formatted

# ESC/POS commands
ESC = b'\x1B'
GS = b'\x1D'
ESC_INIT = ESC + b'@'  # Initialize printer
ESC_ALIGN_CENTER = ESC + b'a\x01'  # Align center
ESC_ALIGN_LEFT = ESC + b'a\x00'  # Align left
ESC_BOLD_ON = ESC + b'E\x01'  # Bold on
ESC_BOLD_OFF = ESC + b'E\x00'  # Bold off
ESC_CUT = GS + b'V\x41\x03'  # Cut paper

# QR Code commands
GS_QR = GS + b'k'  # QR Code command
GS_QR_SIZE = b'\x03'  # Size 3 (1-16)
GS_QR_ERROR_CORRECTION = b'\x00'  # Error correction level L (0-3)
GS_QR_MODEL = b'\x01'  # Model 1 (1-2)

class ThermalPrinter:
    def __init__(self):
        self.ep = None
        self.printer = None
        
    def initialize(self):
        """Initialize the printer connection."""
        try:
            # Initialize both USB interfaces
            self.printer = Usb(0x6868, 0x0200)
            
            # Find the printer for raw commands
            printer = usb.core.find(idVendor=0x6868, idProduct=0x0200)
            
            if printer is None:
                raise Exception("Printer not found!")
            
            # Set configuration
            printer.set_configuration()
            
            # Get the interface
            cfg = printer.get_active_configuration()
            interface = cfg[(0, 0)]
            
            # Find the OUT endpoint
            self.ep = usb.util.find_descriptor(
                interface,
                custom_match=lambda e: 
                    usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
            )
            
            if self.ep is None:
                raise Exception("Endpoint not found!")
            
            # Initialize printer
            self.ep.write(ESC_INIT)
            time.sleep(1)  # Wait for printer to initialize
            
        except Exception as e:
            print(f"Error initializing printer: {e}")
            sys.exit(1)
    
    def print_text(self, text, center=False):
        """Print formatted text."""
        # Format text to 32 characters per line
        formatted = print_format(text, 32)
        
        # Set alignment
        if center:
            self.ep.write(ESC_ALIGN_CENTER)
        else:
            self.ep.write(ESC_ALIGN_LEFT)
        
        # Print the formatted text
        self.ep.write(formatted.encode())
    
    def print_custom_header(self, poem_number, image_name, poem_name):
        """Print custom header with poem number, image name, and poem name."""
        now = datetime.now()
        date_str = now.strftime("%b %d, %Y")
        time_str = now.strftime("%I:%M %p")

        # Center and print poem number
        self.printer.set(align='center')
        self.printer.set(bold=True)
        poem_header = f"* HAIKU #{poem_number} *\n"
        self.printer.text(poem_header)
        self.printer.set(bold=False)
        
        # Print author and handle
        self.printer.text("a poem by berlin\n")
        self.printer.text("@notnotjohnnie\n")
        
        # Switch to left alignment for the rest
        self.printer.set(align='left')
        
        # Format image name line (left: image name, right: date)
        # Calculate padding needed
        padding = 32 - len(image_name) - len(date_str)
        image_line = f"{image_name}{' ' * padding}{date_str}\n"
        self.printer.text(image_line)
        
        # Format poem name line (left: poem name, right: time)
        padding = 32 - len(poem_name) - len(time_str)
        poem_line = f"{poem_name}{' ' * padding}{time_str}\n"
        self.printer.text(poem_line)
        
        # Print divider
        divider = "-" * 32 + "\n"
        self.printer.text(divider)
    
    def print_main(self, text, center=False):
        """Print the main content."""
        # Format text to 32 characters per line
        formatted = print_format(text, 32)
        
        # Set alignment
        self.printer.set(align='center' if center else 'left')
        
        # Print the formatted text
        self.printer.text(formatted)
    
    def print_qr(self, data, size=5):
        """Print QR code using escpos library."""
        self.printer.qr(data, size=size, native=False)
    
    def print_footer(self, code_version: str = "v0.1"):
        """Print the footer with QR code and cut the paper."""
        # Print divider
        divider = "-" * 32 + "\n"
        self.printer.text(divider)
        
        # Center alignment for footer
        self.printer.set(align='center')
        
        # Print thank you message in bold
        self.printer.set(bold=True)
        self.printer.text("Thank you for creating with us!\n")
        self.printer.set(bold=False)
        
        # Print version
        self.printer.text(f"rpi-berlin-{code_version}")
        
        # Print QR code
        self.print_qr("www.notnotjohnnie.com", size=7)
        
        # Cut paper
        self.printer.cut()

def main():
    """Example usage of the printing functions."""
    try:
        # Initialize printer
        printer = ThermalPrinter()
        printer.initialize()
        
        # Print header
        printer.print_custom_header(1, "Image1", "Poem1")
        
        # Example text
        text = "This is an example of the main content that will be printed."
        
        # Print main content
        printer.print_main(text, center=True)
        
        # Print footer
        printer.print_footer()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 