"""
Handles motion detection and LED feedback for MiniAnki
"""

import board
import digitalio
import neopixel
import time
from MiniAnki.Constants import *

class MotionManager:
    def __init__(self, pir_pin=board.GP16, led_pin=board.GP17):
        # Setup PIR sensor
        self.pir_sensor = digitalio.DigitalInOut(pir_pin)
        self.pir_sensor.direction = digitalio.Direction.INPUT
        
        # Setup LED strip
        self.pixels = neopixel.NeoPixel(led_pin, NUM_PIXELS, brightness=0.3)
        self.pixels.fill(OFF_COLOR)
        
        # State tracking
        self.motion_detected = False
        self.last_motion_time = 0
    
    def update(self):
        """
        Update motion state and LED display
        Returns: True if system should be active, False if in standby
        """
        current_time = time.monotonic()
        if self.pir_sensor.value:
            if not self.motion_detected:
                print("Motion detected - activating system")
            self.motion_detected = True
            self.last_motion_time = current_time
            self.pixels.fill(WARM_WHITE)
            return True
            
        elif self.motion_detected and (current_time - self.last_motion_time) > MOTION_TIMEOUT:
            print("No motion detected - entering standby mode")
            self.motion_detected = False
            self.pixels.fill(OFF_COLOR)
            return False
            
        return self.motion_detected
    
    def cleanup(self):
        """Turn off LEDs and cleanup"""
        self.pixels.fill(OFF_COLOR)
