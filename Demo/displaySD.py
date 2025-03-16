import time
import board
import displayio
import busio
import adafruit_ssd1680
import sdcardio
import storage
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import os

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
    rotation=180
)

# SPI0 setup (for SD card)
sd_spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)  
sd_cs = board.GP5

# Initialize SD card
sdcard = sdcardio.SDCard(sd_spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")


# Load font
print("Files on SD card:", os.listdir("/sd"))
print("loading font")
font = bitmap_font.load_font("/sd/ChineseFont.bdf")
print("font loaded")


# Create a display group
g = displayio.Group()
print("display group created")

# Create a text label with Chinese characters
text = "你"
text_area = label.Label(font, text=text, color=0xFFFFFF, x=10, y=50, scale =2)
g.append(text_area)
print("display group appended")

display.root_group = g
print("Refreshing display")
display.refresh()

while True:
    time.sleep(180)
    print("Can refresha again")


