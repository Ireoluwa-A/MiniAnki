import time
import board
import displayio
import busio
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire
import adafruit_ssd1680

print("1. Releasing displays...")
displayio.release_displays()

print("2. Initializing SPI...")
spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)
epd_cs = board.GP9
epd_dc = board.GP8
epd_reset = board.GP12
epd_busy = board.GP13

print("3. Setting up display bus...")
display_bus = FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)

print("4. Initializing display...")
display = adafruit_ssd1680.SSD1680(
    display_bus,
    width=250,
    height=122,
    busy_pin=epd_busy,
    highlight_color=0xFF0000,
    rotation=270,
)

print("5. Creating display group...")
g = displayio.Group()

print("6. Opening bitmap file...")
with open("/display-ruler.bmp", "rb") as f:
    print("7. Creating bitmap object...")
    pic = displayio.OnDiskBitmap(f)
    print("8. Creating tile grid...")
    t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
    print("9. Appending to group...")
    g.append(t)
    print("10. Setting root group...")
    display.root_group = g
    print("11. Starting refresh...")
    display.refresh()
    print("12. Refresh command sent")
    print(f"13. Waiting {display.time_to_refresh} seconds plus 5 second buffer...")
    time.sleep(display.time_to_refresh + 5)
    print("14. Wait completed")

while True:
    time.sleep(10)


