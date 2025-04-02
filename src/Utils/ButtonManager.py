"""
Button handling for MiniAnki
Manages button setup and interactions
"""

import board
import digitalio
import time
from Utils.Constants import *

class ButtonManager:
    def __init__(self, 
                 easy_pin=BUTTON_EASY_PIN, 
                 medium_pin=BUTTON_MEDIUM_PIN, 
                 hard_pin=BUTTON_HARD_PIN,
                 debounce_time=0.1):
        
        """Initialize the buttons with given pin numbers"""
        self.debounce_time = debounce_time

        # Setup easy button
        self.easy_button = digitalio.DigitalInOut(BUTTON_EASY_PIN)
        self.easy_button.direction = digitalio.Direction.INPUT
        self.easy_button.pull = digitalio.Pull.UP
        
        # Setup medium button
        self.medium_button = digitalio.DigitalInOut(BUTTON_MEDIUM_PIN)
        self.medium_button.direction = digitalio.Direction.INPUT
        self.medium_button.pull = digitalio.Pull.UP
        
        # Setup hard button
        self.hard_button = digitalio.DigitalInOut(BUTTON_HARD_PIN)
        self.hard_button.direction = digitalio.Direction.INPUT
        self.hard_button.pull = digitalio.Pull.UP
        
        # List of all buttons for convenience
        self.buttons = [self.easy_button, self.medium_button, self.hard_button]
        print("Button manager initialized")
    
    def is_any_button_pressed(self):
        """Check if any button is currently pressed"""
        return not self.easy_button.value or not self.medium_button.value or not self.hard_button.value
    
    def wait_for_any_button(self, timeout=RESPONSE_TIMEOUT_SEC):
        """
        Wait until any button is pressed and released, with a timeout
        """
        start_time = time.monotonic()
        
        # Wait for all buttons to be released first
        while self.is_any_button_pressed():
            time.sleep(self.debounce_time)
            if time.monotonic() - start_time > timeout:
                print("Timeout waiting for buttons to be released")
                return None
        
        # Wait for a button press or timeout
        while not self.is_any_button_pressed():
            time.sleep(self.debounce_time)
            
            # Check for timeout
            if time.monotonic() - start_time > timeout:
                print("Timeout waiting for button press")
                return "hard"  # Default to hard if timeout occurs
        
        # Wait for debounce
        time.sleep(self.debounce_time)
        
        # Return which button was pressed
        if not self.easy_button.value:
            return "easy"
        elif not self.medium_button.value:
            return "medium"
        elif not self.hard_button.value:
            return "hard"
        
        return None
    
    def wait_for_response(self):
        """Wait for a button press that represents a response quality"""
        response = self.wait_for_any_button()
        
        if response == "easy":
            return RESPONSE_EASY
        elif response == "medium":
            return RESPONSE_MEDIUM
        elif response == "hard":
            return RESPONSE_HARD
        
        # Default in case something goes wrong
        return DEFAULT_RESPONSE
    
    def wait_for_button_release(self):
        """Wait until all buttons are released"""
        while self.is_any_button_pressed():
            time.sleep(self.debounce_time)
    
    def cleanup(self):
        """Clean up resources"""
        for button in self.buttons:
            button.deinit()