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
    def __init__(self):
        """Initialize the e-ink display and required hardware"""
        self.display = None
        self.font = None
        self.group = None
        
        # Initialize the display
        self._initialize_display()
        self._load_font()
    
    def _initialize_display(self):
        """Initialize the e-ink display hardware"""
        try:
            displayio.release_displays()
            
            spi_epd = busio.SPI(clock=EINK_SCK_PIN, MOSI=EINK_MOSI_PIN)  
            
            # Create display bus
            display_bus = displayio.FourWire(
                spi_epd, 
                command=EINK_DC_PIN, 
                chip_select=EINK_CS_PIN, 
                reset=EINK_RESET_PIN, 
                baudrate=EINK_BAUDRATE
            )
            
            # Initialize the display
            self.display = adafruit_ssd1680.SSD1680(
                display_bus,
                width=EINK_WIDTH,
                height=EINK_HEIGHT,
                busy_pin=EINK_BUSY_PIN,
                highlight_color=EINK_COLOR,
                rotation=EINK_ROTATION
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
            # Assuming SD card is already mounted
            print("Loading font...")
            self.font = bitmap_font.load_font(MANDARIN_FONT_PATH)
            print("Font loaded")
            
        except Exception as e:
            print(f"Error loading font: {e}")
           
            try:
                from adafruit_bitmap_font import bitmap_font
                self.font = bitmap_font.load_font("/fonts/Arial-12.bdf")
                print("Fallback font loaded")
            except:
                print("No font available")
        
    def _clear_display(self):
        """Clear all items from display group"""
        while len(self.group) > 0:
            self.group.pop()
    
    def refresh(self):
        """Refresh the display using built-in timing"""
        if not self.display:
            return False
        
        # Refresh the display
        print(f"Refreshing display (will take {self.display.time_to_refresh} seconds)...")
        time.sleep(self.display.time_to_refresh)
        self.display.refresh()
        
        return True
    
    def show_card(self, card, show_answer=False):
        """Show a flashcard on the display"""
        if not self.display or not self.font:
            return False

        # Clear the display
        self._clear_display()
        
        # Create labels for the card
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

        if show_answer:
            self.group.append(question_label)
            self.group.append(pinyin_label)
            self.group.append(english_label)
        else:
            self.group.append(question_label)
        
        return self.refresh()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self._clear_display()
            if self.display:
                self.display.refresh()
        except:
            pass

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