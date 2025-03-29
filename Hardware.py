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

def setup_sd_card():
    """
    Initialize the SD card
    
    Returns:
        bool: True if SD card was successfully mounted, False otherwise
    """
    try:
        # Create the SPI bus
        spi = io.SPI(board.GP10,    # SCK
                       board.GP11,      # MOSI
                       board.GP12)      # MISO

        # Create the CS (Chip Select) pin
        cs = digitalio.DigitalInOut(board.GP13)
        
        # Initialize SD card
        sdcard = adafruit_sdcard.SDCard(spi, cs)
        
        # Create the filesystem
        vfs = storage.VfsFat(sdcard)
        
        # Mount the filesystem
        try:
            storage.mount(vfs, "/sd")
            print("SD card mounted successfully at /sd")
        except RuntimeError as e:
            # If already mounted, unmount and try again
            storage.umount("/sd")
            storage.mount(vfs, "/sd")
            print("SD card remounted successfully at /sd")
            
        return True
        
    except Exception as e:
        print(f"Failed to mount SD card: {str(e)}")
        return False

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