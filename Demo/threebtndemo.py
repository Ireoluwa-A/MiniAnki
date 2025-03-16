import board
import digitalio
import time

# Set up the buttons
button1 = digitalio.DigitalInOut(board.GP21)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP  # Using internal pull-up resistor

button2 = digitalio.DigitalInOut(board.GP20)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP  # Using internal pull-up resistor

button3 = digitalio.DigitalInOut(board.GP19)
button3.direction = digitalio.Direction.INPUT
button3.pull = digitalio.Pull.UP  # Using internal pull-up resistor

# Button to name mapping
buttons = {
    button1: "Button 1 (GP21)",
    button2: "Button 2 (GP20)",
    button3: "Button 3 (GP19)"
}

# To track previous button states
previous_states = {button1: True, button2: True, button3: True}

while True:
    for button, name in buttons.items():
        if not button.value:  # Button is pressed (reads False due to pull-up)
            if previous_states[button]:  # Only print if state changed from not pressed to pressed
                print(f"{name} pressed!")
            previous_states[button] = False
        else:
            previous_states[button] = True
    print("nothing")
    time.sleep(0.1)  # Small delay to debounce
