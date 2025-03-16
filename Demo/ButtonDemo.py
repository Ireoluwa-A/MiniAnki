import board
import digitalio
import time

# Set up the button
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Using internal pull-up resistor


while True:
    if not button.value:  # Button is pressed (reads False due to pull-up)
        print("Button pressed!")
    else:
        print("button not pressed!")
    
    time.sleep(0.1)  # Small delay to debounce
