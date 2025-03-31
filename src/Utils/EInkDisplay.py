"""
E-Ink display handler for MiniAnki
Manages display initialization, refresh timing, and content rendering
"""

import time
import board
import displayio
import busio
import adafruit_ssd1680
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from Utils.Constants import *

class EInkDisplay:
    def __init__(self, min_refresh_interval=EINK_REFRESH_INTERVAL_SEC):
        """Initialize the e-ink display and required hardware"""
        self.min_refresh_interval = min_refresh_interval
        self.last_refresh_time = 0
        self.display = None
        self.font = None
        self.group = None
        
        # Initialize the display
        self._initialize_display()
        
        self._load_font()
        
        # self._show_startup_screen()
    
    def _initialize_display(self):
        """Initialize the e-ink display hardware"""
        try:
            # Release any existing displays
            displayio.release_displays()
            
            # SPI1 setup (for e-ink display) - using direct pin assignments
            spi_epd = busio.SPI(clock=board.GP10, MOSI=board.GP11)  
            epd_cs = board.GP9
            epd_dc = board.GP8
            epd_reset = board.GP12
            epd_busy = board.GP13
            
            # Create display bus
            display_bus = displayio.FourWire(
                spi_epd, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
            )
            
            # Initialize the display
            self.display = adafruit_ssd1680.SSD1680(
                display_bus,
                width=250,
                height=122,
                busy_pin=epd_busy,
                highlight_color=0xFF0000,
                rotation=270
            )
            
            # Initialize display group
            self.group = displayio.Group()
            self.display.root_group = self.group
            
            print("E-ink display initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing e-ink display: {e}")
            return False
    
    def _load_font(self):
        """Load Chinese font from SD card"""
        try:
            # Assuming SD card is already mounted at /sd
            print("Loading font...")
            self.font = bitmap_font.load_font("/sd/ChineseFont.bdf")
            print("Font loaded")
            
        except Exception as e:
            print(f"Error loading font: {e}")
            # Create a fallback font if possible
            try:
                from adafruit_bitmap_font import bitmap_font
                self.font = bitmap_font.load_font("/fonts/Arial-12.bdf")
                print("Fallback font loaded")
            except:
                print("No font available")
    
    def _show_startup_screen(self):
        """Show initial startup screen"""
        if not self.display or not self.font:
            return False
            
        self._clear_display()
            
        title = label.Label(
            self.font, 
            text="MiniAnki", 
            color=0xFFFFFF, 
            x=80, 
            y=40, 
            scale=2
        )
        
        subtitle = label.Label(
            self.font, 
            text="Ready for learning", 
            color=0xFFFFFF, 
            x=60, 
            y=80, 
            scale=1
        )
        
        self.group.append(title)
        self.group.append(subtitle)
        
        self.refresh()
    
    def _clear_display(self):
        """Clear all items from display group"""
        while len(self.group) > 0:
            self.group.pop()
    
    def can_refresh(self):
        """Check if enough time has passed since last refresh"""
        if not self.display:
            return False
            
        current_time = time.monotonic()
        return current_time - self.last_refresh_time >= self.min_refresh_interval
    
    def time_until_refresh(self):
        """Return seconds until refresh is possible"""
        if not self.display:
            return self.min_refresh_interval
            
        current_time = time.monotonic()
        wait_time = max(0, self.min_refresh_interval - (current_time - self.last_refresh_time))
        print(f"⚠️ E-ink display cooling down. Please wait {int(wait_time)} seconds...")
        return wait_time
    
    def refresh(self):
        """Refresh the display if enough time has passed"""
        if not self.display:
            return False
            
        if self.can_refresh():
            self.display.refresh()
            self.last_refresh_time = time.monotonic()
            return True
        
        return False
    
    def show_card(self, card, show_answer=False):
        """Show a flashcard on the display"""
        
        if not self.can_refresh():
            wait_time = self.time_until_refresh()
            time.sleep(wait_time)
            
        # Clear the display
        self._clear_display()
            
        # Prepare content based on card and whether to show answer
        if show_answer:
            # Show question and answer
            question_label = label.Label(
                self.font, 
                text=card.hanzi, 
                color=0xFFFFFF, 
                x=10, 
                y=30, 
                scale=2
            )
            
            pinyin_label = label.Label(
                self.font, 
                text=card.pinyin, 
                color=0xFFFFFF, 
                x=10, 
                y=60, 
                scale=1
            )
            
            english_label = label.Label(
                self.font, 
                text=card.english, 
                color=0xFFFFFF, 
                x=10, 
                y=90, 
                scale=1
            )
            
            self.group.append(question_label)
            self.group.append(pinyin_label)
            self.group.append(english_label)
        else:
            # Show only question
            question_label = label.Label(
                self.font, 
                text=card.hanzi, 
                color=0xFFFFFF, 
                x=10, 
                y=60, 
                scale=3
            )
            
            self.group.append(question_label)
        
        # Refresh the display
        return self.refresh()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self._clear_display()
            if self.display:
                self.display.refresh()
        except:
            pass