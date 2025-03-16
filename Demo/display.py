import time
import board
import displayio
import busio
import terminalio
from adafruit_display_text import label
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire
import adafruit_ssd1680

# Define colors
BLACK = 0x000000
WHITE = 0xFFFFFF
RED = 0xFF0000

# Set your desired colors
FOREGROUND_COLOR = BLACK
BACKGROUND_COLOR = WHITE

displayio.release_displays()

# Setup SPI and display pins
spi = busio.SPI(board.GP10, MOSI=board.GP11)
epd_cs = board.GP9  # ECS pin
epd_dc = board.GP8
epd_reset = board.GP12
epd_busy = board.GP13

display_bus = FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)

time.sleep(1)

# Create the display object
DISPLAY_WIDTH = 250
DISPLAY_HEIGHT = 122

display = adafruit_ssd1680.SSD1680(
    display_bus,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    busy_pin=epd_busy,
    highlight_color=RED,
    rotation=180,
)

# Create a display group
g = displayio.Group()

# Set a background
background_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
palette = displayio.Palette(1)
palette[0] = BACKGROUND_COLOR

# Create a Tilegrid with the background
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
g.append(t)

# Create text group with scaling and positioning
text_group = displayio.Group(scale=2, x=20, y=40)

# Add text to the text group
text = "Hello World!"
text_area = label.Label(
    terminalio.FONT,
    text=text,
    color=FOREGROUND_COLOR
)
text_group.append(text_area)

# Add the text group to the main group
g.append(text_group)

# Show it on the display
display.root_group = g

print("Refreshing display...")
display.refresh()
time.sleep(display.time_to_refresh + 5)

while True:
    time.sleep(10)
