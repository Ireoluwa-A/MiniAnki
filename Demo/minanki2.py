import time
import board
import displayio
import busio
import adafruit_ssd1680
import sdcardio
import storage
import random
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import digitalio
import os

# Constants for flashcard timing
# MIN_SHOW_INTERVAL = 1 * 60  # Minimum time in s
# MAX_SHOW_INTERVAL = 5 * 60 # Maximum time in s

MIN_SHOW_INTERVAL = 5  # Minimum time in s
MAX_SHOW_INTERVAL = 10 # Maximum time in s

# Release previous displays
displayio.release_displays()

# SPI1 setup (for e-ink display)
spi_epd = busio.SPI(clock=board.GP10, MOSI=board.GP11)  
epd_cs = board.GP9
epd_dc = board.GP8
epd_reset = board.GP12
epd_busy = board.GP13

display_bus = displayio.FourWire(
    spi_epd, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)

display = adafruit_ssd1680.SSD1680(
    display_bus,
    width=250,
    height=122,
    busy_pin=epd_busy,
    highlight_color=0xFF0000,
    rotation=270
)

# SPI0 setup (for SD card)
sd_spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)  
sd_cs = board.GP5

# Initialize SD card
sdcard = sdcardio.SDCard(sd_spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Set up the buttons
button_bad = digitalio.DigitalInOut(board.GP19)
button_bad.direction = digitalio.Direction.INPUT
button_bad.pull = digitalio.Pull.UP

button_medium = digitalio.DigitalInOut(board.GP20)
button_medium.direction = digitalio.Direction.INPUT
button_medium.pull = digitalio.Pull.UP

button_good = digitalio.DigitalInOut(board.GP21)
button_good.direction = digitalio.Direction.INPUT
button_good.pull = digitalio.Pull.UP


buttons = [button_good, button_medium, button_bad]

# Load font
print("Loading font...")
font = bitmap_font.load_font("/sd/ChineseFont.bdf")
print("Font loaded")

# Flashcards: (Chinese character, meaning)
flashcards = [
    ("你好", "Hello"),
    ("谢谢", "Thank you"),
    ("再见", "Goodbye")
]

# Create display group
g = displayio.Group()
print("display group created")

# Function to show a flashcard
def show_flashcard(card_index, show_meaning=False):
    global g
    
    # Clear the group
    while len(g) > 0:
        g.pop()
    
    character, meaning = flashcards[card_index]
    
    # Show the character
    text_area = label.Label(font, text=character, color=0xFFFFFF, x=10, y=40, scale=2)
    g.append(text_area)
    
    # Show the meaning if requested
    if show_meaning:
        meaning_text = label.Label(
            terminalio.FONT if 'terminalio' in globals() else font, 
            text=meaning, 
            color=0xFFFFFF, 
            x=10, 
            y=80, 
            scale=1
        )
        g.append(meaning_text)
    
    # Update the display
    display.root_group = g
    display.refresh()
    print(f"Showing card {card_index}: {character}")
    if show_meaning:
        print(f"Meaning: {meaning}")

def any_button_pressed():
    return not button_good.value or not button_medium.value or not button_bad.value

def wait_for_button():
    while any_button_pressed():
        time.sleep(0.1)
    
    # Now wait for a button to be pressed
    while True:
        if not button_good.value:
            return "good"
        elif not button_medium.value:
            return "medium"
        elif not button_bad.value:
            return "bad"
        time.sleep(0.1)

# Main loop
current_card_index = random.randint(0, len(flashcards) - 1)
while True:

    show_flashcard(current_card_index, show_meaning=False)
    
    # Reveal meaning
    while True:
        print("Waiting for button press to reveal meaning...")
        if any_button_pressed():
            break
        time.sleep(0.1)

    show_flashcard(current_card_index, show_meaning=True)
    
    # Wait for rating
    response = wait_for_button()
    if response == "good":
        current_card_index = (current_card_index + 2) % len(flashcards)
    elif response == "medium":
        current_card_index = (current_card_index + 1) % len(flashcards)
    elif response == "bad":
        pass
    
    # Random interval before next card
    interval = random.randint(MIN_SHOW_INTERVAL, MAX_SHOW_INTERVAL)
    print(f"Waiting {interval // 60} minutes and {interval % 60} seconds")
    
    start_time = time.monotonic()
    while time.monotonic() - start_time < interval:
        # Check if any button is pressed to skip waiting
        if any_button_pressed():
            break
        time.sleep(1)
