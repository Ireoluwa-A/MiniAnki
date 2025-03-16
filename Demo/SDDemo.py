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


