"""
Hardware interface module for MiniAnki
Handles SD card and input/output operations
"""

import board
import busio as io
import digitalio
import storage
import adafruit_sdcard
import supervisor
from MiniAnki.Constants import *

def input_available():
    """
    Check if user input is available from the serial monitor
    
    Returns:
        bool: True if input is available in the serial buffer, False otherwise
    """
    return supervisor.runtime.serial_bytes_available > 0

def read_input():
    """
    Read a line of input from the serial monitor
    
    Returns:
        str: The input string, or None if no input is available
    """
    if input_available():
        try:
            return input().strip()
        except Exception as e:
            print(f"Error reading input: {str(e)}")
    return None