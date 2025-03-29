"""
E-Ink display handler for MiniAnki
Manages display initialization, refresh timing, and content rendering
"""

import time
import board
import busio
import displayio
import adafruit_ssd1680
import sdcardio
import storage
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import os
from MiniAnki.Constants import *

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
        
        if self.display:
            # Show startup screen
            self._show_startup_screen()
    
    def _initialize_display(self):
        """Initialize the e-ink display hardware"""
        try:
            # Release any existing displays
            displayio.release_displays()
            
            # Setup SPI for display
            spi = busio.SPI(
                clock=getattr(board, f"GP{EINK_SCK_PIN}"), 
                MOSI=getattr(board, f"GP{EINK_MOSI_PIN}")
            )
            
            # Setup control pins
            epd_cs = getattr(board, f"GP{EINK_CS_PIN}")
            epd_dc = getattr(board, f"GP{EINK_DC_PIN}")
            epd_reset = getattr(board, f"GP{EINK_RESET_PIN}")
            epd_busy = getattr(board, f"GP{EINK_BUSY_PIN}")
            
            # Create display bus
            display_bus = displayio.FourWire(
                spi, 
                command=epd_dc, 
                chip_select=epd_cs, 
                reset=epd_reset, 
                baudrate=1000000
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
            
            # Load font
            self._load_font()
            
            print("E-ink display initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing e-ink display: {e}")
            return False
    
    def _load_font(self):
        """Load Chinese font from SD card"""
        try:
            # Check if /sd is already mounted
            try:
                font_files = os.listdir("/sd")
                print(f"SD card already mounted. Files: {font_files}")
            except:
                # Setup SD card if not mounted
                print("Mounting SD card for font loading...")
                sd_spi = busio.SPI(
                    clock=getattr(board, f"GP{SPI_SCK_PIN}"), 
                    MOSI=getattr(board, f"GP{SPI_MOSI_PIN}"), 
                    MISO=getattr(board, f"GP{SPI_MISO_PIN}")
                )
                sd_cs = getattr(board, f"GP{SD_CS_PIN}")
                
                # Initialize and mount SD card
                sdcard = sdcardio.SDCard(sd_spi, sd_cs)
                vfs = storage.VfsFat(sdcard)
                
                try:
                    storage.mount(vfs, "/sd")
                    print("SD card mounted at /sd")
                    font_files = os.listdir("/sd")
                    print(f"SD card files: {font_files}")
                except Exception as e:
                    print(f"Error mounting SD card: {e}")
            
            # Load the font
            self.font = bitmap_font.load_font("/sd/ChineseFont.bdf")
            print("Chinese font loaded successfully")
            
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
        if not self.display or not self.font:
            return False
        
        sleep(time_until_refresh())

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
    
    def _show_cooldown_screen(self):
        """Show cooldown information when display can't be refreshed yet"""
        if not self.display or not self.font:
            return False
            
        # Don't actually refresh the display, just show a message on console
        wait_time = self.time_until_refresh()
        
        
        return False
        
    def cleanup(self):
        """Clean up resources"""
        try:
            self._clear_display()
            if self.display:
                self.display.refresh()
        except:
            pass